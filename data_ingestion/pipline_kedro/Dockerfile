FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
COPY install_requirements.sh .

RUN chmod +x install_requirements.sh && ./install_requirements.sh

COPY . .

EXPOSE 4141

ENV PATH="/app/.local/bin:${PATH}"



CMD ["kedro", "run"]
