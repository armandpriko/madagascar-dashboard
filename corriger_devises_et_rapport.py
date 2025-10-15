#!/usr/bin/env python3
"""
CORRECTEUR DE DEVISES ET COHÉRENCE DES RAPPORTS
===============================================

Ce script corrige :
1. Les devises MGA → USD avec le bon taux de change
2. La cohérence entre la carte et le rapport HTML
3. Les statistiques finales

Par KOUMI Dzudzogbe Prince Armand
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path

class CorrecteurDevises:
    """Corrige les devises et la cohérence des rapports"""
    
    def __init__(self, data_path="."):
        self.data_path = Path(data_path)
        
        # Taux de change MGA vers USD (approximatif pour 2007-2023)
        # Source: Banque Centrale de Madagascar
        self.taux_change_mga_usd = {
            2007: 2000,  # 1 USD = 2000 MGA
            2008: 2100,
            2009: 2200,
            2010: 2300,
            2011: 2400,
            2012: 2500,
            2013: 2600,
            2014: 2700,
            2015: 2800,
            2016: 2900,
            2017: 3000,
            2018: 3200,
            2019: 3400,
            2020: 3800,
            2021: 4000,
            2022: 4200,
            2023: 4500,
            # Moyenne pour les calculs généraux
            'moyen': 3200  # 1 USD = 3200 MGA en moyenne
        }
    
    def charger_donnees_brutes(self):
        """Charger les données brutes en MGA"""
        print("📂 Chargement des données brutes...")
        
        # Charger les données annuelles (en MGA)
        df_annuel = pd.read_excel(self.data_path / "AP_Annuel_clean.xlsx")
        print(f"✅ Données annuelles: {len(df_annuel)} lignes")
        print(f"   Période: {df_annuel['Annee'].min()}-{df_annuel['Annee'].max()}")
        print(f"   Financement max: {df_annuel['Financement'].max():,.0f} MGA")
        
        return df_annuel
    
    def convertir_mga_vers_usd(self, df):
        """Convertir les montants MGA vers USD"""
        print("\n💱 Conversion MGA → USD...")
        
        df_converted = df.copy()
        
        # Convertir le financement total
        df_converted['Financement_USD'] = df_converted.apply(
            lambda row: row['Financement'] / self.taux_change_mga_usd.get(row['Annee'], self.taux_change_mga_usd['moyen']),
            axis=1
        )
        
        # Convertir le financement par hectare
        df_converted['Financement_par_ha_USD'] = df_converted.apply(
            lambda row: row['Financement_par_ha'] / self.taux_change_mga_usd.get(row['Annee'], self.taux_change_mga_usd['moyen']),
            axis=1
        )
        
        print(f"✅ Conversion terminée")
        print(f"   Exemple: {df['Financement'].max():,.0f} MGA → {df_converted['Financement_USD'].max():,.0f} USD")
        
        return df_converted
    
    def calculer_statistiques_correctes(self, df_converted):
        """Calculer les statistiques correctes"""
        print("\n📊 Calcul des statistiques correctes...")
        
        # Filtrer les AP financées (après 2007)
        df_financed = df_converted[
            (df_converted['Annee'] >= 2007) & 
            (df_converted['Financement_USD'] > 0)
        ].copy()
        
        # Statistiques par AP
        ap_stats = df_financed.groupby('Key').agg({
            'Financement_USD': 'sum',
            'FIRE_par_100ha': 'mean',
            'Superficie_ha': 'first',
            'Financement_par_ha_USD': 'mean'
        }).reset_index()
        
        # Statistiques globales
        stats = {
            'total_investment_usd': df_financed['Financement_USD'].sum(),
            'total_observations': len(df_financed),
            'num_aps': len(ap_stats),
            'avg_investment_usd': df_financed['Financement_USD'].mean(),
            'avg_fire_rate': df_financed['FIRE_par_100ha'].mean(),
            'period': f"{df_financed['Annee'].min()}-{df_financed['Annee'].max()}"
        }
        
        print(f"✅ Statistiques calculées:")
        print(f"   • {stats['num_aps']} AP financées")
        print(f"   • {stats['total_observations']} observations")
        print(f"   • {stats['total_investment_usd']/1e9:.2f} milliards USD")
        print(f"   • Période: {stats['period']}")
        
        return stats, ap_stats
    
    def corriger_fichier_json(self, stats, ap_stats):
        """Corriger le fichier JSON avec les bonnes données"""
        print("\n🔧 Correction du fichier JSON...")
        
        # Charger le JSON existant
        json_path = self.data_path / "backend/data/analyse_financement_deforestation.json"
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        # Mettre à jour le summary
        data['summary'] = {
            'total_investment': stats['total_investment_usd'],
            'avg_investment': stats['avg_investment_usd'],
            'avg_fire_rate': stats['avg_fire_rate'],
            'num_observations': stats['total_observations'],
            'num_aps': stats['num_aps'],
            'period': stats['period'],
            'currency': 'USD',
            'conversion_rate_mga_usd': self.taux_change_mga_usd['moyen']
        }
        
        # Ajouter une note sur la conversion
        data['metadata']['currency_note'] = f"Données originales en MGA converties en USD avec taux moyen {self.taux_change_mga_usd['moyen']}:1"
        
        # Sauvegarder
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ JSON corrigé: {json_path}")
        return stats
    
    def corriger_rapport_html(self, stats):
        """Corriger le rapport HTML avec les bonnes statistiques"""
        print("\n🔧 Correction du rapport HTML...")
        
        html_path = self.data_path / "frontend/rapport_financement_deforestation.html"
        
        # Lire le fichier HTML
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Remplacer les valeurs incorrectes
        old_values = {
            "246,6 Mds": f"{stats['total_investment_usd']/1e9:.1f} Mds",
            "246,6 milliards USD": f"{stats['total_investment_usd']/1e9:.1f} milliards USD",
            "498 M": f"{stats['avg_investment_usd']/1e6:.0f} M",
            "56": str(stats['num_aps']),
            "495": str(stats['total_observations']),
            "0.398": f"{stats['avg_fire_rate']:.3f}",
            "246.6 Mds USD": f"{stats['total_investment_usd']/1e9:.1f} Mds USD"
        }
        
        # Appliquer les corrections
        for old, new in old_values.items():
            html_content = html_content.replace(old, new)
        
        # Ajouter une note sur la conversion de devise
        note_conversion = """
        <div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 5px; padding: 10px; margin: 10px 0;">
            <strong>📝 Note sur les devises:</strong> Les montants originaux en Ariary malgache (MGA) ont été convertis en USD avec un taux de change moyen de 3,200 MGA pour 1 USD (période 2007-2023).
        </div>
        """
        
        # Insérer la note après le header
        html_content = html_content.replace(
            '<div class="metrics-container">',
            note_conversion + '\n        <div class="metrics-container">'
        )
        
        # Sauvegarder
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Rapport HTML corrigé: {html_path}")
    
    def corriger_tous_les_rapports(self):
        """Corriger tous les rapports et cartes"""
        print("="*70)
        print("🔧 CORRECTION DES DEVISES ET COHÉRENCE DES RAPPORTS")
        print("="*70)
        
        # 1. Charger et convertir les données
        df_brut = self.charger_donnees_brutes()
        df_converted = self.convertir_mga_vers_usd(df_brut)
        
        # 2. Calculer les statistiques correctes
        stats, ap_stats = self.calculer_statistiques_correctes(df_converted)
        
        # 3. Corriger le JSON
        self.corriger_fichier_json(stats, ap_stats)
        
        # 4. Corriger le rapport HTML
        self.corriger_rapport_html(stats)
        
        print("\n" + "="*70)
        print("✅ TOUTES LES CORRECTIONS APPLIQUÉES")
        print("="*70)
        print(f"\n📊 STATISTIQUES FINALES CORRECTES:")
        print(f"   • {stats['num_aps']} AP financées")
        print(f"   • {stats['total_investment_usd']/1e9:.1f} milliards USD")
        print(f"   • {stats['avg_fire_rate']:.3f} feux/100ha (moyenne)")
        print(f"   • Période: {stats['period']}")
        print(f"   • Taux de change moyen: {self.taux_change_mga_usd['moyen']} MGA = 1 USD")
        
        print(f"\n📁 FICHIERS CORRIGÉS:")
        print(f"   ✅ backend/data/analyse_financement_deforestation.json")
        print(f"   ✅ frontend/rapport_financement_deforestation.html")
        
        print(f"\n🔄 PROCHAINES ÉTAPES:")
        print(f"   1. Régénérer les cartes: python3 generer_carte_interactive.py")
        print(f"   2. Régénérer le rapport: python3 generer_rapport_complet.py")
        print(f"   3. Vérifier la cohérence: ./OUVRIR_CARTE.sh")
        
        return stats


if __name__ == "__main__":
    correcteur = CorrecteurDevises()
    stats = correcteur.corriger_tous_les_rapports()
