# 📋 Instructions pour publier sur GitHub Pages

## 🎯 Comment publier votre dashboard sur GitHub (GRATUIT)

### Étape 1: Préparer votre repository GitHub

1. **Allez sur GitHub** : https://github.com
2. **Créez un nouveau repository** (si pas déjà fait) :
   - Cliquez sur le bouton "+" en haut à droite
   - Sélectionnez "New repository"
   - Nom suggéré : `madagascar-dashboard` ou `firerisk-dashboard`
   - Laissez-le **PUBLIC** (important pour GitHub Pages gratuit)
   - NE cochez PAS "Initialize with README" si vous avez déjà du code local
   - Cliquez sur "Create repository"

### Étape 2: Pousser votre code sur GitHub

Ouvrez votre terminal dans le dossier du projet et exécutez :

```bash
# Si c'est un nouveau repository GitHub
git add docs/
git commit -m "Add GitHub Pages files"
git branch -M main
git remote add origin https://github.com/VOTRE-USERNAME/VOTRE-REPO-NAME.git
git push -u origin main
```

**OU si vous avez déjà un repository connecté :**

```bash
git add docs/
git commit -m "Add GitHub Pages files"
git push
```

### Étape 3: Activer GitHub Pages

1. **Allez sur votre repository sur GitHub**
   - URL : `https://github.com/VOTRE-USERNAME/VOTRE-REPO-NAME`

2. **Cliquez sur "Settings"** (dans le menu du repository)

3. **Dans le menu de gauche, cliquez sur "Pages"**

4. **Sous "Source" (ou "Build and deployment") :**
   - Branch : Sélectionnez `main`
   - Folder : Sélectionnez `/docs`
   - Cliquez sur "Save"

5. **Attendez 1-2 minutes** que GitHub déploie votre site

### Étape 4: Obtenir votre lien

Après quelques minutes, retournez sur la page "Settings > Pages"

Vous verrez un message :
```
✅ Your site is live at https://VOTRE-USERNAME.github.io/VOTRE-REPO-NAME/
```

**C'EST CE LIEN QUE VOUS ENVERREZ À VOTRE RESPONSABLE !**

---

## 📧 Email à envoyer à votre responsable

```
Objet : Dashboard d'Analyse - Financement et Déforestation Madagascar

Bonjour [Nom du responsable],

J'ai le plaisir de vous transmettre le dashboard interactif d'analyse du financement 
et de la déforestation des aires protégées de Madagascar.

🔗 Lien d'accès : https://VOTRE-USERNAME.github.io/VOTRE-REPO-NAME/

Le dashboard comprend :
- 🗺️ Une carte interactive avec géolocalisation de toutes les aires protégées
- 📊 Un rapport exécutif complet avec analyses et recommandations

Les données sont basées sur la période 2019-2024.

Cordialement,
[Votre nom]
```

---

## 🔄 Pour mettre à jour le site après des modifications

Si vous modifiez les fichiers HTML plus tard :

```bash
# Copiez les nouveaux fichiers dans docs/
cp frontend/carte_madagascar_complete.html docs/
cp frontend/rapport_financement_deforestation.html docs/
cp -r frontend/visualizations/* docs/visualizations/

# Poussez les modifications
git add docs/
git commit -m "Update dashboard"
git push
```

Le site sera automatiquement mis à jour en 1-2 minutes !

---

## ✅ Structure des fichiers pour GitHub Pages

```
docs/
├── index.html                              # Page d'accueil (créée)
├── carte_madagascar_complete.html          # Carte interactive
├── rapport_financement_deforestation.html  # Rapport exécutif
├── visualizations/                         # Images des graphiques
│   ├── carte_madagascar_ap.png
│   ├── correlation_financement_deforestation.png
│   ├── evolution_temporelle.png
│   └── ... (autres images)
└── .nojekyll                              # Fichier pour désactiver Jekyll
```

---

## 🆘 Problèmes courants et solutions

### Le site n'apparaît pas après 5 minutes
- Vérifiez que le dossier `/docs` est bien sélectionné dans Settings > Pages
- Vérifiez que le repository est PUBLIC
- Essayez de faire un "hard refresh" (Ctrl+F5 ou Cmd+Shift+R)

### Les images ne s'affichent pas
- Vérifiez que le dossier `visualizations/` est bien dans `docs/`
- Les chemins dans le HTML doivent être relatifs : `visualizations/image.png`

### Erreur 404
- Le lien doit finir par `/` : `https://username.github.io/repo-name/`
- Vérifiez que `index.html` est bien à la racine de `docs/`

---

## 💡 Avantages de GitHub Pages

✅ **GRATUIT** - Aucun coût
✅ **Rapide** - CDN global
✅ **Sécurisé** - HTTPS automatique
✅ **Simple** - Mises à jour avec git push
✅ **Professionnel** - Lien propre et permanent

---

## 📱 Le site est responsive

Votre responsable pourra voir le dashboard sur :
- 💻 Ordinateur
- 📱 Téléphone
- 📱 Tablette

Tout s'adapte automatiquement !

---

**Besoin d'aide ?** Consultez la documentation officielle : https://docs.github.com/pages

