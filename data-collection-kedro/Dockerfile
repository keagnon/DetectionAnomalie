FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY .env .env

COPY . .
RUN pip install kedro kedro-docker

EXPOSE 5000
CMD ["kedro", "run"]
