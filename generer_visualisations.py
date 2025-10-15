#!/usr/bin/env python3
"""
Génération de visualisations professionnelles pour l'analyse financement-déforestation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
import warnings
warnings.filterwarnings('ignore')

# Style professionnel
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("deep")
sns.set_context("notebook", font_scale=1.2)

class VisualizationGenerator:
    def __init__(self, data_path="."):
        self.data_path = Path(data_path)
        self.output_dir = self.data_path / "frontend/visualizations"
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
    def load_data(self):
        """Charger les données d'analyse"""
        # Données annuelles
        yearly_path = self.data_path / "backend/data/unified_yearly.csv"
        self.yearly_data = pd.read_csv(yearly_path)
        
        # Rapport d'analyse
        rapport_path = self.data_path / "backend/data/analyse_financement_deforestation.json"
        with open(rapport_path, 'r') as f:
            self.rapport = json.load(f)
        
        print("✅ Données chargées")
    
    def viz1_correlation_scatter(self):
        """Graphique 1: Scatter plot Financement vs Déforestation"""
        print("📊 Génération: Corrélation Financement-Déforestation...")
        
        df = self.yearly_data.copy()
        df = df[(df['Financement_annuel_USD'] > 0) & (df['FIRE_par_100ha_moy'].notna())]
        
        # Nettoyer les outliers extrêmes
        q99_fin = df['Financement_annuel_USD'].quantile(0.99)
        q99_fire = df['FIRE_par_100ha_moy'].quantile(0.99)
        df_plot = df[(df['Financement_annuel_USD'] <= q99_fin) & 
                     (df['FIRE_par_100ha_moy'] <= q99_fire)]
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Scatter plot avec gradient de couleur par année
        scatter = ax.scatter(
            df_plot['Financement_annuel_USD'] / 1e6,  # Convertir en millions
            df_plot['FIRE_par_100ha_moy'],
            c=df_plot['Année'],
            cmap='viridis',
            s=100,
            alpha=0.6,
            edgecolors='black',
            linewidth=0.5
        )
        
        # Ligne de tendance
        z = np.polyfit(df_plot['Financement_annuel_USD'], 
                      df_plot['FIRE_par_100ha_moy'], 1)
        p = np.poly1d(z)
        x_line = np.linspace(df_plot['Financement_annuel_USD'].min(), 
                           df_plot['Financement_annuel_USD'].max(), 100)
        ax.plot(x_line / 1e6, p(x_line), "r--", linewidth=2, 
               label=f'Tendance (r={self.rapport["correlation"]["pearson"]:.3f})')
        
        # Colorbar
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Année', rotation=270, labelpad=20)
        
        # Labels et titre
        ax.set_xlabel('Financement Annuel (Millions MGA)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Taux d\'Incendies (par 100ha)', fontsize=14, fontweight='bold')
        ax.set_title('Impact du Financement sur la Déforestation\nCorrection Négative = L\'argent protège les forêts',
                    fontsize=16, fontweight='bold', pad=20)
        
        # Statistiques
        corr_text = f"Corrélation de Pearson: r = {self.rapport['correlation']['pearson']:.4f}\n"
        corr_text += f"p-value = {self.rapport['correlation']['p_value_pearson']:.6f}\n"
        corr_text += f"Statistiquement significatif (p < 0.05)" if self.rapport['correlation']['p_value_pearson'] < 0.05 else "Non significatif"
        
        ax.text(0.05, 0.95, corr_text, transform=ax.transAxes,
               fontsize=11, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        ax.legend(loc='upper right', fontsize=11)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'correlation_financement_deforestation.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        print("   ✅ correlation_financement_deforestation.png")
    
    def viz2_temporal_evolution(self):
        """Graphique 2: Évolution temporelle double axe"""
        print("📊 Génération: Évolution Temporelle...")
        
        yearly = pd.DataFrame(self.rapport['yearly_trends'])
        
        fig, ax1 = plt.subplots(figsize=(14, 8))
        
        # Axe 1: Investissement
        color = 'tab:blue'
        ax1.set_xlabel('Année', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Investissement Total (Milliards USD)', 
                      color=color, fontsize=14, fontweight='bold')
        line1 = ax1.plot(yearly['Année'], yearly['Total_Investment'] / 1e9,
                color=color, linewidth=3, marker='o', markersize=8,
                label='Investissement Total')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.fill_between(yearly['Année'], yearly['Total_Investment'] / 1e9,
                        alpha=0.3, color=color)
        
        # Axe 2: Taux de feux
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Taux Moyen de Feux (par 100ha)', 
                      color=color, fontsize=14, fontweight='bold')
        line2 = ax2.plot(yearly['Année'], yearly['Avg_Fire_Rate'],
                color=color, linewidth=3, marker='s', markersize=8,
                label='Taux de Feux')
        ax2.tick_params(axis='y', labelcolor=color)
        
        # Titre
        ax1.set_title('Évolution du Financement et de la Déforestation (2007-2023)\n' +
                     'Investissements ↑ mais Pression anthropique ↑ aussi',
                     fontsize=16, fontweight='bold', pad=20)
        
        # Légende combinée
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper left', fontsize=12)
        
        # Grille
        ax1.grid(True, alpha=0.3)
        
        # Annotations clés
        # Point max investment
        max_idx = yearly['Total_Investment'].idxmax()
        ax1.annotate(f'Max: {yearly.loc[max_idx, "Total_Investment"]/1e9:.1f}B USD',
                    xy=(yearly.loc[max_idx, 'Année'], yearly.loc[max_idx, 'Total_Investment']/1e9),
                    xytext=(10, 20), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'evolution_temporelle.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        print("   ✅ evolution_temporelle.png")
    
    def viz3_segmentation_quadrant(self):
        """Graphique 3: Matrice de segmentation des AP"""
        print("📊 Génération: Segmentation des AP...")
        
        segmentation = pd.DataFrame(self.rapport['ap_segmentation'])
        
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Couleurs par catégorie
        colors = {
            '🌟 EFFICACES (Investis + Protégés)': 'green',
            '🌱 NATURELLEMENT PROTÉGÉES (Peu investis + Peu de feux)': 'lightgreen',
            '⚠️  SOUS PRESSION (Investis mais encore fragiles)': 'orange',
            '🚨 CRITIQUES (Peu investis + Forte déforestation)': 'red'
        }
        
        for cat, color in colors.items():
            mask = segmentation['Categorie'] == cat
            if mask.any():
                subset = segmentation[mask]
                ax.scatter(subset['Financement_par_ha'],
                          subset['FIRE_par_100ha_moy'],
                          c=color, s=200, alpha=0.6,
                          edgecolors='black', linewidth=1,
                          label=cat)
        
        # Lignes médianes
        median_fin = segmentation['Financement_par_ha'].median()
        median_fire = segmentation['FIRE_par_100ha_moy'].median()
        
        ax.axvline(median_fin, color='gray', linestyle='--', linewidth=2, alpha=0.5)
        ax.axhline(median_fire, color='gray', linestyle='--', linewidth=2, alpha=0.5)
        
        # Labels
        ax.set_xlabel('Financement par Hectare (USD/ha)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Taux de Feux (par 100ha)', fontsize=14, fontweight='bold')
        ax.set_title('Matrice de Segmentation des Aires Protégées\n' +
                    'Efficacité du Financement par AP',
                    fontsize=16, fontweight='bold', pad=20)
        
        # Annotations des quadrants
        ax.text(0.75, 0.95, '⚠️  SOUS PRESSION\nForte pression\nmalgré financement',
               transform=ax.transAxes, fontsize=10, va='top', ha='center',
               bbox=dict(boxstyle='round', facecolor='orange', alpha=0.3))
        
        ax.text(0.25, 0.95, '🚨 CRITIQUES\nPrioritaires pour\nfinancement',
               transform=ax.transAxes, fontsize=10, va='top', ha='center',
               bbox=dict(boxstyle='round', facecolor='red', alpha=0.3))
        
        ax.text(0.75, 0.05, '🌟 EFFICACES\nModèles de\nréussite',
               transform=ax.transAxes, fontsize=10, va='bottom', ha='center',
               bbox=dict(boxstyle='round', facecolor='green', alpha=0.3))
        
        ax.text(0.25, 0.05, '🌱 NATURELLEMENT\nPROTÉGÉES\nMaintenir vigilance',
               transform=ax.transAxes, fontsize=10, va='bottom', ha='center',
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
        
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'segmentation_ap.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        print("   ✅ segmentation_ap.png")
    
    def viz4_top_performers(self):
        """Graphique 4: Top et Bottom performers"""
        print("📊 Génération: Top/Bottom Performers...")
        
        segmentation = pd.DataFrame(self.rapport['ap_segmentation'])
        
        # Top 10 efficaces et bottom 10
        top10 = segmentation.nlargest(10, 'Efficacite_Score')[['AP_Name', 'Efficacite_Score']]
        bottom10 = segmentation.nsmallest(10, 'Efficacite_Score')[['AP_Name', 'Efficacite_Score']]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
        
        # Top 10
        bars1 = ax1.barh(range(len(top10)), top10['Efficacite_Score'], color='green', alpha=0.7)
        ax1.set_yticks(range(len(top10)))
        ax1.set_yticklabels(top10['AP_Name'], fontsize=10)
        ax1.set_xlabel('Score d\'Efficacité', fontsize=12, fontweight='bold')
        ax1.set_title('🏆 TOP 10 AP LES PLUS EFFICACES\n(Bonnes pratiques à répliquer)',
                     fontsize=14, fontweight='bold', pad=15)
        ax1.grid(axis='x', alpha=0.3)
        
        # Valeurs
        for i, bar in enumerate(bars1):
            width = bar.get_width()
            ax1.text(width, bar.get_y() + bar.get_height()/2,
                    f'{width:.3f}', ha='left', va='center', fontsize=9)
        
        # Bottom 10
        bars2 = ax2.barh(range(len(bottom10)), bottom10['Efficacite_Score'], color='red', alpha=0.7)
        ax2.set_yticks(range(len(bottom10)))
        ax2.set_yticklabels(bottom10['AP_Name'], fontsize=10)
        ax2.set_xlabel('Score d\'Efficacité', fontsize=12, fontweight='bold')
        ax2.set_title('🚨 BOTTOM 10 AP À PRIORISER\n(Nécessitent attention urgente)',
                     fontsize=14, fontweight='bold', pad=15)
        ax2.grid(axis='x', alpha=0.3)
        
        # Valeurs
        for i, bar in enumerate(bars2):
            width = bar.get_width()
            ax2.text(width, bar.get_y() + bar.get_height()/2,
                    f'{width:.3f}', ha='right', va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'top_bottom_performers.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        print("   ✅ top_bottom_performers.png")
    
    def viz5_correlation_by_ap(self):
        """Graphique 5: Corrélations individuelles par AP"""
        print("📊 Génération: Corrélations par AP...")
        
        ap_corr = pd.DataFrame(self.rapport['ap_correlations'])
        if len(ap_corr) == 0:
            print("   ⚠️  Pas de données de corrélation par AP")
            return
        
        # Top 15 et bottom 15
        top15 = ap_corr.nsmallest(15, 'correlation')  # Plus négative = meilleure
        bottom15 = ap_corr.nlargest(15, 'correlation')
        
        combined = pd.concat([top15, bottom15]).sort_values('correlation')
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Couleurs selon le signe
        colors = ['green' if x < -0.3 else 'orange' if x < 0 else 'red' 
                 for x in combined['correlation']]
        
        bars = ax.barh(range(len(combined)), combined['correlation'], color=colors, alpha=0.7)
        ax.set_yticks(range(len(combined)))
        ax.set_yticklabels(combined['AP'], fontsize=9)
        ax.set_xlabel('Corrélation Financement-Déforestation', fontsize=12, fontweight='bold')
        ax.set_title('Corrélation Financement-Feux par Aire Protégée\n' +
                    'Négatif = Financement efficace | Positif = Zones réactives',
                    fontsize=14, fontweight='bold', pad=15)
        
        # Ligne zéro
        ax.axvline(0, color='black', linestyle='-', linewidth=1)
        
        # Zone verte/rouge
        ax.axvspan(-1, -0.3, alpha=0.1, color='green', label='Forte efficacité')
        ax.axvspan(0.3, 1, alpha=0.1, color='red', label='Réactivité (problématique)')
        
        ax.legend(loc='lower right', fontsize=10)
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'correlation_par_ap.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        print("   ✅ correlation_par_ap.png")
    
    def generate_all(self):
        """Générer toutes les visualisations"""
        print("\n🎨 GÉNÉRATION DES VISUALISATIONS PROFESSIONNELLES")
        print("=" * 70)
        
        self.load_data()
        
        self.viz1_correlation_scatter()
        self.viz2_temporal_evolution()
        self.viz3_segmentation_quadrant()
        self.viz4_top_performers()
        self.viz5_correlation_by_ap()
        
        print("\n" + "=" * 70)
        print("✅ TOUTES LES VISUALISATIONS GÉNÉRÉES")
        print(f"📁 Dossier: {self.output_dir}")
        print("=" * 70 + "\n")


if __name__ == "__main__":
    generator = VisualizationGenerator()
    generator.generate_all()

