#!/usr/bin/env python3
"""
Serveur Flask simplifié pour le dashboard environnemental
Version qui fonctionne sans dépendances complexes
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import numpy as np
from datetime import datetime
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Permettre les requêtes cross-origin

# Données simulées pour la démonstration
def generate_sample_data():
    """Générer des données d'exemple pour le dashboard"""
    np.random.seed(42)
    
    # Aires protégées
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
    
    protected_areas = []
    for i, name in enumerate(area_names):
        area_type = np.random.choice(area_types)
        area_size = np.random.uniform(100, 2000)
        base_investment = area_size * np.random.uniform(1000, 5000)
        
        protected_areas.append({
            'area_id': i,
            'name': name,
            'type': area_type,
            'area_km2': round(area_size, 1),
            'investment_2020': round(base_investment),
            'investment_2021': round(base_investment * np.random.uniform(0.8, 1.3)),
            'investment_2022': round(base_investment * np.random.uniform(0.9, 1.4)),
            'investment_2023': round(base_investment * np.random.uniform(1.0, 1.5)),
            'total_investment': round(base_investment * 4),
            'lat': -18.7669 + (np.random.random() - 0.5) * 4,
            'lng': 46.8691 + (np.random.random() - 0.5) * 8
        })
    
    # Données de déforestation
    deforestation_data = []
    for i in range(1000):
        deforestation_rate = np.random.uniform(0.01, 0.15)
        deforestation_data.append({
            'cell_id': i,
            'lat': -18.7669 + (np.random.random() - 0.5) * 4,
            'lng': 46.8691 + (np.random.random() - 0.5) * 8,
            'deforestation_2020': round(deforestation_rate * np.random.uniform(0.8, 1.2), 3),
            'deforestation_2021': round(deforestation_rate * np.random.uniform(0.7, 1.3), 3),
            'deforestation_2022': round(deforestation_rate * np.random.uniform(0.6, 1.4), 3),
            'deforestation_2023': round(deforestation_rate * np.random.uniform(0.5, 1.5), 3),
            'total_deforestation': round(deforestation_rate * 4, 3)
        })
    
    return {
        'protected_areas': protected_areas,
        'deforestation_data': deforestation_data,
        'summary_stats': {
            'total_protected_areas': len(protected_areas),
            'total_investment': sum(area['total_investment'] for area in protected_areas),
            'avg_deforestation_rate': np.mean([cell['total_deforestation'] for cell in deforestation_data])
        }
    }

# Générer les données
DATA = generate_sample_data()

@app.route('/')
def index():
    """Page d'accueil"""
    return jsonify({
        "message": "Dashboard Environnemental Madagascar API",
        "endpoints": [
            "/api/summary",
            "/api/protected-areas",
            "/api/deforestation",
            "/api/correlation",
            "/api/trends"
        ]
    })

@app.route('/api/summary')
def get_summary():
    """Obtenir les statistiques de résumé"""
    try:
        return jsonify({
            "success": True,
            "data": DATA['summary_stats'],
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
        
        data = DATA['protected_areas'].copy()
        
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
    """Obtenir les données de déforestation"""
    try:
        # Paramètres de filtrage
        min_rate = request.args.get('min_rate', type=float)
        max_rate = request.args.get('max_rate', type=float)
        year = request.args.get('year', 'total')
        
        data = DATA['deforestation_data'].copy()
        
        # Appliquer les filtres
        if min_rate is not None:
            data = [cell for cell in data if cell.get(f'deforestation_{year}', cell.get('total_deforestation', 0)) >= min_rate]
            
        if max_rate is not None:
            data = [cell for cell in data if cell.get(f'deforestation_{year}', cell.get('total_deforestation', 0)) <= max_rate]
        
        return jsonify({
            "success": True,
            "data": data,
            "filters_applied": {
                "min_rate": min_rate,
                "max_rate": max_rate,
                "year": year
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Erreur dans get_deforestation: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/correlation')
def get_correlation():
    """Analyser la corrélation entre investissement et déforestation"""
    try:
        correlations = []
        
        for area in DATA['protected_areas']:
            area_investment = area.get('total_investment', 0)
            area_size = area.get('area_km2', 0)
            
            # Simuler l'impact sur la déforestation environnante
            nearby_deforestation = np.random.uniform(0.05, 0.20)
            
            correlations.append({
                "area_id": area.get('area_id'),
                "area_name": area.get('name'),
                "investment": area_investment,
                "area_size": area_size,
                "nearby_deforestation_rate": nearby_deforestation,
                "correlation_coefficient": np.random.uniform(-0.3, -0.1)
            })
        
        return jsonify({
            "success": True,
            "data": correlations,
            "summary": {
                "avg_correlation": np.mean([c["correlation_coefficient"] for c in correlations]),
                "total_areas_analyzed": len(correlations)
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Erreur dans get_correlation: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/trends')
def get_trends():
    """Obtenir les tendances temporelles"""
    try:
        years = ['2020', '2021', '2022', '2023']
        
        # Tendances d'investissement
        investment_trends = []
        for year in years:
            total_investment = sum(
                area.get(f'investment_{year}', 0) 
                for area in DATA['protected_areas']
            )
            investment_trends.append({
                "year": year,
                "total_investment": total_investment,
                "avg_investment_per_area": total_investment / len(DATA['protected_areas'])
            })
        
        # Tendances de déforestation
        deforestation_trends = []
        for year in years:
            avg_deforestation = np.mean([
                cell.get(f'deforestation_{year}', 0) 
                for cell in DATA['deforestation_data']
            ])
            deforestation_trends.append({
                "year": year,
                "avg_deforestation_rate": avg_deforestation,
                "total_deforestation": avg_deforestation * len(DATA['deforestation_data'])
            })
        
        return jsonify({
            "success": True,
            "data": {
                "investment_trends": investment_trends,
                "deforestation_trends": deforestation_trends
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Erreur dans get_trends: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": "Endpoint non trouvé"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "error": "Erreur interne du serveur"}), 500

if __name__ == '__main__':
    print("🌍 Démarrage du serveur API du dashboard environnemental...")
    print("📊 Endpoints disponibles:")
    print("  - GET /api/summary - Statistiques de résumé")
    print("  - GET /api/protected-areas - Données des aires protégées")
    print("  - GET /api/deforestation - Données de déforestation")
    print("  - GET /api/correlation - Analyse de corrélation")
    print("  - GET /api/trends - Tendances temporelles")
    print("\n🌐 Serveur démarré sur http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
