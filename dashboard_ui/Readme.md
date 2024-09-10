# 📊 Anomaly Detection Dashboard (Streamlit)

![Python](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0-red?style=for-the-badge&logo=streamlit)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue?style=for-the-badge&logo=docker)
![MLflow](https://img.shields.io/badge/MLflow-Tracking-orange?style=for-the-badge&logo=mlflow)

## 📑 Introduction

Ce projet est le **tableau de bord final** développé avec **Streamlit** qui englobe toutes les fonctionnalités des différents modèles développés dans le cadre de notre projet de **détection d'anomalies**. Ce tableau de bord permet d'interagir avec plusieurs modèles de machine learning et d'observer leurs performances sur différentes tâches.

Cette partie de notre projet de **détection d'anomalies** se concentre sur les aspects suivants :

- 📈 **Détection d'anomalies** pour repérer des comportements anormaux dans les données.
- 🧠 **Clustering** pour grouper les données par région et mieux comprendre les tendances.
- 🔮 **Prédiction de la consommation** d'énergie en prenant en compte les conditions météorologiques et les mouvements sociaux.
- 📝 **Feedback utilisateur** pour améliorer les modèles en continu.
- 🔍 **Suivi des résultats** et des métriques des modèles via **MLflow**.

---

## 📚 Sommaire

1. [📦 Installation](#installation)
2. [🚀 Lancer l'application](#lancer-lapplication)
3. [📊 Fonctionnalités](#fonctionnalités)
   - [🔍 Détection d'anomalies](#détection-danomalies)
   - [🧠 Clustering](#clustering)
   - [🔮 Prédiction de la consommation en prenant en considération les mouvements sociaux](#prédiction-de-la-consommation)
   - [☁️ Prédiction de la cosommation en prenant en compte kes conditions météorologiques](#prédiction-météo)
   - [📝 Feedback utilisateur](#feedback-utilisateur)
   - [📈 Suivi des résultats et des modèles](#suivi-des-résultats-et-des-modèles)
5. [📁 Structure du projet](#structure-du-projet)
6. [🖼️ Captures d'écran](#captures-d’écran)

---

## 📦 Installation

Avant de commencer, assurez-vous d'avoir **Python 3.9+** et **Docker** installés sur votre machine.

### Étapes d'installation :

1. **Clonez ce dépôt :**

   ```bash
   git clone https://github.com/keagnon/DetectionAnomalie.git
   cd DetectionAnomalie
   ```

2. **Installez les dépendances :**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration des variables d'environnement :**

   Créez un fichier `.env` et renseignez les informations de connexion, notamment MongoDB et Elasticsearch :

   ```env
    GOOGLE_APPLICATION_CREDENTIALS=chemin/vers/fichier.json
    MLFLOW_TRACKING_URI=url-de-suivi-mlflow
    MLFLOW_ARTEFACTS_LOCATION=gs://votre-bucket/mlflow_experiment
    AWS_ACCESS_KEY=votre-aws-access-key
    AWS_SECRET_KEY=votre-aws-secret-key
    S3_BUCKET_NAME=bucketfeedbacks
    S3_REGION_NAME=eu-west-3
   ```

---

## 🚀 Lancer l'application

### Localement avec Python :

```bash
streamlit run app.py
```

### Avec Docker ⚙️ :

Le projet est entièrement **dockerisé** pour faciliter le déploiement dans différents environnements.

1. **Construisez l'image Docker :**

   ```bash
   docker build -t anomaly-dashboard .
   ```

2. **Exécutez le conteneur Docker :**

   ```bash
   docker run -p 8501:8501 --env-file .env anomaly-dashboard
   ```

Accédez à l'application via [http://localhost:8501](http://localhost:8501).

---

## 📊 Fonctionnalités

### 🔍 Détection d'anomalies

La section **détection d'anomalies** utilise des modèles comme **Isolation Forest** pour détecter des comportements anormaux dans les données de consommation. Lorsque des données sont chargées via l'interface, un tableau s'affiche avec les données chargées. Les anomalies sont soulignées en rouge.

![Détection d'anomalies](images/anomaly_detection/anomaly1.png)

### 🧠 Clustering

Dans cette section, nous utilisons des algorithmes de clustering tels que **DBSCAN** et **K-means** pour regrouper les données en clusters distincts. L'utilisateur peut charger des données via notre interface, visualiser les clusters et analyser les tendances.

![Clustering](images/clustering/clustering1.png)

### 🔮 Prédiction de la consommation prise en compte des mouvements sociaux

Cette section permet de tester et de visualiser les résultats de différents modèles de prédiction de la consommation énergétique. L'utilisateur peut charger des données, tester les modèles et voir les prédictions sous forme de graphiques interactifs.

![Prédiction de la consommation](images/prediction_conso/mvt1.png)

### ☁️ Prédiction dela consommation prise en compte météo

Similaire à la prédiction de la consommation, cette section utilise des modèles pour prédire les conditions météorologiques et analyser leur impact sur la consommation d'énergie.

![Prédiction météo](images/prediction_conso_meteo/meteo1.png)

### 📝 Feedback utilisateur

Cette section permet aux utilisateurs d'envoyer des retours sur les prédictions et les anomalies détectées. Les retours utilisateurs sont stockés et utilisés pour améliorer les modèles.

![Feedback](images/feedback/feedback1-1.png)

### 📈 Suivi des résultats et des modèles

Le suivi des résultats est effectué avec **MLflow**, qui permet de visualiser les performances des modèles, de comparer les différentes versions, et de suivre l'historique des expériences via une interface dédiée. Au clic sur l'onglet  **Tracking**, vous serez rediriger vers notre serveur Mlflow mis en place pour notre équipe.

![Suivi des résultats](images/tracking/whenclickingMlflowonMenuUI.png)

## 📁 Structure du projet

Voici un aperçu de la structure du projet :

```bash
dashboard_ui/
│
├── app.py                      # Point d'entrée principal pour Streamlit
├── Dockerfile                   # Fichier Docker pour le déploiement
├── requirements.txt             # Dépendances Python
├── .env                         # Fichier des variables d'environnement (non inclus dans Git)
├── styles.css                   # Styles CSS pour l'application
│
├── page_anomalie_detection.py    # Page de détection d'anomalies
├── page_clustering.py            # Page de clustering
├── page_feedback.py              # Page pour les retours utilisateur
├── page_prediction_conso.py      # Page pour les prédictions de consommation
├── page_prediction_meteo.py      # Page pour les prédictions météo
├── page_tracking.py              # Page pour le suivi des résultats avec MLflow
│
├── mlruns/                       # Répertoire de suivi MLflow
└── dashboard_ui_streamlit/        # Fichiers et assets supplémentaires
```

---

## 🖼️ Captures d'écran

1. **Détection d'anomalies**

   ![Détection d'anomalies](images/anomaly_detection/anomaly1.png)
   ![Détection d'anomalies](images/anomaly_detection/anomaly2.png)
   ![Détection d'anomalies](images/anomaly_detection/anomaly3.png)
   ![Détection d'anomalies](images/anomaly_detection/anomaly_mlflow_communication.png)
   ![Détection d'anomalies](images/anomaly_detection/anomaly4.png)
   ![Détection d'anomalies](images/anomaly_detection/anomaly5.png)
   ![Détection d'anomalies](images/anomaly_detection/anomaly6.png)
   ![Détection d'anomalies](images/anomaly_detection/anomaly7.png)

2. **Clustering**

   ![Clustering](images/clustering/clustering1.png)
   ![Clustering](images/clustering/clustering2.png)
   ![Clustering](images/clustering/clustering3.png)
   ![Clustering](images/clustering/clustering_mlflow_communication.png)

3. **Prédiction de la consommation prise en compte des mouvements sociaux**

   ![Prédiction de la consommation](images/prediction_conso/mvt1.png)
   ![Prédiction de la consommation](images/prediction_conso/mvt2.png)

4. **Prédiction de la consommation prise en compte météo**

   ![Prédiction météo](images/prediction_conso_meteo/meteo1.png)

5. **Feedback utilisateur**

   ![Feedback utilisateur](images/feedback/feedback1-1.png)
   ![Feedback utilisateur](images/feedback/feedback1.png)
   ![Feedback utilisateur](images/feedback/feedback2.png)
   ![Feedback utilisateur](images/feedback/feedback3.png)
   ![Feedback utilisateur](images/feedback/feedback_store_aws.png)
   ![Feedback utilisateur](images/feedback/list_feedback_store_aws.png)

6. **Suivi des résultats**

   ![Suivi des résultats](images/tracking/mlflow_trackin.png)
   ![Suivi des résultats](images/tracking/whenclickingMlflowonMenuUI.png)
