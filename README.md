# 📊 Plataforma Inteligente de Observabilidad IoT (POIA-IoT)

Bienvenido a la **Plataforma POIA-IoT**. Este sistema automatizado recolecta los datos de los sensores de maquinaria pesada de la planta y utiliza Inteligencia Artificial (*Isolation Forest*) para **predecir y aislar fallas mecánicas antes de que ocurran**, previniendo detenciones críticas de producción.

**No necesitas saber programar ni escribir código para usarla.** Toda la ingeniería compleja corre en el fondo de forma transparente y tú interactúas con una interfaz visual amigable desde tu navegador web.

---

## 💾 Arquitectura y Flujo de Datos (Patrón Medallion)

El sistema opera de forma automática simulando el recorrido de los materiales en una fábrica física, organizando la información en tres etapas protegidas:

1. **Capa Bronze (Ingesta Cruda):** Recibe las ráfagas directamente de las máquinas y guarda los archivos JSON inmutables en `lakehouse/bronze/`.
2. **Capa Silver (Filtro Limpiador):** El motor Apache Spark borra datos repetidos y rellena de forma automática los valores perdidos o nulos. Toda la información queda resguardada bajo la seguridad de una tabla **Delta Lake** (`lakehouse/silver/`).
3. **Capa Gold (Cerebro IA):** Extrae las métricas analíticas calculadas en formato Parquet (`lakehouse/gold/`), donde el algoritmo de Inteligencia Artificial evalúa y etiqueta si las variaciones de temperatura o vibración corresponden a una falla real.

---

## 📁 Estructura del Repositorio (Organización del Proyecto)

Para mantener el orden de la planta digital, los archivos están estrictamente clasificados en carpetas independientes. **No debes mover los archivos de su lugar asignado**, ya que el sistema operativo depende de este orden para no fallar:

```
📁 Plataforma-Observabilidad-IoT/  <-- Carpeta principal del proyecto
│
├── 📁 .github/                   # [DEVOPS] Automatización del ciclo de vida del software
│   └── 📁 workflows/
│       └── 📄 ci-cd.yml          # Flujo de automatización para pruebas, calidad y seguridad
│
├── 📁 k8s/                       # [INFRAESTRUCTURA] Manifiestos de orquestación cloud
│   ├── 📄 deployment.yml         # Configuración de réplicas, límites de hardware y salud
│   └── 📄 istio-telemetry.yml    # Inyección de telemetría automática en la malla de servicios
│
├── 📁 tests/                     # [CALIDAD] Pruebas unitarias automatizadas (pytest)
│   ├── 📄 test_orquestador.py    # Tests del orquestador de planta
│   ├── 📄 test_dashboard.py      # Tests del dashboard Streamlit
│   └── 📄 test_dockerfile.py     # Tests de infraestructura (Dockerfile, K8s)
│
├── 📄 docker-compose.yml         # El "botón de encendido" que levanta toda la planta digital local.
├── 📄 Dockerfile                 # Receta de construcción de la imagen de contenedor optimizada
├── 📄 requirements.txt           # Librerías y dependencias técnicas del ecosistema
├── 📄 .gitignore                 # Exclusiones de control de versiones
└── 📄 README.md                  # Este manual de instrucciones que estás leyendo.
│
├── 📁 notebooks/                 # [CEREBRO ANALÍTICO] Códigos de control y pantallas visuales
│   ├── 📄 orquestador_planta.py  # El piloto automático: corre los procesos en orden y envía alertas.
│   ├── 📄 pipeline_silver.ipynb  # El filtro limpiador: corrige errores de sensores en Apache Spark.
│   ├── 📄 pipeline_gold.ipynb    # El calculador: genera las métricas y características para la IA.
│   ├── 📄 ia_model.ipynb         # Isolation Forest: entrena y evalúa la detección de anomalías
│   └── 📄 app_dashboard.py       # La interfaz web: la pantalla visual interactiva que tú utilizas.
│
└── 📁 lakehouse/                 # [ALMACÉN DE DATOS] Repositorios centrales de información
    ├── 📁 bronze/                # Datos Crudos: Archivos JSON exactamente como llegan de las máquinas.
    ├── 📁 silver/                # Datos Limpios: Almacenamiento Delta Lake corregido y libre de duplicados.
    └── 📁 gold/                  # Características: Tabla Parquet optimizada para las predicciones de la IA.
```

