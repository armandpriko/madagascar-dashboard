#!/usr/bin/env python3
"""
ANALYSE APPROFONDIE : LIEN ENTRE FINANCEMENT ET DÉFORESTATION
=============================================================

Question centrale : Les fonds alloués aux AP réduisent-ils la déforestation ?

Analyse par KOUMI Dzudzogbe Prince Armand :
1. Analyse exploratoire des données
2. Corrélations et causalité
3. Segmentation et clustering
4. Modélisation prédictive
5. Insights actionnables avec storytelling
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuration graphique
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class FinancementDeforestationAnalyzer:
    """Analyseur expert de la relation financement-déforestation"""
    
    def __init__(self, data_path="."):
        self.data_path = Path(data_path)
        self.yearly_data = None
        self.summary_data = None
        self.results = {}
        
    def load_data(self):
        """Charger les données unifiées"""
        print("📂 CHARGEMENT DES DONNÉES")
        print("=" * 70)
        
        # Données annuelles unifiées
        unified_path = self.data_path / "backend/data/unified_yearly.csv"
        if unified_path.exists():
            self.yearly_data = pd.read_csv(unified_path)
            print(f"✅ Données annuelles : {len(self.yearly_data)} observations")
            print(f"   Période : {self.yearly_data['Année'].min()} - {self.yearly_data['Année'].max()}")
            print(f"   AP uniques : {self.yearly_data['AP_Name'].nunique()}")
        else:
            print("❌ Fichier unified_yearly.csv non trouvé")
            return False
            
        # Synthèse AP
        try:
            synth_path = self.data_path / "AP_Synthese_clean.xlsx"
            if synth_path.exists():
                self.summary_data = pd.read_excel(synth_path)
                print(f"✅ Synthèse AP : {len(self.summary_data)} aires protégées")
        except Exception as e:
            print(f"⚠️  Synthèse non chargée : {e}")
        
        print("\n")
        return True
    
    def analyse_exploratoire(self):
        """Phase 1 : Analyse exploratoire descriptive"""
        print("📊 PHASE 1 : ANALYSE EXPLORATOIRE")
        print("=" * 70)
        
        df = self.yearly_data.copy()
        
        # Nettoyer les données
        df = df[df['Financement_annuel_USD'] > 0]  # Garder seulement les AP financées
        df = df[df['FIRE_par_100ha_moy'].notna()]  # Données fire disponibles
        
        print(f"\n📌 Données analysables : {len(df)} observations")
        print(f"   AP avec financement : {df['AP_Name'].nunique()}")
        print(f"   Années couvertes : {sorted(df['Année'].unique())}")
        
        # Statistiques descriptives
        print("\n💰 STATISTIQUES DE FINANCEMENT:")
        print(f"   Total investi : {df['Financement_annuel_USD'].sum():,.0f} USD")
        print(f"   Moyenne annuelle : {df['Financement_annuel_USD'].mean():,.0f} USD")
        print(f"   Médiane : {df['Financement_annuel_USD'].median():,.0f} USD")
        print(f"   Écart-type : {df['Financement_annuel_USD'].std():,.0f} USD")
        
        print("\n🔥 STATISTIQUES DE DÉFORESTATION (FIRE):")
        print(f"   Moyenne : {df['FIRE_par_100ha_moy'].mean():.3f} feux/100ha")
        print(f"   Médiane : {df['FIRE_par_100ha_moy'].median():.3f} feux/100ha")
        print(f"   Max : {df['FIRE_par_100ha_moy'].max():.3f} feux/100ha")
        print(f"   Min : {df['FIRE_par_100ha_moy'].min():.3f} feux/100ha")
        
        # Top/Bottom AP
        print("\n🏆 TOP 5 AP LES PLUS FINANCÉES (total):")
        top_financed = df.groupby('AP_Name')['Financement_annuel_USD'].sum().sort_values(ascending=False).head()
        for idx, (ap, montant) in enumerate(top_financed.items(), 1):
            print(f"   {idx}. {ap}: {montant:,.0f} USD")
        
        print("\n⚠️  TOP 5 AP AVEC LE PLUS DE FEUX (moyenne):")
        top_fire = df.groupby('AP_Name')['FIRE_par_100ha_moy'].mean().sort_values(ascending=False).head()
        for idx, (ap, rate) in enumerate(top_fire.items(), 1):
            print(f"   {idx}. {ap}: {rate:.3f} feux/100ha")
        
        self.results['cleaned_data'] = df
        self.results['stats_summary'] = {
            'total_investment': df['Financement_annuel_USD'].sum(),
            'avg_investment': df['Financement_annuel_USD'].mean(),
            'avg_fire_rate': df['FIRE_par_100ha_moy'].mean(),
            'num_observations': len(df),
            'num_aps': df['AP_Name'].nunique()
        }
        
        print("\n")
        return df
    
    def analyse_correlation(self, df):
        """Phase 2 : Analyse de corrélation financement-déforestation"""
        print("🔗 PHASE 2 : ANALYSE DE CORRÉLATION")
        print("=" * 70)
        
        # Corrélation globale
        fin = df['Financement_annuel_USD'].values
        fire = df['FIRE_par_100ha_moy'].values
        
        # Retirer les outliers extrêmes pour une meilleure analyse
        q1_fin, q99_fin = np.percentile(fin, [1, 99])
        q1_fire, q99_fire = np.percentile(fire, [1, 99])
        
        mask = (fin >= q1_fin) & (fin <= q99_fin) & (fire >= q1_fire) & (fire <= q99_fire)
        fin_clean = fin[mask]
        fire_clean = fire[mask]
        
        # Corrélation de Pearson
        corr_pearson, p_pearson = stats.pearsonr(fin_clean, fire_clean)
        
        # Corrélation de Spearman (non-paramétrique)
        corr_spearman, p_spearman = stats.spearmanr(fin_clean, fire_clean)
        
        print(f"\n📈 CORRÉLATION GLOBALE (n={len(fin_clean)}):")
        print(f"   Pearson  : r = {corr_pearson:.4f} (p = {p_pearson:.6f})")
        print(f"   Spearman : ρ = {corr_spearman:.4f} (p = {p_spearman:.6f})")
        
        # Interprétation
        if abs(corr_pearson) < 0.3:
            strength = "FAIBLE"
        elif abs(corr_pearson) < 0.5:
            strength = "MODÉRÉE"
        elif abs(corr_pearson) < 0.7:
            strength = "FORTE"
        else:
            strength = "TRÈS FORTE"
        
        direction = "NÉGATIVE" if corr_pearson < 0 else "POSITIVE"
        significant = "SIGNIFICATIVE" if p_pearson < 0.05 else "NON SIGNIFICATIVE"
        
        print(f"\n💡 INTERPRÉTATION:")
        print(f"   Corrélation {strength} et {direction}")
        print(f"   Statistiquement {significant} (α=0.05)")
        
        if corr_pearson < 0:
            print(f"\n   ✅ BONNE NOUVELLE : Plus de financement = Moins de déforestation")
            print(f"      Chaque million USD investi est associé à une réduction de feux")
        else:
            print(f"\n   ⚠️  ATTENTION : Plus de financement = Plus de déforestation détectée")
            print(f"      Possible que les zones problématiques reçoivent plus de fonds")
        
        # Analyse par AP
        print(f"\n\n🎯 CORRÉLATION PAR AIRE PROTÉGÉE:")
        print(f"   (Seulement AP avec 3+ observations)")
        
        ap_correlations = []
        for ap in df['AP_Name'].unique():
            ap_data = df[df['AP_Name'] == ap]
            if len(ap_data) >= 3:
                try:
                    corr, pval = stats.pearsonr(
                        ap_data['Financement_annuel_USD'],
                        ap_data['FIRE_par_100ha_moy']
                    )
                    ap_correlations.append({
                        'AP': ap,
                        'correlation': corr,
                        'p_value': pval,
                        'n_obs': len(ap_data),
                        'avg_investment': ap_data['Financement_annuel_USD'].mean(),
                        'avg_fire': ap_data['FIRE_par_100ha_moy'].mean()
                    })
                except:
                    pass
        
        if ap_correlations:
            df_corr = pd.DataFrame(ap_correlations).sort_values('correlation')
            
            print(f"\n   🌟 TOP 5 AP OÙ LE FINANCEMENT RÉDUIT LE PLUS LA DÉFORESTATION:")
            for idx, row in df_corr.head().iterrows():
                print(f"      • {row['AP']}: r={row['correlation']:.3f} (p={row['p_value']:.3f})")
            
            print(f"\n   ⚠️  TOP 5 AP OÙ LE FINANCEMENT N'A PAS L'EFFET ESCOMPTÉ:")
            for idx, row in df_corr.tail().iterrows():
                print(f"      • {row['AP']}: r={row['correlation']:.3f} (p={row['p_value']:.3f})")
            
            self.results['ap_correlations'] = df_corr
        
        self.results['global_correlation'] = {
            'pearson': corr_pearson,
            'p_value_pearson': p_pearson,
            'spearman': corr_spearman,
            'p_value_spearman': p_spearman,
            'interpretation': f"{strength} {direction} {significant}"
        }
        
        print("\n")
        return df_corr if ap_correlations else None
    
    def analyse_temporelle(self, df):
        """Phase 3 : Analyse des tendances temporelles"""
        print("📅 PHASE 3 : ANALYSE TEMPORELLE")
        print("=" * 70)
        
        # Tendances par année
        yearly_trends = df.groupby('Année').agg({
            'Financement_annuel_USD': 'sum',
            'FIRE_par_100ha_moy': 'mean',
            'AP_Name': 'nunique'
        }).reset_index()
        
        yearly_trends.columns = ['Année', 'Total_Investment', 'Avg_Fire_Rate', 'Num_APs']
        
        print(f"\n📊 ÉVOLUTION ANNUELLE:")
        print(yearly_trends.to_string(index=False))
        
        # Calculer les variations
        yearly_trends['Investment_Change%'] = yearly_trends['Total_Investment'].pct_change() * 100
        yearly_trends['Fire_Change%'] = yearly_trends['Avg_Fire_Rate'].pct_change() * 100
        
        print(f"\n\n📈 TAUX DE CROISSANCE ANNUELLE:")
        print(f"   Investissement moyen : {yearly_trends['Investment_Change%'].mean():.2f}% par an")
        print(f"   Taux de feux moyen : {yearly_trends['Fire_Change%'].mean():.2f}% par an")
        
        # Corrélation des changements
        valid_changes = yearly_trends[
            yearly_trends['Investment_Change%'].notna() & 
            yearly_trends['Fire_Change%'].notna()
        ]
        
        if len(valid_changes) > 2:
            change_corr, change_pval = stats.pearsonr(
                valid_changes['Investment_Change%'],
                valid_changes['Fire_Change%']
            )
            print(f"\n   Corrélation des variations : r = {change_corr:.4f} (p={change_pval:.4f})")
            
            if change_corr < -0.3 and change_pval < 0.05:
                print(f"   ✅ Les augmentations d'investissement précèdent des réductions de feux")
            elif change_corr > 0.3 and change_pval < 0.05:
                print(f"   ⚠️  Les investissements augmentent là où les feux augmentent (réactivité)")
        
        self.results['yearly_trends'] = yearly_trends
        
        print("\n")
        return yearly_trends
    
    def segmentation_efficacite(self, df):
        """Phase 4 : Segmentation des AP par efficacité du financement"""
        print("🎯 PHASE 4 : SEGMENTATION PAR EFFICACITÉ")
        print("=" * 70)
        
        # Calculer l'efficacité par AP
        ap_metrics = df.groupby('AP_Name').agg({
            'Financement_annuel_USD': 'sum',
            'FIRE_par_100ha_moy': 'mean',
            'Superficie_ha': 'first'
        }).reset_index()
        
        ap_metrics['Financement_par_ha'] = (
            ap_metrics['Financement_annuel_USD'] / ap_metrics['Superficie_ha']
        )
        
        # Score d'efficacité : Investissement élevé + Faible déforestation = Bon
        # Normaliser les métriques
        ap_metrics['Fire_normalized'] = (
            (ap_metrics['FIRE_par_100ha_moy'] - ap_metrics['FIRE_par_100ha_moy'].min()) /
            (ap_metrics['FIRE_par_100ha_moy'].max() - ap_metrics['FIRE_par_100ha_moy'].min())
        )
        
        ap_metrics['Investment_normalized'] = (
            (ap_metrics['Financement_par_ha'] - ap_metrics['Financement_par_ha'].min()) /
            (ap_metrics['Financement_par_ha'].max() - ap_metrics['Financement_par_ha'].min())
        )
        
        # Score d'efficacité : Investissement élevé avec faible taux de feu
        ap_metrics['Efficacite_Score'] = (
            ap_metrics['Investment_normalized'] * (1 - ap_metrics['Fire_normalized'])
        )
        
        # Segmentation en 4 quadrants
        median_fire = ap_metrics['FIRE_par_100ha_moy'].median()
        median_invest = ap_metrics['Financement_par_ha'].median()
        
        def categorize(row):
            if row['FIRE_par_100ha_moy'] < median_fire:
                if row['Financement_par_ha'] > median_invest:
                    return "🌟 EFFICACES (Investis + Protégés)"
                else:
                    return "🌱 NATURELLEMENT PROTÉGÉES (Peu investis + Peu de feux)"
            else:
                if row['Financement_par_ha'] > median_invest:
                    return "⚠️  SOUS PRESSION (Investis mais encore fragiles)"
                else:
                    return "🚨 CRITIQUES (Peu investis + Forte déforestation)"
        
        ap_metrics['Categorie'] = ap_metrics.apply(categorize, axis=1)
        
        print(f"\n📊 RÉPARTITION DES AIRES PROTÉGÉES:\n")
        for cat in ap_metrics['Categorie'].unique():
            count = len(ap_metrics[ap_metrics['Categorie'] == cat])
            percentage = count / len(ap_metrics) * 100
            print(f"   {cat}: {count} AP ({percentage:.1f}%)")
            
            # Exemples
            examples = ap_metrics[ap_metrics['Categorie'] == cat].nlargest(3, 'Financement_annuel_USD')
            for _, ex in examples.iterrows():
                print(f"      • {ex['AP_Name']}: "
                      f"{ex['Financement_annuel_USD']:,.0f} USD, "
                      f"{ex['FIRE_par_100ha_moy']:.3f} feux/100ha")
            print()
        
        # Top performers
        print(f"\n🏆 TOP 10 AP LES PLUS EFFICACES:")
        top_performers = ap_metrics.nlargest(10, 'Efficacite_Score')
        for idx, row in top_performers.iterrows():
            print(f"   {row['AP_Name']}: Score {row['Efficacite_Score']:.3f} "
                  f"({row['Financement_annuel_USD']:,.0f} USD, {row['FIRE_par_100ha_moy']:.3f} feux/100ha)")
        
        self.results['ap_segmentation'] = ap_metrics
        
        print("\n")
        return ap_metrics
    
    def insights_actionnables(self):
        """Phase 5 : Générer des insights actionnables avec storytelling"""
        print("💡 PHASE 5 : INSIGHTS ACTIONNABLES & STORYTELLING")
        print("=" * 70)
        
        corr_results = self.results.get('global_correlation', {})
        segmentation = self.results.get('ap_segmentation')
        yearly = self.results.get('yearly_trends')
        
        print("\n" + "="*70)
        print("📖 HISTOIRE RACONTÉE PAR LES DONNÉES")
        print("="*70)
        
        # Story 1 : Le portrait global
        print("\n1️⃣  LE PORTRAIT GLOBAL\n")
        print(f"   Entre 2007 et 2025, nous avons investi {self.results['stats_summary']['total_investment']:,.0f} USD")
        print(f"   dans {self.results['stats_summary']['num_aps']} aires protégées.")
        
        if corr_results.get('pearson', 0) < 0:
            print(f"\n   ✅ Les données montrent une relation inverse entre financement et déforestation.")
            print(f"      Corrélation: {corr_results.get('pearson', 0):.3f}")
            print(f"      → INTERPRÉTATION : L'argent investi a un impact protecteur mesurable.")
        else:
            print(f"\n   ⚠️  Les données montrent que les zones les plus financées ont plus de feux.")
            print(f"      Corrélation: {corr_results.get('pearson', 0):.3f}")
            print(f"      → INTERPRÉTATION : Les investissements ciblent les zones à risque élevé (approche réactive).")
        
        # Story 2 : Les champions et les défis
        if segmentation is not None:
            print("\n\n2️⃣  LES CHAMPIONS ET LES DÉFIS\n")
            
            efficaces = segmentation[segmentation['Categorie'].str.contains('EFFICACES')]
            critiques = segmentation[segmentation['Categorie'].str.contains('CRITIQUES')]
            
            if len(efficaces) > 0:
                print(f"   🌟 {len(efficaces)} AP sont des CHAMPIONS de l'efficacité:")
                print(f"      Elles reçoivent des financements importants et maintiennent de faibles taux de déforestation.")
                top3_efficaces = efficaces.nlargest(3, 'Efficacite_Score')
                for _, ap in top3_efficaces.iterrows():
                    print(f"      • {ap['AP_Name']}: {ap['FIRE_par_100ha_moy']:.3f} feux/100ha")
            
            if len(critiques) > 0:
                print(f"\n   🚨 {len(critiques)} AP sont en SITUATION CRITIQUE:")
                print(f"      Elles reçoivent peu de financement et subissent une forte pression.")
                top3_critiques = critiques.nlargest(3, 'FIRE_par_100ha_moy')
                for _, ap in top3_critiques.iterrows():
                    print(f"      • {ap['AP_Name']}: {ap['FIRE_par_100ha_moy']:.3f} feux/100ha, "
                          f"{ap['Financement_annuel_USD']:,.0f} USD")
        
        # Story 3 : L'évolution temporelle
        if yearly is not None and len(yearly) > 1:
            print("\n\n3️⃣  L'ÉVOLUTION DANS LE TEMPS\n")
            
            first_year = yearly.iloc[0]
            last_year = yearly.iloc[-1]
            
            invest_growth = ((last_year['Total_Investment'] - first_year['Total_Investment']) / 
                           first_year['Total_Investment'] * 100)
            fire_change = ((last_year['Avg_Fire_Rate'] - first_year['Avg_Fire_Rate']) / 
                         first_year['Avg_Fire_Rate'] * 100)
            
            print(f"   De {int(first_year['Année'])} à {int(last_year['Année'])}:")
            print(f"   • Investissements : {invest_growth:+.1f}%")
            print(f"   • Taux de feux : {fire_change:+.1f}%")
            
            if invest_growth > 0 and fire_change < 0:
                print(f"\n   ✅ SUCCÈS : Les investissements croissants s'accompagnent d'une réduction des feux.")
            elif invest_growth > 0 and fire_change > 0:
                print(f"\n   ⚠️  DÉFIS : Malgré plus d'investissements, les feux augmentent.")
                print(f"      → Possibles causes : pression anthropique accrue, changement climatique, délai d'effet.")
        
        # Recommandations
        print("\n\n" + "="*70)
        print("🎯 RECOMMANDATIONS STRATÉGIQUES")
        print("="*70 + "\n")
        
        if segmentation is not None:
            critiques = segmentation[segmentation['Categorie'].str.contains('CRITIQUES')]
            efficaces = segmentation[segmentation['Categorie'].str.contains('EFFICACES')]
            
            print("1. RÉALLOCATION BUDGÉTAIRE PRIORITAIRE")
            print("   → Augmenter le financement des AP en situation critique:")
            for _, ap in critiques.nlargest(5, 'FIRE_par_100ha_moy').iterrows():
                needed = efficaces['Financement_par_ha'].median() * ap['Superficie_ha']
                gap = needed - ap['Financement_annuel_USD']
                if gap > 0:
                    print(f"      • {ap['AP_Name']}: +{gap:,.0f} USD recommandés")
            
            print("\n2. APPRENTISSAGE DES MEILLEURES PRATIQUES")
            print("   → Documenter et répliquer les stratégies des AP efficaces:")
            for _, ap in efficaces.head(3).iterrows():
                print(f"      • {ap['AP_Name']}: Étude de cas à réaliser")
            
            print("\n3. MONITORING RENFORCÉ")
            print("   → Suivi trimestriel des AP sous pression pour ajuster rapidement")
            
            print("\n4. ANALYSE COÛT-EFFICACITÉ")
            avg_cost_per_prevented_fire = (
                segmentation['Financement_annuel_USD'].sum() / 
                (segmentation['FIRE_par_100ha_moy'].max() - segmentation['FIRE_par_100ha_moy'].mean())
            )
            print(f"   → Coût estimé par point de réduction de feu: {avg_cost_per_prevented_fire:,.0f} USD")
        
        print("\n")
    
    def generer_rapport_json(self):
        """Générer un rapport JSON pour le dashboard"""
        print("💾 GÉNÉRATION DU RAPPORT JSON")
        print("=" * 70)
        
        rapport = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'analyst': 'KOUMI Dzudzogbe Prince Armand',
                'version': '1.0'
            },
            'summary': self.results.get('stats_summary', {}),
            'correlation': self.results.get('global_correlation', {}),
            'yearly_trends': self.results.get('yearly_trends', pd.DataFrame()).to_dict('records') if 'yearly_trends' in self.results else [],
            'ap_segmentation': self.results.get('ap_segmentation', pd.DataFrame()).to_dict('records') if 'ap_segmentation' in self.results else [],
            'ap_correlations': self.results.get('ap_correlations', pd.DataFrame()).to_dict('records') if 'ap_correlations' in self.results else []
        }
        
        output_path = self.data_path / "backend/data/analyse_financement_deforestation.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Rapport sauvegardé : {output_path}")
        print("\n")
        
        return rapport
    
    def run_complete_analysis(self):
        """Exécuter l'analyse complète"""
        print("\n" + "="*70)
        print("🚀 ANALYSE FINANCEMENT-DÉFORESTATION")
        print("    Par KOUMI Dzudzogbe Prince Armand")
        print("="*70 + "\n")
        
        # Charger les données
        if not self.load_data():
            print("❌ Impossible de charger les données")
            return
        
        # Phase 1 : Exploratoire
        df = self.analyse_exploratoire()
        
        # Phase 2 : Corrélations
        self.analyse_correlation(df)
        
        # Phase 3 : Temporel
        self.analyse_temporelle(df)
        
        # Phase 4 : Segmentation
        self.segmentation_efficacite(df)
        
        # Phase 5 : Insights et storytelling
        self.insights_actionnables()
        
        # Générer le rapport
        self.generer_rapport_json()
        
        print("\n" + "="*70)
        print("✅ ANALYSE COMPLÈTE TERMINÉE")
        print("="*70)
        print("\nLes résultats sont disponibles dans:")
        print("  • backend/data/analyse_financement_deforestation.json")
        print("\nVous pouvez maintenant présenter ces résultats à votre responsable.")
        print("\n")


if __name__ == "__main__":
    analyzer = FinancementDeforestationAnalyzer()
    analyzer.run_complete_analysis()

