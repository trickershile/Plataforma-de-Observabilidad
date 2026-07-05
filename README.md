# Plataforma de Observabilidad e IA para IoT Industrial (POIA-IoT)

POIA-IoT es una plataforma de observabilidad a nivel de **Data Lakehouse** orientada a la ingesta masiva, limpieza automatizada transaccional (ACID) y modelado predictivo de telemetría proveniente de activos industriales críticos. Utiliza un algoritmo no supervisado (*Isolation Forest*) para aislar desviaciones térmicas y de vibración en tiempo real, notificando automáticamente fallas críticas a los ingenieros de planta.

---


##  Arquitectura y Flujo de Datos (Patrón Medallion)

La plataforma procesa ráfagas continuas de datos a través de una arquitectura multi-capa optimizada:

1. **Capa Bronze (Ingesta Cruda):** El simulador de sensores genera archivos JSON inmutables con lecturas de temperatura, voltaje y vibración en `lakehouse/bronze/`.
2. **Capa Silver (Limpieza Transaccional):** Apache Spark de-duplica marcas de tiempo y aplica funciones de ventana analíticas para imputar valores nulos de forma inteligente, persistiendo los datos con tolerancia a fallos en formato **Delta Lake** (`lakehouse/silver/`).
3. **Capa Gold (Features e IA):** Se consolida la ingeniería de características en formato Parquet (`lakehouse/gold/`) donde el modelo entrenado segmenta y etiqueta las anomalías mecánicas.

---

##  Estructura del Repositorio



📁 Plataforma-Observabilidad-IoT/
├── 📄 docker-compose.yml         # Infraestructura como Código (IaC) de la plataforma
├── 📄 README.md                  # Documentación principal del sistema
├── 📁 notebooks/                 # Scripts de orquestación, procesamiento y visualización
│   ├── 📄 orquestador_planta.py  # Centralizador secuencial del flujo de datos y alertas
│   ├── 📄 pipeline_silver.ipynb  # ETL transaccional y cálculo de KPIs en PySpark
│   ├── 📄 pipeline_gold.ipynb    # Agregación temporal e ingeniería de características
│   └── 📄 app_dashboard.py       # Frontend interactivo unificado en Streamlit
└── 📁 lakehouse/                 # Volúmenes locales persistentes del Lakehouse
    ├── 📁 bronze/                # Repositorio inmutable de telemetría cruda (.json)
    ├── 📁 silver/                # Tabla Delta Lake optimizada (telemetry_clean)
    └── 📁 gold/                  # Características y predicciones listas para la IA

    
##  Estrategia de KPIs DataOps Implementados
La salud operativa del pipeline y la confianza del modelo de Inteligencia Artificial se auditan programáticamente mediante 4 métricas clave:

DER (Tasa de Error de Datos): Porcentaje de JSONs corruptos o nulos recibidos. Umbral crítico: < 1.5%.

PL (Latencia del Pipeline): Tiempo físico de procesamiento extremo a extremo. Umbral óptimo: < 5 segundos.

DCR (Tasa de Completitud): Éxito de la restauración matemática de nulos en Spark. Objetivo: ≥ 99.8%.

Score F1 (Rendimiento de IA): Balance de precisión del algoritmo Isolation Forest. Umbral aprobado: > 85%.

##  Guía de Instalación y Despliegue Local
Requisitos Previos
Tener instalado Docker y Docker Compose.

Conexión a internet (para la descarga inicial de las imágenes contenerizadas).

## Paso 1: Levantar la Infraestructura Aislada
Clona el repositorio en tu máquina local, navega hasta la raíz del proyecto y ejecuta el entorno contenerizado en segundo plano:


docker-compose up -d
Este comando descargará e inicializará el stack tecnológico, configurando los entornos de Apache Spark, Delta Lake, Jupyter Lab y la interfaz web sin generar conflictos con tus librerías locales.

## Paso 2: Ejecución del Orquestador Automático
El contenedor ejecuta automáticamente el script orquestador_planta.py al iniciar. Si deseas forzar un nuevo ciclo de captura, limpieza e inferencia de la IA de forma manual, corre:


docker exec -it spark_delta_lakehouse python /home/jovyan/work/notebooks/orquestador_planta.py
El orquestador registrará los tiempos del pipeline (KPI PL), actualizará las bitácoras de calidad (KPI DER) y disparará un Webhook directo a Discord si localiza fallas mecánicas.


## Paso 3: Acceder a las Interfaces de Control
Una vez levantado el contenedor, puedes interactuar con el sistema a través de tu navegador web:

Panel de Control Global (Streamlit): Accede a http://localhost:8501 para visualizar gráficos interactivos en tiempo real, tablas de auditoría y la pestaña de Gobierno de Datos con todas las métricas DataOps.

IDE de Ingeniería (Jupyter Lab): Accede a http://localhost:8888 para explorar y modificar el código de los notebooks directamente.

Consola de Spark (Spark UI): Monitoriza el rendimiento de los grafos acíclicos directos (DAGs) de tus consultas distribuidas en http://localhost:4040.

##  Seguridad, Gobierno y Cumplimiento (EU AI Act)
Trazabilidad Histórica: Gracias al Transaction Log de la arquitectura Delta Lake, cualquier ingeniero de la planta puede realizar consultas retrospectivas (VERSION AS OF), garantizando auditoría completa del linaje de datos.

Cumplimiento Regulatorio: Al actuar sobre infraestructura industrial crítica, este sistema ha sido diseñado bajo los lineamientos para Sistemas de IA de Alto Riesgo de la Ley de Inteligencia Artificial de la Unión Europea, implementando bitácoras de calidad automatizadas y un panel web explícito para la supervisión humana directa.

Desarrollado con fines académicos y de producción bajo estándares de MLOps y DataOps. Autor: Víctor Manuel Garay Soto — Duoc UC

Diseñado para democratizar la Inteligencia Artificial industrial. Desarrollado por Víctor Manuel Garay Soto — Duoc UC. Para soporte técnico, contactar al administrador del sistema.
