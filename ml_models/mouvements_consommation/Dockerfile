FROM python:3.9-slim
WORKDIR /app

# Mise à jour de pip avant installation des dépendances
RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt --index-url=https://pypi.org/simple

COPY . .
COPY .env .env

EXPOSE 8501
CMD ["python", "anomaly_detection_energy.py"]
