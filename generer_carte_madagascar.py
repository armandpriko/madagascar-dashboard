#!/usr/bin/env python3
"""
CARTE MADAGASCAR : Visualisation Géographique des Aires Protégées
==================================================================

Carte interactive montrant les 56 AP analysées avec :
- Positionnement géographique précis
- Taille des points = Superficie de l'AP
- Couleur = Catégorie (Champions, Critiques, etc.)

Par KOUMI Dzudzogbe Prince Armand
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import json
import warnings
warnings.filterwarnings('ignore')

class CarteMadagascar:
    """Générateur de carte Madagascar avec les AP"""
    
    def __init__(self, data_path="."):
        self.data_path = Path(data_path)
        self.output_dir = self.data_path / "frontend/visualizations"
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
            
            # Trouver les coordonnées
            coord = None
            for _, c in self.coords.iterrows():
                key = str(c['Key']).upper().strip()
                if key in ap_name or ap_name in key:
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
                    'categorie': seg['Categorie'],
                    'efficacite_score': seg['Efficacite_Score']
                })
        
        return pd.DataFrame(data)
    
    def create_map(self):
        """Créer la carte principale de Madagascar"""
        print("\n🗺️  Génération de la carte Madagascar...")
        
        # Configuration de la figure
        fig, ax = plt.subplots(figsize=(16, 20))
        
        # Définir les couleurs par catégorie
        couleurs = {
            '🌟 EFFICACES (Investis + Protégés)': '#2ecc71',  # Vert
            '🌱 NATURELLEMENT PROTÉGÉES (Peu investis + Peu de feux)': '#a8e6cf',  # Vert clair
            '⚠️  SOUS PRESSION (Investis mais encore fragiles)': '#f39c12',  # Orange
            '🚨 CRITIQUES (Peu investis + Forte déforestation)': '#e74c3c'  # Rouge
        }
        
        # Dessiner les contours approximatifs de Madagascar
        # (rectangle simplifié pour visualisation)
        madagascar_lng = [43.2, 50.5]
        madagascar_lat = [-25.6, -12.0]
        
        # Fond de carte
        ax.set_xlim(madagascar_lng[0] - 0.5, madagascar_lng[1] + 0.5)
        ax.set_ylim(madagascar_lat[0] - 0.5, madagascar_lat[1] + 0.5)
        ax.set_facecolor('#e8f4f8')  # Bleu clair (océan)
        
        # Grille
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        
        # Normaliser les superficies pour la taille des points
        superficies_norm = self.data['superficie_ha'] / self.data['superficie_ha'].max()
        sizes = 100 + superficies_norm * 900  # Taille entre 100 et 1000
        
        # Tracer chaque catégorie
        for cat, couleur in couleurs.items():
            mask = self.data['categorie'] == cat
            if mask.any():
                subset = self.data[mask]
                
                ax.scatter(
                    subset['lng'],
                    subset['lat'],
                    s=sizes[mask],
                    c=couleur,
                    alpha=0.7,
                    edgecolors='black',
                    linewidth=1.5,
                    label=cat.split(' (')[0],  # Nom court pour légende
                    zorder=3
                )
        
        # Annotations pour les AP critiques et champions
        critiques = self.data[self.data['categorie'].str.contains('CRITIQUES')]
        champions = self.data[self.data['categorie'].str.contains('EFFICACES')]
        
        # Top 5 critiques
        top_critiques = critiques.nlargest(5, 'fire_rate')
        for _, ap in top_critiques.iterrows():
            ax.annotate(
                ap['name'],
                xy=(ap['lng'], ap['lat']),
                xytext=(10, 10),
                textcoords='offset points',
                fontsize=9,
                color='darkred',
                weight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffebee', alpha=0.8),
                arrowprops=dict(arrowstyle='->', color='darkred', lw=1.5)
            )
        
        # Top 3 champions
        top_champions = champions.nlargest(3, 'efficacite_score')
        for _, ap in top_champions.iterrows():
            ax.annotate(
                ap['name'],
                xy=(ap['lng'], ap['lat']),
                xytext=(-10, -10),
                textcoords='offset points',
                fontsize=9,
                color='darkgreen',
                weight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#e8f5e9', alpha=0.8),
                arrowprops=dict(arrowstyle='->', color='darkgreen', lw=1.5)
            )
        
        # Titres et labels
        ax.set_xlabel('Longitude', fontsize=14, fontweight='bold')
        ax.set_ylabel('Latitude', fontsize=14, fontweight='bold')
        ax.set_title(
            'CARTE DE MADAGASCAR : Aires Protégées Financées (56 AP)\n' +
            'Taille = Superficie | Couleur = Efficacité du Financement\n' +
            'Analyse par KOUMI Dzudzogbe Prince Armand',
            fontsize=16,
            fontweight='bold',
            pad=20
        )
        
        # Légende principale
        legend1 = ax.legend(
            loc='upper left',
            fontsize=11,
            framealpha=0.95,
            title='Catégories d\'AP',
            title_fontsize=12
        )
        legend1.get_title().set_fontweight('bold')
        
        # Légende des tailles (exemple)
        sizes_legend = [100, 300, 600, 1000]
        labels_legend = ['Petite', 'Moyenne', 'Grande', 'Très grande']
        
        legend_elements = [
            plt.scatter([], [], s=s, c='gray', alpha=0.5, edgecolors='black', linewidth=1)
            for s in sizes_legend
        ]
        
        legend2 = ax.legend(
            legend_elements,
            labels_legend,
            loc='lower left',
            fontsize=10,
            framealpha=0.95,
            title='Superficie',
            title_fontsize=11,
            scatterpoints=1
        )
        legend2.get_title().set_fontweight('bold')
        ax.add_artist(legend1)  # Réajouter la première légende
        
        # Calculer les statistiques complètes (toutes les AP, pas seulement celles avec coordonnées)
        total_aps = len(self.segmentation[self.segmentation['AP_Name'] != 'TOTAL'])
        total_financement = self.segmentation[self.segmentation['AP_Name'] != 'TOTAL']['Financement_annuel_USD'].sum()
        total_superficie = self.segmentation[self.segmentation['AP_Name'] != 'TOTAL']['Superficie_ha'].sum()
        
        # Ajouter texte d'information
        info_text = (
            f'📊 Données analysées :\n'
            f'   • {len(self.data)} AP avec coordonnées GPS\n'
            f'   • {total_aps} AP au total analysées\n'
            f'   • Financement total : {total_financement/1e9:.1f} Mds USD\n'
            f'   • Superficie totale : {total_superficie/1e6:.2f} M ha\n\n'
            f'🚨 TOP 5 CRITIQUES (rouge) :\n'
            f'   Zones nécessitant intervention urgente\n\n'
            f'🏆 TOP 3 CHAMPIONS (vert) :\n'
            f'   Modèles de réussite à répliquer'
        )
        
        ax.text(
            0.98, 0.5,
            info_text,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='center',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9),
            family='monospace'
        )
        
        # Marquer les villes principales (repères)
        villes = {
            'Antananarivo': (47.5, -18.9),
            'Toamasina': (49.4, -18.1),
            'Toliara': (43.7, -23.4),
            'Mahajanga': (46.3, -15.7),
            'Antsiranana': (49.3, -12.3)
        }
        
        for ville, (lng, lat) in villes.items():
            ax.plot(lng, lat, 'k*', markersize=15, zorder=5)
            ax.text(lng, lat - 0.3, ville, fontsize=9, ha='center', 
                   weight='bold', style='italic', color='#34495e')
        
        plt.tight_layout()
        
        # Sauvegarder
        output_file = self.output_dir / 'carte_madagascar_ap.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"✅ Carte sauvegardée : {output_file}")
        return output_file
    
    def create_map_zoom_nord(self):
        """Créer un zoom sur le nord (concentration d'AP)"""
        print("\n🔍 Génération du zoom Nord...")
        
        fig, ax = plt.subplots(figsize=(14, 12))
        
        # Filtrer les AP du nord
        nord = self.data[self.data['lat'] > -16]
        
        couleurs = {
            '🌟 EFFICACES (Investis + Protégés)': '#2ecc71',
            '🌱 NATURELLEMENT PROTÉGÉES (Peu investis + Peu de feux)': '#a8e6cf',
            '⚠️  SOUS PRESSION (Investis mais encore fragiles)': '#f39c12',
            '🚨 CRITIQUES (Peu investis + Forte déforestation)': '#e74c3c'
        }
        
        # Limites
        ax.set_xlim(nord['lng'].min() - 1, nord['lng'].max() + 1)
        ax.set_ylim(nord['lat'].min() - 0.5, nord['lat'].max() + 0.5)
        ax.set_facecolor('#e8f4f8')
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        
        # Normaliser superficies
        superficies_norm = nord['superficie_ha'] / nord['superficie_ha'].max()
        sizes = 150 + superficies_norm * 700
        
        # Tracer
        for cat, couleur in couleurs.items():
            mask = nord['categorie'] == cat
            if mask.any():
                subset = nord[mask]
                sizes_subset = 150 + (subset['superficie_ha'] / nord['superficie_ha'].max()) * 700
                
                ax.scatter(
                    subset['lng'],
                    subset['lat'],
                    s=sizes_subset,
                    c=couleur,
                    alpha=0.7,
                    edgecolors='black',
                    linewidth=1.5,
                    label=cat.split(' (')[0]
                )
        
        # Annoter toutes les AP du nord
        for _, ap in nord.iterrows():
            ax.annotate(
                ap['name'],
                xy=(ap['lng'], ap['lat']),
                fontsize=8,
                ha='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7, edgecolor='gray')
            )
        
        ax.set_xlabel('Longitude', fontsize=12, fontweight='bold')
        ax.set_ylabel('Latitude', fontsize=12, fontweight='bold')
        ax.set_title(
            f'ZOOM : Nord de Madagascar ({len(nord)} AP)\n' +
            'Zone à forte concentration d\'aires protégées',
            fontsize=14,
            fontweight='bold',
            pad=15
        )
        
        ax.legend(loc='best', fontsize=10, framealpha=0.95)
        
        plt.tight_layout()
        
        output_file = self.output_dir / 'carte_madagascar_zoom_nord.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"✅ Zoom Nord sauvegardé : {output_file}")
        return output_file
    
    def create_map_zoom_sud(self):
        """Créer un zoom sur le sud"""
        print("\n🔍 Génération du zoom Sud...")
        
        fig, ax = plt.subplots(figsize=(14, 12))
        
        # Filtrer les AP du sud
        sud = self.data[self.data['lat'] < -21]
        
        couleurs = {
            '🌟 EFFICACES (Investis + Protégés)': '#2ecc71',
            '🌱 NATURELLEMENT PROTÉGÉES (Peu investis + Peu de feux)': '#a8e6cf',
            '⚠️  SOUS PRESSION (Investis mais encore fragiles)': '#f39c12',
            '🚨 CRITIQUES (Peu investis + Forte déforestation)': '#e74c3c'
        }
        
        # Limites
        ax.set_xlim(sud['lng'].min() - 1, sud['lng'].max() + 1)
        ax.set_ylim(sud['lat'].min() - 0.5, sud['lat'].max() + 0.5)
        ax.set_facecolor('#e8f4f8')
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        
        # Normaliser superficies
        superficies_norm = sud['superficie_ha'] / sud['superficie_ha'].max()
        sizes = 150 + superficies_norm * 700
        
        # Tracer
        for cat, couleur in couleurs.items():
            mask = sud['categorie'] == cat
            if mask.any():
                subset = sud[mask]
                sizes_subset = 150 + (subset['superficie_ha'] / sud['superficie_ha'].max()) * 700
                
                ax.scatter(
                    subset['lng'],
                    subset['lat'],
                    s=sizes_subset,
                    c=couleur,
                    alpha=0.7,
                    edgecolors='black',
                    linewidth=1.5,
                    label=cat.split(' (')[0]
                )
        
        # Annoter toutes les AP du sud
        for _, ap in sud.iterrows():
            ax.annotate(
                ap['name'],
                xy=(ap['lng'], ap['lat']),
                fontsize=8,
                ha='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7, edgecolor='gray')
            )
        
        ax.set_xlabel('Longitude', fontsize=12, fontweight='bold')
        ax.set_ylabel('Latitude', fontsize=12, fontweight='bold')
        ax.set_title(
            f'ZOOM : Sud de Madagascar ({len(sud)} AP)\n' +
            'Zone à forte pression anthropique',
            fontsize=14,
            fontweight='bold',
            pad=15
        )
        
        ax.legend(loc='best', fontsize=10, framealpha=0.95)
        
        plt.tight_layout()
        
        output_file = self.output_dir / 'carte_madagascar_zoom_sud.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"✅ Zoom Sud sauvegardé : {output_file}")
        return output_file
    
    def generate_all_maps(self):
        """Générer toutes les cartes"""
        print("\n" + "="*70)
        print("🗺️  GÉNÉRATION DES CARTES MADAGASCAR")
        print("="*70 + "\n")
        
        self.load_data()
        
        # Carte principale
        carte_principale = self.create_map()
        
        # Zooms régionaux
        zoom_nord = self.create_map_zoom_nord()
        zoom_sud = self.create_map_zoom_sud()
        
        print("\n" + "="*70)
        print("✅ TOUTES LES CARTES GÉNÉRÉES AVEC SUCCÈS")
        print("="*70)
        print(f"\n📁 Fichiers créés :")
        print(f"   1. {carte_principale.name} (carte complète)")
        print(f"   2. {zoom_nord.name} (zoom nord)")
        print(f"   3. {zoom_sud.name} (zoom sud)")
        print(f"\n📍 {len(self.data)} AP positionnées avec succès sur {len(self.segmentation)} analysées")
        print(f"   ({len(self.data)/len(self.segmentation)*100:.1f}% de couverture GPS)")
        print("\n")


if __name__ == "__main__":
    generator = CarteMadagascar()
    generator.generate_all_maps()

