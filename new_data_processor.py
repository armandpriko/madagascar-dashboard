#!/usr/bin/env python3
"""
Nouveau processeur de données pour le dashboard des aires protégées
Utilise les fichiers spécifiés par l'utilisateur :
- AP_Annuel_clean.xlsx (données annuelles)
- AP_Classement_clean.xlsx (classements)
- AP_Synthese_clean.xlsx (synthèse)
- OutLook 2024 data Analyse deforestation & fires.xlsx (sheet '14 MAY data')
- AP_coords.csv (coordonnées GPS)
"""

import pandas as pd
import json
import numpy as np
from pathlib import Path
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewDataProcessor:
    def __init__(self, data_path="."):
        self.data_path = Path(data_path)
        self.ap_annuel = None
        self.ap_classement = None
        self.ap_synthese = None
        self.outlook_data = None
        self.ap_coords = None
        
    def load_all_data(self):
        """Charger toutes les données selon les spécifications"""
        logger.info("🔄 Chargement des données selon les nouvelles spécifications...")
        
        # 1. AP_Annuel_clean.xlsx - Données annuelles
        try:
            self.ap_annuel = pd.read_excel(self.data_path / "AP_Annuel_clean.xlsx")
            logger.info(f"✅ AP_Annuel_clean.xlsx chargé: {len(self.ap_annuel)} lignes")
            logger.info(f"   Colonnes: {list(self.ap_annuel.columns)}")
            logger.info(f"   APs uniques: {self.ap_annuel['Key'].nunique()}")
        except Exception as e:
            logger.error(f"❌ Erreur chargement AP_Annuel_clean: {e}")
            
        # 2. AP_Classement_clean.xlsx - Classements
        try:
            self.ap_classement = pd.read_excel(self.data_path / "AP_Classement_clean.xlsx")
            logger.info(f"✅ AP_Classement_clean.xlsx chargé: {len(self.ap_classement)} lignes")
            logger.info(f"   Colonnes: {list(self.ap_classement.columns)}")
            logger.info(f"   APs uniques: {self.ap_classement['Key'].nunique()}")
        except Exception as e:
            logger.error(f"❌ Erreur chargement AP_Classement_clean: {e}")
            
        # 3. AP_Synthese_clean.xlsx - Synthèse
        try:
            self.ap_synthese = pd.read_excel(self.data_path / "AP_Synthese_clean.xlsx")
            logger.info(f"✅ AP_Synthese_clean.xlsx chargé: {len(self.ap_synthese)} lignes")
            logger.info(f"   Colonnes: {list(self.ap_synthese.columns)}")
            logger.info(f"   APs uniques: {self.ap_synthese['Key'].nunique()}")
        except Exception as e:
            logger.error(f"❌ Erreur chargement AP_Synthese_clean: {e}")
            
        # 4. OutLook 2024 data - Sheet '14 MAY data'
        try:
            self.outlook_data = pd.read_excel(
                self.data_path / "OutLook 2024 data Analyse deforestation & fires.xlsx", 
                sheet_name="14 MAY data"
            )
            # Filtrer les lignes valides
            self.outlook_data = self.outlook_data[self.outlook_data['Terrestrial Protected Area Name'].notna()]
            logger.info(f"✅ OutLook 2024 '14 MAY data' chargé: {len(self.outlook_data)} lignes")
            logger.info(f"   Colonnes importantes: Terrestrial Protected Area Name, area(Ha), Tree cover loss Ha, FIRE alert")
            logger.info(f"   APs terrestres uniques: {self.outlook_data['Terrestrial Protected Area Name'].nunique()}")
        except Exception as e:
            logger.error(f"❌ Erreur chargement OutLook 2024: {e}")
            
        # 5. AP_coords.csv - Coordonnées GPS
        try:
            coords_df = pd.read_csv(self.data_path / "AP_coords.csv")
            self.ap_coords = {}
            for _, row in coords_df.iterrows():
                self.ap_coords[row['Key'].strip().upper()] = {
                    'lat': row['Latitude'], 
                    'lng': row['Longitude']
                }
            logger.info(f"✅ AP_coords.csv chargé: {len(self.ap_coords)} coordonnées")
        except Exception as e:
            logger.error(f"❌ Erreur chargement coordonnées: {e}")
            
    def create_unified_dataset(self):
        """Créer le dataset unifié en connectant toutes les sources"""
        if not all([self.ap_annuel is not None, self.ap_classement is not None, 
                   self.ap_synthese is not None, self.outlook_data is not None]):
            raise ValueError("Toutes les données de base doivent être chargées")
            
        logger.info("🔄 Création du dataset unifié...")
        
        # Utiliser les APs terrestres comme base de référence
        terrestrial_aps = self.outlook_data['Terrestrial Protected Area Name'].unique()
        logger.info(f"📊 APs terrestres de référence: {len(terrestrial_aps)}")
        
        # Créer le dataset principal avec les APs terrestres
        unified_data = []
        
        for ap_name in terrestrial_aps:
            ap_name_clean = ap_name.strip().upper()
            
            # Données de synthèse (AP_Synthese_clean)
            synthese_data = self.ap_synthese[self.ap_synthese['Key'].str.upper() == ap_name_clean]
            
            # Données de classement (AP_Classement_clean)
            classement_data = self.ap_classement[self.ap_classement['Key'].str.upper() == ap_name_clean]
            
            # Données Outlook (OutLook 2024)
            outlook_data = self.outlook_data[self.outlook_data['Terrestrial Protected Area Name'].str.upper() == ap_name_clean]
            
            # Coordonnées GPS
            coords = self.ap_coords.get(ap_name_clean, {})
            
            if not synthese_data.empty:
                synthese_row = synthese_data.iloc[0]
                classement_row = classement_data.iloc[0] if not classement_data.empty else None
                outlook_row = outlook_data.iloc[0] if not outlook_data.empty else None
                
                # Créer l'entrée unifiée
                unified_entry = {
                    'area_id': ap_name_clean,
                    'name': ap_name,
                    'gestionnaire': 'N/A',  # Pas disponible dans les fichiers actuels
                    'total_financement': float(synthese_row.get('Financement_total', 0)),
                    'lat': coords.get('lat'),
                    'lng': coords.get('lng'),
                    'superficie_ha': float(synthese_row.get('Superficie_ha', 0)),
                    'score_global': float(synthese_row.get('Score_global', 0.5)),
                    'fire_total': float(synthese_row.get('FIRE_total', 0)),
                    'fire_par_100ha': float(synthese_row.get('FIRE_par_100ha_moy', 0)),
                    'type': 'Terrestrial Protected Area',
                    
                    # Données supplémentaires de synthèse
                    'financement_par_ha_moy': float(synthese_row.get('Financement_par_ha_moy', 0)),
                    'fcl_pct_moy': float(synthese_row.get('FCL_pct_moy', 0)),
                    'fcl_ha_total': float(synthese_row.get('FCL_ha_total', 0)),
                    'ipc_moy': float(synthese_row.get('IPC_moy', 0)),
                    
                    # Données de classement si disponibles
                    's_ipc': float(classement_row.get('S_IPC', 0)) if classement_row is not None else 0,
                    's_fcl': float(classement_row.get('S_FCL', 0)) if classement_row is not None else 0,
                    's_fire': float(classement_row.get('S_FIRE', 0)) if classement_row is not None else 0,
                    
                    # Données Outlook si disponibles
                    'tree_cover_2000_ha': float(str(outlook_row.get('tree cover 2000 (Ha)', 0)).replace(',', '.')) if outlook_row is not None else 0,
                    'tree_cover_loss_ha': float(str(outlook_row.get('Tree cover loss Ha', 0)).replace(',', '.')) if outlook_row is not None else 0,
                    'fire_alerts_outlook': float(str(outlook_row.get('FIRE alert', 0)).replace(',', '.')) if outlook_row is not None else 0,
                    'fire_alerts_per_100ha_outlook': float(str(outlook_row.get('FIRE alert / 100 Ha', 0)).replace(',', '.')) if outlook_row is not None else 0,
                    'iucn_category': outlook_row.get('IUCN Category', 'N/A') if outlook_row is not None else 'N/A'
                }
                
                unified_data.append(unified_entry)
        
        logger.info(f"✅ Dataset unifié créé: {len(unified_data)} APs terrestres")
        return unified_data
        
    def create_yearly_dataset(self):
        """Créer le dataset annuel à partir d'AP_Annuel_clean"""
        if self.ap_annuel is None:
            raise ValueError("AP_Annuel_clean doit être chargé")
            
        logger.info("🔄 Création du dataset annuel...")
        
        # Utiliser les données annuelles directement
        yearly_data = self.ap_annuel.copy()
        
        # Ajouter les coordonnées
        yearly_data['lat'] = yearly_data['Key'].apply(
            lambda x: self.ap_coords.get(x.strip().upper(), {}).get('lat')
        )
        yearly_data['lng'] = yearly_data['Key'].apply(
            lambda x: self.ap_coords.get(x.strip().upper(), {}).get('lng')
        )
        
        # Renommer les colonnes pour correspondre au format attendu
        yearly_data = yearly_data.rename(columns={
            'Key': 'AP_Name',
            'Annee': 'Année',
            'Financement': 'Financement_annuel_USD',
            'FIRE_par_100ha': 'FIRE_par_100ha_moy',
            'FCL_ha': 'FCL_ha_annuel',
            'FCL_pct_surface': 'FCL_pct_surface_annuel'
        })
        
        logger.info(f"✅ Dataset annuel créé: {len(yearly_data)} lignes")
        logger.info(f"   Années: {sorted(yearly_data['Année'].unique())}")
        logger.info(f"   APs: {yearly_data['AP_Name'].nunique()}")
        
        return yearly_data
        
    def generate_dashboard_data(self):
        """Générer les données finales pour le dashboard"""
        self.load_all_data()
        
        # Créer les datasets
        unified_data = self.create_unified_dataset()
        yearly_data = self.create_yearly_dataset()
        
        # Calculer les statistiques de résumé
        total_protected_areas = len(unified_data)
        total_financement_usd = sum(d['total_financement'] for d in unified_data)
        avg_score_global = np.mean([d['score_global'] for d in unified_data if d['score_global'] is not None])
        avg_fire_rate = np.mean([d['fire_par_100ha'] for d in unified_data if d['fire_par_100ha'] is not None])
        
        # Créer la structure finale
        dashboard_data = {
            'protected_areas': {
                'analysis': {
                    'total_areas': total_protected_areas,
                    'total_area_km2': sum(d['superficie_ha'] for d in unified_data) / 100 if unified_data else 0,
                    'columns': list(unified_data[0].keys()) if unified_data else []
                },
                'data': unified_data
            },
            'summary_stats': {
                'total_protected_areas': total_protected_areas,
                'total_financement_mga': total_financement_usd,
                'avg_score_global': avg_score_global,
                'avg_deforestation_rate': avg_fire_rate
            },
            'yearly_data': yearly_data.to_dict(orient='records')
        }
        
        # Sauvegarder les fichiers
        output_path = Path("backend/data")
        output_path.mkdir(exist_ok=True)
        
        # Sauvegarder dashboard_data.json
        with open(output_path / "dashboard_data.json", "w", encoding="utf-8") as f:
            json.dump(dashboard_data, f, indent=2, default=str)
            
        # Sauvegarder unified_yearly.csv
        yearly_data.to_csv(output_path / "unified_yearly.csv", index=False)
        
        logger.info("✅ Données du dashboard générées avec succès!")
        logger.info(f"📊 Aires protégées terrestres: {total_protected_areas}")
        logger.info(f"💰 Financement total: {total_financement_usd:,.0f} USD")
        logger.info(f"🔥 Taux d'incendie moyen: {avg_fire_rate:.2f} par 100ha")
        logger.info(f"📈 Score moyen: {avg_score_global:.3f}")
        
        return dashboard_data

if __name__ == "__main__":
    print("🔄 Génération des données du dashboard avec les nouveaux fichiers...")
    processor = NewDataProcessor(".")
    processed_data = processor.generate_dashboard_data()
    print("\n🎉 Dashboard mis à jour avec les données des fichiers spécifiés!")
    print(f"- {processed_data['summary_stats']['total_protected_areas']} aires protégées terrestres")
    print(f"- {processed_data['summary_stats']['total_financement_mga']:,.0f} USD de financement total")
    print(f"- Score moyen: {processed_data['summary_stats']['avg_score_global']:.3f}")
