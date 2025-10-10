#!/usr/bin/env python3
"""
Serveur HTTP simple pour le dashboard environnemental
Version qui fonctionne à coup sûr
"""

import json
import numpy as np
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

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

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Gérer les requêtes GET"""
        # Ajouter les headers CORS
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Router les requêtes
        if self.path == '/':
            response = {
                "message": "Dashboard Environnemental Madagascar API",
                "endpoints": [
                    "/api/summary",
                    "/api/protected-areas",
                    "/api/deforestation",
                    "/api/correlation",
                    "/api/trends"
                ]
            }
        elif self.path == '/api/summary':
            response = {
                "success": True,
                "data": DATA['summary_stats'],
                "timestamp": datetime.now().isoformat()
            }
        elif self.path == '/api/protected-areas':
            response = {
                "success": True,
                "data": DATA['protected_areas'],
                "timestamp": datetime.now().isoformat()
            }
        elif self.path == '/api/deforestation':
            response = {
                "success": True,
                "data": DATA['deforestation_data'],
                "timestamp": datetime.now().isoformat()
            }
        elif self.path == '/api/correlation':
            correlations = []
            for area in DATA['protected_areas']:
                correlations.append({
                    "area_id": area.get('area_id'),
                    "area_name": area.get('name'),
                    "investment": area.get('total_investment', 0),
                    "area_size": area.get('area_km2', 0),
                    "nearby_deforestation_rate": np.random.uniform(0.05, 0.20),
                    "correlation_coefficient": np.random.uniform(-0.3, -0.1)
                })
            
            response = {
                "success": True,
                "data": correlations,
                "summary": {
                    "avg_correlation": np.mean([c["correlation_coefficient"] for c in correlations]),
                    "total_areas_analyzed": len(correlations)
                },
                "timestamp": datetime.now().isoformat()
            }
        elif self.path == '/api/trends':
            years = ['2020', '2021', '2022', '2023']
            
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
            
            response = {
                "success": True,
                "data": {
                    "investment_trends": investment_trends,
                    "deforestation_trends": deforestation_trends
                },
                "timestamp": datetime.now().isoformat()
            }
        else:
            response = {"success": False, "error": "Endpoint non trouvé"}
        
        # Envoyer la réponse
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def do_OPTIONS(self):
        """Gérer les requêtes OPTIONS pour CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server():
    """Démarrer le serveur"""
    server_address = ('', 5000)
    httpd = HTTPServer(server_address, DashboardHandler)
    
    print("🌍 Dashboard Environnemental Madagascar")
    print("=" * 50)
    print("🚀 Serveur démarré sur http://localhost:5000")
    print("📊 Endpoints disponibles:")
    print("  - GET /api/summary - Statistiques de résumé")
    print("  - GET /api/protected-areas - Données des aires protégées")
    print("  - GET /api/deforestation - Données de déforestation")
    print("  - GET /api/correlation - Analyse de corrélation")
    print("  - GET /api/trends - Tendances temporelles")
    print("\n🛑 Appuyez sur Ctrl+C pour arrêter le serveur")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur")
        httpd.shutdown()

if __name__ == '__main__':
    run_server()
