# 🗺️ CARTES INTERACTIVES - AIRES PROTÉGÉES DE MADAGASCAR

## 📍 Vue d'ensemble

Ce document décrit les cartes géographiques générées pour visualiser les **56 Aires Protégées** analysées dans le cadre de l'étude sur l'efficacité des financements vs déforestation.

---

## 🎯 CARTES DISPONIBLES

### 1. 🌐 CARTE INTERACTIVE (Recommandée)

**Fichier** : `frontend/carte_madagascar_complete.html`

**Ouverture rapide** :
```bash
./OUVRIR_CARTE.sh
```

**Fonctionnalités** :
- ✅ **Carte interactive** avec OpenStreetMap, Terrain, et vue Satellite
- ✅ **54 AP géolocalisées** avec précision GPS
- ✅ **Taille des cercles** = Superficie de l'AP (8-30 pixels)
- ✅ **Couleur des cercles** = Catégorie d'efficacité :
  - 🟢 **Vert** : EFFICACES (Investis + Protégés)
  - 🟢 **Vert clair** : NATURELLEMENT PROTÉGÉES
  - 🟠 **Orange** : SOUS PRESSION (Investis mais fragiles)
  - 🔴 **Rouge** : CRITIQUES (Peu investis + Forte déforestation)
- ✅ **Popup au clic** : Détails complets (financement, taux de feu, score, etc.)
- ✅ **Tooltip au survol** : Nom et superficie
- ✅ **Villes principales** : Antananarivo, Toamasina, Toliara, Mahajanga, Antsiranana
- ✅ **Contrôles** :
  - Zoom/Pan interactif
  - Choix du fond de carte (OpenStreetMap, Terrain, Satellite)
  - Activation/désactivation des catégories d'AP
  - Plein écran
  - Minimap
  - Mesure de distance

