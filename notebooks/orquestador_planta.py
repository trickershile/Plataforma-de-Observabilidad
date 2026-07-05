import os
import subprocess
import time
import json
import urllib.request
import pandas as pd
from datetime import datetime

# Configuración de rutas compartidas dentro del volumen del Lakehouse
KPI_INFRA_PATH = "/home/jovyan/work/lakehouse/kpis_infra.txt"
RUTA_GOLD = "/home/jovyan/work/lakehouse/gold/telemetry_features"

def ejecutar_fase(nombre_notebook):
    print(f"⚙️ Ejecutando componente: {nombre_notebook}...")
    # Usamos nbconvert de manera segura pasando los argumentos como una lista (evita inyecciones y problemas de escape)
    comando = ["jupyter", "nbconvert", "--to", "notebook", "--execute", nombre_notebook, "--inplace"]
    resultado = subprocess.run(comando, capture_output=True, text=True)
    
    if resultado.returncode == 0:
        print(f"✅ {nombre_notebook} finalizado con éxito.\n")
        return True
    else:
        print(f"❌ Error crítico en {nombre_notebook}:\n", resultado.stderr)
        return False

def enviar_alerta_discord(mensaje):
    # URL de Webhook proporcionada para las notificaciones de los ingenieros de planta
    url_webhook = "https://discord.com/api/webhooks/1522461729454559272/5jakziF9FenpW8fWc8IKnbRuVaTpVpB9CBr27RlIubgR8faKE4XSHyooDIzoD2QP33em" 
    
    payload = {"content": mensaje}
    headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
    
    try:
        req = urllib.request.Request(url_webhook, data=json.dumps(payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req) as response:
            pass
        print("📲 Alerta enviada con éxito a los ingenieros de planta.")
    except Exception as e:
        print(f"⚠️ No se pudo enviar la notificación a Discord: {e}")

def verificar_anomalias_y_notificar():
    try:
        if not os.path.exists(RUTA_GOLD):
            print("⚠️ Capa Gold no encontrada. Saltando notificación externa.")
            return

        # Leemos el parquet generado por la capa Gold / IA
        df = pd.read_parquet(RUTA_GOLD)
        col_anomalia = [c for c in df.columns if 'anomalia' in c.lower() or 'anomaly' in c.lower()]
        
        if not col_anomalia:
            print("⚠️ No se encontró la columna de anomalías en la capa Gold.")
            return
            
        alertas = df[df[col_anomalia[0]] == 1]
        
        if len(alertas) > 0:
            msg = f"🚨 **[POIA-IoT AI] ALERTA DE FALLA CRÍTICA** 🚨\n" \
                  f"El modelo *Isolation Forest* ha detectado **{len(alertas)} desviaciones anómalas** " \
                  f"en el último lote de sensores. Por favor revise el Dashboard de control."
            enviar_alerta_discord(msg)
        else:
            enviar_alerta_discord("✅ **[POIA-IoT AI]** Ciclo de monitoreo completado. Operación de planta estable sin anomalías.")
    except Exception as e:
        print(f"Error al auditar alertas para notificación: {e}")

if __name__ == "__main__":
    print("🚀 --- INICIANDO SISTEMA DE OBSERVABILIDAD DE PLANTA AUTOMÁTICO ---")
    
    # Registrar el tiempo de inicio exacto para medir el KPI PL
    tiempo_inicio = time.time()
    
    # 1. Absorber nuevos datos y limpiar (Capa Silver)
    if ejecutar_fase("pipeline_silver.ipynb"):
        
        # 2. Actualizar métricas móviles e Ingeniería de Características (Capa Gold)
        if ejecutar_fase("pipeline_gold.ipynb"):
            
            # 3. Evaluar anomalías y etiquetar con la IA
            if ejecutar_fase("ia_model.ipynb"):
                print("🧠 Procesamiento analítico y predictivo completado con éxito.")
            else:
                print("⚠️ Falló la ejecución del modelo de IA.")
        else:
            print("⚠️ Flujo interrumpido: Falló la fase de agregación Gold.")
    else:
        print("⚠️ Flujo interrumpido: Falló la fase de procesamiento Silver.")

    # Registrar el tiempo final de ejecución de la infraestructura
    tiempo_fin = time.time()
    
    # Cálculo e integración del KPI - Latencia Total del Pipeline (PL)
    pipeline_latency = tiempo_fin - tiempo_inicio
    print(f"⏱️ KPI - Latencia Total del Pipeline (PL): {pipeline_latency:.2f} segundos")
    
    # Guardamos este KPI de infraestructura para que Streamlit lo consuma de forma asíncrona
    try:
        with open(KPI_INFRA_PATH, "w") as f:
            f.write(f"latency:{pipeline_latency:.2f}\n")
        print(f"📊 Métrica de latencia persistida en {KPI_INFRA_PATH}")
    except Exception as e:
        print(f"⚠️ No se pudo guardar el archivo de métricas de infraestructura: {e}")

    # Verificar si el Isolation Forest etiquetó registros con 1 y lanzar alertas DataOps
    verificar_anomalias_y_notificar()
    
    print("🏁 --- CICLO DE MONITOREO FINALIZADO ---")