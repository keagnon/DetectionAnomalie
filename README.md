# Projet de Détection des Anomalies Énergétiques

## Description

Ce projet est un pipeline complet de bout en bout pour la détection des anomalies dans la consommation énergétique. Il inclut la collecte et l'ingestion des données, l'ingénierie des features, l'entraînement et l'évaluation des modèles de machine learning, ainsi que la mise en production et le monitoring.

## Structure du Projet

```
root_project/
├── data/                           # Données utilisées dans le projet
│   ├── raw/                        # Données brutes collectées
│   ├── processed/                  # Données traitées
│   └── external/                   # Données provenant de sources externes
│
├── notebooks/                      # Notebooks Jupyter pour exploration et analyse
│
├── src/                            # Code source du projet
│   ├── data/
│   │   ├── ingestion.py            # Scripts pour la collecte et l'ingestion des données
│   │   └── preprocessing.py        # Scripts pour le prétraitement des données
│   │
│   ├── features/
│   │   └── feature_engineering.py  # Scripts pour l'ingénierie des features
│   │
│   ├── models/
│   │   ├── train.py                # Scripts pour l'entraînement des modèles
│   │   ├── predict.py              # Scripts pour les prédictions
│   │   └── evaluate.py             # Scripts pour l'évaluation des modèles
│   │
│   ├── pipelines/                  # Pipelines Kedro
│   │   ├── pipeline.py             # Définition du pipeline
│   │   └── nodes.py                # Nodes pour le pipeline Kedro
│   │
│   ├── deployment/
│   │   ├── mlflow/                 # Configuration et scripts pour Mlflow
│   │   └── serve.py                # Scripts pour la mise en production
│   │
│   ├── monitoring/
│   │   └── grafana/                # Configuration et dashboards pour Grafana
│   │
│   └── tests/                      # Tests unitaires
│       ├── test_ingestion.py       # Tests pour ingestion.py
│       ├── test_preprocessing.py   # Tests pour preprocessing.py
│       ├── test_train.py           # Tests pour train.py
│       ├── test_predict.py         # Tests pour predict.py
│       └── test_evaluate.py        # Tests pour evaluate.py
│
├── config/
│   ├── parameters.yml              # Fichier de configuration des paramètres
│   └── catalog.yml                 # Fichier de configuration du catalogue Kedro
│
├── scripts/
│   └── financial_analysis.py       # Script pour l'analyse financière et génération de graphiques
│
├── .github/
│   └── workflows/
│       └── ci.yml                  # Configuration de l'intégration continue avec GitHub Actions
│
├── requirements.txt                # Liste des dépendances du projet
├── README.md                       # Documentation du projet
└── .gitignore                      # Fichiers et dossiers à ignorer par Git
```

## Architecture du Projet

![Architecture du Projet](path/to/your/image.png)

1. **Data Collection**
   - Source : CSV, API
   - Documentation & Maintenance

2. **Preprocessing**
   - Data Cleaning
   - Transformation
   - Documentation & Maintenance

3. **Model Development**
   - Keras/TF
   - Model Testing
   - Hyperparameter Optimization
   - Model Tracking
   - Model Registry
   - Documentation & Maintenance

4. **User Interface**
   - Streamlit
   - Mlflow UI
   - Documentation & Maintenance

5. **Deployment**
   - Testing
   - Containerization
   - Deployment with Mlflow
   - Documentation & Maintenance

## Installation

Pour installer les dépendances du projet, exécutez la commande suivante :

```sh
pip install -r requirements.txt
```
