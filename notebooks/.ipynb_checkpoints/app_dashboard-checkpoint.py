import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Monitoreo de Planta - IA", layout="wide")

st.title("🏭 Panel de Control y Observabilidad IoT (PharmaGuard)")
st.markdown("---")

# Ruta relativa hacia la capa Gold procesada desde la carpeta notebooks/
ruta_gold = "../lakehouse/gold/telemetry_features"

if os.path.exists(ruta_gold):
    # Leemos el último estado procesado por Spark e IA
    df = pd.read_parquet(ruta_gold)
    
    # 1. Indicadores clave (Métricas superiores)
    total_datos = len(df)
    # Suponiendo que el modelo guarda la columna como 'is_anomaly' o 'es_anomalia'
    # Si la columna se llama distinto en tu ia_model, cámbiala acá:
    col_anomalia = 'es_anomalia' if 'es_anomalia' in df.columns else df.columns[-1]
    anomalias = df[df[col_anomalia] == 1]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Mediciones Procesadas", f"{total_datos:,}")
    c2.metric("Alertas Críticas Detectadas", f"{len(anomalias)}", delta_color="inverse")
    c3.metric("Estado General de Planta", "🚨 CRÍTICO" if len(anomalias) > 0 else "✅ ESTABLE")
    
    st.markdown("---")
    
    # 2. Despliegue de Datos
    st.subheader("🚨 Historial Reciente de Alertas Tempranas (IA)")
    if len(anomalias) > 0:
        st.dataframe(anomalias.tail(10), use_container_width=True)
    else:
        st.success("No hay anomalías registradas en las últimas horas de operación.")
        
else:
    st.error(f"No se encontró la capa Gold en la ruta: {ruta_gold}. Ejecuta el orquestador primero.")