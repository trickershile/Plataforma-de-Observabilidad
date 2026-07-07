# =============================================================================
# Dockerfile - Plataforma Inteligente de Observabilidad IoT (POIA-IoT)
# Basado en python:3.10-slim con Java 11 para soporte PySpark + Delta Lake
# =============================================================================

FROM python:3.10-slim

# -----------------------------------------------------------
# Instalación de Java Runtime (requerido por PySpark)
# -----------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jre-headless \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# -----------------------------------------------------------
# Directorio de trabajo
# -----------------------------------------------------------
WORKDIR /app

# -----------------------------------------------------------
# Copia e instalación de dependencias Python
# -----------------------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------------------------------------
# Instalación de PySpark y Delta Lake
# -----------------------------------------------------------
RUN pip install --no-cache-dir pyspark delta-spark

# -----------------------------------------------------------
# Copia completa del código del proyecto
# -----------------------------------------------------------
COPY . .

# -----------------------------------------------------------
# Puertos: Streamlit (8501), Spark UI (4040), Jupyter (8888)
# -----------------------------------------------------------
EXPOSE 8501 4040 8888

# -----------------------------------------------------------
# Comando por defecto: orquestador de planta
# -----------------------------------------------------------
CMD ["python", "notebooks/orquestador_planta.py"]
