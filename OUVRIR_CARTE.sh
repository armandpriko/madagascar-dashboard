#!/bin/bash

# Script pour ouvrir la carte interactive de Madagascar
# Par KOUMI Dzudzogbe Prince Armand

echo "🗺️  Ouverture de la carte interactive de Madagascar..."
echo ""

# Chemin vers la carte
CARTE="frontend/carte_madagascar_complete.html"

# Vérifier si le fichier existe
if [ ! -f "$CARTE" ]; then
    echo "❌ La carte n'existe pas encore!"
    echo "🔧 Génération de la carte..."
    python3 generer_carte_interactive.py
fi

# Ouvrir dans le navigateur
echo "✅ Ouverture de la carte dans votre navigateur..."
open "$CARTE"

echo ""
echo "📍 Carte affichant 54 Aires Protégées de Madagascar"
echo "💡 Cliquez sur les cercles pour voir les détails de chaque AP"
echo "🎨 Couleurs: Vert=Efficace, Orange=Sous pression, Rouge=Critique"
echo ""

