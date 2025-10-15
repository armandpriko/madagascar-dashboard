#!/usr/bin/env python3
"""
CARTE INTERACTIVE MADAGASCAR : Visualisation Géographique des Aires Protégées
==============================================================================

Carte interactive HTML avec fond OpenStreetMap montrant les 56 AP analysées avec :
- Positionnement géographique précis sur vraie carte
- Taille des points = Superficie de l'AP
- Couleur = Catégorie (Champions, Critiques, etc.)
- Popup avec détails complets au clic
- Zoom/Pan interactif

Par KOUMI Dzudzogbe Prince Armand
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
import folium
from folium import plugins
import warnings
warnings.filterwarnings('ignore')

class CarteInteractiveMadagascar:
    """Générateur de carte interactive Madagascar avec les AP"""
    
    def __init__(self, data_path="."):
        self.data_path = Path(data_path)
        self.output_dir = self.data_path / "frontend"
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
    def load_data(self):
        """Charger les données"""
        print("📂 Chargement des données...")
        
        # Coordonnées GPS
        self.coords = pd.read_csv(self.data_path / "AP_coords.csv")
        print(f"✅ Coordonnées : {len(self.coords)} AP")
        
        # Rapport d'analyse
        rapport_path = self.data_path / "backend/data/analyse_financement_deforestation.json"
        with open(rapport_path, 'r') as f:
            self.rapport = json.load(f)
        
        # Segmentation
        self.segmentation = pd.DataFrame(self.rapport['ap_segmentation'])
        print(f"✅ Segmentation : {len(self.segmentation)} AP analysées")
        
        # Fusionner
        self.data = self.merge_data()
        print(f"✅ Données fusionnées : {len(self.data)} AP avec coordonnées")
        
    def merge_data(self):
        """Fusionner coordonnées et segmentation"""
        data = []
        
        for _, seg in self.segmentation.iterrows():
            ap_name = seg['AP_Name'].upper().strip()
            
            # Sauter les lignes de total
            if ap_name == 'TOTAL':
                continue
            
            # Trouver les coordonnées
            coord = None
            for _, c in self.coords.iterrows():
                key = str(c['Key']).upper().strip()
                
                # Correspondances exactes ou partielles
                if key in ap_name or ap_name in key:
                    coord = c
                    break
                    
                # Cas spéciaux
                if 'MONTAGNE DES FRANCAIS' in ap_name and 'MONTAGNE DES FRANCAIS' in key:
                    coord = c
                    break
                if 'TSIMEMBO' in ap_name and 'TSIMEMBO' in key:
                    coord = c
                    break
                if 'ITREMO' in ap_name and 'ITREMO' in key:
                    coord = c
                    break
            
            if coord is not None:
                data.append({
                    'name': seg['AP_Name'],
                    'lat': coord['Latitude'],
                    'lng': coord['Longitude'],
                    'superficie_ha': seg['Superficie_ha'],
                    'fire_rate': seg['FIRE_par_100ha_moy'],
                    'financement': seg['Financement_annuel_USD'],
                    'financement_par_ha': seg['Financement_par_ha'],
                    'categorie': seg['Categorie'],
                    'efficacite_score': seg['Efficacite_Score']
                })
        
        return pd.DataFrame(data)
    
    def get_color_from_category(self, categorie):
        """Obtenir la couleur selon la catégorie"""
        if '🌟 EFFICACES' in categorie:
            return '#2ecc71'  # Vert
        elif '🌱 NATURELLEMENT' in categorie:
            return '#a8e6cf'  # Vert clair
        elif '⚠️  SOUS PRESSION' in categorie:
            return '#f39c12'  # Orange
        elif '🚨 CRITIQUES' in categorie:
            return '#e74c3c'  # Rouge
        else:
            return '#95a5a6'  # Gris par défaut
    
    def get_category_emoji(self, categorie):
        """Obtenir l'emoji de la catégorie"""
        if '🌟 EFFICACES' in categorie:
            return '🌟'
        elif '🌱 NATURELLEMENT' in categorie:
            return '🌱'
        elif '⚠️  SOUS PRESSION' in categorie:
            return '⚠️'
        elif '🚨 CRITIQUES' in categorie:
            return '🚨'
        else:
            return '❓'
    
    def format_number(self, num):
        """Formater un nombre avec séparateurs"""
        if num >= 1e9:
            return f"{num/1e9:.2f} Mds"
        elif num >= 1e6:
            return f"{num/1e6:.2f} M"
        elif num >= 1e3:
            return f"{num/1e3:.1f} K"
        else:
            return f"{num:.0f}"
    
    def create_interactive_map(self):
        """Créer la carte interactive principale"""
        print("\n🗺️  Génération de la carte interactive...")
        
        # Créer la carte centrée sur Madagascar
        m = folium.Map(
            location=[-18.8792, 47.5079],  # Centre de Madagascar
            zoom_start=6,
            tiles='OpenStreetMap',
            control_scale=True
        )
        
        # Ajouter contrôle de couches avec attributions
        folium.TileLayer(
            tiles='https://tiles.stadiamaps.com/tiles/stamen_terrain/{z}/{x}/{y}.png',
            attr='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> &copy; <a href="https://stamen.com/">Stamen Design</a> &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
            name='Terrain',
            overlay=False,
            control=True
        ).add_to(m)
        
        folium.TileLayer(
            tiles='CartoDB positron',
            name='Carto Light',
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/">CARTO</a>'
        ).add_to(m)
        
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
            name='Satellite',
            overlay=False,
            control=True
        ).add_to(m)
        
        # Normaliser les superficies pour la taille des marqueurs
        superficies_norm = self.data['superficie_ha'] / self.data['superficie_ha'].max()
        
        # Créer des groupes de marqueurs par catégorie
        feature_groups = {
            '🌟 EFFICACES': folium.FeatureGroup(name='🌟 EFFICACES (Investis + Protégés)'),
            '🌱 NATURELLEMENT': folium.FeatureGroup(name='🌱 NATURELLEMENT PROTÉGÉES'),
            '⚠️  SOUS PRESSION': folium.FeatureGroup(name='⚠️ SOUS PRESSION'),
            '🚨 CRITIQUES': folium.FeatureGroup(name='🚨 CRITIQUES (Urgent!)')
        }
        
        # Ajouter chaque AP comme marqueur
        for _, ap in self.data.iterrows():
            # Calculer la taille du marqueur (entre 5 et 30)
            size = 8 + (ap['superficie_ha'] / self.data['superficie_ha'].max()) * 22
            
            # Couleur selon catégorie
            color = self.get_color_from_category(ap['categorie'])
            emoji = self.get_category_emoji(ap['categorie'])
            
            # Créer le popup HTML avec détails
            popup_html = f"""
            <div style="font-family: Arial; width: 300px;">
                <h3 style="color: {color}; margin-bottom: 10px;">
                    {emoji} {ap['name']}
                </h3>
                <table style="width: 100%; font-size: 12px;">
                    <tr>
                        <td><b>📊 Catégorie:</b></td>
                        <td>{ap['categorie']}</td>
                    </tr>
                    <tr style="background-color: #f8f9fa;">
                        <td><b>📐 Superficie:</b></td>
                        <td>{self.format_number(ap['superficie_ha'])} ha</td>
                    </tr>
                    <tr>
                        <td><b>💰 Financement:</b></td>
                        <td>${self.format_number(ap['financement'])} USD/an</td>
                    </tr>
                    <tr style="background-color: #f8f9fa;">
                        <td><b>💵 Financement/ha:</b></td>
                        <td>${ap['financement_par_ha']:.0f} USD/ha</td>
                    </tr>
                    <tr>
                        <td><b>🔥 Taux de feu:</b></td>
                        <td>{ap['fire_rate']:.4f} feux/100ha</td>
                    </tr>
                    <tr style="background-color: #f8f9fa;">
                        <td><b>⭐ Score efficacité:</b></td>
                        <td>{ap['efficacite_score']:.4f}</td>
                    </tr>
                    <tr>
                        <td><b>📍 Position:</b></td>
                        <td>{ap['lat']:.4f}, {ap['lng']:.4f}</td>
                    </tr>
                </table>
            </div>
            """
            
            # Créer le marqueur circulaire
            folium.CircleMarker(
                location=[ap['lat'], ap['lng']],
                radius=size,
                popup=folium.Popup(popup_html, max_width=350),
                tooltip=f"{ap['name']} ({self.format_number(ap['superficie_ha'])} ha)",
                color='black',
                weight=2,
                fill=True,
                fillColor=color,
                fillOpacity=0.7
            ).add_to(self.get_feature_group(ap['categorie'], feature_groups))
        
        # Ajouter les groupes à la carte
        for group in feature_groups.values():
            group.add_to(m)
        
        # Ajouter contrôle de couches
        folium.LayerControl(collapsed=False).add_to(m)
        
        # Ajouter plugin fullscreen
        plugins.Fullscreen(
            position='topright',
            title='Plein écran',
            title_cancel='Sortir du plein écran',
            force_separate_button=True
        ).add_to(m)
        
        # Ajouter minimap
        minimap = plugins.MiniMap(toggle_display=True)
        m.add_child(minimap)
        
        # Ajouter mesure de distance
        plugins.MeasureControl(
            position='topleft',
            primary_length_unit='kilometers',
            secondary_length_unit='miles',
            primary_area_unit='hectares',
            secondary_area_unit='sqmiles'
        ).add_to(m)
        
        # Ajouter marqueurs des villes principales
        villes = {
            'Antananarivo': (-18.9, 47.5),
            'Toamasina': (-18.1, 49.4),
            'Toliara': (-23.4, 43.7),
            'Mahajanga': (-15.7, 46.3),
            'Antsiranana': (-12.3, 49.3)
        }
        
        villes_group = folium.FeatureGroup(name='🏙️ Villes principales', show=True)
        
        for ville, (lat, lng) in villes.items():
            folium.Marker(
                location=[lat, lng],
                popup=f"<b>{ville}</b><br>Ville principale",
                tooltip=ville,
                icon=folium.Icon(color='gray', icon='home', prefix='fa')
            ).add_to(villes_group)
        
        villes_group.add_to(m)
        
        # Ajouter titre personnalisé
        title_html = '''
        <div style="position: fixed; 
                    top: 10px; 
                    left: 50px; 
                    width: 500px; 
                    height: auto; 
                    background-color: white; 
                    border: 2px solid #2ecc71;
                    border-radius: 5px;
                    z-index: 9999; 
                    padding: 10px;
                    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">
            <h2 style="margin: 0; color: #2c3e50; font-size: 18px;">
                🗺️ CARTE INTERACTIVE - MADAGASCAR
            </h2>
            <p style="margin: 5px 0; font-size: 12px; color: #7f8c8d;">
                <b>56 Aires Protégées</b> | Taille = Superficie | Couleur = Efficacité<br>
                <span style="font-size: 10px;">Par KOUMI Dzudzogbe Prince Armand</span>
            </p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(title_html))
        
        # Ajouter légende
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; 
                    right: 50px; 
                    width: 250px; 
                    background-color: white; 
                    border: 2px solid gray;
                    border-radius: 5px;
                    z-index: 9999; 
                    padding: 10px;
                    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">
            <h4 style="margin: 0 0 10px 0; color: #2c3e50;">Légende</h4>
            <p style="margin: 5px 0; font-size: 12px;">
                <span style="color: #2ecc71;">●</span> <b>Efficaces</b> - Investis + Protégés<br>
                <span style="color: #a8e6cf;">●</span> <b>Naturellement protégées</b><br>
                <span style="color: #f39c12;">●</span> <b>Sous pression</b> - Fragiles<br>
                <span style="color: #e74c3c;">●</span> <b>Critiques</b> - Urgent!<br>
            </p>
            <p style="margin: 10px 0 0 0; font-size: 11px; color: #7f8c8d;">
                💡 Cliquez sur les cercles pour voir les détails
            </p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        # Sauvegarder
        output_file = self.output_dir / 'carte_madagascar_interactive.html'
        m.save(str(output_file))
        
        print(f"✅ Carte interactive sauvegardée : {output_file}")
        return output_file
    
    def get_feature_group(self, categorie, groups):
        """Obtenir le groupe de features correspondant à la catégorie"""
        if '🌟 EFFICACES' in categorie:
            return groups['🌟 EFFICACES']
        elif '🌱 NATURELLEMENT' in categorie:
            return groups['🌱 NATURELLEMENT']
        elif '⚠️  SOUS PRESSION' in categorie:
            return groups['⚠️  SOUS PRESSION']
        elif '🚨 CRITIQUES' in categorie:
            return groups['🚨 CRITIQUES']
        else:
            return groups['🚨 CRITIQUES']
    
    def create_statistics_overlay(self):
        """Créer une page HTML avec statistiques et carte"""
        print("\n📊 Génération de la page complète avec statistiques...")
        
        # Calculer statistiques à partir de TOUTES les données (pas seulement celles avec coordonnées)
        all_segmentation = pd.DataFrame(self.rapport['ap_segmentation'])
        # Exclure seulement la ligne TOTAL
        all_aps = all_segmentation[all_segmentation['AP_Name'] != 'TOTAL']
        
        # Identifier les AP sans coordonnées
        ap_sans_coords = []
        for _, ap in all_aps.iterrows():
            ap_name = ap['AP_Name'].upper().strip()
            coord_trouvee = False
            
            for _, c in self.coords.iterrows():
                key = str(c['Key']).upper().strip()
                if key in ap_name or ap_name in key:
                    coord_trouvee = True
                    break
                # Cas spéciaux
                if 'MONTAGNE DES FRANCAIS' in ap_name and 'MONTAGNE DES FRANCAIS' in key:
                    coord_trouvee = True
                    break
                if 'TSIMEMBO' in ap_name and 'TSIMEMBO' in key:
                    coord_trouvee = True
                    break
                if 'ITREMO' in ap_name and 'ITREMO' in key:
                    coord_trouvee = True
                    break
            
            if not coord_trouvee:
                ap_sans_coords.append(ap['AP_Name'])
        
        print(f"⚠️  AP sans coordonnées GPS : {ap_sans_coords}")
        
        stats = {
            'total_ap': len(all_aps),  # Toutes les AP (pas seulement celles avec coordonnées)
            'total_superficie': all_aps['Superficie_ha'].sum(),
            'total_financement': all_aps['Financement_annuel_USD'].sum(),
            'efficaces': len(all_aps[all_aps['Categorie'].str.contains('EFFICACES')]),
            'naturelles': len(all_aps[all_aps['Categorie'].str.contains('NATURELLEMENT')]),
            'pression': len(all_aps[all_aps['Categorie'].str.contains('SOUS PRESSION')]),
            'critiques': len(all_aps[all_aps['Categorie'].str.contains('CRITIQUES')]),
            'fire_rate_moyen': all_aps['FIRE_par_100ha_moy'].mean(),
            'financement_moyen': all_aps['Financement_annuel_USD'].mean()
        }
        
        html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Carte Interactive - Aires Protégées de Madagascar</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f6fa;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
            color: white;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        .stats-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            padding: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.2s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .stat-card .value {{
            font-size: 32px;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .stat-card .label {{
            font-size: 14px;
            color: #7f8c8d;
        }}
        
        .efficace {{ color: #2ecc71; }}
        .naturelle {{ color: #a8e6cf; }}
        .pression {{ color: #f39c12; }}
        .critique {{ color: #e74c3c; }}
        
        .map-container {{
            width: 100%;
            height: calc(100vh - 300px);
            min-height: 600px;
        }}
        
        iframe {{
            width: 100%;
            height: 100%;
            border: none;
        }}
        
        .footer {{
            background-color: #2c3e50;
            color: white;
            text-align: center;
            padding: 15px;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🗺️ CARTE INTERACTIVE DES AIRES PROTÉGÉES DE MADAGASCAR</h1>
        <p>Analyse de l'efficacité des financements sur 56 Aires Protégées | Par KOUMI Dzudzogbe Prince Armand</p>
    </div>
    
    <div class="stats-container">
        <div class="stat-card">
            <div class="label">📍 AIRES PROTÉGÉES</div>
            <div class="value">{stats['total_ap']}</div>
            <div class="label">AP cartographiées</div>
        </div>
        
        <div class="stat-card">
            <div class="label">📐 SUPERFICIE TOTALE</div>
            <div class="value">{stats['total_superficie']/1e6:.2f}</div>
            <div class="label">Millions d'hectares</div>
        </div>
        
        <div class="stat-card">
            <div class="label">💰 FINANCEMENT TOTAL</div>
            <div class="value">${stats['total_financement']/1e9:.2f}</div>
            <div class="label">Milliards USD/an</div>
        </div>
        
        <div class="stat-card">
            <div class="label efficace">🌟 EFFICACES</div>
            <div class="value efficace">{stats['efficaces']}</div>
            <div class="label">Investis + Protégés</div>
        </div>
        
        <div class="stat-card">
            <div class="label naturelle">🌱 NATURELLES</div>
            <div class="value naturelle">{stats['naturelles']}</div>
            <div class="label">Naturellement protégées</div>
        </div>
        
        <div class="stat-card">
            <div class="label pression">⚠️ SOUS PRESSION</div>
            <div class="value pression">{stats['pression']}</div>
            <div class="label">Investis mais fragiles</div>
        </div>
        
        <div class="stat-card">
            <div class="label critique">🚨 CRITIQUES</div>
            <div class="value critique">{stats['critiques']}</div>
            <div class="label">Intervention urgente!</div>
        </div>
        
        <div class="stat-card">
            <div class="label">🔥 TAUX DE FEU MOYEN</div>
            <div class="value">{stats['fire_rate_moyen']:.3f}</div>
            <div class="label">Feux/100ha</div>
        </div>
        
        <div class="stat-card">
            <div class="label">📍 AP CARTOGRAPHIÉES</div>
            <div class="value">{len(self.data)}</div>
            <div class="label">sur {stats['total_ap']} analysées</div>
        </div>
    </div>
    
    <div style="padding: 20px; max-width: 1400px; margin: 0 auto;">
        <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h3 style="color: #2c3e50; margin-bottom: 10px;">📊 Note sur les données</h3>
            <p style="margin: 5px 0; font-size: 14px; color: #7f8c8d;">
                • <strong>{len(self.data)} AP</strong> ont des coordonnées GPS et sont visibles sur la carte<br>
                • <strong>{len(ap_sans_coords)} AP</strong> n'ont pas de coordonnées GPS : {', '.join(ap_sans_coords) if ap_sans_coords else 'Aucune'}<br>
                • Les statistiques affichées incluent <strong>toutes les {stats['total_ap']} AP</strong> analysées<br>
                • Financement total : <strong>${stats['total_financement']/1e9:.2f} milliards USD</strong> (2007-2023)
            </p>
        </div>
    </div>
    
    <div class="map-container">
        <iframe src="carte_madagascar_interactive.html"></iframe>
    </div>
    
    <div class="footer">
        © 2025 KOUMI Dzudzogbe Prince Armand | Analyse Financement vs Déforestation - Madagascar<br>
        Données : 2007-2023 | Sources : MNP, Bailleurs internationaux, FIRMS NASA
    </div>
</body>
</html>
        """
        
        output_file = self.output_dir / 'carte_madagascar_complete.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Page complète sauvegardée : {output_file}")
        return output_file
    
    def generate_all_maps(self):
        """Générer toutes les cartes interactives"""
        print("\n" + "="*70)
        print("🗺️  GÉNÉRATION DES CARTES INTERACTIVES MADAGASCAR")
        print("="*70 + "\n")
        
        self.load_data()
        
        # Carte interactive
        carte_interactive = self.create_interactive_map()
        
        # Page complète avec stats
        page_complete = self.create_statistics_overlay()
        
        print("\n" + "="*70)
        print("✅ TOUTES LES CARTES INTERACTIVES GÉNÉRÉES AVEC SUCCÈS")
        print("="*70)
        print(f"\n📁 Fichiers créés :")
        print(f"   1. {carte_interactive.name} (carte interactive seule)")
        print(f"   2. {page_complete.name} (page complète avec statistiques)")
        print(f"\n📍 {len(self.data)} AP positionnées avec succès sur {len(self.segmentation)-1} analysées")
        print(f"   ({len(self.data)/(len(self.segmentation)-1)*100:.1f}% de couverture GPS)")
        print(f"\n🌐 Ouvrez {page_complete.name} dans votre navigateur pour voir la carte!")
        print("\n")


if __name__ == "__main__":
    generator = CarteInteractiveMadagascar()
    generator.generate_all_maps()

