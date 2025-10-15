#!/usr/bin/env python3
"""
Script pour convertir les montants USD restants en MGA
"""

import re

def convert_remaining_usd():
    """Convertit tous les montants USD restants en MGA"""
    
    input_file = '/Users/armandkoumi/projects/firerisk/dashboard/docs/carte_madagascar_complete.html'
    
    # Lire le fichier
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📖 Lecture du fichier: {input_file}")
    
    # Taux de change
    USD_TO_MGA = 4495
    
    # Pattern pour capturer $X.XX Mds MGA, $X.XX M MGA, $X.XX MGA
    patterns = [
        (r'\$([0-9]+(?:\.[0-9]+)?)\s+Mds\s+MGA', r'\1 Mds MGA'),
        (r'\$([0-9]+(?:\.[0-9]+)?)\s+M\s+MGA', r'\1 M MGA'),
        (r'\$([0-9]+(?:\.[0-9]+)?)\s+MGA', r'\1 MGA'),
    ]
    
    # Compter les occurrences avant
    usd_before = len(re.findall(r'\$[0-9]+', content))
    print(f"💰 Montants USD trouvés: {usd_before}")
    
    # Remplacer les patterns
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    # Maintenant convertir les montants numériques
    def convert_numeric_amount(match):
        amount_str = match.group(1)
        unit = match.group(2) if match.group(2) else ""
        
        try:
            amount = float(amount_str)
            converted = amount * USD_TO_MGA
            
            if unit == "Mds":
                return f"{converted/1000000:.0f} Mds"
            elif unit == "M":
                return f"{converted/1000:.0f} M"
            else:
                return f"{converted:.0f}"
        except:
            return match.group(0)
    
    # Convertir les montants numériques
    content = re.sub(r'([0-9]+(?:\.[0-9]+)?)\s+(Mds|M)?\s*MGA', convert_numeric_amount, content)
    
    # Compter après
    usd_after = len(re.findall(r'\$[0-9]+', content))
    mga_count = len(re.findall(r'[0-9]+ Mds MGA|[0-9]+ M MGA|[0-9]+ MGA', content))
    
    print(f"✅ Conversion terminée!")
    print(f"💰 Montants USD restants: {usd_after}")
    print(f"🇲🇬 Montants MGA: {mga_count}")
    
    # Sauvegarder
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"💾 Fichier sauvegardé")

if __name__ == "__main__":
    convert_remaining_usd()
