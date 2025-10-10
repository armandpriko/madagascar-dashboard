#!/usr/bin/env python3
"""
Backend Flask pour le dashboard d'analyse des aires protégées
API pour servir les données géographiques et statistiques
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import pandas as pd
from pathlib import Path
import numpy as np
from datetime import datetime
import logging

# Import conditionnel de geopandas
try:
    import geopandas as gpd
    GEOPANDAS_AVAILABLE = True
except ImportError:
    GEOPANDAS_AVAILABLE = False
    print("⚠️ GeoPandas non disponible, utilisation de données simulées")

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Permettre les requêtes cross-origin

# Configuration
DATA_PATH = Path("data")
STATIC_PATH = Path("static")
YEARLY_CSV = DATA_PATH / "unified_yearly.csv"

class DashboardAPI:
    def __init__(self):
        self.data = self.load_dashboard_data()
        
    def load_dashboard_data(self):
        """Charger les données du dashboard"""
        try:
            data_file = DATA_PATH / "dashboard_data.json"
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning("Fichier de données non trouvé, génération de données par défaut")
                return self.generate_default_data()
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données: {e}")
            return self.generate_default_data()
    
    def generate_default_data(self):
        """Générer des données par défaut si les vraies données ne sont pas disponibles"""
        print("⚠️ Utilisation de données par défaut - les vraies données ne sont pas disponibles")
        return {
            "protected_areas": {
                "analysis": {
                    "total_areas": 15,
                    "total_area_km2": 12500.5,
                    "columns": ["NAME", "TYPE", "AREA", "geometry"]
                },
                "data": [
                    {
                        "area_id": i,
                        "name": f"Aire Protégée {i+1}",
                        "type": np.random.choice(["Parc National", "Réserve Naturelle", "Site Ramsar"]),
                        "area_km2": np.random.uniform(100, 2000),
                        "investment_2020": np.random.uniform(50000, 500000),
                        "investment_2021": np.random.uniform(60000, 600000),
                        "investment_2022": np.random.uniform(70000, 700000),
                        "investment_2023": np.random.uniform(80000, 800000),
                        "total_investment": np.random.uniform(200000, 2000000)
                    }
                    for i in range(15)
                ]
            },
            "grid_data": {
                "analysis": {
                    "total_cells": 1000,
                    "columns": ["cell_id", "deforestation_rate", "geometry"]
                },
                "data": [
                    {
                        "cell_id": i,
                        "deforestation_2020": np.random.uniform(0.01, 0.15),
                        "deforestation_2021": np.random.uniform(0.01, 0.15),
                        "deforestation_2022": np.random.uniform(0.01, 0.15),
                        "deforestation_2023": np.random.uniform(0.01, 0.15),
                        "total_deforestation": np.random.uniform(0.04, 0.60)
                    }
                    for i in range(1000)
                ]
            },
            "summary_stats": {
                "total_protected_areas": 15,
                "total_investment": 15000000,
                "avg_deforestation_rate": 0.12
            }
        }

# Instance de l'API
api = DashboardAPI()

def load_yearly_df():
    if YEARLY_CSV.exists():
        try:
            return pd.read_csv(YEARLY_CSV)
        except Exception as e:
            logger.error(f"Erreur lecture unified_yearly.csv: {e}")
    return pd.DataFrame()

@app.route('/')
def index():
    """Page d'accueil"""
    return send_from_directory(STATIC_PATH, 'index.html')

