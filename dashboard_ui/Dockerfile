FROM python:3.9-slim
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
COPY .env .env

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