**Statistiques affichées** :
- 📍 56 Aires Protégées cartographiées
- 📐 Superficie totale (millions d'hectares)
- 💰 Financement total (milliards USD/an)
- Distribution par catégorie (Efficaces, Naturelles, Pression, Critiques)
- 🔥 Taux de feu moyen

---

### 2. 📊 CARTES STATIQUES (PNG)

**Localisation** : `frontend/visualizations/`

#### a) Carte complète de Madagascar
**Fichier** : `carte_madagascar_ap.png`
- Vue d'ensemble de toute l'île
- 54 AP positionnées
- Top 5 AP critiques annotées (rouge)
- Top 3 AP champions annotées (vert)
- Légende des catégories et tailles
- Villes principales marquées
- Résolution 300 DPI (haute qualité)

#### b) Zoom Nord
**Fichier** : `carte_madagascar_zoom_nord.png`
- Focus sur les AP au nord de -16° latitude
- Zone à forte concentration d'AP
- Toutes les AP annotées
- Idéal pour présentation régionale

#### c) Zoom Sud
**Fichier** : `carte_madagascar_zoom_sud.png`
- Focus sur les AP au sud de -21° latitude
- Zone à forte pression anthropique
- Toutes les AP annotées
- Identifie les zones critiques du sud

---

## 📈 COUVERTURE GPS

Sur les **56 AP analysées** :
- ✅ **54 AP ont des coordonnées GPS** (96.4% de couverture)
- ❌ **2 AP sans coordonnées** :
  - TOTAL (ligne agrégée, pas une AP réelle)
  - Potentiellement une autre AP manquante dans le fichier de coordonnées

---

## 🎨 LÉGENDE DES COULEURS

### Catégories d'efficacité

| Couleur | Catégorie | Description | Nombre |
|---------|-----------|-------------|--------|
| 🟢 Vert foncé | **EFFICACES** | Investis + Bien protégés | 14 AP |
| 🟢 Vert clair | **NATURELLES** | Peu investis mais peu de feux | 13 AP |
| 🟠 Orange | **SOUS PRESSION** | Investis mais encore fragiles | 15 AP |
| 🔴 Rouge | **CRITIQUES** | Peu investis + Forte déforestation | 14 AP |

---

## 📍 EXEMPLES D'AP PAR CATÉGORIE

### 🌟 TOP 3 EFFICACES (Champions)
1. **ORONJIA** - Score: 0.289 (très petit, très investi, très protégé)
2. **IVOHIBE** - Score: 0.221 (investi massivement, bien protégé)
3. **MAROMIZAHA** - Score: 0.222 (petit mais excellent modèle)

### 🚨 TOP 3 CRITIQUES (Urgence)
1. **ANDRANOMENA** - 3.16 feux/100ha (situation catastrophique)
2. **ZOMBITSE VOHIBASIA** - 1.81 feux/100ha
3. **KALAMBATRITRA** - 1.50 feux/100ha

---

## 🛠️ COMMENT GÉNÉRER LES CARTES

### Cartes statiques (PNG)
```bash
python3 generer_carte_madagascar.py
```

### Cartes interactives (HTML)
```bash
python3 generer_carte_interactive.py
```

---

## 💡 UTILISATION DANS LES PRÉSENTATIONS

### Pour un email
→ Joindre : `carte_madagascar_ap.png`

### Pour une réunion en ligne
→ Partager l'écran avec : `carte_madagascar_complete.html`

### Pour un rapport PDF
→ Inclure : Les 3 cartes PNG (complète + zooms)

### Pour un site web
→ Intégrer : `carte_madagascar_interactive.html` en iframe

---

## 🔧 DÉPENDANCES TECHNIQUES

### Cartes statiques
- `matplotlib` : Visualisations
- `pandas` : Manipulation de données
- `numpy` : Calculs

### Cartes interactives
- `folium` : Cartes web interactives
- `pandas` : Manipulation de données
- Basé sur Leaflet.js (JavaScript)

### Installation
```bash
pip install matplotlib pandas numpy folium
```

---

## 📊 DONNÉES SOURCES

1. **Coordonnées GPS** : `AP_coords.csv`
   - 123 AP avec coordonnées latitude/longitude
   - Source : Base de données Madagascar National Parks

2. **Analyse financière** : `backend/data/analyse_financement_deforestation.json`
   - 56 AP avec données de financement et déforestation
   - Période : 2007-2023
   - Source : Analyse par KOUMI Dzudzogbe Prince Armand

3. **Fusion** : 54 AP avec coordonnées ET données financières
   - Matching par nom (avec gestion des variations)
   - Cas spéciaux gérés (Montagne des Français, Tsimembo, Itremo)

---

## 🎓 INTERPRÉTATION GÉOGRAPHIQUE

### Observations clés

1. **Nord de Madagascar** :
   - Forte concentration d'AP
   - Mix de catégories (efficaces et critiques)
   - Zone importante pour la biodiversité

2. **Sud de Madagascar** :
   - Pression anthropique élevée
   - Plusieurs AP critiques (Zombitse, Kalambatritra)
   - Zone prioritaire pour interventions

3. **Centre-Est** :
   - Corridor forestier important
   - Plusieurs AP efficaces (Anjanaharibe Sud, Marojejy)
   - À préserver comme modèle

4. **Ouest** :
   - Vastes AP peu denses
   - Surtout naturellement protégées
   - Surveillance nécessaire pour maintien

---

## 📞 SUPPORT

Pour toute question sur les cartes :
- **Auteur** : KOUMI Dzudzogbe Prince Armand
- **Projet** : Analyse Financement vs Déforestation - Madagascar
- **Année** : 2025
- **Données** : 2007-2023

---

## 🚀 PROCHAINES ÉTAPES

1. ✅ Cartes générées
2. ⏭️ Intégration dans le dashboard web
3. ⏭️ Export en haute résolution pour publication
4. ⏭️ Cartes animées (évolution temporelle)
5. ⏭️ Cartes de chaleur (hotspots de déforestation)

---

## 📝 NOTES TECHNIQUES

### Format des coordonnées
- **Latitude** : -25.6 à -12.0 (Sud de Madagascar)
- **Longitude** : 43.2 à 50.5 (Étendue Est-Ouest)
- **Système** : WGS84 (standard GPS)

### Taille des fichiers
- Cartes PNG : ~2-5 MB chacune (haute résolution)
- Carte HTML : ~500 KB (avec toutes les données embarquées)

### Compatibilité navigateurs
- ✅ Chrome/Edge : Parfait
- ✅ Firefox : Parfait
- ✅ Safari : Parfait
- ⚠️ Internet Explorer : Non supporté (utiliser Edge)

---

**Dernière mise à jour** : 2025-10-12

**Auteur** : KOUMI Dzudzogbe Prince Armand

