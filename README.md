# 🚀 Détection d'Anomalies dans la Consommation d'Énergie

### Langage

![Python Badge](https://img.shields.io/badge/python-3.9-blue)

### Frameworks et Outils de Développement

![Streamlit Badge](https://img.shields.io/badge/Streamlit-1.38.0-orange)
![MLFlow Badge](https://img.shields.io/badge/MLFlow-2.16.0-orange)
![Flask Badge](https://img.shields.io/badge/Flask-3.0.3-black)
![Docker Badge](https://img.shields.io/badge/Docker-Enabled-blue)
![Kedro Badge](https://img.shields.io/badge/Kedro-0.19.8-brightgreen)
![Pre-commit Badge](https://img.shields.io/badge/Pre--Commit--Hooks-4.6.0-blue)
![GitPython Badge](https://img.shields.io/badge/GitPython-3.1.43-orange)

### Machine Learning & Data Science

![MLFlow Badge](https://img.shields.io/badge/MLFlow-2.16.0-orange)
![Pandas Badge](https://img.shields.io/badge/Pandas-2.2.2-brightgreen)
![Scikit-Learn Badge](https://img.shields.io/badge/Scikit--learn-1.5.1-orange)
![Matplotlib Badge](https://img.shields.io/badge/Matplotlib-3.9.2-blue)
![Plotly Badge](https://img.shields.io/badge/Plotly-5.24.0-blue)
![KMeans Badge](https://img.shields.io/badge/KMeans-Clustering-yellow)
![DBSCAN Badge](https://img.shields.io/badge/DBSCAN-Clustering-brightgreen)
![Isolation Forest Badge](https://img.shields.io/badge/Isolation--Forest-Anomaly%20Detection-blue)
![Ridge Regression Badge](https://img.shields.io/badge/Ridge--Regression-Prediction-lightblue)
![Random Forest Badge](https://img.shields.io/badge/Random--Forest-Prediction-brightgreen)

### Cloud & Stockage

![Google Cloud Storage Badge](https://img.shields.io/badge/Google%20Cloud%20Storage-2.18.2-orange)
![Elasticsearch Badge](https://img.shields.io/badge/Elasticsearch-8.15.0-grey)
![PyMongo Badge](https://img.shields.io/badge/PyMongo-4.8.0-green)
![Boto3 Badge](https://img.shields.io/badge/Boto3-1.35.14-green)

### CI/CD et Outils de Débogage

![Pre-Commit Badge](https://img.shields.io/badge/Pre--Commit--Hooks-4.6.0-blue)
![Pylint Badge](https://img.shields.io/badge/Pylint-Enabled-green)
![Isort Badge](https://img.shields.io/badge/Isort-Enabled-brightgreen)
![Black Badge](https://img.shields.io/badge/Black-Enabled-black)
![GitHub Actions Badge](https://img.shields.io/badge/GitHub--Actions-CI%2FCD-brightgreen)


## 📑 Sommaire
1. [🔍 Contexte du Projet](#1-contexte-du-projet)
2. [🎯 Pourquoi ce projet ?](#2-pourquoi-ce-projet)
3. [🎯 Objectifs du Projet](#3-objectifs-du-projet)
4. [🏗️ Architecture du Projet](#4-architecture-du-projet)
5. [⚙️ Intégration Continue (CI) et Tests Unitaires](#5-intégration-continue-ci-et-tests-unitaires)
6. [📂 Structure du Projet](#6-structure-du-projet)
7. [🔄 Pipelines de Collecte de Données avec Kedro](#7-pipelines-de-collecte-de-données-avec-kedro)
8. [💻 Traitement des Données et Utilisation de Google Colab](#8-traitement-des-données-et-utilisation-de-google-colab)
9. [🤖 Modèles de Machine Learning](#9-modèles-de-machine-learning)
10. [🖥️ Interface Utilisateur avec Streamlit](#10-interface-utilisateur-avec-streamlit)
11. [📊 Ordonnancement des Données avec Airflow](#11-ordonnancement-des-données-avec-airflow)

---

## 1. 🔍 Contexte du Projet
La détection précoce des anomalies énergétiques est essentielle pour la gestion proactive de l'énergie, en particulier pendant les périodes de forte demande (hiver, été) ou durant des événements comme les mouvements sociaux. Ce projet vise à identifier ces anomalies en se basant sur des données variées (météorologiques, sociales, etc.) et à fournir une interface utilisateur permettant la visualisation et l'analyse des résultats. La solution est structurée en plusieurs sous-projets interconnectés, chacun avec des objectifs spécifiques.

## 2. 🎯 Pourquoi ce projet ?
Nous avons identifié plusieurs défis majeurs dans la gestion énergétique :
- **Surconsommation en Hiver et en Été** : Augmentation significative de la demande en électricité pendant les périodes de froid ou de chaleur extrême.
- **Jours Fériés et Mouvements Sociaux** : Les variations imprévues dans la consommation peuvent déséquilibrer l'offre et la demande.

Nos cibles principales incluent :
- **Entreprises d'Électricité** (comme Engie et EDF) qui doivent surveiller la consommation en temps réel et ajuster leur production.
- **Industries à Forte Consommation** qui nécessitent une gestion optimale de leur énergie pour éviter des interruptions.

## 3. 🎯 Objectifs du Projet
Notre projet se concentre sur six grands objectifs :
1. **🔍 Détection des Anomalies** : Identifier en temps réel les anomalies de consommation et les cyberattaques potentielles.
2. **📈 Prédiction des Incidents** : Utiliser des modèles prédictifs pour anticiper les risques futurs.
3. **⚡ Optimisation des Ressources** : Aider les entreprises à optimiser leur consommation énergétique.
4. **🔄 Amélioration Continue** : Intégrer les retours des utilisateurs pour perfectionner notre système.
5. **🌍 Réduction de l'Empreinte Carbone** : Calculer l'impact carbone de nos serveurs et de nos traitements de données.
6. **📅 Prévision et Planification** : Utiliser des séries temporelles pour prédire les besoins futurs en énergie.

## 4. 🏗️ Architecture du Projet
Le projet est divisé en plusieurs modules interconnectés, chacun jouant un rôle clé dans l'ensemble du système.

### Workflow Général
![Workflow](images/Workflow.png)

### 🛠️ Module Collecte et Stockage des Données

### 🛠️ Module Traitement, Stockage et Visualisation

### 🛠️ Module Entraînement et Suivi des Modèles

### 🛠️ Module Déploiement et Feedback

### 🛠️ Module d'Orchestration et Conteneurisation

## 5. ⚙️ Intégration Continue (CI) et Tests Unitaires
Nous avons mis en place une CI via GitHub Actions, qui exécute des tests unitaires pour chaque sous-projet à chaque commit.

### Outils utilisés pour la CI :
- **🧪 Pytest** pour les tests unitaires
- **🔍 Pylint, Black, Mypy** pour l'analyse statique et le formatage du code
- **📊 Coverage** pour mesurer la couverture des tests

Le pipeline de CI est disponible dans le répertoire `.github/workflows`.

Chaque module du projet est containerisé avec Docker pour garantir la portabilité et la cohérence des environnements. Les fichiers `.env` sont utilisés pour configurer les variables d'environnement de manière flexible.

## 6. 📂 Structure du Projet
(Insérer la structure détaillée du projet ici)

Nous utilisons un **🛠️ Makefile** pour automatiser les processus de build, de tests et faciliter la gestion de la CI locale.

## 7. 🔄 Pipelines de Collecte de Données avec Kedro
Deux pipelines Kedro ont été mis en place :
1. **Pipeline ETL** : Ce pipeline collecte, transforme et stocke les données dans MongoDB.
2. **Pipeline d'Enrichissement** : Ce pipeline charge les données, les fusionne et les stocke dans Elasticsearch.

Les données brutes stockées dans Elasticsearch sont visualisées dans un tableau de bord **Kibana** hébergé sur une machine virtuelle **GCP**. Voici une capture d'écran du dashboard Kibana :

![Capture du Dashboard Kibana](lien_capture_kibana)

Pour plus de détails, consultez le [README de la partie Kedro](lien_readme_kedro).

## 8. 💻 Traitement des Données et Utilisation de Google Colab
Certaines données volumineuses ont été traitées avec **Google Colab**, notamment pour les membres de l'équipe ayant des limitations matérielles. Voici une capture d'écran de nos notebooks sur Google Colab ainsi que notre bucket GCP pour le stockage des données et artefacts. Nous utilisons MLflow pour le tracking de nos modèles :

![Capture du Bucket GCP](lien_capture_bucket)

## 9. 🤖 Modèles de Machine Learning
Les données ont été divisées en deux groupes :
1. **Consommation journalière par région avec données météorologiques**.
2. **Consommation journalière et mouvements sociaux** (avec une colonne "mouvement social" indiquant les jours avec des événements).

Ces deux groupes de données ont conduit à deux sous-projets distincts :
- [Sous-projet sur la consommation régionale et les données météo](lien_readme_conso_meteo).
- [Sous-projet sur la consommation et les mouvements sociaux](lien_readme_conso_social).

Ces sous-projets, ainsi que notre interface Streamlit, utilisent **MLflow** pour le suivi et la mise en production des modèles. Un serveur **MLFlow** a été déployé sur une VM GCP pour permettre à l'équipe de suivre les performances des modèles.

## 10. 🖥️ Interface Utilisateur avec Streamlit
L'interface utilisateur finale a été développée avec **Streamlit**. Elle permet :
- Le téléchargement de datasets.
- La visualisation des résultats des modèles de machine learning.
- La collecte de feedbacks utilisateurs.

Cette interface est déployée localement et sur **Streamlit Community**. Pour plus de détails, voir le [README de l’interface Streamlit](lien_readme_streamlit).

## 11. 📊 Ordonnancement des Données avec Airflow
Nous avons documenté plusieurs étapes critiques du projet :
1. **Mise en place d’un serveur MLFlow sur GCP** : [lien_documentation_mlflow]
2. **Mise en place d’un serveur Airflow en local** : [lien_documentation_airflow]
3. **Ordonnancement des Données avec Airflow** : [lien_documentation_airflow]

**Airflow** est utilisé pour orchestrer les pipelines de collecte de données via des DAGs. Un exemple de DAG est utilisé pour enrichir nos datasets avec des données d'API. Ce script Airflow s'exécute chaque jour à 20h pour une durée de 30 minutes. Voici des images de notre DAG et de notre interface Airflow :
