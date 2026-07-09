import os
import sys
import subprocess
import time
import json
import urllib.request
import pandas as pd

# ---------------------------------------------------------------------------
# Configuración de rutas (configurables vía variables de entorno)
# Por defecto usa la ruta relativa al script, funciona en Docker y local
# En Dockerfile/K8s se puede sobreescribir con LAKEHOUSE_PATH
# ---------------------------------------------------------------------------
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, ".."))
_DEFAULT_LAKEHOUSE = os.path.join(_PROJECT_ROOT, "lakehouse")

LAKEHOUSE_BASE = os.environ.get("LAKEHOUSE_PATH", _DEFAULT_LAKEHOUSE)
KPI_INFRA_PATH = os.path.join(LAKEHOUSE_BASE, "kpis_infra.txt")
RUTA_GOLD = os.path.join(LAKEHOUSE_BASE, "gold", "telemetry_features")

# URL del webhook de Discord (NUNCA hardcodear tokens - usar variable de entorno)
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")


def ejecutar_fase(nombre_notebook):
    print(f"⚙️ Ejecutando componente: {nombre_notebook}...")
    comando = [
        sys.executable, "-m", "jupyter", "nbconvert",
        "--to", "notebook", "--execute", nombre_notebook, "--inplace"
    ]
    resultado = subprocess.run(comando, capture_output=True, text=True)

    if resultado.returncode == 0:
        print(f"✅ {nombre_notebook} finalizado con éxito.\n")
        return True
    else:
        print(f"❌ Error crítico en {nombre_notebook}:\n", resultado.stderr)
        return False


def enviar_alerta_discord(mensaje):
    if not DISCORD_WEBHOOK_URL:
        print("⚠️ DISCORD_WEBHOOK_URL no configurado. Omitiendo notificación.")
        return
    payload = {"content": mensaje}
    headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
    try:
        req = urllib.request.Request(
            DISCORD_WEBHOOK_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers
        )
        urllib.request.urlopen(req)
        print("📲 Alerta enviada con éxito a los ingenieros de planta.")
    except Exception as e:
        print(f"⚠️ No se pudo enviar la notificación a Discord: {e}")


def verificar_anomalias_y_notificar():
    try:
        if not os.path.exists(RUTA_GOLD):
            print("⚠️ Capa Gold no encontrada. Saltando notificación externa.")
            return
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
            msg_ok = (
                "✅ **[POIA-IoT AI]** Ciclo de monitoreo completado. "
                "Operación de planta estable sin anomalías."
            )
            enviar_alerta_discord(msg_ok)
    except Exception as e:
        print(f"Error al auditar alertas para notificación: {e}")


if __name__ == "__main__":
    print("🚀 --- INICIANDO SISTEMA DE OBSERVABILIDAD DE PLANTA AUTOMÁTICO ---")
    tiempo_inicio = time.time()

    if ejecutar_fase("pipeline_silver.ipynb"):
        if ejecutar_fase("pipeline_gold.ipynb"):
            if ejecutar_fase("ia_model.ipynb"):
                print("🧠 Procesamiento analítico y predictivo completado con éxito.")
            else:
                print("⚠️ Falló la ejecución del modelo de IA.")
        else:
            print("⚠️ Flujo interrumpido: Falló la fase de agregación Gold.")
    else:
        print("⚠️ Flujo interrumpido: Falló la fase de procesamiento Silver.")

    tiempo_fin = time.time()
    pipeline_latency = tiempo_fin - tiempo_inicio
    print(f"⏱️ KPI - Latencia Total del Pipeline (PL): {pipeline_latency:.2f} segundos")

    try:
        with open(KPI_INFRA_PATH, "w", encoding="utf-8") as f:
            f.write(f"latency:{pipeline_latency:.2f}\n")
        print(f"📊 Métrica de latencia persistida en {KPI_INFRA_PATH}")
    except Exception as e:
        print(f"⚠️ No se pudo guardar el archivo de métricas de infraestructura: {e}")

    verificar_anomalias_y_notificar()
    print("🏁 --- CICLO DE MONITOREO FINALIZADO ---")
