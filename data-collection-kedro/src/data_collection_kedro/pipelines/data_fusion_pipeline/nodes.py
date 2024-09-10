"""
This is a boilerplate pipeline 'data_fusion_pipeline'
generated using Kedro 0.19.5
"""
import os
import sys

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, exceptions, helpers
from pymongo import MongoClient


def load_collections(collection_names, db_name, connect_timeout: int = 20000):
    """
    Charger les collections MongoDB spécifiées et les retourner sous forme de DataFrames.
    params ::
        collection_names : List des noms des collections à charger
        db_name : Nom de la base de données MongoDB
        connect_timeout : Délai de connexion en millisecondes
    """

    load_dotenv()

    username = os.getenv("MONGODB_USERNAME")
    password = os.getenv("MONGODB_PASSWORD")
    cluster = os.getenv("MONGODB_CLUSTER")

    mongodb_uri = f"mongodb+srv://{username}:{password}@{cluster}/?appName=Energy&connectTimeoutMS={connect_timeout}"
    client = MongoClient(mongodb_uri, tls=True, tlsAllowInvalidCertificates=True)

    db = client[db_name]
    dataframes = []

    for name in collection_names:
        collection = db[name]
        data = pd.DataFrame(list(collection.find()))
        dataframes.append(data)
        print(f"Collection {name} loaded successfully")
        print(data.head())
        print(data.columns)

    return dataframes


def select_columns(dataframes, columns_to_select):
    """
    Sélectionner les colonnes spécifiques pour chaque DataFrame.
    params ::
        dataframes : List des DataFrames à traiter
        columns_to_select : List des colonnes à sélectionner pour chaque DataFrame
    """

    selected_dataframes = []
    for df, cols in zip(dataframes, columns_to_select):
        print(f"Colonnes disponibles dans le DataFrame: {df.columns}")
        try:
            selected_dataframes.append(df[cols])
        except KeyError as e:
            print(f"Erreur lors de la sélection des colonnes: {e}")
            raise
    return selected_dataframes


def normalize_columns(dataframes):
    """
    Normalise les colonnes avant la fusion des DataFrames.
    Renomme et convertit les colonnes de dates et de régions pour assurer la cohérence.
    params ::
        dataframes : List dataframe à normaliser
    """
    region_mapping = {
        "alsace": "grand est",
        "aquitaine": "nouvelle-aquitaine",
        "ardeche": "auvergne-rhône-alpes",
        "auvergne": "auvergne-rhône-alpes",
        "bourgogne": "bourgogne-franche-comté",
        "franche-comte": "bourgogne-franche-comté",
        "champagne-ardenne": "grand est",
        "corse": "corse",
        "limousin": "nouvelle-aquitaine",
        "languedoc-roussillon": "occitanie",
        "lorraine": "grand est",
        "midi-pyrenees": "occitanie",
        "nord-pas-de-calais": "hauts-de-france",
        "picardie": "hauts-de-france",
        "poitou-charentes": "nouvelle-aquitaine",
        "pays-de-la-loire": "pays de la loire",
        "provence-alpes-c-te-d-azur": "provence-alpes-côte d'azur",
        "ile-de-france": "île-de-france",
        "ile-de-re": "nouvelle-aquitaine",
        "rh-ne-alpes": "auvergne-rhône-alpes",
        "centre": "centre-val de loire",
    }

    for i, df in enumerate(dataframes):
        print(f"Normalisation du DataFrame {i} :")

        # Dataset "Courbe de Charge"
        if "date" in df.columns and "00:00" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            df["région"] = df["région"].astype(str).str.lower().str.strip()
            df = df.fillna(0)
            print(f"type colone region courbe {df['région'].dtypes}")
            print(f"type colone date courbe { df['date'].dtypes}")
            print(df.head())
            print("----------------------------------------------------")
        # Dataset "Mouvements Sociaux"
        elif "date_de_fin" in df.columns:
            df["date"] = pd.to_datetime(df["date_de_debut"])
            df["motif"] = df["motif"].astype(str).str.lower().str.strip()
            df = df.fillna(0)
            df["motif"] = df["motif"].fillna(np.nan)
            print(f"type colone mouvement courbe { df['date'].dtypes}")
            print(df.head())
            print("----------------------------------------------------")
        # Dataset "Météo"
        elif "TempMax_Deg" in df.columns:
            df.rename(columns={"day": "date"}, inplace=True)
            df["date"] = pd.to_datetime(df["date"])
            df.rename(columns={"region": "région"}, inplace=True)
            df["région"] = df["région"].astype(str).str.lower().str.strip()
            df["région"] = df["région"].replace(region_mapping)
            print(f"type colone date meteo { df['date'].dtypes}")
            print(f"type colone region meteo {df['région'].dtypes}")
            df = df.fillna(0)
            print(df.head())

        print(df.head())
        print(df.dtypes)

    return dataframes


def display_dataframes(dataframes):
    """
    Affiche les premières lignes de chaque DataFrame dans la liste donnée.
    params ::
        dataframes : List des DataFrames à afficher
    """
    for i, df in enumerate(dataframes):
        print(f"DataFrame {i+1}:")
        print(df.head())
        print("\n")

    return dataframes


