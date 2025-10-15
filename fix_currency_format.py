#!/usr/bin/env python3
"""
Script pour corriger le format des devises dans carte_madagascar_complete.html
- Remplacer "USD" par "MGA"
- Supprimer le symbole "$" devant les chiffres
- Nettoyer les formats incorrects comme "MGAds MGA MGA"
"""

import re

def fix_currency_format():
    file_path = "docs/carte_madagascar_complete.html"
    
    # Lire le fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Sauvegarder l'original
    with open(file_path + '.backup', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Fichier original sauvegardé dans carte_madagascar_complete.html.backup")
    
    # 1. Supprimer le symbole $ devant les chiffres
    content = re.sub(r'\$(\d+)', r'\1', content)
    
    # 2. Remplacer USD par MGA
    content = content.replace('USD', 'MGA')
    
    # 3. Nettoyer les formats incorrects comme "MGAds MGA MGA"
    # Pattern pour capturer les montants avec formats incorrects
    patterns_to_fix = [
        # Format: "nombre MGAds MGA MGA" -> "nombre MGA"
        (r'(\d+(?:\.\d+)?)\s+MGAds\s+MGA\s+MGA', r'\1 MGA'),
        # Format: "nombre MGA M" -> "nombre M MGA" 
        (r'(\d+(?:\.\d+)?)\s+MGA\s+M', r'\1 M MGA'),
        # Format: "nombre MGAds MGA None" -> "nombre MGA"
        (r'(\d+(?:\.\d+)?)\s+MGAds\s+MGA\s+None', r'\1 MGA'),
        # Format: "nombre MGA MGA" -> "nombre MGA"
        (r'(\d+(?:\.\d+)?)\s+MGA\s+MGA', r'\1 MGA'),
    ]
    
    for pattern, replacement in patterns_to_fix:
        content = re.sub(pattern, replacement, content)
    
    # 4. Corriger les formats spécifiques pour les montants
    # Format: "nombre MGA/an" -> "nombre MGA/an" (garder tel quel)
    # Format: "nombre MGA/ha" -> "nombre MGA/ha" (garder tel quel)
    
    # Écrire le fichier corrigé
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Format des devises corrigé dans docs/carte_madagascar_complete.html")
    print("Changements appliqués:")
    print("- Suppression du symbole $ devant les chiffres")
    print("- Remplacement de USD par MGA")
    print("- Nettoyage des formats incorrects")

if __name__ == "__main__":
    fix_currency_format()
