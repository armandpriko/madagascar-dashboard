#!/bin/bash

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║              VÉRIFICATION DE TOUS LES FICHIERS                     ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

check_file() {
    if [ -f "$1" ]; then
        size=$(ls -lh "$1" | awk '{print $5}')
        echo "✅ $1 ($size)"
        return 0
    else
        echo "❌ $1 (MANQUANT)"
        return 1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        count=$(ls -1 "$1" | wc -l | tr -d ' ')
        echo "✅ $1/ ($count fichiers)"
        return 0
    else
        echo "❌ $1/ (MANQUANT)"
        return 1
    fi
}

total=0
ok=0

echo "🔥 DOCUMENTS POUR LE RESPONSABLE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file "SYNTHESE_1PAGE_RESPONSABLE.md" && ((ok++)); ((total++))
check_file "EMAIL_POUR_RESPONSABLE.txt" && ((ok++)); ((total++))
check_file "frontend/rapport_financement_deforestation.html" && ((ok++)); ((total++))
check_dir "frontend/visualizations" && ((ok++)); ((total++))
echo ""

echo "📊 VISUALISATIONS (5 graphiques)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file "frontend/visualizations/correlation_financement_deforestation.png" && ((ok++)); ((total++))
check_file "frontend/visualizations/segmentation_ap.png" && ((ok++)); ((total++))
check_file "frontend/visualizations/top_bottom_performers.png" && ((ok++)); ((total++))
check_file "frontend/visualizations/evolution_temporelle.png" && ((ok++)); ((total++))
check_file "frontend/visualizations/correlation_par_ap.png" && ((ok++)); ((total++))
echo ""

echo "📚 DOCUMENTATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file "RAPPORT_EXECUTIF_FINANCEMENT_DEFORESTATION.md" && ((ok++)); ((total++))
check_file "README_ANALYSE.md" && ((ok++)); ((total++))
check_file "RECAPITULATIF_COMPLET.md" && ((ok++)); ((total++))
check_file "🌳_START_HERE.md" && ((ok++)); ((total++))
echo ""

echo "💾 DONNÉES & SCRIPTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_file "backend/data/analyse_financement_deforestation.json" && ((ok++)); ((total++))
check_file "backend/data/unified_yearly.csv" && ((ok++)); ((total++))
check_file "analyse_financement_deforestation.py" && ((ok++)); ((total++))
check_file "generer_visualisations.py" && ((ok++)); ((total++))
check_file "generer_rapport_complet.py" && ((ok++)); ((total++))
check_file "OUVRIR_RAPPORT.sh" && ((ok++)); ((total++))
check_file "VERIFICATION.sh" && ((ok++)); ((total++))
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 RÉSULTAT : $ok/$total fichiers présents"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $ok -eq $total ]; then
    echo ""
    echo "�� TOUT EST EN ORDRE ! Vous êtes prêt(e) à présenter !"
    echo ""
    echo "🚀 PROCHAINES ÉTAPES :"
    echo "   1. Lisez : cat 🌳_START_HERE.md"
    echo "   2. Ou ouvrez : ./OUVRIR_RAPPORT.sh"
    echo "   3. Ou lisez : cat SYNTHESE_1PAGE_RESPONSABLE.md"
    echo ""
else
    missing=$((total - ok))
    echo ""
    echo "⚠️  $missing fichier(s) manquant(s)"
    echo ""
    echo "Pour régénérer tout :"
    echo "   python3 generer_rapport_complet.py"
    echo ""
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