def store_in_elasticsearch(df, es, index_name, chunk_size=500):
    """
    Fonction pour stocker un DataFrame dans Elasticsearch par petits morceaux.
    params ::
        df : DataFrame à stocker
        es : Instance de connexion Elasticsearch
        index_name : Nom de l'index Elasticsearch
        chunk_size : Taille de chaque morceau à insérer dans Elasticsearch
    """
    try:
        # Diviser le DataFrame en plusieurs morceaux (chunks)
        for chunk in np.array_split(df, len(df) // chunk_size + 1):
            actions = [
                {
                    "_index": index_name,
                    "_source": row.to_dict(),
                }
                for _, row in chunk.iterrows()
            ]
            # Utiliser helpers.bulk pour insérer les données en bloc
            helpers.bulk(es, actions)

        print(f"Données insérées avec succès dans l'index Elasticsearch : {index_name}")

    except Exception as e:
        print(
            f"Échec de l'insertion des données dans l'index Elasticsearch {index_name} : {str(e)}"
        )


def create_index(es, index_name):
    """
    Crée un index dans Elasticsearch si celui-ci n'existe pas déjà.
    params ::
        es : Instance de connexion Elasticsearch
        index_name : Nom de l'index à créer
    """
    try:
        if not es.indices.exists(index=index_name):
            es.indices.create(index=index_name)
            print(f"Index '{index_name}' créé avec succès.")
        else:
            print(f"L'index '{index_name}' existe déjà.")
    except Exception as e:
        print(f"Échec de la création de l'index Elasticsearch {index_name} : {str(e)}")


def merge_data_store_in_elastic(dataframes):
    """
    Fusionne les DataFrames pour créer de nouveaux jeux de données et les stocke dans deux index Elasticsearch distincts.
    params ::
        dataframes : List des DataFrames à fusionner
    """

    es_host = os.getenv("ELASTIC_DEPLOYMENT_ENDPOINT")
    es_username = os.getenv("ELASTIC_USERNAME")
    es_password = os.getenv("ELASTIC_PASSWORD")

    if not es_host or not es_username or not es_password:
        raise ValueError(
            "Les informations d'identification Elasticsearch ne sont pas définies dans les variables d'environnement."
        )

    try:
        es = Elasticsearch(
            [es_host],
            http_auth=(es_username, es_password),
        )

        if not es.ping():
            print("Could not connect to Elasticsearch.")
            return
        else:
            print("Connected to Elasticsearch.")

        meteo_courbe_index = "meteo_courbe_indexx"
        courbe_mouvement_index = "courbe_mouvement_indexx"

        # Création index
        create_index(es, meteo_courbe_index)
        create_index(es, courbe_mouvement_index)

        # Chargement des DataFrames
        df_meteo = dataframes[0]
        df_courbe = dataframes[1]
        df_mouvement = dataframes[2]

        # Fusion des DataFrames
        merge_meteo_courbe = pd.merge(
            df_meteo, df_courbe, on=["date", "région"], how="inner"
        )
        merge_meteo_courbe.to_csv("merge_meteo_courbe.csv")
        print(f"Nombre de lignes après fusion meteo-courbe: {len(merge_meteo_courbe)}")

        merge_courbe_mouvement = df_courbe.copy()
        merge_courbe_mouvement["movement_social"] = merge_courbe_mouvement["date"].isin(
            df_mouvement["date"]
        )
        merge_courbe_mouvement = pd.merge(
            merge_courbe_mouvement,
            df_mouvement[["date", "motif"]],
            on="date",
            how="left",
        )
        merge_courbe_mouvement.to_csv("merge_courbe_mouvement.csv")
        print(
            f"Nombre de lignes après fusion courbe-mouvement: {len(merge_courbe_mouvement)}"
        )

        # Remplacement des valeurs NaN par 0 pour certaines colonnes dans merge_meteo_courbe
        merge_meteo_courbe["TempMax_Deg"].fillna(value=0, inplace=True)
        merge_meteo_courbe["TempMin_Deg"].fillna(value=0, inplace=True)
        merge_meteo_courbe["CloudCoverage_percent"].fillna(value=0, inplace=True)

        # Remplacement des valeurs NaN par "inconnu" pour la colonne "motif" dans merge_courbe_mouvement
        merge_courbe_mouvement["motif"].fillna(value="inconnu", inplace=True)

        store_in_elasticsearch(
            merge_meteo_courbe, es, index_name=meteo_courbe_index, chunk_size=500
        )
        store_in_elasticsearch(
            merge_courbe_mouvement,
            es,
            index_name=courbe_mouvement_index,
            chunk_size=500,
        )

        print("----------------------------------------------------")
        print(es.count(index="courbe_mouvement_index")["count"])
        print(es.count(index="meteo_courbe_index")["count"])

    except exceptions.ConnectionError as e:
        print(f"Error connecting to Elasticsearch: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return merge_meteo_courbe, merge_courbe_mouvement
