#!/bin/bash

# Script de déploiement GitHub Pages
# Ce script prépare et pousse votre dashboard sur GitHub

echo "🚀 Déploiement du Dashboard sur GitHub Pages"
echo "=============================================="
echo ""

# Couleurs pour le terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Vérifier si git est initialisé
if [ ! -d .git ]; then
    echo -e "${YELLOW}⚠️  Git n'est pas initialisé. Initialisation...${NC}"
    git init
    echo -e "${GREEN}✅ Git initialisé${NC}"
fi

# Copier les fichiers les plus récents dans docs/
echo -e "${BLUE}📁 Copie des fichiers dans docs/...${NC}"
mkdir -p docs/visualizations
cp frontend/carte_madagascar_complete.html docs/ 2>/dev/null || echo "Carte déjà copiée"
cp frontend/rapport_financement_deforestation.html docs/ 2>/dev/null || echo "Rapport déjà copié"
cp frontend/visualizations/* docs/visualizations/ 2>/dev/null || echo "Visualisations déjà copiées"
echo -e "${GREEN}✅ Fichiers copiés${NC}"

# Ajouter tous les fichiers
echo -e "${BLUE}📦 Ajout des fichiers à Git...${NC}"
git add docs/
git add INSTRUCTIONS_GITHUB_PAGES.md
git add DEPLOY_GITHUB.sh

# Créer un commit
echo -e "${BLUE}💾 Création du commit...${NC}"
git commit -m "Deploy: Add GitHub Pages dashboard - $(date '+%Y-%m-%d %H:%M')"

# Vérifier si une remote est configurée
if ! git remote | grep -q origin; then
    echo ""
    echo -e "${YELLOW}⚠️  Aucune remote GitHub configurée${NC}"
    echo ""
    echo "Pour continuer, vous devez :"
    echo "1. Créer un repository sur GitHub : https://github.com/new"
    echo "2. Puis exécuter cette commande :"
    echo ""
    echo -e "${BLUE}   git remote add origin https://github.com/VOTRE-USERNAME/VOTRE-REPO.git${NC}"
    echo -e "${BLUE}   git branch -M main${NC}"
    echo -e "${BLUE}   git push -u origin main${NC}"
    echo ""
    echo "Ensuite, allez dans Settings > Pages et sélectionnez '/docs' comme source"
else
    # Pousser sur GitHub
    echo -e "${BLUE}⬆️  Push vers GitHub...${NC}"
    git push
    
    echo ""
    echo -e "${GREEN}✅ Déploiement terminé !${NC}"
    echo ""
    echo "📋 Prochaines étapes :"
    echo "1. Allez sur votre repository GitHub"
    echo "2. Settings > Pages"
    echo "3. Sélectionnez 'main' branch et '/docs' folder"
    echo "4. Attendez 1-2 minutes"
    echo "5. Votre site sera disponible à :"
    echo -e "${BLUE}   https://VOTRE-USERNAME.github.io/VOTRE-REPO/${NC}"
fi

echo ""
echo "📖 Consultez INSTRUCTIONS_GITHUB_PAGES.md pour plus de détails"
echo ""

