
# 📊 Modèles de ML pour la Prédiction et la Détection d'Anomalies Énergétiques

### 🔗 Langage
![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)

### 🛠️ Frameworks et Outils de Développement
![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-red?style=for-the-badge&logo=streamlit)
![MLflow](https://img.shields.io/badge/MLflow-v2.16.0-orange?style=for-the-badge&logo=mlflow)

### Empreinte Carbone
![CodeCarbon](https://img.shields.io/badge/CODECARBON-v1.2.0-brightgreen)

### 📊 Machine Learning & Data Science
![KMeans](https://img.shields.io/badge/KMeans-Clustering-yellow?style=for-the-badge)
![DBSCAN](https://img.shields.io/badge/DBSCAN-Clustering-green?style=for-the-badge)
![Isolation Forest](https://img.shields.io/badge/Isolation--Forest-Anomaly%20Detection-lightblue?style=for-the-badge)
![Ridge Regression](https://img.shields.io/badge/Ridge--Regression-Prediction-lightblue?style=for-the-badge)
![Random Forest](https://img.shields.io/badge/Random--Forest-Prediction-lightgreen?style=for-the-badge)

### ☁️ Cloud & Stockage
![Google Cloud Storage](https://img.shields.io/badge/Google%20Cloud%20Storage-2.18.2-orange?style=for-the-badge&logo=googlecloud)

## 📑 Présentation du Projet


Ce projet fait partie de notre solution globale de **détection d'anomalies** dans la consommation énergétique, combinant plusieurs techniques avancées de machine learning. L'application utilise l'algorithme **Isolation Forest** pour identifier les comportements anormaux dans les données. Elle intègre également des méthodes de **clustering**, notamment **K-means** et **DBSCAN**, afin de regrouper les régions en fonction de la similitude de leur consommation énergétique.

Pour la **prédiction de la consommation future**, des modèles de régression tels que **Ridge Regression** et **Random Forest** sont déployés, prenant en compte divers facteurs externes comme les **mouvements sociaux**.

Le suivi et la gestion des modèles sont assurés via **MLflow**, qui permet une traçabilité complète des versions et des performances des modèles. Nous avons choisi de déployer MLflow sur une infrastructure cloud via **Google Cloud Platform (GCP)**, offrant ainsi un accès centralisé et une flexibilité dans la gestion des artefacts. L'URL du serveur MLflow est stockée dans nos fichiers `.env`, facilitant l'accès et l'utilisation de l'outil.


## 📚 Sommaire

1. [📦 Installation](#installation)
2. [🚀 Utilisation de l'Application](#utilisation)
3. [📁 Structure du Projet](#structure-du-projet)
4. [🌍 Calcul empreinte carbone](#empreinte-carbone)
5. [🖼️ Interface Utilisateur](#interface-utilisateur)
6. [📈 Intégration avec MLflow](#intégration-mlflow)
7. [🖼️ Captures d'écran](#captures-d’écran)

## 📦 Installation <a name="installation"></a>

Avant de commencer, assurez-vous d'avoir **Python 3.10+** et les bibliothèques nécessaires installés.

### Étapes d'installation

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

   Créez un fichier `.env` avec les informations suivantes :

   ```env
   GOOGLE_APPLICATION_CREDENTIALS=chemin/vers/credentials.json
   MLFLOW_TRACKING_URI=url-du-suivi-mlflow
   MLFLOW_ARTEFACTS_LOCATION=gs://votre-bucket/mlflow
   ```

## 🚀 Utilisation de l'Application <a name="utilisation"></a>

Pour lancer l'application **Streamlit**, exécutez la commande suivante dans le répertoire racine :

```bash
streamlit run StreamlitUI/app_detection_anomalie.py
```

Vous pouvez également exécuter les autres modules de l'interface Streamlit pour explorer les fonctionnalités spécifiques comme le clustering et la prédiction :

```bash
streamlit run StreamlitUI/app_clustering.py
```

```bash
streamlit run StreamlitUI/app_prediction_conso_mvt.py
```

L'application permet de :

- **Charger des jeux de données** pour analyser la consommation.
- **Lancer la détection d'anomalies** sur des périodes ou des régions spécifiques.
- **Visualiser les clusters et les prédictions** de manière interactive.


## 📁 Structure du Projet <a name="structure-du-projet"></a>

Le projet est organisé de manière modulaire pour garantir une maintenabilité et une évolutivité optimales. Voici la structure principale :

```bash
mouvements_consommation/
├── images/                               # Répertoire contenant des sous-répertoires d'images
│   ├── anomaly_detection/                # Images pour la détection d'anomalies
│   ├── clustering/                       # Images pour le clustering
│   └── prediction_mouvement/             # Images pour la prédiction de mouvements
│   └── other/                            # Autres images
│   └── logs_carbon/                      # Répertoire contenant des sous-répertoires d'images pour les logs de suivi de l'empreinte carbone
│        ├── dbscan/                      # Images logs de carbone pour le modèle DBSCAN
│        ├── isolationforest/             # Images logs de carbone pour le modèle Isolation Forest
│        ├── random_forest/               # Images logs de carbone pour le modèle Random Forest
│        ├── ridge/                       # Images logs de carbone pour le modèle Ridge Regression
│
├── log/                                  # Répertoire pour les logs divers
│   ├── dbscan/                           # Logs pour DBSCAN
│   ├── log_carbon_anomalie/              # Log carbone pour la détection d'anomalies
│   ├── log_carbon_random_forest_model/   # Log carbone pour Random Forest
│   └── log_carbon_ridge_model/           # Log carbone pour Ridge Regression
│
├── mlruns/                               # Répertoire pour les expériences MLflow
├── modele_mouvement_conso/               # Modèles de mouvement de consommation
├── tests_models/                         # Répertoire pour les tests des modèles
│   └── data_test/                        # Jeux de données de test
│
├── anomaly_detection_energy.py           # Détection des anomalies dans la consommation énergétique
├── clustering_model.py                   # Implémentation des modèles de clustering
├── prediction_conso_mvt.py               # Modèle de prédiction de la consommation prenant en compte les mouvements
├── mlflow_utils.py                       # Utilitaires pour MLflow
├── register_model.py                     # Script pour l'enregistrement des modèles
├── .env                                  # Variables d'environnement (non incluses dans le dépôt)
├── requirements.txt                      # Liste des dépendances
└── Readme.md                             # Fichier README

```

## 🌍 Calcul empreinte carbone<a name="empreinte-carbone"></a>

Dans le cadre de ce sous-projet dédié à la **détection d'anomalies** dans la consommation énergétique, nous avons intégré le suivi de l'empreinte carbone à travers **CodeCarbon**. Ce suivi a permis de mesurer l'impact environnemental des différents algorithmes utilisés, tels que **Isolation Forest** pour la détection d'anomalies, et les méthodes de **clustering** comme **K-means** et **DBSCAN**. De plus, des modèles de régression tels que **Ridge Regression** et **Random Forest**, qui prennent en compte des facteurs comme les **mouvements sociaux**, ont été évalués en termes d'émissions de CO2eq lors de leur exécution.

Les résultats de ces suivis sont stockés dans des logs pour analyser et optimiser l'efficacité énergétique de chaque composant.[voir section capture d'écran](#captures-d’écran)


## 🖼️ Interface Utilisateur <a name="interface-utilisateur"></a>

L'interface **Streamlit** permet une interaction directe avec les modèles de machine learning. Voici les principales fonctionnalités :

1. **Détection d'Anomalies** : Détection des anomalies dans les données de consommation énergétique avec **Isolation Forest**.
   - L'utilisateur peut charger des jeux de données, lancer l'algorithme et visualiser les anomalies détectées.
   - Les résultats sont stockés et suivis sur **MLflow**.

2. **Clustering** : L'algorithme de clustering (K-means ou DBSCAN) regroupe les régions par similitudes.
   - Une visualisation des clusters est disponible après l'exécution, avec possibilité de les sauvegarder dans **MLflow**.

3. **Prédiction de la Consommation** : La prédiction de la consommation énergétique est effectuée à l'aide de modèles comme **Ridge Regression** et **Random Forest**.
   - L'utilisateur peut ajuster les hyperparamètres et observer les performances du modèle.


## 📈 Intégration avec MLflow <a name="intégration-mlflow"></a>

**MLflow** est utilisé pour le suivi, la gestion et la comparaison des modèles de machine learning développés dans ce projet. Il enregistre des métriques comme l'**inertie** pour **K-means**, la taille des clusters ou encore le **taux de contamination** pour **Isolation Forest**, permettant ainsi une traçabilité complète des expériences et une optimisation des hyperparamètres.

### Déployer MLflow

#### 1. Utilisation Locale de MLflow

Pour un déploiement local de MLflow, voici les étapes à suivre :

1. **Installer MLflow** :
   ```bash
   pip install mlflow
   ```

2. **Démarrer le serveur MLflow** :
   ```bash
   mlflow ui
   ```

3. **Accéder à l'interface** :
   Rendez-vous sur `http://localhost:5000` pour suivre vos expériences et gérer vos modèles localement.

#### 2. Utilisation de MLflow sur le Cloud (GCP)

Nous avons opté pour une solution cloud avec **Google Cloud Platform (GCP)** pour la gestion centralisée des modèles et des artefacts. L'URL du serveur MLflow est stockée dans les fichiers `.env` pour un accès facile.

Pour configurer MLflow sur GCP :

1. **Créer un bucket Google Cloud** pour stocker les artefacts.
2. **Déployer MLflow sur une instance Compute Engine**.
3. **Configurer les variables d'environnement** pour connecter MLflow au bucket et au serveur.

![Bucket](images/other/bucket.png)
Pour plus de détails sur la mise en place de MLflow sur GCP, consultez le fichier **PDF** dans le répertoire **documentation** :

📄 [Documentation - Mise en place du serveur MLflow sur GCP](https://github.com/keagnon/DetectionAnomalie/blob/grace_clustering_mvt/documentation/etapes_mise_en_place.pdf)

## 🖼️ Captures d'écran <a name="captures-d’écran"></a>

1. **Détection d'Anomalies**

   ![Détection d'anomalies](images/anomaly_detection/im1.png)
   ![Détection d'anomalies](images/anomaly_detection/im2.png)
   ![Détection d'anomalies](images/anomaly_detection/im3.png)
   ![Détection d'anomalies](images/anomaly_detection/im4.png)
   ![Détection d'anomalies](images/anomaly_detection/im5.png)
   ![Détection d'anomalies](images/anomaly_detection/im6.png)
   ![Détection d'anomalies](images/anomaly_detection/im7.png)
   ![Détection d'anomalies](images/anomaly_detection/im8.png)

2. **Clustering**

   ![Clustering](images/clustering/im1.png)
   ![Clustering](images/clustering/im2.png)
   ![Clustering](images/clustering/im3.png)
   ![Clustering](images/clustering/im5.png)
   ![Clustering](images/clustering/im6.png)
   ![Clustering](images/clustering/im7.png)
   ![Clustering](images/clustering/im8.png)
   ![Clustering](images/clustering/im9.png)
   ![Clustering](images/clustering/im10.png)


3. **Prédiction de la consommation prise en compte des mouvements sociaux**

   ![Prédiction de la consommation](images/prediction_mouvement/im1.png)
   ![Prédiction de la consommation](images/prediction_mouvement/im2.png)
   ![Prédiction de la consommation](images/prediction_mouvement/im3.png)
   ![Prédiction de la consommation](images/prediction_mouvement/im4.png)
   ![Prédiction de la consommation](images/prediction_mouvement/im5.png)
   ![Prédiction de la consommation](images/prediction_mouvement/im6.png)
   ![Prédiction de la consommation](images/prediction_mouvement/im7.png)

3. **Empreinte carbone modèle DBSCAN**

   ![dbscan_carbon_tracker](images/logs_carbon/dbscan/dbscan_co2.png)
   ![dbscan_carbon_tracker](images/logs_carbon/dbscan/dbscan_emissions_tracker.png)

3. **Empreinte carbone modèle Ridge**

   ![ridge_carbon_tracker](images/logs_carbon/ridge/ridge_co2.png)

3. **Empreinte carbone modèle Random Forest**

   ![random_forest_carbon_tracker](images/logs_carbon/random_forest/random_forest_co2.png)
   ![random_forest_carbon_tracker](images/logs_carbon/random_forest/random_forest_emissions_tracker1.png)

3. **Empreinte carbone modèle IsolationForest**

   ![isolation_forest_carbon_tracker](images/logs_carbon/isolatioforest/carboneprint_anomalie_detection.png)
   ![isolation_forest_carbon_tracker](images/logs_carbon/isolatioforest/isolation_forest_co2.png)

