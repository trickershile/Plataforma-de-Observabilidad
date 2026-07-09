#!/bin/bash
set -e

cd /app/notebooks

echo "[ENTRY] Iniciando Streamlit dashboard en puerto 8501..."
streamlit run app_dashboard.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true &
PID_STREAMLIT=$!
echo "[ENTRY] Streamlit PID: $PID_STREAMLIT"

echo "[ENTRY] Iniciando Jupyter Lab en puerto 8888..."
jupyter lab \
    --ip=0.0.0.0 \
    --port=8888 \
    --no-browser \
    --allow-root \
    --NotebookApp.token='poia-token' \
    --NotebookApp.disable_check_xsrf=True &
PID_JUPYTER=$!
echo "[ENTRY] Jupyter PID: $PID_JUPYTER"

echo "[ENTRY] Esperando 5 segundos para que los servicios inicien..."
sleep 5

echo "[ENTRY] Ejecutando orquestador de datos..."
python orquestador_planta.py || echo "[ENTRY] Orquestador finalizado con advertencias (continuando...)"

echo "[ENTRY] Todos los servicios iniciados. Contenedor operativo."
echo "[ENTRY]   Streamlit:  http://localhost:8501"
echo "[ENTRY]   Jupyter Lab: http://localhost:8888 (token: poia-token)"
echo "[ENTRY]   Spark UI:   http://localhost:4040"

wait -n
