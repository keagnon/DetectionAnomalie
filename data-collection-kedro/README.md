# **🚀 Data-collection-kedro - Projet Kedro**

## **Table des matières** 📚
1. [Vue d'ensemble du projet](#vue-densemble-du-projet)
2. [Architecture du projet](#architecture-du-projet)
3. [Installation et configuration](#installation-et-configuration)
4. [Structure du projet](#structure-du-projet)
5. [Exécution du projet](#exécution-du-projet)
6. [Description des pipelines](#description-des-pipelines)
7. [Fichiers de configuration](#fichiers-de-configuration)
8. [Tests du projet](#tests-du-projet)
9. [Contribution](#contribution)
10. [Licence](#licence)

---

## **Vue d'ensemble du projet** 🌍

data-collection-kedro est un projet de pipeline de données construit autour du framework Kedro, utilisé pour automatiser les processus d'extraction, de transformation et de chargement (ETL). Il inclut des fonctionnalités de détection d'anomalies dans des données temporelles et catégoriques, avec stockage dans MongoDB et Elasticsearch.

Le projet se concentre sur l'intégration de données provenant de diverses sources (API, fichiers CSV, XML), leur stockage et leur fusion dans des bases de données.

---

## **Architecture du projet** 🏗️

Le projet suit une architecture modulaire basée sur Kedro, où chaque tâche de traitement de données est encapsulée dans des pipelines distincts pour favoriser la flexibilité et la maintenance.

### **Vue d'ensemble des pipelines :**

- **Pipeline ETL (`etl_pipeline`)** : Extraction, transformation et stockage des données dans MongoDB.
- **Pipeline de Fusion de Données (`data_fusion_pipeline`)** : Fusion et stockage des données dans Elasticsearch.

---

## **Installation et configuration** ⚙️

### **Prérequis :**

- **Python 3.8** ou version plus récente
- **MongoDB** (cloud ou instance locale)
- **Elasticsearch** (cloud ou instance locale)
- **Docker** (optionnel pour containeriser le projet)

### **Étapes d'installation :**

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/votreutilisateur/detectionanomalie.git
   cd detectionanomalie
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

   ELASTIC_USERNAME=nom_utilisateur_elastic
   ELASTIC_PASSWORD=mot_de_passe_elastic
   ELASTIC_DEPLOYMENT_ENDPOINT=adresse_du_cluster_elastic
   ```

---

## **Structure du projet** 🗂️

La structure du projet suit les conventions de Kedro :

```
detectionanomalie/
│
├── data/
│   ├── 01_raw/            # Données brutes
│   ├── 02_intermediate/    # Données intermédiaires
│   ├── 03_primary/         # Données nettoyées
│   └── README.md           # Documentation sur les données
│
├── conf/
│   ├── base/               # Configuration commune à tous les environnements
│   └── local/              # Configuration spécifique à l'environnement local
│
├── src/
│   ├── data_collection_kedro/
│   │   ├── pipelines/      # Définition des pipelines
│   └── __init__.py
│
├── tests/                  # Tests unitaires
│
├── Dockerfile              # Dockerfile pour containeriser le projet
├── pyproject.toml          # Métadonnées et dépendances du projet
└── README.md               # Documentation du projet
```

---

## **Exécution du projet** 🚀

### **Exécuter localement :**

- **Exécuter tous les pipelines :**
   ```bash
   kedro run
   ```

- **Exécuter un pipeline spécifique :**
   ```bash
   kedro run --pipeline=etl_pipeline
   ```

### **Exécuter avec Docker :**

- **Construire l'image Docker :**
   ```bash
   docker build -t kedro-data-engineering .
   ```

- **Exécuter le conteneur Docker :**
   ```bash
   docker run -it kedro-data-engineering
   ```

---

## **Description des pipelines** 🔄

### **Pipeline ETL (`etl_pipeline`)** 🛠️

- **Objectif** : Extraire des données API/CSV, les transformer et les stocker dans MongoDB.
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

---

## **Fichiers de configuration** 🛠️

### **1. `catalog.yml`** :
- Définit les jeux de données, leurs sources et destinations (MongoDB, Elasticsearch).

### **2. `parameters.yml`** :
- Contient les paramètres globaux comme la taille des chunks ou les URL des API.

---

## **Tests du projet** 🧪

Les tests sont réalisés avec **pytest**. Les tests unitaires sont disponibles dans le répertoire `tests/`.

### **Exécuter les tests :**

- **Tous les tests** :
   ```bash
   pytest
   ```

- **Tester un pipeline spécifique** :
   ```bash
   pytest tests/pipelines/etl_pipeline/
   ```

---

## **Exemples d'images** 🖼️

Vous pouvez inclure des captures d'écran des exécutions de vos pipelines, ainsi que des résultats de tests ou du coverage :

### **Exemple d'image - Exécution du pipeline ETL :**

```markdown
![Pipeline ETL](./images/pipeline_etl_execution.png)
```

### **Exemple d'image - Exécution du pipeline de fusion :**

```markdown
![Pipeline de fusion](./images/pipeline_fusion_execution.png)
```

### **Exemple d'image - Tests unitaires et couverture :**

```markdown
![Tests unitaires](./images/test_execution.png)
![Coverage des tests](./images/coverage.png)
```

### **Exemple d'image - Visualisation MongoDB :**

Vous pouvez également ajouter une capture de la base de données MongoDB :

```markdown
![MongoDB](./images/mongodb.png)
```

### **Exemple d'image - Visualisation Elasticsearch :**

De la même manière, ajoutez une capture pour Elasticsearch :

```markdown
![Elasticsearch](./images/elasticsearch.png)
```

> Placez les images dans le répertoire `images/` à la racine du projet.

---

