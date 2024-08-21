https://odre.opendatasoft.com/explore/dataset/consommation-nationale-horaire-de-gaz-donnees-provisoires-grtgaz-terega-v2/api/?disjunctive.operateur&sort=date&dataChart=eyJxdWVyaWVzIjpbeyJjaGFydHMiOlt7InR5cGUiOiJjb2x1bW4iLCJmdW5jIjoiU1VNIiwieUF4aXMiOiJjb25zb21tYXRpb25fam91cm5hbGllcmVfbXdoX3BjcyIsInNjaWVudGlmaWNEaXNwbGF5Ijp0cnVlLCJjb2xvciI6InJhbmdlLUFjY2VudCIsInBvc2l0aW9uIjoiY2VudGVyIn1dLCJ4QXhpcyI6ImRhdGUiLCJtYXhwb2ludHMiOiIiLCJ0aW1lc2NhbGUiOiJtb250aCIsInNvcnQiOiIiLCJzZXJpZXNCcmVha2Rvd24iOiJvcGVyYXRldXIiLCJzZXJpZXNCcmVha2Rvd25UaW1lc2NhbGUiOiIiLCJzdGFja2VkIjoiIiwiY29uZmlnIjp7ImRhdGFzZXQiOiJjb25zb21tYXRpb24tbmF0aW9uYWxlLWhvcmFpcmUtZGUtZ2F6LWRvbm5lZXMtcHJvdmlzb2lyZXMtZ3J0Z2F6LXRlcmVnYS12MiIsIm9wdGlvbnMiOnsiZGlzanVuY3RpdmUub3BlcmF0ZXVyIjp0cnVlLCJzb3J0IjoiZGF0ZSJ9fX1dLCJkaXNwbGF5TGVnZW5kIjp0cnVlLCJhbGlnbk1vbnRoIjp0cnVlfQ%3D%3D
https://www.data.gouv.fr/fr/datasets/production-regionale-annuelle-des-energies-renouvelables-2008-a-2021/
https://data.sncf.com/explore/dataset/mouvements-sociaux-depuis-2002/api/?sort=date_de_debut
https://opendata.agenceore.fr/explore/dataset/conso-elec-gaz-annuelle-par-secteur-dactivite-agregee-departement/table/?stage_theme=true
https://data.opendatasoft.com/explore/dataset/prix-des-energies-en-france%40akajoule/table/?dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6InByaXgtZGVzLWVuZXJnaWVzLWVuLWZyYW5jZUBha2Fqb3VsZSIsIm9wdGlvbnMiOnt9fSwiY2hhcnRzIjpbeyJhbGlnbk1vbnRoIjp0cnVlLCJ0eXBlIjoibGluZSIsImZ1bmMiOiJBVkciLCJ5QXhpcyI6ImVsZWNfdHQiLCJzY2llbnRpZmljRGlzcGxheSI6dHJ1ZSwiY29sb3IiOiIjMTQyRTdCIn1dLCJ4QXhpcyI6InBlcmlvZGUiLCJtYXhwb2ludHMiOiIiLCJ0aW1lc2NhbGUiOiJ5ZWFyIiwic29ydCI6IiJ9XSwiZGlzcGxheUxlZ2VuZCI6dHJ1ZSwiYWxpZ25Nb250aCI6dHJ1ZX0%3D
https://odre.opendatasoft.com/explore/dataset/consommation-quotidienne-brute/api/   a y reflechir pas de localité compliqué a analyser
https://data.opendatasoft.com/explore/dataset/consommation-quotidienne-brute-regionale%40reseaux-energies-rte/information/?disjunctive.code_insee_region&disjunctive.region&sort=-date_heure remplacer par celui ci plus pertinanat presence des region et cp



pour le dags airflow etapes : pip install kedro-airflow puisn kedro airflow create

garder
https://data.opendatasoft.com/explore/dataset/consommation-nationale-horaire-de-gaz-donnees-definitives-grtgaz-v2%40reseaux-energies-rte/information/?disjunctive.operateur&sort=date
https://data.opendatasoft.com/explore/dataset/prix-carburants-quotidien%40opendatamef/table/

collection_names1:
  - "csv_mouvements_sociaux"
  - "csv_prix_energies"
  - "csv_prix_carburants"
  - "csv_courbe_de_charge"

columns_to_select:
  -

  -
   -


-

def load_collections(collection_names, db_name, connect_timeout: int = 60000, max_retries: int = 3):
    """
    Charger les collections MongoDB spécifiées et les retourner sous forme de DataFrames.

    Params:
    - collection_names: List of collection names to load from MongoDB.
    - db_name: The name of the MongoDB database.
    - connect_timeout: Connection timeout in milliseconds.
    - max_retries: Number of retries in case the connection to MongoDB fails.

    Returns:
    - List of DataFrames containing the data from the specified collections.
    """
    load_dotenv()

    username = os.getenv('MONGODB_USERNAME')
    password = os.getenv('MONGODB_PASSWORD')
    cluster = os.getenv('MONGODB_CLUSTER')

    mongodb_uri = f"mongodb+srv://{username}:{password}@{cluster}/?appName=Energy&connectTimeoutMS={connect_timeout}"

    # Attempt to connect to MongoDB with retries
    for attempt in range(max_retries):
        try:
            client = MongoClient(mongodb_uri, tls=True, tlsAllowInvalidCertificates=True)
            break  # Exit the loop if the connection is successful
        except Exception as e:
            print(f"Attempt {attempt + 1} to connect to MongoDB failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)  # Wait for 5 seconds before retrying
            else:
                print("All connection attempts failed. Exiting.")
                raise e  # Raise the exception if all retries fail

    try:
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

    except Exception as e:
        print(f"Error when loading collections: {e}")
        raise e  # Raise the exception if something goes wrong after connection


db_name1: "DBEnergy"

collection_names1:
  - "csv_previsions_meteo"
  - "csv_prix_energies"
  - "csv_mouvements_sociaux"

columns_to_select:
  - ["date_et_heure_de_la_prévision", "prevision", "position","date_du_calcul", "2_metre_temperature","minimum_temperature_at_2_metres", "maximum_temperature_at_2_metres","2_metre_relative_humidity", "total_precipitation", "10m_wind_speed","surface_net_solar_radiation", "surface_net_thermal_radiation","surface_solar_radiation_downwards", "surface_latent_heat_flux","surface_sensible_heat_flux", "commune", "nombre_date"]
  - ["période", "source", "électricité", "gaz_naturel"]
  - ["date", "date_de_fin", "motif_exprimé", "nombre_de_grévistes_du_préavis"]