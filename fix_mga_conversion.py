#!/usr/bin/env python3
"""
Script pour corriger et finaliser la conversion USD vers MGA
"""

import re

def fix_mga_conversion():
    """Corrige les conversions MGA malformées"""
    
    input_file = '/Users/armandkoumi/projects/firerisk/dashboard/docs/carte_madagascar_complete.html'
    
    # Lire le fichier
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📖 Lecture du fichier: {input_file}")
    
    # Taux de change USD vers MGA
    USD_TO_MGA = 4495
    
    # Patterns à corriger
    corrections = [
        # Corriger les formats malformés
        (r'(\d+)\s+Mds\s+M', r'\1 Mds MGA'),
        (r'(\d+)\s+M\s+Mds', r'\1 Mds MGA'),
        (r'(\d+)\s+Mds/an', r'\1 Mds MGA/an'),
        (r'(\d+)\s+M/an', r'\1 M MGA/an'),
        (r'(\d+)\s+MGA/ha', r'\1 MGA/ha'),
        
        # Ajouter MGA manquant
        (r'(\d+)\s+Mds(?!/)', r'\1 Mds MGA'),
        (r'(\d+)\s+M(?!/)', r'\1 M MGA'),
    ]
    
    # Appliquer les corrections
    for pattern, replacement in corrections:
        content = re.sub(pattern, replacement, content)
    
    # Maintenant convertir les montants USD restants
    def convert_usd_amount(match):
        amount_str = match.group(1)
        unit = match.group(2) if len(match.groups()) > 1 else ""
        
        try:
            amount = float(amount_str)
            converted = amount * USD_TO_MGA
            
            if unit == "Mds":
                return f"{converted/1000000:.0f} Mds MGA"
            elif unit == "M":
                return f"{converted/1000:.0f} M MGA"
            else:
                return f"{converted:.0f} MGA"
        except:
            return match.group(0)
    
    # Chercher et convertir les montants USD restants
    usd_patterns = [
        r'\$([0-9]+(?:\.[0-9]+)?)\s+(Mds|M)?',
        r'([0-9]+(?:\.[0-9]+)?)\s+Mds\s+MGA(?!/)',
        r'([0-9]+(?:\.[0-9]+)?)\s+M\s+MGA(?!/)',
    ]
    
    for pattern in usd_patterns:
        content = re.sub(pattern, convert_usd_amount, content)
    
    # Compter les résultats
    mga_count = len(re.findall(r'[0-9]+ Mds MGA|[0-9]+ M MGA|[0-9]+ MGA', content))
    usd_count = len(re.findall(r'\$[0-9]+', content))
    
    print(f"✅ Correction terminée!")
    print(f"💰 Montants USD restants: {usd_count}")
    print(f"🇲🇬 Montants MGA: {mga_count}")
    
    # Sauvegarder
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"💾 Fichier sauvegardé")
    
    # Afficher quelques exemples
    examples = re.findall(r'[0-9]+ Mds MGA|[0-9]+ M MGA|[0-9]+ MGA', content)[:5]
    print("\n📋 Exemples de montants MGA:")
    for example in examples:
        print(f"   • {example}")

if __name__ == "__main__":
    fix_mga_conversion()