---

## 🛠️ Estrategia DevOps: Automatización, Calidad y Cloud

### 1. Modelo de Ramificación y Estrategia de Git Flow (IE1, IE2, IE3)

El repositorio opera bajo una estrategia de **Git Flow** adaptada para entornos Cloud colaborativos, garantizando la trazabilidad absoluta de los artefactos de datos y modelos de IA:

| Rama | Propósito | Base | Fusiona a |
|---|---|---|---|
| `main` | Entorno productivo estable. Solo recibe código aprobado mediante Pull Requests | — | — |
| `develop` | Integración continua. Aquí confluyen las características antes de pasar a producción | `main` | `main` |
| `feature/*` | Ramas temporales para desarrollo de nuevos componentes (ej: `feature/k8s-resources-config`) | `develop` | `develop` |
| `hotfix/*` | Correcciones urgentes de seguridad o bugs críticos en producción (ej: `hotfix/snyk-secret-rotation`) | `main` | `main` y `develop` |

**Convención de Commits — Conventional Commits (IE3):**
Se aplica rigurosamente el estándar **Conventional Commits** para garantizar auditorías automatizadas y generación de changelog:

```
feat:     Nueva funcionalidad (Feature)
fix:      Corrección de bug
test:     Adición o modificación de tests
docs:     Cambios en documentación
refactor: Cambios de código que no corrigen bugs ni añaden features
chore:    Tareas de mantenimiento (dependencias, configs)
```

**Ejemplos del historial:**
```
feat(tests): add test suite structure with pytest
test(quality): add unit tests for orquestador, dashboard and infrastructure
fix(security): rotate Snyk token and remove hardcoded credentials
merge(feature): integrate K8s resource configuration into develop
```

---

### 2. Automatización del Pipeline CI/CD con GitHub Actions (IE4, IE9)

El corazón de la automatización reside en el flujo configurado en `.github/workflows/ci-cd.yml`. Este pipeline se dispara automáticamente ante cualquier **push en develop** o **pull_request hacia main**, ejecutando de manera secuencial:

```
[Git push] ──> [data-qa-security] ──> [deploy-lakehouse]
                  │                          │
            (Quality Gate)            (Despliegue Cloud)
                  │                          │
            flake8 (IE5)               Docker Hub build
            Snyk (IE6)                 Push image
            SonarQube (IE6)            Simulación K8s
            Pytest (IE7)
```

**Job 1: `data-qa-security`** — Validaciones, Calidad y Seguridad:
1. **Checkout** con `fetch-depth: 0` para análisis completo
2. **Python 3.10** configurado
3. **Instalación de dependencias** + flake8 + pytest
4. **Flake8 (IE5):** Escaneo sintáctico estático con flags `E9,F63,F7,F82`
5. **Pytest (IE7):** Ejecución de batería de 9 pruebas unitarias
6. **Snyk (IE6/IE13):** Escaneo de vulnerabilidades críticas en dependencias
7. **SonarQube (IE6/IE13):** Análisis estático con Quality Gate

**Job 2: `deploy-lakehouse`** — Despliegue Continuo:
- Depende del éxito absoluto de `data-qa-security`
- Solo se ejecuta en **Pull Request aprobado hacia `main`**
- Autenticación en Docker Hub via `DOCKERHUB_USERNAME` / `DOCKERHUB_TOKEN`
- Construcción y publicación de imagen Docker
- Trazabilidad completa del despliegue con confirmación de manifiestos K8s e Istio

---

### 3. DevSecOps: Calidad de Código y Políticas de Cumplimiento (IE5, IE6, IE8, IE13)

Garantizamos la seguridad y gobernanza de la plataforma mediante herramientas de análisis en el ciclo CI/CD:

