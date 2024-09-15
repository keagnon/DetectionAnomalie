
import json
import boto3
import streamlit as st
from datetime import datetime
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, InvalidRegionError

def load_aws_config(config_file=r'scripts/aws_config.json'):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

aws_config = load_aws_config()
AWS_ACCESS_KEY = aws_config['aws_access_key_id']
AWS_SECRET_KEY = aws_config['aws_secret_access_key']
S3_BUCKET_NAME = 'bucketfeedbacks'  
S3_REGION_NAME = aws_config['region_name']

# Initialisation du client S3 avec boto3.client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=S3_REGION_NAME
)

def upload_feedback_to_s3(username, feedback):
    """
    Fonction pour envoyer les données de feedback au compartiment S3
    ::params
        username: str : Nom d'utilisateur
        feedback: str : Feedback de l'utilisateur
    """

    try:
        # Création d'un nom de fichier basé sur le nom d'utilisateur et la date
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f'{username}_{timestamp}.txt'

        content = f"Nom d'utilisateur: {username}\nFeedback: {feedback}"
        
        # Envoie du fichier au compartiment S3
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=file_name,
            Body=content,
            ContentType='text/plain'
        )
        
        st.success('Feedback envoyé avec succès !')
    except NoCredentialsError:
        st.error("Aucune information d'identification fournie.")
    except PartialCredentialsError:
        st.error("Informations d'identification partielles fournies.")
    except InvalidRegionError:
        st.error(f"Nom de région invalide : {S3_REGION_NAME}")
    except Exception as e:
        st.error(f"Une erreur s'est produite : {e}")

# Interface utilisateur avec Streamlit
st.title('Formulaire de Feedback')
username = st.text_input('Nom d\'utilisateur')
feedback = st.text_area('Votre feedback')

if st.button('Envoyer'):
    if username and feedback:
        upload_feedback_to_s3(username, feedback)
    else:
        st.error("Veuillez remplir tous les champs.")