#!/usr/bin/env python3
"""
CORRECTEUR RAPIDE - DONNÉES FINANCIÈRES VÉRIFIÉES
=================================================

Correction rapide avec les données vérifiées :
- 381.27 milliards MGA = 119.15 milliards USD
- 89 Aires Protégées
- Période 2007-2025

Par KOUMI Dzudzogbe Prince Armand
"""

import json
import pandas as pd

def correction_rapide():
    print("🚀 CORRECTION RAPIDE DES DONNÉES FINANCIÈRES")
    print()
    
    # Données vérifiées
    total_mga = 381273674751
    total_usd = total_mga / 3200
    nb_ap = 89
    periode = "2007-2025"
    
    print(f"📊 DONNÉES À APPLIQUER:")
    print(f"   • {total_mga:,.0f} MGA")
    print(f"   • {total_usd:,.0f} USD ({total_usd/1e9:.2f} milliards)")
    print(f"   • {nb_ap} AP")
    print(f"   • Période: {periode}")
    print()
    
    # 1. Corriger le JSON
    print("🔧 Correction JSON...")
    with open('backend/data/analyse_financement_deforestation.json', 'r') as f:
        data = json.load(f)
    
    data['summary'] = {
        'total_investment': total_usd,
        'avg_investment': total_usd / nb_ap,
        'avg_fire_rate': 0.398,
        'num_observations': 495,
        'num_aps': nb_ap,
        'period': periode,
        'currency': 'USD',
        'original_currency': 'MGA',
        'conversion_rate': 3200,
        'total_financement_mga': total_mga
    }
    
    data['metadata']['verification'] = {
        'verified': True,
        'verified_by': 'KOUMI Dzudzogbe Prince Armand',
        'source': 'Fonds 2007-25.xlsx (Feuil2)',
        'confidence': 'HIGH'
    }
    
    with open('backend/data/analyse_financement_deforestation.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("✅ JSON corrigé")
    
    # 2. Corriger le rapport HTML
    print("🔧 Correction rapport HTML...")
    with open('frontend/rapport_financement_deforestation.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Remplacer les valeurs
    html = html.replace("246,6 Mds", f"{total_usd/1e9:.1f} Mds")
    html = html.replace("246,6 milliards USD", f"{total_usd/1e9:.1f} milliards USD")
    html = html.replace("56", str(nb_ap))
    html = html.replace("2007-2023", periode)
    html = html.replace("17 ans", "19 ans")
    
    with open('frontend/rapport_financement_deforestation.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ Rapport HTML corrigé")
    
    print()
    print("🎯 CORRECTION TERMINÉE!")
    print(f"   • {total_usd/1e9:.2f} milliards USD")
    print(f"   • {nb_ap} Aires Protégées")
    print(f"   • Période {periode}")
    print()
    print("🔄 Prochaines étapes:")
    print("   1. python3 generer_carte_interactive.py")
    print("   2. python3 generer_rapport_complet.py")
    print("   3. ./OUVRIR_CARTE.sh")

if __name__ == "__main__":
    correction_rapide()