| Herramienta | Función | Indicador |
|---|---|---|
| **flake8** | Análisis sintáctico estático (errores fatales) | IE5 |
| **pytest** | Pruebas unitarias automatizadas (9 tests) | IE7 |
| **SonarQube** | Code smells, bugs, duplicación, Quality Gate | IE6, IE13 |
| **Snyk** | Vulnerabilidades de seguridad en dependencias | IE6, IE13 |
| **Quality Gate** | Interrupción del pipeline si falla cualquier análisis | IE6 |

**Medidas de Seguridad (IE8):**
- Todos los tokens y credenciales almacenados en **GitHub Secrets** (nunca en código fuente)
- `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` — Autenticación Docker Hub
- `SNYK_TOKEN` — Escaneo de vulnerabilidades
- `SONAR_TOKEN`, `SONAR_HOST_URL` — Análisis SonarQube
- `DISCORD_WEBHOOK_URL` — Notificaciones a ingenieros (entorno, no hardcodeado)

---

### 4. Contenedorización y Orquestación Cloud (IE6, IE10)

**Dockerfile** — Imagen reproducible y eficiente:
- Base: `python:3.10-slim` (imagen ligera ~120MB)
- Java 11 Runtime para ejecución de PySpark
- Dependencias Python: streamlit, plotly, pandas, scikit-learn, pyspark, delta-spark
- Puertos expuestos: **8501** (Streamlit), **4040** (Spark UI), **8888** (Jupyter)
- CMD por defecto: `python notebooks/orquestador_planta.py`

**Kubernetes Deployment** — Alta disponibilidad y gobernanza (IE8, IE10):
```yaml
replicas: 3                    # 3 réplicas simultáneas
resources:
  limits:
    cpu: "1000m"               # Máximo 1 núcleo CPU
    memory: "1Gi"              # Máximo 1GB RAM
  requests:
    cpu: "500m"                # Reserva mínima garantizada
    memory: "512Mi"
livenessProbe:                 # Auto-diagnóstico y reinicio
  httpGet:
    path: /
    port: 8501
  initialDelaySeconds: 30
  periodSeconds: 30
  failureThreshold: 3
```

---

### 5. Service Mesh y Telemetría con Istio (IE11, IE12)

El archivo `k8s/istio-telemetry.yml` define un recurso `Telemetry` que inyecta observabilidad automática en la malla de servicios:

| Componente | Provider | Datos recolectados |
|---|---|---|
| **Métricas** | Prometheus | Latencia del pipeline (PL), throughput, tasas de éxito/error |
| **Logs de acceso** | Envoy | Registros con `response.code >= 400` (errores) |

**Tags contextuales inyectados:**
- `request_operation` — Ruta de la petición
- `source_app` — Workload origen
- `destination_app` — Workload destino

**Dashboard de Métricas (IE12):** El panel de Streamlit en `http://localhost:8501` consume y visualiza:

| Métrica | Descripción | Ubicación |
|---|---|---|
| **PL (Pipeline Latency)** | Tiempo total del ciclo Bronze→Silver→Gold→IA | `lakehouse/kpis_infra.txt` |
| **DER (Data Error Rate)** | Porcentaje de datos corruptos en ingesta | `lakehouse/alertas.log` |
| **DCR (Data Completeness Rate)** | Porcentaje de datos completados por imputación | Calculado en `pipeline_silver.ipynb` |
| **F1 Score** | Precisión del modelo Isolation Forest | Calculado en `app_dashboard.py` |

---

## 🚀 Guía de Encendido Rápido en 3 Pasos

### Requisito Único: Tener Docker Encendido
Asegúrate de tener instalado y abierto el programa gratuito Docker Desktop en tu computadora. Si no lo tienes, puedes descargarlo de forma común desde su página oficial.

### Paso 1: Entrar a la Carpeta desde la Terminal
Abre la consola de comandos de tu sistema (en Windows busca "CMD" o "Símbolo del Sistema"; en Mac busca "Terminal"). Escribe `cd` seguido de un espacio, arrastra la carpeta descompresa del proyecto dentro de la ventana negra y presiona Enter. Ejemplo:

