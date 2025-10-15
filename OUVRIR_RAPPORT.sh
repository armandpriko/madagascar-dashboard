#!/bin/bash

# Script pour ouvrir le rapport d'analyse Financement-Déforestation

echo "═══════════════════════════════════════════════════════════════"
echo "🚀 OUVERTURE DU RAPPORT FINANCEMENT-DÉFORESTATION"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Chemin du rapport HTML
RAPPORT_HTML="frontend/rapport_financement_deforestation.html"

# Vérifier que le fichier existe
if [ ! -f "$RAPPORT_HTML" ]; then
    echo "❌ Erreur : Le rapport n'existe pas encore"
    echo ""
    echo "Veuillez d'abord générer le rapport avec :"
    echo "   python3 generer_rapport_complet.py"
    echo ""
    exit 1
fi

echo "✅ Rapport trouvé : $RAPPORT_HTML"
echo ""

# Ouvrir le rapport selon l'OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "🌐 Ouverture dans votre navigateur (macOS)..."
    open "$RAPPORT_HTML"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "🌐 Ouverture dans votre navigateur (Linux)..."
    xdg-open "$RAPPORT_HTML" 2>/dev/null || firefox "$RAPPORT_HTML" 2>/dev/null || google-chrome "$RAPPORT_HTML" 2>/dev/null
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    echo "🌐 Ouverture dans votre navigateur (Windows)..."
    start "$RAPPORT_HTML"
else
    echo "⚠️  Système d'exploitation non reconnu"
    echo "Ouvrez manuellement : $(pwd)/$RAPPORT_HTML"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ LE RAPPORT DEVRAIT S'OUVRIR DANS VOTRE NAVIGATEUR"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "📄 Autres documents disponibles :"
echo "   • SYNTHESE_1PAGE_RESPONSABLE.md (résumé 1 page)"
echo "   • RAPPORT_EXECUTIF_FINANCEMENT_DEFORESTATION.md (complet)"
echo "   • EMAIL_POUR_RESPONSABLE.txt (template email)"
echo "   • frontend/visualizations/ (5 graphiques PNG)"
echo ""
echo "🎯 Pour présenter à votre responsable :"
echo "   1. Utilisez le rapport HTML qui vient de s'ouvrir"
echo "   2. Ou envoyez l'email avec les documents joints"
echo "   3. Ou imprimez la synthèse 1 page"
echo ""
echo "═══════════════════════════════════════════════════════════════"

