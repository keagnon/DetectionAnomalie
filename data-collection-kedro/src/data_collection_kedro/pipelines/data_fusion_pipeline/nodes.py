"""
This is a boilerplate pipeline 'data_fusion_pipeline'
generated using Kedro 0.19.5
"""
from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv
import os

def load_collections(collection_names, db_name,connect_timeout: int = 20000):
    """
    Charger les collections MongoDB spécifiées et les retourner sous forme de DataFrames.
    """
    load_dotenv()

    username = os.getenv('MONGODB_USERNAME')
    password = os.getenv('MONGODB_PASSWORD')
    cluster = os.getenv('MONGODB_CLUSTER')

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


def display_selected_data(dataframes):
    """
    Afficher les premières lignes des DataFrames après sélection des colonnes.
    """
    for i, df in enumerate(dataframes):
        print(f"Affichage des données sélectionnées pour la collection {i+1}:")
        print(df.head())
        print(len(df))
    return dataframes


def normalize_columns(dataframes):
    """
    Normalise les colonnes avant la fusion des DataFrames.
    Renomme et convertit les colonnes de dates et de régions pour assurer la cohérence.
    """
    for i, df in enumerate(dataframes):
        # Dataset "Prix du Carburant"
        if 'début_rupture' in df.columns:
            df['début_rupture'] = pd.to_datetime(df['début_rupture'], format='%Y-%m-%d %H:%M', errors='coerce')
            df['fin_rupture'] = pd.to_datetime(df['fin_rupture'], format='%Y-%m-%d %H:%M', errors='coerce')
            df['date'] = df['début_rupture']
            print(f"DataFrame {i} (Prix du Carburant) après normalisation :")

        # Dataset "Courbe de Charge"
        elif 'date' in df.columns and '00:00' in df.columns:
            df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
            # Renommer la colonne 'Région' en 'région'
            if 'Région' in df.columns:
                df.rename(columns={'Région': 'région'}, inplace=True)
            print(f"DataFrame {i} (Courbe de Charge) après normalisation :")

        # Dataset "Mouvements Sociaux"
        elif 'date_de_fin' in df.columns:
            df['date'] = pd.to_datetime(df['date_de_debut'], format='%Y-%m-%d', errors='coerce')
            df['date_de_fin'] = pd.to_datetime(df['date_de_fin'], format='%Y-%m-%d', errors='coerce')
            print(f"DataFrame {i} (Mouvements Sociaux) après normalisation :")

        # Dataset "Météo"
        elif 'forecast_timestamp' in df.columns:
            df['date'] = pd.to_datetime(df['forecast_timestamp'].apply(lambda x: str(x).split(' ')[0]), format='%Y-%m-%d', errors='coerce')
            df['heure'] = df['forecast_timestamp'].apply(lambda x: ' '.join(str(x).split(' ')[1:]))
            df.rename(columns={'commune': 'région'}, inplace=True)
            print(f"DataFrame {i} (Météo) après normalisation :")
            # Supprimer la colonne forecast_timestamp
            df.drop(columns=['forecast_timestamp'], inplace=True)

        # Remplacer NaT par une date par défaut
        df['date'].fillna(pd.Timestamp('1970-01-01'), inplace=True)

        # Afficher les lignes avec des erreurs de conversion
        if df['date'].isnull().any():
            print(f"Warning: Null values encountered in 'date' column after conversion in DataFrame {i}.")
            print(df[df['date'].isnull()])

        # Afficher les premières lignes et les types de données après normalisation
        print(df.head())
        print(df.dtypes)

    return dataframes


def display_dataframes(dataframes):
    """
    Affiche les premières lignes de chaque DataFrame dans la liste donnée.
    """
    for i, df in enumerate(dataframes):
        print(f"DataFrame {i+1}:")
        print(df.head())
        print("\n")

    return dataframes

def merge_data(dataframes):
    # Charger les 1000 premières lignes de chaque DataFrame
    df_carburant = dataframes[0].head(1000)
    df_meteo = dataframes[1].head(1000)
    df_courbe = dataframes[2].head(1000)
    df_mouvement = dataframes[3].head(1000)
    print(f"les colones du dataset carburant {df_carburant.columns}")
    print(f"les colones du dataset meteo {df_meteo.columns}")
    print(f"les colones du dataset courbe {df_courbe.columns}")
    print(f"les colones du dataset mouvement {df_mouvement.columns}")

    # # Étape 1 : Ajouter l'indicateur de mouvement social au DataFrame météo
    # df_meteo['movement_social'] = df_meteo['date'].isin(df_mouvement['date'])
    # print("Indicateur de mouvement social ajouté à la météo :")
    # print(df_meteo.head())
    # print(len(df_meteo))
    # print(df_meteo.columns)

    return df_courbe


def display_final_dataframe(dataframe):
    """
    Affiche les premières lignes du DataFrame final fusionné.
    """
    print("DataFrame Final Fusionné :")
    print(dataframe.head())
    return dataframe


def store_in_mongodb(data: pd.DataFrame, db_name: str, collection_name: str) -> None:
    """
    Store the cleaned data in MongoDB.
    """
    load_dotenv()

    username = os.getenv('MONGODB_USERNAME')
    password = os.getenv('MONGODB_PASSWORD')
    cluster = os.getenv('MONGODB_CLUSTER')

    mongodb_uri = f"mongodb+srv://{username}:{password}@{cluster}/?appName=Energy"
    try:
        client = MongoClient(mongodb_uri, tls=True, tlsAllowInvalidCertificates=True)
        db = client[db_name]
        collection = db[collection_name]

        if isinstance(data, pd.DataFrame):
            data = data.to_dict('records')

        collection.insert_many(data)
        print(f"{len(data)} records stored successfully in {collection_name}.")
    except Exception as e:
        print(f"Error when inserting data: {e}")

