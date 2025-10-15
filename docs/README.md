# 🇲🇬 Dashboard Madagascar - Aires Protégées

Ce dossier contient les fichiers du dashboard web hébergé sur GitHub Pages.

## 📁 Contenu

- **index.html** : Page d'accueil avec navigation vers les deux rapports
- **carte_madagascar_complete.html** : Carte interactive des aires protégées
- **rapport_financement_deforestation.html** : Rapport exécutif avec analyses
- **visualizations/** : Images et graphiques
- **.nojekyll** : Fichier pour désactiver Jekyll (traitement GitHub Pages)

## 🌐 Accès

Une fois déployé sur GitHub Pages, ce dashboard est accessible via :
```
https://VOTRE-USERNAME.github.io/VOTRE-REPO-NAME/
```

## 🔄 Mise à jour

Pour mettre à jour le dashboard après des modifications :
```bash
cp ../frontend/*.html .
cp -r ../frontend/visualizations/* visualizations/
git add .
git commit -m "Update dashboard"
git push
```

Le site sera automatiquement mis à jour en 1-2 minutes.

