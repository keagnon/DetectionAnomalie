
## 🌦️ Projet Météo - Détection d'Anomalies

### Langage
![Python](https://img.shields.io/badge/python-3.9-blue)

### Frameworks et Outils de Développement
![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-orange?logo=streamlit)
![MLflow](https://img.shields.io/badge/MLFlow-2.16.0-orange)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![CodeCarbon](https://img.shields.io/badge/CodeCarbon-2.7.1-brightgreen)

### Machine Learning & Data Science
![Pandas](https://img.shields.io/badge/Pandas-2.2.2-green)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.5.1-yellow)
![CatBoost](https://img.shields.io/badge/CatBoost-Prediction-green)

### Cloud & Stockage
![Google Cloud Storage](https://img.shields.io/badge/Google_Cloud_Storage-2.18.2-blue)


Le suivi et la gestion des modèles sont assurés via MLflow, qui permet une traçabilité complète des versions et des performances des modèles. Nous avons choisi de déployer MLflow sur une infrastructure cloud via Google Cloud Platform (GCP), offrant ainsi un accès centralisé et une flexibilité dans la gestion des artefacts. L'URL du serveur MLflow est stockée dans nos fichiers .env, facilitant l'accès et l'utilisation de l'outil.

Voici l'arborescence du projet pour vous guider dans les différentes parties du code et des données :

📦 DETECTIONANOMALIE/
├── 📁 conf/                      # Fichiers de configuration
├── 📁 data/                      # Données utilisées dans le projet
│   ├── 📁 01_raw/                # Données brutes
│   ├── 📁 02_intermediate/       # Données intermédiaires
│   ├── 📁 03_primary/            # Données primaires nettoyées
│   ├── 📁 04_feature/            # Features pour les modèles
│   ├── 📁 05_model_input/        # Données prêtes pour les modèles
│   ├── 📁 06_models/             # Modèles d'apprentissage automatique
│   ├── 📁 07_model_output/       # Résultats des modèles
│   └── 📁 08_reporting/          # Rapports et visualisations des résultats
├── 📁 docs/                      # Documentation du projet
├── 📁 MeteoMLFLOW/               # Gestion des expériences ML avec MLFlow
├── 📁 notebooks/                 # Notebooks Jupyter pour l'analyse exploratoire
├── 📁 src/                       # Code source principal
│   ├── 📁 meteo/                 # Code spécifique à la météo
│   │   ├── 📁 pipelines/         # Pipelines de traitement
│   │   │   ├── 📁 data_processing/  # Scripts de traitement des données
│   │   │   ├── 📁 data_science/     # Scripts liés aux modèles
│   │   │   └── 📁 data_viz/         # Scripts de visualisation des données
├── 📁 mlflow-artifacts/          # Artifacts générés par MLFlow
├── 📁 mlruns/                    # Logs et informations sur les runs MLFlow
└── 📁 notebooks/                 # Notebooks d'analyse



## 📈 Intégration avec MLflow

MLflow est utilisé pour le suivi, la gestion et la comparaison des modèles de machine learning développés dans ce projet.
⚙️ Déployer MLflow

1. Utilisation Locale de MLflow

Pour un déploiement local de MLflow, voici les étapes à suivre :

Installer MLflow :

pip install mlflow


Démarrer le serveur MLflow :


mlflow ui

Accéder à l'interface :

Rendez-vous sur http://localhost:5000 pour suivre vos expériences et gérer vos modèles localement.

