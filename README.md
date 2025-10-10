# Dashboard Environnemental Madagascar
## Analyse des Aires Protégées et Déforestation

### Description
Dashboard interactif professionnel pour analyser la relation entre les investissements dans les aires protégées et la déforestation à Madagascar.

### Fonctionnalités
- 🗺️ **Carte interactive** avec visualisation des aires protégées et zones de déforestation
- 📊 **Diagrammes interactifs** montrant les tendances d'investissement et corrélations
- 🎛️ **Contrôles et filtres** pour analyser les données par type, année, taux de déforestation
- 📈 **Statistiques en temps réel** avec métriques clés
- 🎨 **Interface moderne** avec thème environnemental professionnel

### Structure du Projet
```
dashboard/
├── backend/                 # Serveur Flask API
│   ├── app.py              # Application principale
│   ├── requirements.txt    # Dépendances Python
│   └── data/               # Données générées
├── frontend/               # Interface utilisateur
│   └── index.html         # Dashboard HTML/CSS/JS
├── data_analysis/         # Scripts d'analyse
│   └── data_explorer.py   # Exploration des données
├── generate_data.py       # Génération des données
└── start_dashboard.py    # Script de démarrage
```

### Installation et Utilisation

#### 1. Prérequis
- Python 3.8+
- Pip ou Conda
- Navigateur web moderne

#### 2. Installation des dépendances
```bash
cd dashboard/backend
pip install -r requirements.txt
```

#### 3. Génération des données
```bash
cd dashboard
python generate_data.py
```

#### 4. Démarrage du dashboard
```bash
python start_dashboard.py
```

Le dashboard sera accessible à l'adresse : `http://localhost:5000`

### API Endpoints

- `GET /api/summary` - Statistiques de résumé
- `GET /api/protected-areas` - Données des aires protégées
- `GET /api/deforestation` - Données de déforestation
- `GET /api/correlation` - Analyse de corrélation
- `GET /api/trends` - Tendances temporelles
- `GET /api/geojson/protected-areas` - GeoJSON des aires protégées

### Technologies Utilisées

#### Backend
- **Flask** - Framework web Python
- **Pandas** - Manipulation des données
- **GeoPandas** - Données géographiques
- **NumPy** - Calculs numériques

#### Frontend
- **HTML5/CSS3** - Structure et style
- **JavaScript ES6** - Logique interactive
- **Leaflet** - Cartes interactives
- **Chart.js** - Graphiques et diagrammes
- **Font Awesome** - Icônes

### Données Sources
- Aires protégées de Madagascar (`AP_Mada.zip`)
- Grille de données (`grid_1km.gpkg`)
- Données MNP (`mnp_norm.gpkg`)

### Fonctionnalités Avancées
- Filtrage en temps réel par type d'aire protégée
- Analyse temporelle des tendances
- Calcul automatique des corrélations
- Visualisation géographique interactive
- Interface responsive et moderne

### Personnalisation
Le dashboard peut être facilement personnalisé en modifiant :
- Les couleurs dans `frontend/index.html`
- Les endpoints API dans `backend/app.py`
- Les calculs d'analyse dans `data_analysis/data_explorer.py`

### Support
Pour toute question ou problème, consultez les logs du serveur Flask ou les erreurs dans la console du navigateur.
