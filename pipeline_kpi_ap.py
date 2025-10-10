#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline KPI Aires Protégées (corrigé)
"""

import pandas as pd
import numpy as np
import re
from fuzzywuzzy import process

# ----------------------
# 1) Normalisation des textes
# ----------------------
def normalize_text(x: str) -> str:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return ""
    s = str(x).upper().strip()
    s = re.sub(r"\(.*?\)", "", s)
    mapping = {
        "É":"E","È":"E","Ê":"E","Ë":"E",
        "À":"A","Â":"A","Ä":"A",
        "Î":"I","Ï":"I",
        "Ô":"O","Ö":"O",
        "Ù":"U","Û":"U","Ü":"U",
        "Ç":"C",
    }
    for k,v in mapping.items():
        s = s.replace(k,v)
    s = re.sub(r"[’`'_.,;:!?]", " ", s)
    s = re.sub(r"[-/]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

# ----------------------
# 2) Chargement des données déforestation & feux
# ----------------------
file_outlook = "OutLook 2024 data Analyse deforestation & fires.xlsx"
an = pd.read_excel(file_outlook, sheet_name="Analysis")
an = an.rename(columns={
    'Terrestrial Protected Area Name\n(Yellow are Ramsar Sites)': 'Site',
    'PA area (Ha)': 'Superficie_ha',
})
an["Key"] = an["Site"].apply(normalize_text)

# Colonnes FCL
fcl_year_map = {}
for c in an.columns:
    if isinstance(c, str) and c.startswith("FCL "):
        match = re.search(r"\b(\d{4})\b", c)
        if match:
            fcl_year_map[c] = int(match.group(1))

fcl = an.melt(id_vars=["Site","Key","Superficie_ha"], value_vars=list(fcl_year_map.keys()),
              var_name="FCL_col", value_name="FCL_ha")
fcl["Annee"] = fcl["FCL_col"].map(fcl_year_map)
fcl = fcl.drop(columns=["FCL_col"])
fcl["FCL_ha"] = pd.to_numeric(fcl["FCL_ha"], errors="coerce").fillna(0)

# Colonnes FIRE
fire_cols = [c for c in an.columns if isinstance(c,str) and c.startswith("FIRE alert ")]
fire = an.melt(id_vars=["Site","Key","Superficie_ha"], value_vars=fire_cols,
               var_name="FIRE_col", value_name="FIRE_alerts")
fire["Annee"] = fire["FIRE_col"].str.extract(r"(\d{4})").astype(int)
fire = fire.drop(columns=["FIRE_col"])
fire["FIRE_alerts"] = pd.to_numeric(fire["FIRE_alerts"], errors="coerce").fillna(0)

# ----------------------
# 3) Chargement financements
# ----------------------
file_fonds = "Fonds 2007-25.xlsx"
fonds = pd.read_excel(file_fonds, sheet_name=1).rename(columns={"Nom AP": "Site"})

# Expansion des AP multiples (séparés par "/")
expanded_rows = []
for _, row in fonds.iterrows():
    sites_split = re.split(r"[/]", str(row["Site"]))
    for site in sites_split:
        site_clean = site.strip()
        if site_clean and "COORDINATION" not in site_clean.upper():
            new_row = row.copy()
            new_row["Site"] = site_clean
            expanded_rows.append(new_row)
fonds_expanded = pd.DataFrame(expanded_rows)

# Colonnes annuelles
year_cols = [c for c in fonds_expanded.columns if isinstance(c, str) and c.startswith("Fonds totale en ")]
fund = fonds_expanded.melt(id_vars=["Site"], value_vars=year_cols,
                           var_name="Annee_col", value_name="Financement")
fund["Annee"] = fund["Annee_col"].str.extract(r"(\d{4})").astype(int)
fund = fund.drop(columns=["Annee_col"])
fund["Key"] = fund["Site"].apply(normalize_text)
fund["Financement"] = pd.to_numeric(fund["Financement"], errors="coerce").fillna(0)

# Totaux
fonds_expanded["Key"] = fonds_expanded["Site"].apply(normalize_text)
totaux = fonds_expanded[["Key","FINANACEMENT TOTALS 2007-2025"]].drop_duplicates()
totaux = totaux.rename(columns={"FINANACEMENT TOTALS 2007-2025":"Financement_total"})

# ----------------------
# 4) Correction via fuzzy matching
# ----------------------
keys_analysis = set(an["Key"].unique())
keys_fonds = set(fund["Key"].unique())

corrections = {}
for key in keys_fonds:
    match, score = process.extractOne(key, keys_analysis)
    if score >= 90:  # seuil configurable
        corrections[key] = match

fund["Key_corr"] = fund["Key"].apply(lambda k: corrections.get(k, k))

# ----------------------
# 5) Fusion des datasets
# ----------------------
df = pd.merge(fcl[["Key","Annee","FCL_ha","Superficie_ha"]],
              fire[["Key","Annee","FIRE_alerts"]],
              on=["Key","Annee"], how="outer")

df = pd.merge(df, fund[["Key_corr","Annee","Financement"]].rename(columns={"Key_corr":"Key"}),
              on=["Key","Annee"], how="left")

# Nettoyage
for col in ["Financement","Superficie_ha","FIRE_alerts","FCL_ha"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# KPI
df["FIRE_par_100ha"] = (df["FIRE_alerts"] / (df["Superficie_ha"]+1e-6))*100
df["FCL_pct_surface"] = (df["FCL_ha"] / (df["Superficie_ha"]+1e-6))*100
df["Financement_par_ha"] = df["Financement"] / (df["Superficie_ha"]+1e-6)
df["FCL_pct_variation"] = df.groupby("Key")["FCL_pct_surface"].diff()
df["FIRE_per_fin"] = df["FIRE_alerts"] / (df["Financement"]+1e-6)
df["IPC"] = df["FCL_pct_surface"] / (df["Financement_par_ha"]+1e-6)

# ----------------------
# 6) Agrégation
# ----------------------
agg = df.groupby("Key").agg(
    Superficie_ha=("Superficie_ha","first"),
    Financement_total_annuel=("Financement","sum"),
    Financement_par_ha_moy=("Financement_par_ha","mean"),
    FCL_pct_moy=("FCL_pct_surface","mean"),
    FCL_pct_var_moy=("FCL_pct_variation","mean"),
    FCL_ha_total=("FCL_ha","sum"),
    FIRE_total=("FIRE_alerts","sum"),
    FIRE_par_100ha_moy=("FIRE_par_100ha","mean"),
    FIRE_per_fin_moy=("FIRE_per_fin","mean"),
    IPC_moy=("IPC","mean"),
).reset_index()

# Fallback financement total
agg = pd.merge(agg, totaux, on="Key", how="left")
agg["Financement_total"] = agg["Financement_total"].fillna(agg["Financement_total_annuel"])

# ----------------------
# 7) Score global
# ----------------------
eps = 1e-6
def norm_inverse(series):
    mx = max(series.max(), eps)
    return 1 - (series / (mx + eps))

agg["S_IPC"] = norm_inverse(agg["IPC_moy"])
agg["S_FCL"] = norm_inverse(agg["FCL_pct_moy"])
agg["S_FIRE"] = norm_inverse(agg["FIRE_par_100ha_moy"])
agg["Score_global"] = 0.4*agg["S_IPC"] + 0.4*agg["S_FCL"] + 0.2*agg["S_FIRE"]

classement = agg.sort_values("Score_global", ascending=False)

# ----------------------
# 8) Export Excel
# ----------------------
df.to_excel("AP_Annuel_clean.xlsx", index=False)
agg.to_excel("AP_Synthese_clean.xlsx", index=False)
classement.to_excel("AP_Classement_clean.xlsx", index=False)

print("✔ Base annuelle : AP_Annuel_clean.xlsx")
print("✔ Synthèse par AP : AP_Synthese_clean.xlsx")
print("✔ Classement : AP_Classement_clean.xlsx")
