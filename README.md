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
├── 📄 docker-compose.yml         # El "botón de encendido" que levanta toda la planta digital local.
├── 📄 Dockerfile                 # Receta de construcción de la imagen de contenedor optimizada
├── 📄 requirements.txt           # Librerías y dependencias técnicas del ecosistema
└── 📄 README.md                  # Este manual de instrucciones que estás leyendo.
│
├── 📁 notebooks/                 # [CEREBRO ANALÍTICO] Códigos de control y pantallas visuales
│   ├── 📄 orquestador_planta.py  # El piloto automático: corre los procesos en orden y envía alertas.
│   ├── 📄 pipeline_silver.ipynb  # El filtro limpiador: corrige errores de sensores en Apache Spark.
│   ├── 📄 pipeline_gold.ipynb    # El calculador: genera las métricas y características para la IA.
│   └── 📄 app_dashboard.py       # La interfaz web: la pantalla visual interactiva que tú utilizas.
│
└── 📁 lakehouse/                 # [ALMACÉN DE DATOS] Repositorios centrales de información
    ├── 📁 bronze/                # Datos Crudos: Archivos JSON exactamente como llegan de las máquinas.
    ├── 📁 silver/                # Datos Limpios: Almacenamiento Delta Lake corregido y libre de duplicados.
    └── 📁 gold/                  # Características: Tabla Parquet optimizada para las predicciones de la IA.
