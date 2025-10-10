#!/usr/bin/env python3
"""
Script de génération des données pour le dashboard
Exécute l'analyse des données existantes et génère les fichiers JSON
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire data_analysis au path
sys.path.append(str(Path(__file__).parent / "data_analysis"))

from data_explorer import DataExplorer

def main():
    print("🌍 Génération des données pour le dashboard environnemental...")
    
    # Créer les répertoires nécessaires
    backend_data_dir = Path("backend/data")
    backend_data_dir.mkdir(exist_ok=True)
    
    # Initialiser l'explorateur de données
    explorer = DataExplorer(data_path="../data")
    
    try:
        # Générer les données du dashboard
        dashboard_data = explorer.generate_dashboard_data()
        
        print("\n✅ Données générées avec succès!")
        print(f"📊 Aires protégées: {dashboard_data['summary_stats']['total_protected_areas']}")
        print(f"💰 Investissement total: {dashboard_data['summary_stats']['total_investment']:,.0f} USD")
        print(f"🌳 Taux de déforestation moyen: {dashboard_data['summary_stats']['avg_deforestation_rate']:.2%}")
        
        print("\n📁 Fichiers créés:")
        print(f"  - {backend_data_dir}/dashboard_data.json")
        print(f"  - {backend_data_dir}/investment_data.csv")
        print(f"  - {backend_data_dir}/deforestation_data.csv")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération des données: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
