#!/usr/bin/env python3
"""
Script d'exploration des données pour le dashboard
Analyser les données d'aires protégées et de déforestation
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Import conditionnel de geopandas
try:
    import geopandas as gpd
    from shapely.geometry import Point
    GEOPANDAS_AVAILABLE = True
except ImportError:
    GEOPANDAS_AVAILABLE = False
    print("⚠️ GeoPandas non disponible, utilisation de données simulées")

class DataExplorer:
    def __init__(self, data_path="../data"):
        self.data_path = Path(data_path)
        self.ap_data = None
        self.grid_data = None
        self.mnp_data = None
        
    def load_data(self):
        """Charger toutes les données géographiques"""
        print("Chargement des données...")
        
        if GEOPANDAS_AVAILABLE:
            # Charger les aires protégées
            ap_path = self.data_path / "AP_Mada_extracted" / "AP_Mada" / "AP_update.shp"
            if ap_path.exists():
                self.ap_data = gpd.read_file(ap_path)
                print(f"Aires protégées chargées: {len(self.ap_data)} entités")
            
            # Charger la grille
            grid_path = self.data_path / "grid_1km.gpkg"
            if grid_path.exists():
                self.grid_data = gpd.read_file(grid_path)
                print(f"Grille chargée: {len(self.grid_data)} cellules")
            
            # Charger les données MNP
            mnp_path = self.data_path / "mnp_norm.gpkg"
            if mnp_path.exists():
                self.mnp_data = gpd.read_file(mnp_path)
                print(f"Données MNP chargées: {len(self.mnp_data)} entités")
        else:
            print("Utilisation de données simulées pour la démonstration")
            self.ap_data = self.create_sample_protected_areas()
            self.grid_data = self.create_sample_grid_data()
    
    def analyze_protected_areas(self):
        """Analyser les données d'aires protégées"""
        if self.ap_data is None:
            return None
            
        analysis = {
            'total_areas': len(self.ap_data),
            'total_area_km2': self.ap_data['AREA'].sum() if 'AREA' in self.ap_data.columns else 0,
            'columns': list(self.ap_data.columns),
            'sample_data': self.ap_data.head().to_dict('records')
        }
        
        # Statistiques par type d'aire protégée
        if 'TYPE' in self.ap_data.columns:
            type_stats = self.ap_data.groupby('TYPE').agg({
                'AREA': ['sum', 'mean', 'count'] if 'AREA' in self.ap_data.columns else 'count'
            }).round(2)
            # Convertir les tuples en strings pour la sérialisation JSON
            analysis['type_statistics'] = {str(k): v for k, v in type_stats.to_dict().items()}
        
        return analysis
    
    def analyze_grid_data(self):
        """Analyser les données de grille"""
        if self.grid_data is None:
            return None
            
        analysis = {
            'total_cells': len(self.grid_data),
            'columns': list(self.grid_data.columns),
            'sample_data': self.grid_data.head().to_dict('records')
        }
        
        # Statistiques numériques
        numeric_cols = self.grid_data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            analysis['numeric_statistics'] = self.grid_data[numeric_cols].describe().to_dict()
        
        return analysis
    
    def create_sample_investment_data(self):
        """Créer des données d'investissement simulées pour la démonstration"""
        if self.ap_data is None:
            return None
            
        # Simuler des données d'investissement basées sur la taille des aires protégées
        np.random.seed(42)
        
        investment_data = []
        for idx, row in self.ap_data.iterrows():
            area_km2 = row.get('AREA', 1000)  # Utiliser la colonne AREA au lieu de geometry.area
            
            # Simulation d'investissement basé sur la taille et un facteur aléatoire
            base_investment = area_km2 * np.random.uniform(1000, 5000)
            
            investment_data.append({
                'area_id': idx,
                'name': row.get('NAME', f'Area_{idx}'),
                'type': row.get('TYPE', 'Unknown'),
                'area_km2': area_km2,
                'investment_2020': base_investment,
                'investment_2021': base_investment * np.random.uniform(0.8, 1.3),
                'investment_2022': base_investment * np.random.uniform(0.9, 1.4),
                'investment_2023': base_investment * np.random.uniform(1.0, 1.5),
                'total_investment': base_investment * 4,
                'geometry': row.get('geometry', 'POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))')
            })
        
        return pd.DataFrame(investment_data)
    
    def create_deforestation_data(self):
        """Créer des données de déforestation simulées"""
        if self.grid_data is None:
            return None
            
        np.random.seed(42)
        
        # Simuler des données de déforestation
        deforestation_data = []
        for idx, row in self.grid_data.iterrows():
            deforestation_rate = np.random.uniform(0.01, 0.15)  # 1-15% par an
            
            deforestation_data.append({
                'cell_id': idx,
                'lat': row.get('lat', -18.7669),
                'lng': row.get('lng', 46.8691),
                'deforestation_2020': deforestation_rate * np.random.uniform(0.8, 1.2),
                'deforestation_2021': deforestation_rate * np.random.uniform(0.7, 1.3),
                'deforestation_2022': deforestation_rate * np.random.uniform(0.6, 1.4),
                'deforestation_2023': deforestation_rate * np.random.uniform(0.5, 1.5),
                'total_deforestation': deforestation_rate * 4,
                'geometry': f"POINT({row.get('lng', 46.8691)} {row.get('lat', -18.7669)})"
            })
        
        return pd.DataFrame(deforestation_data)
    
    def create_sample_protected_areas(self):
        """Créer des données d'aires protégées simulées"""
        np.random.seed(42)
        
        areas_data = []
        area_names = [
            "Parc National d'Andringitra", "Parc National de Ranomafana",
            "Parc National d'Isalo", "Parc National d'Ankarafantsika",
            "Parc National de Marojejy", "Parc National de Masoala",
            "Réserve Naturelle Intégrale de Tsingy de Bemaraha",
            "Réserve Spéciale d'Ankarana", "Réserve Spéciale d'Analamazaotra",
            "Site Ramsar de Lac Alaotra", "Site Ramsar de Mangoky",
            "Parc National de Kirindy Mitea", "Parc National de Tsimanampetsotsa",
            "Réserve Naturelle de Lokobe", "Parc National de Midongy du Sud"
        ]
        
        area_types = ["Parc National", "Réserve Naturelle", "Site Ramsar", "Réserve Spéciale"]
        
        for i, name in enumerate(area_names):
            area_type = np.random.choice(area_types)
            area_size = np.random.uniform(100, 2000)
            
            areas_data.append({
                'NAME': name,
                'TYPE': area_type,
                'AREA': area_size,
                'geometry': f"POLYGON(({47.0 + i*0.1} {-18.0 + i*0.1}, {47.1 + i*0.1} {-18.0 + i*0.1}, {47.1 + i*0.1} {-18.1 + i*0.1}, {47.0 + i*0.1} {-18.1 + i*0.1}, {47.0 + i*0.1} {-18.0 + i*0.1}))"
            })
        
        return pd.DataFrame(areas_data)
    
    def create_sample_grid_data(self):
        """Créer des données de grille simulées"""
        np.random.seed(42)
        
        grid_data = []
        for i in range(1000):
            grid_data.append({
                'cell_id': i,
                'lat': -18.7669 + (np.random.random() - 0.5) * 4,
                'lng': 46.8691 + (np.random.random() - 0.5) * 8,
                'deforestation_rate': np.random.uniform(0.01, 0.15)
            })
        
        return pd.DataFrame(grid_data)
    
    def generate_dashboard_data(self):
        """Générer toutes les données nécessaires pour le dashboard"""
        print("Génération des données du dashboard...")
        
        # Charger les données
        self.load_data()
        
        # Analyser les données existantes
        ap_analysis = self.analyze_protected_areas()
        grid_analysis = self.analyze_grid_data()
        
        # Créer des données simulées pour la démonstration
        investment_df = self.create_sample_investment_data()
        deforestation_df = self.create_deforestation_data()
        
        # Préparer les données pour l'API
        dashboard_data = {
            'protected_areas': {
                'analysis': ap_analysis,
                'data': investment_df.to_dict('records') if investment_df is not None else []
            },
            'grid_data': {
                'analysis': grid_analysis,
                'data': deforestation_df.to_dict('records') if deforestation_df is not None else []
            },
            'summary_stats': {
                'total_protected_areas': len(investment_df) if investment_df is not None else 0,
                'total_investment': investment_df['total_investment'].sum() if investment_df is not None else 0,
                'avg_deforestation_rate': deforestation_df['total_deforestation'].mean() if deforestation_df is not None else 0
            }
        }
        
        # Sauvegarder les données
        output_path = Path("backend/data")
        output_path.mkdir(exist_ok=True)
        
        with open(output_path / "dashboard_data.json", "w", encoding="utf-8") as f:
            json.dump(dashboard_data, f, indent=2, default=str)
        
        # Sauvegarder les DataFrames
        if investment_df is not None:
            investment_df.to_csv(output_path / "investment_data.csv", index=False)
        if deforestation_df is not None:
            deforestation_df.to_csv(output_path / "deforestation_data.csv", index=False)
        
        print("Données du dashboard générées avec succès!")
        return dashboard_data

if __name__ == "__main__":
    explorer = DataExplorer()
    data = explorer.generate_dashboard_data()
    print("\nRésumé des données générées:")
    print(f"- Aires protégées: {data['summary_stats']['total_protected_areas']}")
    print(f"- Investissement total: {data['summary_stats']['total_investment']:,.0f} USD")
    print(f"- Taux de déforestation moyen: {data['summary_stats']['avg_deforestation_rate']:.2%}")