```

<<<<<<< HEAD
### 🛠️ Ciclo de Vida DevOps & Arquitectura de Infraestructura Cloud
Para transformar este prototipo local en una plataforma industrial escalable de alta disponibilidad, se implementó un flujo completo de Gobernanza DevOps, automatizando el ciclo de integración y despliegue continuo (CI/CD) bajo estándares empresariales.
```
[Repositorio GitHub] ──> [GitHub Actions] ──> [SonarQube/Snyk] ──> [Docker Hub] ──> [Kubernetes Clúster]
    (develop/main)         (Build & Test)       (Quality Gate)     (Push Image)      (3 Réplicas / Istio)
    ```

### 1. Modelo de Ramificación y Estrategia de Git Flow (IE1, IE2, IE3)El repositorio opera bajo una estrategia de Git Flow adaptada para entornos Cloud colaborativos, garantizando la trazabilidad absoluta de los artefactos de datos y modelos de IA:  main: Entorno productivo estable de la plataforma. Solo recibe código aprobado mediante Pull Requests.  develop: Rama de integración continua. Aquí confluyen las características antes de pasar a producción.  feature/*: Ramas temporales para el desarrollo de nuevos componentes analíticos (Ej: feature/isolation-forest-tuning).  Convención de Commits: Se aplica rigurosamente Conventional Commits (feat:, fix:, docs:, chore:) para facilitar auditorías automatizadas del código fuente. 

### 2. Automatización del Pipeline CI/CD con GitHub Actions (IE4, IE9)El corazón de la automatización reside en el flujo configurado en .github/workflows/ci-cd.yml. Este pipeline se dispara automáticamente ante cualquier push en develop o pull_request hacia main, ejecutando de manera secuencial:  Construcción del Entorno: Configuración de contenedores virtuales Linux con entornos aislados de Python 3.10.  Pruebas Automatizadas (IE7): Ejecución de baterías de pruebas unitarias sobre los módulos de procesamiento analítico mediante pytest antes de autorizar cualquier mezcla de código.  Validación Automática del Pipeline (IE6): Si un test falla, el pipeline interrumpe de forma inmediata su ejecución, bloqueando el merge para proteger la integridad del entorno productivo.  

### 3. DevSecOps: Calidad de Código y Políticas de Cumplimiento (IE5, IE6, IE8)Garantizamos la seguridad y gobernanza de la plataforma mediante la inyección de herramientas de análisis estático y seguridad en el ciclo de construcción:  Análisis Estático con SonarQube: Evalúa la mantenibilidad del código, duplicaciones y detecta code smells en los scripts de procesamiento del Lakehouse.  Auditoría de Seguridad con Snyk & Dependabot: Escanea de forma automatizada las dependencias declaradas en requirements.txt en busca de vulnerabilidades críticas o secretos expuestos.  Mecanismos de Interrupción (Quality Gates): El pipeline está programado para fallar e interpretar un corte obligatorio del flujo si SonarQube detecta que la calidad está por debajo del estándar exigido, o si Snyk encuentra brechas críticas de seguridad.  

### 4. Orquestación y Despliegue en Kubernetes & Istio Service Mesh (IE10, IE11, IE12)Para el despliegue en un entorno cloud simulado de gran envergadura, la plataforma migra desde el entorno local de Docker Compose hacia una arquitectura orquestada en Kubernetes (K8s) a través de los manifiestos alojados en la carpeta /k8s:  Escalabilidad y Alta Disponibilidad (IE8): El archivo k8s/deployment.yml define un esquema de 3 réplicas simultáneas para el contenedor de procesamiento, distribuyendo el tráfico mediante balanceadores de carga y asignando límites estrictos de hardware (máximo 1Gi de Memoria y 1000m de CPU) para mitigar caídas por desbordamiento de recursos.  Monitoreo y Observabilidad Automática (IE1, IE3): Acoplamos políticas de telemetría a través de Istio Service Mesh (k8s/istio-telemetry.yml). Las métricas nativas de tráfico e inyección de logs (registradas en alertas.log y kpis_infra.txt) son recolectadas automáticamente por los Sidecar Proxies (Envoy) del clúster, alimentando dashboards dinámicos para analizar en tiempo real:  Latencia del pipeline de datos (PL).Tasa de error de datos (DER).Estado de las réplicas y porcentaje de éxito en despliegues.  


### Guía de Encendido Rápido en 3 Pasos
Requisito Único: Tener Docker Encendido
Asegúrate de tener instalado y abierto el programa gratuito Docker Desktop en tu computadora. Si no lo tienes, puedes descargarlo de forma común desde su página oficial.

### Paso 1: Entrar a la Carpeta desde la Terminal
=======

## Guía de Encendido Rápido en 3 Pasos
Requisito Único: Tener Docker Encendido
Asegúrate de tener instalado y abierto el programa gratuito Docker Desktop en tu computadora. Si no lo tienes, puedes descargarlo de forma común desde su página oficial.



## Paso 1: Entrar a la Carpeta desde la Terminal
>>>>>>> 25f65476f1751937fd0f430339e11c66d2b077b7
Abre la consola de comandos de tu sistema (en Windows busca "CMD" o "Símbolo del Sistema"; en Mac busca "Terminal"). Escribe cd seguido de un espacio, arrastra la carpeta descompresa del proyecto dentro de la ventana negra y presiona Enter. Ejemplo:

cd Escritorio/Plataforma-Observabilidad-IoT

<<<<<<< HEAD
Paso 2: Encender la Plataforma
=======


## Paso 2: Encender la Plataforma
>>>>>>> 25f65476f1751937fd0f430339e11c66d2b077b7
Para descargar, configurar e inicializar de forma aislada las bases de datos, los motores de Spark y la pantalla web con un solo clic virtual, ejecuta el siguiente comando:



docker-compose up -d

<<<<<<< HEAD
Paso 3: Abrir tus Pantallas de Control
Abre tu navegador web e ingresa a las siguientes direcciones:

Panel de Control e IA (Streamlit): Ingresa a http://localhost:8501. Esta es tu pantalla de trabajo diaria donde monitoreas el estado de la planta.
=======


## Paso 3: Abrir tus Pantallas de Control
Abre tu navegador web (Google Chrome, Edge o Safari) e ingresa a las siguientes direcciones:



##  Panel de Control e IA (Streamlit): Ingresa a http://localhost:8501. Esta es tu pantalla de trabajo diaria donde monitoreas el estado de la planta.
>>>>>>> 25f65476f1751937fd0f430339e11c66d2b077b7

Monitor Técnico de Spark UI: Ingresa a http://localhost:4040 solo si deseas auditar los procesos de cómputo distribuidos.

Entorno de Desarrollo (Jupyter Lab): Ingresa a http://localhost:8888 en caso de requerir inspeccionar los bloques de código directamente.

<<<<<<< HEAD
### ¿Cómo interpretar las Pantallas de Control? (Métricas DataOps)
Al ingresar al Panel de Control (http://localhost:8501), verás una interfaz dividida en dos pestañas principales:

Pestaña 1: Monitoreo de Operaciones (Para Jefes de Planta)
=======


##  ¿Cómo interpretar las Pantallas de Control? (Métricas DataOps)
Al ingresar al Panel de Control (http://localhost:8501), verás una interfaz dividida en dos pestañas principales:



## Pestaña 1: Monitoreo de Operaciones (Para Jefes de Planta)
>>>>>>> 25f65476f1751937fd0f430339e11c66d2b077b7
Mediciones Totales: Muestra cuántos registros han enviado los sensores en el turno actual.

Alertas Críticas de IA: Indica cuántas veces la Inteligencia Artificial detectó anomalías mecánicas peligrosas.

Estado de la Maquinaria: Letrero de seguridad. Si está en VERDE (Operación Estable) todo marcha bien. Si cambia a ROJO (Crítico / Mantenimiento), la IA detectó fallas activas y debes revisar los equipos.

Análisis de Tendencia: Gráfico interactivo en tiempo real. Si la IA detecta una falla, marcará automáticamente un punto con una "X" de color rojo en la línea de tiempo.


<<<<<<< HEAD
Pestaña 2: Gobierno de Datos y KPIs (Para Auditores Técnicos)
=======

## Pestaña 2: Gobierno de Datos y KPIs (Para Auditores Técnicos)
>>>>>>> 25f65476f1751937fd0f430339e11c66d2b077b7
DER (Tasa de Error de Datos): Mide la cantidad de mensajes corruptos que envían los sensores. Debe mantenerse por debajo del < 1.5%. Si se supera, el sistema registra la anomalía en el archivo alertas.log.

PL (Latencia del Pipeline): Indica en segundos cuánto tarda un dato desde que sale de la máquina hasta que se visualiza en la pantalla web. El umbral óptimo de la planta es < 5 segundos.

DCR (Tasa de Completitud): Porcentaje de registros rellenados exitosamente por Spark. Objetivo: ≥ 99.8%.

Score F1 (Salud de la IA): Precisión del algoritmo. Un valor superior a 0.85 confirma que la IA está bien calibrada y libre de falsas alarmas.

<<<<<<< HEAD
🔒 Privacidad, Gobernanza y Ley N° 19.628 (Chile)
=======


##  Privacidad, Gobernanza y Ley N° 19.628 (Chile)
>>>>>>> 25f65476f1751937fd0f430339e11c66d2b077b7
Aunque el sistema procesa telemetría técnica de máquinas, las bitácoras registran de forma colateral el identificador del operador en turno (operador_id) para asegurar la trazabilidad de las reparaciones. Para cumplir estrictamente con la Ley N° 19.628 de Protección de la Vida Privada en Chile, el sistema implementa:

Minimización: No se almacenan nombres, RUT, correos ni datos sensibles de personas en ninguna capa del Lakehouse.

Seudonimización: Los códigos de los ingenieros se encriptan de forma matemática irreversible (Hash SHA-256) al ingresar a la capa Silver, impidiendo identificar a los trabajadores en caso de una filtración.

Acceso Seguro (Supervisión Humana): Bajo los lineamientos de la Ley de IA de la Unión Europea (EU AI Act) para sistemas de alto riesgo, la consola interactiva web está separada del motor de código para asegurar un control y supervisión humana transparente sin riesgos operativos.


<<<<<<< HEAD
Plan de Escalabilidad y Mejoras Futuras
=======

##  Plan de Escalabilidad y Mejoras Futuras
>>>>>>> 25f65476f1751937fd0f430339e11c66d2b077b7
El sistema cuenta con una ruta de desarrollo realista estructurada en tres fases para pasar de este prototipo local a un entorno corporativo de alta disponibilidad:

Fase 1: Piloto Automático Avanzado (Apache Airflow): Se sustituirá la orquestación síncrona manual por un programador empresarial para automatizar los flujos de re-entrenamientos de la IA y reintentos ante caídas de red.

Fase 2: Monitoreo con Gráficos de Alta Fidelidad (Grafana): Las métricas de latencia de kpis_infra.txt se conectarán a paneles interactivos en Grafana con alertas sonoras en vivo para el equipo de soporte técnico de TI.

Fase 3: Análisis Instantáneo en Milisegundos (Apache Kafka): Se migrará el procesamiento por lotes hacia un bus de eventos en streaming. Esto reducirá la latencia operativa a milisegundos, aislando impactos mecánicos dañinos de forma inmediata al momento de ocurrir.

<<<<<<< HEAD
¿Cómo apagar el sistema de forma segura?
=======


##  ¿Cómo apagar el sistema de forma segura?
>>>>>>> 25f65476f1751937fd0f430339e11c66d2b077b7
Cuando termine tu turno o desees apagar el monitoreo, vuelve a la ventana de la consola (CMD / Terminal) y presiona las teclas Control + C para liberar la línea de comandos. Luego, escribe la siguiente instrucción:

docker-compose down


Este comando apagará todos los procesos de forma limpia y liberará por completo la memoria RAM de tu computadora. No perderás información: todo el histórico acumulado de la planta quedará guardado de forma segura dentro de tu carpeta lakehouse/ para el día siguiente.

<<<<<<< HEAD
=======


Plataforma POIA-IoT — Democratizando la IA Industrial. 

Desarrollado por Víctor Manuel Garay Soto — Sección 002D — Duoc UC.

Desarrollado con fines académicos y de producción bajo estándares de MLOps y DataOps. Autor: Víctor Manuel Garay Soto — Duoc UC
>>>>>>> 25f65476f1751937fd0f430339e11c66d2b077b7



Desarrollado con fines académicos y de producción bajo estándares de MLOps y DataOps.

Autor: Víctor Manuel Garay Soto

Sección: 002D

Institución: Duoc UC

Plataforma POIA-IoT — Democratizando la IA Industrial.