@app.route('/api/summary')
def get_summary():
    """Obtenir les statistiques de résumé"""
    try:
        return jsonify({
            "success": True,
            "data": api.data["summary_stats"],
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Erreur dans get_summary: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/protected-areas')
def get_protected_areas():
    """Obtenir les données des aires protégées"""
    try:
        # Paramètres de filtrage
        area_type = request.args.get('type')
        min_area = request.args.get('min_area', type=float)
        max_area = request.args.get('max_area', type=float)
        
        data = api.data["protected_areas"]["data"]
        
        # Appliquer les filtres
        if area_type:
            data = [area for area in data if area.get('type') == area_type]
        
        if min_area is not None:
            data = [area for area in data if area.get('area_km2', 0) >= min_area]
            
        if max_area is not None:
            data = [area for area in data if area.get('area_km2', 0) <= max_area]
        
        return jsonify({
            "success": True,
            "data": data,
            "analysis": api.data["protected_areas"]["analysis"],
            "filters_applied": {
                "type": area_type,
                "min_area": min_area,
                "max_area": max_area
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Erreur dans get_protected_areas: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/deforestation')
def get_deforestation():
    """Obtenir les données de déforestation (tolère l'absence de grid_data)"""
    try:
        # Paramètres de filtrage
        min_rate = request.args.get('min_rate', type=float)
        max_rate = request.args.get('max_rate', type=float)
        year = request.args.get('year', 'total')

        # Si grid_data n'existe pas, retourner une liste vide pour ne pas casser le frontend
        if "grid_data" not in api.data or "data" not in api.data["grid_data"]:
            return jsonify({
                "success": True,
                "data": [],
                "analysis": {"total_cells": 0, "columns": []},
                "filters_applied": {"min_rate": min_rate, "max_rate": max_rate, "year": year},
                "timestamp": datetime.now().isoformat()
            })

        data = api.data["grid_data"]["data"]

        # Appliquer les filtres
        if min_rate is not None:
            data = [cell for cell in data if cell.get(f'deforestation_{year}', cell.get('total_deforestation', 0)) >= min_rate]
        if max_rate is not None:
            data = [cell for cell in data if cell.get(f'deforestation_{year}', cell.get('total_deforestation', 0)) <= max_rate]

        return jsonify({
            "success": True,
            "data": data,
            "analysis": api.data["grid_data"].get("analysis", {}),
            "filters_applied": {"min_rate": min_rate, "max_rate": max_rate, "year": year},
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Erreur dans get_deforestation: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/correlation')
def get_correlation():
    """Corrélation simple: financement total vs indicateur pression (feux/ha ou 1-score)"""
    try:
        protected_areas = api.data["protected_areas"]["data"]

        points = []
        for area in protected_areas:
            inv = area.get('total_financement') or area.get('total_investment') or 0
            pressure = area.get('fire_par_100ha')
            if pressure is None:
                score = area.get('score_global')
                pressure = (1 - score) if score is not None else None
            if pressure is not None:
                points.append({"x": inv, "y": pressure, "area_name": area.get('name')})

        corr = None
        if len(points) >= 2:
            x = np.array([p["x"] for p in points], dtype=float)
            y = np.array([p["y"] for p in points], dtype=float)
            if x.std() > 0 and y.std() > 0:
                corr = float(np.corrcoef(x, y)[0, 1])

        return jsonify({
            "success": True,
            "data": points,
            "summary": {"avg_correlation": corr, "total_areas_analyzed": len(points)},
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Erreur dans get_correlation: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/trends')
def get_trends():
    """Obtenir les tendances temporelles à partir des champs disponibles"""
    try:
        years_set = set()
        for area in api.data["protected_areas"]["data"]:
            for key in area.keys():
                if key.startswith('financement_') or key.startswith('investment_'):
                    y = key.split('_')[-1]
                    if y.isdigit():
                        years_set.add(y)
        years = sorted(list(years_set)) or ['2020', '2021', '2022', '2023']

        investment_trends = []
        for year in years:
            total = 0.0
            for area in api.data["protected_areas"]["data"]:
                total += area.get(f'financement_{year}', 0) or area.get(f'investment_{year}', 0) or 0
            avg = total / max(1, len(api.data["protected_areas"]["data"]))
            investment_trends.append({"year": year, "total_investment": total, "avg_investment_per_area": avg})

        deforestation_trends = [{"year": y, "avg_deforestation_rate": None, "total_deforestation": None} for y in years]

        return jsonify({
            "success": True,
            "data": {"investment_trends": investment_trends, "deforestation_trends": deforestation_trends},
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Erreur dans get_trends: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/aps')
def list_aps():
    """Lister les AP disponibles (terrestres) depuis unified_yearly.csv"""
    try:
        df = load_yearly_df()
        if df.empty:
            names = sorted({a.get('name') for a in api.data.get('protected_areas', {}).get('data', []) if a.get('name')})
            return jsonify({"success": True, "data": names})
        names = sorted(df['AP_Name'].dropna().unique().tolist())
        return jsonify({"success": True, "data": names})
    except Exception as e:
        logger.error(f"Erreur dans /api/aps: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/yearly')
def get_yearly():
    """Tableau annuel unifié avec filtres ?ap=...&start=2007&end=2023"""
    try:
        ap = request.args.get('ap')
        start = request.args.get('start', type=int)
        end = request.args.get('end', type=int)
        df = load_yearly_df()
        if df.empty:
            return jsonify({"success": True, "data": [], "count": 0})
        if ap:
            df = df[df['AP_Name'].str.upper() == ap.upper()]
        if start:
            df = df[df['Année'] >= start]
        if end:
            df = df[df['Année'] <= end]
        df = df.sort_values(['Année'])
        return jsonify({
            "success": True,
            "data": df.to_dict(orient='records'),
            "years": sorted(df['Année'].unique().tolist()),
            "count": len(df)
        })
    except Exception as e:
        logger.error(f"Erreur dans /api/yearly: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/geojson/protected-areas')
def get_protected_areas_geojson():
    """Obtenir les aires protégées en format GeoJSON"""
    try:
        # Simuler des données GeoJSON pour la démonstration
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "id": area.get('area_id'),
                        "name": area.get('name'),
                        "type": area.get('type'),
                        "area_km2": area.get('area_km2'),
                        "total_investment": area.get('total_investment')
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [47.0 + i*0.1, -18.0 + i*0.1],
                            [47.1 + i*0.1, -18.0 + i*0.1],
                            [47.1 + i*0.1, -18.1 + i*0.1],
                            [47.0 + i*0.1, -18.1 + i*0.1],
                            [47.0 + i*0.1, -18.0 + i*0.1]
                        ]]
                    }
                }
                for i, area in enumerate(api.data["protected_areas"]["data"])
            ]
        }
        
        return jsonify(geojson)
    except Exception as e:
        logger.error(f"Erreur dans get_protected_areas_geojson: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": "Endpoint non trouvé"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "error": "Erreur interne du serveur"}), 500

if __name__ == '__main__':
    # Créer les dossiers nécessaires
    DATA_PATH.mkdir(exist_ok=True)
    STATIC_PATH.mkdir(exist_ok=True)
    
    print("🌍 Démarrage du serveur API du dashboard environnemental...")
    print("📊 Endpoints disponibles:")
    print("  - GET /api/summary - Statistiques de résumé")
    print("  - GET /api/protected-areas - Données des aires protégées")
    print("  - GET /api/deforestation - Données de déforestation")
    print("  - GET /api/correlation - Analyse de corrélation")
    print("  - GET /api/trends - Tendances temporelles")
    print("  - GET /api/geojson/protected-areas - GeoJSON des aires protégées")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
