#!/usr/bin/env python3
"""
Script pour convertir tous les montants USD en MGA dans la carte HTML
Taux de change: 1 USD = 4,495 MGA
"""

import re
import sys

def convert_usd_to_mga(html_content):
    """
    Convertit tous les montants USD en MGA dans le contenu HTML
    """
    # Taux de change USD vers MGA
    USD_TO_MGA = 4495
    
    def convert_amount(match):
        """Convertit un montant USD en MGA"""
        amount_str = match.group(1)
        unit = match.group(2)
        
        try:
            # Parse le montant
            amount = float(amount_str)
            
            # Convertir en MGA
            converted_amount = amount * USD_TO_MGA
            
            # Formater le résultat
            if converted_amount >= 1000000:  # Millions
                formatted = f"{converted_amount/1000000:.0f} Mds"
            elif converted_amount >= 1000:  # Milliers
                formatted = f"{converted_amount/1000:.0f} M"
            else:
                formatted = f"{converted_amount:.0f}"
            
            return f"{formatted} {unit}"
            
        except ValueError:
            # Si on ne peut pas parser le montant, retourner tel quel
            return match.group(0)
    
    # Pattern pour capturer les montants USD
    # Exemples: $3.94 Mds MGA/an, $224.09 M MGA/an, $7738 MGA/ha
    pattern = r'\$([0-9]+(?:\.[0-9]+)?)\s+(Mds|M|K)?\s*MGA(/[a-z]+)?'
    
    # Remplacer tous les montants USD par MGA
    converted_content = re.sub(pattern, convert_amount, html_content)
    
    return converted_content

def main():
    """Fonction principale"""
    input_file = '/Users/armandkoumi/projects/firerisk/dashboard/docs/carte_madagascar_complete.html'
    
    try:
        # Lire le fichier
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📖 Lecture du fichier: {input_file}")
        print(f"📏 Taille du fichier: {len(content):,} caractères")
        
        # Compter les occurrences USD avant conversion
        usd_count_before = len(re.findall(r'\$[0-9]+', content))
        print(f"💰 Montants USD trouvés: {usd_count_before}")
        
        # Convertir
        converted_content = convert_usd_to_mga(content)
        
        # Compter les occurrences USD après conversion
        usd_count_after = len(re.findall(r'\$[0-9]+', converted_content))
        mga_count = len(re.findall(r'[0-9]+ Mds MGA|[0-9]+ M MGA|[0-9]+ MGA', converted_content))
        
        print(f"✅ Conversion terminée!")
        print(f"💰 Montants USD restants: {usd_count_after}")
        print(f"🇲🇬 Montants MGA créés: {mga_count}")
        
        # Sauvegarder
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(converted_content)
        
        print(f"💾 Fichier sauvegardé: {input_file}")
        
        # Afficher quelques exemples de conversion
        print("\n📋 Exemples de conversions:")
        examples = re.findall(r'[0-9]+ Mds MGA|[0-9]+ M MGA|[0-9]+ MGA', converted_content)[:5]
        for example in examples:
            print(f"   • {example}")
            
    except FileNotFoundError:
        print(f"❌ Erreur: Fichier non trouvé: {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