```
cd Escritorio/Plataforma-Observabilidad-IoT
```

### Paso 2: Encender la Plataforma
Para descargar, configurar e inicializar de forma aislada las bases de datos, los motores de Spark y la pantalla web con un solo clic virtual, ejecuta el siguiente comando:

```
docker-compose up -d
```

### Paso 3: Abrir tus Pantallas de Control
Abre tu navegador web e ingresa a las siguientes direcciones:

- **Panel de Control e IA (Streamlit):** Ingresa a http://localhost:8501. Esta es tu pantalla de trabajo diaria donde monitoreas el estado de la planta.
- **Monitor Técnico de Spark UI:** Ingresa a http://localhost:4040 solo si deseas auditar los procesos de cómputo distribuidos.
- **Entorno de Desarrollo (Jupyter Lab):** Ingresa a http://localhost:8888 en caso de requerir inspeccionar los bloques de código directamente.

---

## 📊 ¿Cómo interpretar las Pantallas de Control? (Métricas DataOps)

Al ingresar al Panel de Control (http://localhost:8501), verás una interfaz dividida en dos pestañas principales:

### Pestaña 1: Monitoreo de Operaciones (Para Jefes de Planta)
- **Mediciones Totales:** Muestra cuántos registros han enviado los sensores en el turno actual.
- **Alertas Críticas de IA:** Indica cuántas veces la Inteligencia Artificial detectó anomalías mecánicas peligrosas.
- **Estado de la Maquinaria:** Letrero de seguridad. Si está en VERDE (Operación Estable) todo marcha bien. Si cambia a ROJO (Crítico / Mantenimiento), la IA detectó fallas activas y debes revisar los equipos.
- **Análisis de Tendencia:** Gráfico interactivo en tiempo real. Si la IA detecta una falla, marcará automáticamente un punto con una "X" de color rojo en la línea de tiempo.

### Pestaña 2: Gobierno de Datos y KPIs (Para Auditores Técnicos)
- **DER (Tasa de Error de Datos):** Mide la cantidad de mensajes corruptos que envían los sensores. Debe mantenerse por debajo del < 1.5%. Si se supera, el sistema registra la anomalía en el archivo `alertas.log`.
- **PL (Latencia del Pipeline):** Indica en segundos cuánto tarda un dato desde que sale de la máquina hasta que se visualiza en la pantalla web. El umbral óptimo de la planta es < 5 segundos.
- **DCR (Tasa de Completitud):** Porcentaje de registros rellenados exitosamente por Spark. Objetivo: ≥ 99.8%.
- **Score F1 (Salud de la IA):** Precisión del algoritmo. Un valor superior a 0.85 confirma que la IA está bien calibrada y libre de falsas alarmas.

---

## 🔐 Privacidad, Gobernanza y Ley N° 19.628 (Chile)

Aunque el sistema procesa telemetría técnica de máquinas, las bitácoras registran de forma colateral el identificador del operador en turno (`operador_id`) para asegurar la trazabilidad de las reparaciones. Para cumplir estrictamente con la Ley N° 19.628 de Protección de la Vida Privada en Chile, el sistema implementa:

- **Minimización:** No se almacenan nombres, RUT, correos ni datos sensibles de personas en ninguna capa del Lakehouse.
- **Seudonimización:** Los códigos de los ingenieros se encriptan de forma matemática irreversible (Hash SHA-256) al ingresar a la capa Silver, impidiendo identificar a los trabajadores en caso de una filtración.
- **Acceso Seguro (Supervisión Humana):** Bajo los lineamientos de la Ley de IA de la Unión Europea (EU AI Act) para sistemas de alto riesgo, la consola interactiva web está separada del motor de código para asegurar un control y supervisión humana transparente sin riesgos operativos.

---

## 📈 Plan de Escalabilidad y Mejoras Futuras

El sistema cuenta con una ruta de desarrollo realista estructurada en tres fases para pasar de este prototipo local a un entorno corporativo de alta disponibilidad:

- **Fase 1: Piloto Automático Avanzado (Apache Airflow):** Se sustituirá la orquestación síncrona manual por un programador empresarial para automatizar los flujos de re-entrenamientos de la IA y reintentos ante caídas de red.
- **Fase 2: Monitoreo con Gráficos de Alta Fidelidad (Grafana):** Las métricas de latencia de `kpis_infra.txt` se conectarán a paneles interactivos en Grafana con alertas sonoras en vivo para el equipo de soporte técnico de TI.
- **Fase 3: Análisis Instantáneo en Milisegundos (Apache Kafka):** Se migrará el procesamiento por lotes hacia un bus de eventos en streaming. Esto reducirá la latencia operativa a milisegundos, aislando impactos mecánicos dañinos de forma inmediata al momento de ocurrir.

---

## 🔌 ¿Cómo apagar el sistema de forma segura?

Cuando termine tu turno o desees apagar el monitoreo, vuelve a la ventana de la consola (CMD / Terminal) y presiona las teclas **Control + C** para liberar la línea de comandos. Luego, escribe la siguiente instrucción:

```
docker-compose down
```

Este comando apagará todos los procesos de forma limpia y liberará por completo la memoria RAM de tu computadora. No perderás información: todo el histórico acumulado de la planta quedará guardado de forma segura dentro de tu carpeta `lakehouse/` para el día siguiente.

---

## 📋 Mapeo de Indicadores de Evaluación (IE)

| IE | Descripción | ¿Dónde se implementa? |
|---|---|---|
| **IE1/IE2** | Ramificación Git Flow | Ramas `main`, `develop`, `feature/*`, `hotfix/*` |
| **IE3** | Trazabilidad Git | Commits con Conventional Commits y merge strategy |
| **IE4** | Automatización CI/CD | `.github/workflows/ci-cd.yml` — 2 jobs secuenciales |
| **IE5** | Documentación y buenas prácticas | Este README, estructura de carpetas, convenciones |
| **IE6/IE10** | Contenedores y orquestación | `Dockerfile` + `k8s/deployment.yml` (3 réplicas) |
| **IE7** | Pruebas automatizadas | `tests/` con pytest, integrado en pipeline CI/CD |
| **IE8** | Escalabilidad y gobernanza | `resources.limits` CPU 1000m / Memoria 1Gi + GitHub Secrets |
| **IE9** | Despliegue automático | Pipeline CD: Docker Hub build/push → simulación K8s |
| **IE12** | Dashboards y métricas | Streamlit dashboard: PL, DER, DCR, F1 Score |
| **IE13** | Cumplimiento y auditoría | SonarQube + Snyk en pipeline con Quality Gates |

---

## 🏗️ Ciclo de Vida DevOps & Arquitectura de Infraestructura Cloud

Para transformar este prototipo local en una plataforma industrial escalable de alta disponibilidad, se implementó un flujo completo de Gobernanza DevOps, automatizando el ciclo de integración y despliegue continuo (CI/CD) bajo estándares empresariales:

```
[Repositorio GitHub] ──> [GitHub Actions] ──> [SonarQube/Snyk] ──> [Docker Hub] ──> [Kubernetes Clúster]
    (develop/main)         (Build & Test)       (Quality Gate)      (Push Image)      (3 Réplicas / Istio)
```

**Pipeline CI/CD End-to-End:**
1. Push a `develop` o PR hacia `main` → dispara el pipeline
2. Job `data-qa-security`: flake8 → pytest → Snyk → SonarQube
3. Si Quality Gate falla → pipeline detenido, merge bloqueado
4. Si PR a `main` es aprobado → Job `deploy-lakehouse`
5. Login Docker Hub → Build → Push image → Simulación despliegue K8s
6. Manifiestos aplicados: `deployment.yml` + `istio-telemetry.yml`

---

Desarrollado con fines académicos y de producción bajo estándares de MLOps y DataOps.

**Autor:** Víctor Manuel Garay Soto
**Sección:** 002D
**Institución:** Duoc UC

*Plataforma POIA-IoT — Democratizando la IA Industrial.*
< ! - -   T r i g g e r   D e v O p s   P i p e l i n e   C h e c k   - - >  
 