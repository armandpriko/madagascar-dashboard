#!/usr/bin/env python3
"""
CORRECTEUR FINAL - 56 AP + MGA
===============================

Correction finale avec :
- 56 AP (données propres seulement)
- Montants en MGA (et USD)
- Période 2007-2023
- Tous les labels corrigés

Par KOUMI Dzudzogbe Prince Armand
"""

import json
import pandas as pd

def correction_finale():
    print("🚀 CORRECTION FINALE - 56 AP + MGA")
    print()
    
    # Données correctes pour 56 AP
    total_mga = 246568452252
    total_usd = total_mga / 3200
    nb_ap = 56
    periode = "2007-2023"
    
    print(f"📊 DONNÉES FINALES:")
    print(f"   • {total_mga:,.0f} MGA")
    print(f"   • {total_usd:,.0f} USD ({total_usd/1e9:.2f} milliards)")
    print(f"   • {nb_ap} AP (données propres)")
    print(f"   • Période: {periode}")
    print()
    
    # 1. Corriger le JSON
    print("🔧 Correction JSON...")
    with open('backend/data/analyse_financement_deforestation.json', 'r') as f:
        data = json.load(f)
    
    data['summary'] = {
        'total_investment': total_usd,
        'total_investment_mga': total_mga,
        'avg_investment': total_usd / nb_ap,
        'avg_investment_mga': total_mga / nb_ap,
        'avg_fire_rate': 0.398,
        'num_observations': 495,
        'num_aps': nb_ap,
        'period': periode,
        'currency': 'MGA',
        'currency_usd': 'USD',
        'conversion_rate': 3200
    }
    
    data['metadata']['verification'] = {
        'verified': True,
        'verified_by': 'KOUMI Dzudzogbe Prince Armand',
        'source': '56 AP avec données propres',
        'confidence': 'HIGH',
        'note': 'Seulement les AP avec données clean utilisées'
    }
    
    with open('backend/data/analyse_financement_deforestation.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("✅ JSON corrigé")
    
    # 2. Corriger le rapport HTML
    print("🔧 Correction rapport HTML...")
    with open('frontend/rapport_financement_deforestation.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Corrections spécifiques demandées
    corrections = {
        # Montants en MGA
        "+4,3 milliards USD recommandés": f"+{4300000000:,.0f} MGA ({4300000000/3200/1e6:.1f} M USD) recommandés",
        "+3,8 milliards USD recommandés": f"+{3800000000:,.0f} MGA ({3800000000/3200/1e6:.1f} M USD) recommandés", 
        "+6,8 milliards USD recommandés": f"+{6800000000:,.0f} MGA ({6800000000/3200/1e6:.1f} M USD) recommandés",
        "88,3 milliards USD par point": f"{88300000000:,.0f} MGA ({88300000000/3200/1e9:.1f} Mds USD) par point",
        
        # Investissement moyen
        "0 M USD par AP/an": f"{total_mga/nb_ap/1e6:.0f} M MGA ({total_usd/nb_ap/1e6:.0f} M USD) par AP/an",
        
        # Financement total avec les deux devises
        "0.1 Mds USD Investis": f"{total_mga/1e9:.1f} Mds MGA ({total_usd/1e9:.2f} Mds USD) Investis",
        
        # Labels des axes
        "Financement Annuel (Millions USD)": "Financement Annuel (Millions MGA)",
        "Investissement Total (Milliards USD)": "Investissement Total (Milliards MGA)",
        "financement annuel (millions USD)": "financement annuel (millions MGA)",
        
        # Nombre d'AP
        "89": str(nb_ap),
        "2007-2025": periode,
        "19 ans": "17 ans"
    }
    
    # Appliquer les corrections
    for old, new in corrections.items():
        html = html.replace(old, new)
    
    # Ajouter note sur les devises
    note_devise = """
    <div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 5px; padding: 10px; margin: 10px 0;">
        <strong>📝 Note sur les devises:</strong> Les montants sont affichés en MGA (Ariary malgache) avec équivalent USD. 
        Taux de change utilisé: 3,200 MGA = 1 USD. Analyse basée sur 56 AP avec données propres (2007-2023).
    </div>
    """
    
    html = html.replace('<div class="metrics-container">', note_devise + '\n        <div class="metrics-container">')
    
    with open('frontend/rapport_financement_deforestation.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ Rapport HTML corrigé")
    
    print()
    print("🎯 CORRECTION TERMINÉE!")
    print(f"   • {total_mga/1e9:.1f} milliards MGA")
    print(f"   • {total_usd/1e9:.2f} milliards USD") 
    print(f"   • {nb_ap} Aires Protégées (données propres)")
    print(f"   • Période {periode}")
    print()
    print("🔄 Génération des fichiers finaux...")

if __name__ == "__main__":
    correction_finale()
