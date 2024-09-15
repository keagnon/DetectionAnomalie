

# 🌦️ Projet Météo - Détection d'Anomalies

![Python](https://img.shields.io/badge/python-3.9-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-orange?logo=streamlit)
![MLFlow](https://img.shields.io/badge/MLFlow-2.16.0-orange)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![CodeCarbon](https://img.shields.io/badge/CodeCarbon-2.7.1-brightgreen)
![Pandas](https://img.shields.io/badge/Pandas-2.2.2-green)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.5.1-yellow)
![CatBoost](https://img.shields.io/badge/CatBoost-Prediction-green)
![Google Cloud Storage](https://img.shields.io/badge/Google_Cloud_Storage-2.18.2-blue)


Le projet Météo vise à la détection d'anomalies et la prédiction de consommation énergétique à partir des données météorologiques. Il utilise des outils avancés de machine learning et des frameworks modernes pour créer un pipeline de bout en bout, de la collecte de données à la visualisation des résultats.
📋 Sommaire

    🌦️ Introduction
    🚀 Langages et Outils
    🗂️ Structure du Projet
    📈 Intégration avec MLflow
    🔧 Installation
    💻 Utilisation
    📚 Documentation
    🔗 Liens Utiles

# 🌦️ Introduction

Ce projet de détection d'anomalies utilise les données météorologiques pour prévoir la consommation énergétique et identifier les anomalies dans les données. Le modèle est entraîné à l'aide de CatBoost, un algorithme puissant de machine learning supervisé, et suivi via MLflow pour une gestion efficace des modèles et des expériences.
🚀 Langages et Outils
Outils	Versions
Python	3.9
Streamlit	1.38.0
MLflow	2.16.0
Docker	Enabled
CodeCarbon	2.7.1
Pandas	2.2.2
Scikit-learn	1.5.1
CatBoost	Prediction
Google Cloud Storage	2.18.2

Les modèles sont gérés via MLflow, offrant une traçabilité complète des versions et des performances. MLflow est déployé sur Google Cloud Platform (GCP), offrant ainsi un accès centralisé et une flexibilité dans la gestion des artefacts.

# 🗂️ Structure du Projet

Voici l'arborescence du projet pour vous guider à travers les différentes parties :

bash

📦 DETECTIONANOMALIE/
├── 📁 conf/                      # Fichiers de configuration
├── 📁 data/                      # Données utilisées dans le projet
│   ├── 📁 01_raw/                # Données brutes
│   ├── 📁 02_intermediate/       # Données intermédiaires
│   ├── 📁 03_primary/            # Données nettoyées
│   ├── 📁 04_feature/            # Features pour les modèles
│   ├── 📁 05_model_input/        # Données prêtes pour les modèles
│   ├── 📁 06_models/             # Modèles d'apprentissage automatique
│   ├── 📁 07_model_output/       # Résultats des modèles
│   └── 📁 08_reporting/          # Rapports et visualisations
├── 📁 docs/                      # Documentation du projet
├── 📁 MeteoMLFLOW/               # Gestion des expériences ML avec MLflow
├── 📁 notebooks/                 # Notebooks Jupyter pour l'analyse exploratoire
├── 📁 src/                       # Code source principal
│   ├── 📁 meteo/                 # Code spécifique à la météo
│   │   ├── 📁 pipelines/         # Pipelines de traitement
│   │   │   ├── 📁 data_processing/  # Scripts de traitement des données
│   │   │   ├── 📁 data_science/     # Scripts liés aux modèles
│   │   │   └── 📁 data_viz/         # Scripts de visualisation
├── 📁 mlflow-artifacts/          # Artifacts générés par MLflow
└── 📁 mlruns/                    # Logs et informations sur les runs MLflow

# 📈 Intégration avec MLflow

MLflow est utilisé pour le suivi, la gestion et la comparaison des modèles développés dans ce projet.
⚙️ Déployer MLflow
Utilisation Locale de MLflow

Pour exécuter MLflow en local :

    Installer MLflow :

    bash

pip install mlflow

Démarrer le serveur MLflow :

bash

    mlflow ui

    Accéder à l'interface : Ouvrez votre navigateur et rendez-vous sur http://localhost:5000 pour suivre vos expériences et gérer vos modèles.

![alt text](ml1.png) 
![alt text](ml2.png)

🔧 Installation

    Clonez le dépôt :

    bash

git clone https://github.com/votre-utilisateur/DETECTIONANOMALIE.git
cd DETECTIONANOMALIE

Installez les dépendances :

bash

pip install -r requirements.txt

Configurez vos variables d'environnement dans un fichier .env :

bash

    MLFLOW_TRACKING_URI=http://localhost:5000
    GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json

# 💻 Utilisation

    Lancer Streamlit :

    bash

    streamlit run src/meteo/template_connected.py



    Sélectionner les options dans l'interface utilisateur pour prédire la consommation énergétique, détecter les anomalies ou visualiser les résultats.



🛠️ Contribuer

Nous accueillons les contributions pour améliorer ce projet. Veuillez consulter le guide de contribution dans docs/CONTRIBUTING.md.
