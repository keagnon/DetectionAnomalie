# **🚀 Projet Kedro : Mise en place des pipelines de données**

### Langage

![Python](https://img.shields.io/badge/Python-3.11.5-blue?style=for-the-badge&logo=python)

### Frameworks et Outils de Développement

![Kedro](https://img.shields.io/badge/Kedro-0.19.8-green?style=for-the-badge&logo=kedro)
![Dynaconf](https://img.shields.io/badge/Dynaconf-3.2.6-yellow?style=for-the-badge&logo=python)
![Jinja2](https://img.shields.io/badge/Jinja2-3.1.4-red?style=for-the-badge&logo=jinja2)
![Pre-commit Hooks](https://img.shields.io/badge/Pre--commit--hooks-4.6.0-blue?style=for-the-badge&logo=pre-commit)
![GitPython](https://img.shields.io/badge/GitPython-3.1.43-orange?style=for-the-badge&logo=git)
![Cookiecutter](https://img.shields.io/badge/Cookiecutter-2.6.0-green?style=for-the-badge&logo=cookiecutter)

### Empreinte Carbone

![CodeCarbon](https://img.shields.io/badge/CODECARBON-v1.2.0-brightgreen)


### Cloud & Bases de Données

![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.15.0-005571?style=for-the-badge&logo=elasticsearch)
![Pymongo](https://img.shields.io/badge/Pymongo-4.8.0-darkgreen?style=for-the-badge&logo=mongodb)
![Dynaconf](https://img.shields.io/badge/Dynaconf-3.2.6-orange?style=for-the-badge&logo=python)

### Bibliothèques de Données & Machine Learning

![Pandas](https://img.shields.io/badge/Pandas-2.2.2-green?style=for-the-badge&logo=pandas)
![Numpy](https://img.shields.io/badge/Numpy-2.1.0-blue?style=for-the-badge&logo=numpy)
![Fsspec](https://img.shields.io/badge/Fsspec-2024.6.1-lightblue?style=for-the-badge&logo=python)
![Matplotlib](https://img.shields.io/badge/Matplotlib--inline-0.1.7-blue?style=for-the-badge&logo=python)

### Outils de Débogage et de Terminal

![IPython](https://img.shields.io/badge/IPython-8.27.0-lightgrey?style=for-the-badge&logo=ipython)
![Rich](https://img.shields.io/badge/Rich-13.8.0-blue?style=for-the-badge&logo=rich)
![Pygments](https://img.shields.io/badge/Pygments-2.18.0-yellow?style=for-the-badge&logo=python)
![Prompt_toolkit](https://img.shields.io/badge/Prompt--Toolkit-3.0.47-lightgrey?style=for-the-badge&logo=python)


## **Table des matières** 📚
1. [🌍 Vue d'ensemble du projet](#vue-densemble-du-projet)
2. [🏗️ Architecture du projet](#architecture-du-projet)
3. [⚙️ Installation et configuration](#installation-et-configuration)
4. [🗂️ Structure du projet](#structure-du-projet)
5. [🌍 Empreinte Carbone](#empreinte_carbone)
6. [🚀 Exécution du projet](#exécution-du-projet)
7. [🔄 Description des pipelines](#description-des-pipelines)
8. [📊 Visualisation des données brutes collectées](#visualisation-des-données-brutes-collectées)
9. [🛠️ Fichiers de configuration](#fichiers-de-configuration)
10. [🧪 Tests du projet](#tests-du-projet)
11. [🖼️ Exemples d'images](#exemples-dimages)


## **Vue d'ensemble du projet** 🌍 <a name="vue-densemble-du-projet"></a>

`Data-collection-kedro` est un projet de pipeline de données construit autour du framework Kedro, utilisé pour automatiser les processus d'extraction, de transformation et de chargement (ETL). Il est inclure dans notre projet de détection d'anomalies dans des données temporelles et catégoriques, avec stockage des données dans MongoDB et Elasticsearch.

Le projet se concentre sur l'intégration de données provenant de diverses sources (API, fichiers CSV, XML), leur stockage et leur fusion dans des bases de données.
**Une fonctionnalité clé** du projet est le **suivi de l'empreinte carbone** des opérations de traitement, réalisé à l'aide de la bibliothèque **CodeCarbon**. Cela permet de mesurer l'impact environnemental des pipelines de données à chaque exécution, contribuant ainsi à un développement plus durable.

## **Architecture du projet** 🏗️ <a name="architecture-du-projet"></a>

Ce sous-projet suit une architecture modulaire basée sur Kedro, où chaque tâche de traitement de données est encapsulée dans des pipelines distincts pour favoriser la flexibilité et la maintenance.


### **Vue d'ensemble des pipelines :**

- **Pipeline ETL (`etl_pipeline`)** : Extraction, transformation et stockage des données dans MongoDB.
- **Pipeline de Fusion de Données (`data_fusion_pipeline`)** : Fusion et stockage des données dans Elasticsearch.

## **Installation et configuration** ⚙️ <a name="installation-et-configuration"></a>

### **Prérequis :**

- **Python 3.8** ou version plus récente
- **MongoDB** (cloud ou instance locale)
- **Elasticsearch** (cloud ou instance locale)
- **Docker** (optionnel pour containeriser le projet)

### **Étapes d'installation :**

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/keagnon/DetectionAnomalie.git
   cd DetectionAnomalie
   ```

2. **Créer un environnement virtuel :**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Unix
   # Ou
   venv\Scripts\activate     # Windows
   ```

3. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement :**
   Créez un fichier `.env` et renseignez les informations de connexion MongoDB et Elasticsearch :
   ```env
   MONGODB_USERNAME=nom_utilisateur_mongo
   MONGODB_PASSWORD=mot_de_passe_mongo
   MONGODB_CLUSTER=adresse_du_cluster_mongo
   MONGODB_DBNAME=nom_base_de_donnée

   ELASTIC_USERNAME=nom_utilisateur_elastic
   ELASTIC_PASSWORD=mot_de_passe_elastic
   ELASTIC_DEPLOYMENT_ENDPOINT=adresse_du_cluster_elastic
   ```

## **Structure du projet** 🗂️ <a name="structure-du-projet"></a>

La structure du projet suit les conventions de Kedro :

```
data-collection-kedro/
│
├── conf/                                # Fichiers de configuration
│   ├── base/
│   │   ├── catalog.yml                  # Définition des jeux de données et leurs emplacements
│   │   ├── parameters_data_fusion_pipeline.yml
│   │   ├── parameters_etl_pipeline.yml
│   │   └── parameters.yml               # Paramètres globaux du projet
│   └── local/                           # Configuration spécifique à l'environnement local
│
├── data/                                # Données utilisées dans le projet
│   ├── data_carburant_xml/
│   ├── data_merge/
│   ├── meteo/
│   │   ├── combined_meteo_data.csv
│   │   ├── courbe_de_charge_data_2018_2024.csv
│   │   ├── meteo_data_2018_2024.csv
│   │   ├── movement_data_2018_2024.csv
│   │   └── prix_du_carburant_data_2018_2024.csv
│   └── README.md                       # Documentation sur les données
│
├── images/                             # Captures d'écran
│   ├── data_fusion/
│   ├── elastic_search/
│   ├── etl_pipeline/
│   └── tests_unitaires/
│
├── logs/                               # Dossier de logs pour l'empreinte carbone et autres logs
│   ├── log_data_fusion_pipeline/       # Logs générés par CodeCarbon lors de l'exécution de la pipeline data fusion pipeline
│   │   ├── emissions.csv               # Fichier CSV contenant les émissions de carbone
│   ├── logs_etl_pipeline/              # Logs générés par CodeCarbon lors de l'exécution de la pipeline ETL pipeline
│   │   ├── emissions.csv               # Fichier CSV contenant les émissions de carbone
│
├── kedro-dataeng-env/                   # Environnement virtuel Kedro
│
├── src/
│   ├── data_collection_kedro/           # Répertoire principal des sources du projet
│   │   ├── pipelines/                   # Pipelines de traitement des données
│   │   │   ├── data_fusion_pipeline/
│   │   │   │   ├── nodes.py             # Fonctions spécifiques au pipeline de fusion de données
│   │   │   │   ├── pipeline.py          # Définition des pipelines
│   │   │   ├── etl_pipeline/
│   │   │   │   ├── nodes.py             # Fonctions spécifiques au pipeline ETL
│   │   │   │   ├── pipeline.py          # Définition de la pipeline ETL
│   │   └── pipeline_registry.py         # Enregistrement des pipelines Kedro
│
├── tests/                               # Tests unitaires pour le projet
│   ├── pipelines/
│   │   ├── data_fusion_pipeline/
│   │   │   ├── test_pipeline.py         # Tests pour le pipeline de fusion de données
│   │   ├── etl_pipeline/
│   │   │   ├── test_pipeline.py         # Tests pour le pipeline ETL
│   │   │   ├── test_transform.py        # Tests pour les transformations de données ETL
│
├── Dockerfile                           # Fichier Docker pour containeriser le projet
├── pyproject.toml                       # Fichier de configuration du projet et des dépendances
├── README.md                            # Documentation principale du projet
└── requirements.txt                     # Liste des dépendances Python du projet

```

## **Empreinte Carbone** 🌍  <a name="empreinte_carbone"></a>

Pour ce projet de collecte de données avec Kedro, nous avons utilisé la bibliothèque **CodeCarbon** pour suivre l'empreinte carbone des pipelines, comme **data_fusion** et **etl_pipeline**. Les résultats sont stockés dans le dossier **logs**, offrant une vue détaillée des émissions de CO2eq générées par chaque traitement.

### Résultats de l'Empreinte Carbone :

![Empreinte Carbone dans le Terminal](images/carbon_logs/etl_pipeline/im3.png)
![Empreinte Carbone dans le Terminal](images/carbon_logs/data_fusion/data_fusion_pipeline_co2_3.png)

## **Exécution du projet** 🚀 <a name="exécution-du-projet"></a>

### **Exécuter localement :**

- **Exécuter tous les pipelines :**
   ```bash
   kedro run
   ```

- **Exécuter un pipeline spécifique :**
   - **Pipeline ETL** :
     ```bash
     kedro run --pipeline=etl_pipeline
     ```

   - **Pipeline de Fusion de Données** :
     ```bash
     kedro run --pipeline=data_fusion_pipeline
     ```

---

### **Exécuter avec Docker :**

- **Construire l'image Docker :**
   ```bash
   docker build -t kedro-data-engineering .
   ```

- **Exécuter le conteneur Docker :**
   ```bash
   docker run -it kedro-data-engineering
   ```


## **Description des pipelines** 🔄 <a name="description-des-pipelines"></a>

### **Pipeline ETL (`etl_pipeline`)** 🛠️

- **Objectif** : Extraire des données API/CSV/XML, les transformer et les stocker dans MongoDB.
- **Fonctions principales** :
  - `fetch_data_from_api()`
  - `read_csv_file()`
  - `store_in_mongodb()`

### **Pipeline de Fusion de Données (`data_fusion_pipeline`)** 🔗

- **Objectif** : Fusionner plusieurs jeux de données, normaliser les colonnes et les stocker dans Elasticsearch.
- **Fonctions principales** :
  - `load_collections()`
  - `select_columns()`
  - `normalize_columns()`
  - `merge_data_store_in_elastic()`


## **Visualisation des données brutes collectées** 🔄 <a name="visualisation-des-données-brutes-collectées"></a>

Les données brutes stockées dans Elasticsearch sont visualisées dans un tableau de bord **Kibana** hébergé sur une machine virtuelle **GCP**. Voici une capture d'écran du dashboard Kibana :

![Capture du Dashboard Kibana](images/dashboard_kibana/donnee_brute_kibana.png)

Les trois premiers graphiques montrent comment la consommation d'énergie varie en fonction des régions et des saisons, influencée par les conditions météorologiques, tandis que les deux derniers mettent en lumière l'impact des mouvements sociaux sur la baisse de la consommation énergétique.

### 1. **Consommation énergétique par région (2018-2024)** (Graphique en haut à gauche)
   Ce graphique représente l'évolution de la **consommation énergétique cumulée par région** sur la période 2018-2024. Les pics de consommation semblent être saisonniers, avec des hausses notables en hiver, ce qui peut indiquer une corrélation avec les basses températures et une demande accrue de chauffage. On observe également une légère baisse vers 2021, ce qui pourrait coïncider avec une réduction d'activité économique, peut-être liée aux restrictions sanitaires.

### 2. **Répartition de la consommation énergétique par région** (Diagramme circulaire au centre)
   Ce diagramme montre la part de la **consommation énergétique par région**. La **région Île-de-France** domine avec environ **30,88 %** de la consommation totale, suivie de **Auvergne-Rhône-Alpes** (18,47 %) et des **Hauts-de-France** (17,4 %). Cela reflète les différences régionales en termes de densité de population et d'activité économique.

### 3. **Évolution de la consommation énergétique et des températures minimales** (Graphique à droite)
   Ce tableau liste les **dates et les températures minimales** par opérateur avec les moyennes de consommation journalière. Il permet de comparer l'impact des variations météorologiques (températures basses) sur la consommation d'énergie, mais les colonnes de température semblent vides ici, ce qui pourrait indiquer des données manquantes ou non disponibles à cette étape.

### 4. **Graphique comparatif entre les jours avec et sans mouvement social** (Graphique en bas à gauche)
   Ce graphique illustre l'impact des **mouvements sociaux** sur la consommation énergétique. On observe que les jours avec des mouvements sociaux (barres bleues) entraînent une baisse notable de la consommation d'énergie dans plusieurs régions. Cela suggère une perturbation des activités économiques, probablement due à des grèves ou des manifestations.

### 5. **Série temporelle des consommations journalières et horaires** (Graphique en bas à droite)
   Ce graphique montre une **série temporelle** comparant les jours avec mouvements sociaux (en bleu foncé) et sans mouvements sociaux (en vert). La tendance générale indique que la consommation énergétique est plus faible pendant les périodes de mouvements sociaux, avec des pics réguliers sans ces mouvements. Cela confirme l'impact des perturbations sociales sur la consommation énergétique.

## **Fichiers de configuration** 🛠️ <a name="fichiers-de-configuration"></a>

### **1. `parameters_data_fusion_pipeline.yml`** :
- Définit les jeux de données, leurs sources et destinations (MongoDB, Elasticsearch).

### **2. `parameters_etl_pipeline.yml`** :
- Contient les paramètres globaux comme la taille des chunks ou les URL des API.


## **Tests du projet** 🧪 <a name="tests-du-projet"></a>

Les tests sont réalisés avec **pytest**. Les tests unitaires sont disponibles dans le répertoire `tests/`.

### **Exécuter les tests :**

- **Tous les tests** :
   ```bash
   pytest tests/
   ```

- **Tester un pipeline spécifique** :
   ```bash
   pytest tests/pipelines/etl_pipeline/
   ```

## **Exemples d'images** 🖼️ <a name="exemples-dimages"></a>

Ici vous trouverez les captures d'écran des exécutions de nos pipelines, ainsi que des résultats de tests ou du coverage.


### **Exemple d'image - Tests unitaires et couverture :**

![Tests unitaires](images/tests_unitaires/im1.png)


### **Exemple d'image - Visualisation MongoDB :**

![MongoDB](images/mongodb/im1.png)
![MongoDB](images/mongodb/im2.png)
![MongoDB](images/mongodb/im3.png)
![MongoDB](images/mongodb/im4.png)

### **Exemple d'image - Exécution du pipeline ETL :**

![Pipeline ETL](images/etl_pipeline/im1.png)
![Pipeline ETL](images/etl_pipeline/im2.png)
![Pipeline ETL](images/etl_pipeline/im3.png)
![Pipeline ETL](images/etl_pipeline/im4.png)
![Pipeline ETL](images/etl_pipeline/im5.png)


### **Exemple d'image - Visualisation Elasticsearch :**

![Elasticsearch](images/elastic_search/im1.png)
![Elasticsearch](images/elastic_search/im2.png)
![Elasticsearch](images/elastic_search/im4.png)
![Elasticsearch](images/elastic_search/im5.png)
![Elasticsearch](images/elastic_search/im7.png)

### **Exemple d'image - Exécution du pipeline de fusion :**

![Pipeline de fusion](images/data_fusion/im1.png)
![Pipeline de fusion](images/data_fusion/im2.png)
![Pipeline de fusion](images/data_fusion/im3.png)
![Pipeline de fusion](images/data_fusion/im4.png)
![Pipeline de fusion](images/data_fusion/im6.png)

### **Exemple d'image - Empreinte carbone tracking pipeline ETL:**

![Empreinte carbone](images/carbon_logs/data_fusion/data_fusion_pipeline_co2_1.png)
![Empreinte carbone](images/carbon_logs/data_fusion/data_fusion_pipeline_co2_2.png)
![Empreinte carbone](images/carbon_logs/data_fusion/data_fusion_pipeline_co2_3.png)

### **Exemple d'image - Empreinte carbone tracking pipeline Data fusion:**

![Empreinte carbone](images/carbon_logs/etl_pipeline/im1.png)
![Empreinte carbone](images/carbon_logs/etl_pipeline/im2.png)
![Empreinte carbone](images/carbon_logs/etl_pipeline/im3.png)
![Empreinte carbone](images/data_fusion/im7.png)
