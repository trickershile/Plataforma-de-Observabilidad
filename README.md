## Plataforma Inteligente de Observabilidad IoT (POIA-IoT)

Bienvenido a la Plataforma POIA-IoT. Este sistema automatizado ha sido diseñado para conectarse a la maquinaria de la planta, recolectar los datos de los sensores de forma inteligente y usar Inteligencia Artificial para predecir y avisar fallas mecánicas antes de que ocurran, protegiendo los equipos de detenciones imprevistas.
Lo mejor de este sistema es que no necesitas saber programar ni escribir código para usarlo. Toda la tecnología pesada corre oculta en el fondo y tú interactúas con una interfaz visual muy sencilla en tu navegador web.

###  ¿Cómo funciona el sistema? (Flujo Visual)

El sistema opera de forma automática simulando el recorrido de los materiales en una fábrica física, pero con datos:


  [ Sensores en Maquinaria ] 
             │
             ▼
  ( Capa 1: Datos Crudos )  --> Guarda todo tal como llega de las máquinas.
             │
             ▼
  ( Capa 2: Limpiador )     --> Corrige errores y rellena datos perdidos de forma automática.
             │
             ▼
  ( Capa 3: Cerebro IA )    --> El algoritmo analiza si la temperatura o vibración es peligrosa.
             │
             ▼
 [ Dashboard Web / Discord ] --> Te muestra los gráficos interactivos y te envía alertas al celular.

##  Guía de Encendido en 3 Pasos (Sin programar)
## Para poner en marcha la plataforma en tu computadora, solo debes seguir estas instrucciones visuales:

Requisito Único: Instalar Docker
Antes de empezar, necesitas tener instalado un programa gratuito llamado Docker Desktop. Puedes descargarlo e instalarlo como cualquier programa común (siguiente, siguiente, finalizar) desde su página oficial: https://www.docker.com/products/docker-desktop/. Asegúrate de abrirlo antes de ir al Paso 1.

## Paso 1: Descargar los archivos del proyecto
Si no usas herramientas de programación, simplemente haz clic en el botón verde de este repositorio de GitHub que dice "Code" y selecciona "Download ZIP". Descomprime esa carpeta en cualquier lugar cómodo de tu computadora (por ejemplo, en tu Escritorio).

## Paso 2: Encender la Planta Digital
Abre la terminal de tu computadora (En Windows busca "CMD" o "Símbolo del Sistema"; en Mac busca "Terminal").

Entra a la carpeta que descomprimiste escribiendo el comando cd seguido de la ruta de tu carpeta. Ejemplo:


cd Escritorio/Plataforma-Observabilidad-IoT
Enciende todo el sistema ejecutando la siguiente instrucción:


docker-compose up -d
Nota: La primera vez tardará unos minutos mientras descarga los componentes. Verás que aparecen textos en verde diciendo Started. ¡Listo! Las bases de datos y la IA ya están encendidas.

## Paso 3: Abrir tus Paneles de Control
Abre tu navegador web de preferencia (Google Chrome, Edge, Safari) e ingresa a las siguientes direcciones de acuerdo a lo que necesites revisar:

## Panel de Control e IA (Streamlit): Ingresa a http://localhost:8501. Esta es tu pantalla principal. Aquí verás si las máquinas están estables o críticas, los gráficos de aguja, las tendencias de temperatura y el rendimiento de la IA.

 Monitor del Motor Técnico (Spark UI): Ingresa a http://localhost:4040. Solo si deseas auditar cómo el motor técnico procesa los miles de datos por minuto en tiempo real.

##  ¿Cómo leer las pantallas de control? (Gobernanza DataOps)
Cuando ingreses al Panel de Control (http://localhost:8501), encontrarás dos pestañas en la parte superior. Esto es lo que significa cada indicador visual:

## Pestaña 1: Monitoreo de Operaciones (Para Jefes de Planta)
Mediciones Totales: Cantidad de datos que han enviado los sensores en el turno actual.

Alertas Críticas de IA: El número total de veces que el "Bosque de Aislamiento" (nuestra IA) detectó que la máquina vibró o se calentó a niveles peligrosos.

Estado de la Maquinaria: Un letrero gigante. Si está en VERDE (Operación Estable) todo marcha bien. Si cambia a ROJO (Crítico / Mantenimiento), significa que hay anomalías activas y debes revisar las máquinas.

Gráfico de Tendencias: Un gráfico de líneas interactivo. Puedes pasar el mouse sobre él para ver los valores exactos. Si la IA detecta una falla, marcará automáticamente un punto con una "X" de color rojo en el mapa temporal.

## Pestaña 2: Gobierno de Datos y KPIs (Para Auditores Técnicos)
Score F1 (Salud de la IA): Te dice qué tan precisa está siendo la Inteligencia Artificial. Si marca un mensaje en verde con un valor superior a 0.85, significa que la IA está calibrada con precisión científica y no tiene falsas alarmas.

Latencia Total (PL): Muestra cuántos segundos tardan los datos desde que salen del sensor físico hasta que se analizan en tu pantalla. Lo ideal es que sea menor a 5 segundos.

Bitácora de Errores (DER): Si un sensor se moja, se rompe o envía datos corruptos (como letras en vez de números), el limpiador automático los frena y te dejará un mensaje en rojo aquí explicando el día y la hora del problema.

 Alertas Automáticas a tu Celular (Discord)
No necesitas estar mirando la pantalla todo el día. El sistema cuenta con un vigilante virtual incorporado. Cada vez que termina un ciclo de análisis, el orquestador revisa los resultados y enviará una notificación automática al canal de comunicaciones del equipo:

Si todo está bien, enviará un mensaje confirmando la estabilidad.

Si localiza una anomalía mecánica, enviará una alarma roja de falla crítica etiquetando la cantidad exacta de desviaciones para que envíes al equipo de mantenimiento de inmediato.

##  ¿Cómo apagar el sistema?
Cuando termines tu jornada o desees detener el monitoreo, vuelve a la ventana negra (CMD / Terminal) y escribe:


docker-compose down
Esto apagará todos los motores digitales de forma segura y liberará por completo la memoria de tu computadora sin perder el histórico de datos resguardado en la carpeta lakehouse/.

Diseñado para democratizar la Inteligencia Artificial industrial. Desarrollado por Víctor Manuel Garay Soto — Duoc UC. Para soporte técnico, contactar al administrador del sistema.