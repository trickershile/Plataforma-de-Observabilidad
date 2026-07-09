FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-21-jre-headless \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir pyspark delta-spark

COPY notebooks/ ./notebooks/
COPY lakehouse/ ./lakehouse/

EXPOSE 8501 4040 8888

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \ 
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501')" || exit 1

CMD ["python", "notebooks/orquestador_planta.py"]
