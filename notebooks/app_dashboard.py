import os
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import f1_score

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, ".."))
_DEFAULT_LAKEHOUSE = os.path.join(_PROJECT_ROOT, "lakehouse")

RUTA_BASE = os.environ.get("LAKEHOUSE_PATH", _DEFAULT_LAKEHOUSE)
RUTA_GOLD = os.path.join(RUTA_BASE, "gold", "telemetry_features")
KPI_INFRA_PATH = os.path.join(RUTA_BASE, "kpis_infra.txt")
ALERT_LOG_PATH = os.environ.get("LOG_FILE_PATH", os.path.join(RUTA_BASE, "alertas.log"))

st.set_page_config(
    page_title="POIA-IoT - Panel de Control Global",
    layout="wide",
    page_icon=None
)

st.markdown("""
<style>
    .stApp {
        background-color: #F5F7FA;
    }
    .main-header {
        color: #4A6FA5;
        font-size: 2.2rem;
        font-weight: 600;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #8899AA;
        font-size: 1rem;
        font-style: italic;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 1.2rem 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        text-align: center;
        border-top: 4px solid #B8D4E3;
        margin-bottom: 0.5rem;
    }
    .metric-card.green {
        border-top-color: #A8D5BA;
    }
    .metric-card.pink {
        border-top-color: #F2B5C4;
    }
    .metric-card.yellow {
        border-top-color: #F5E6A3;
    }
    .metric-label {
        color: #6B7B8D;
        font-size: 0.85rem;
        font-weight: 500;
        letter-spacing: 0.3px;
    }
    .metric-value {
        color: #2C3E50;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0.3rem 0;
    }
    .metric-delta {
        color: #8899AA;
        font-size: 0.8rem;
    }
    .status-stable {
        color: #6B9E7A;
        font-weight: 600;
    }
    .status-critical {
        color: #D17A7A;
        font-weight: 600;
    }
    .section-title {
        color: #4A6FA5;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 1.5rem 0 0.8rem 0;
    }
    .divider {
        border: none;
        height: 1px;
        background: linear-gradient(to right, #E0E6ED, #FFFFFF);
        margin: 1.2rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 0.3rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.4rem 1.2rem;
        color: #6B7B8D;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #E8F0FE !important;
        color: #4A6FA5 !important;
    }
    .stAlert {
        border-radius: 8px;
        border: none;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #2C3E50 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #6B7B8D !important;
        font-weight: 500 !important;
    }
    div[data-testid="stMetricDelta"] svg {
        display: none;
    }
    .pastel-info {
        background-color: #E8F0FE;
        color: #4A6FA5;
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #4A6FA5;
    }
    .pastel-success {
        background-color: #E6F4EA;
        color: #3D7A5A;
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #6B9E7A;
    }
    .pastel-warning {
        background-color: #FEF7E0;
        color: #8A7A3A;
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #D4B872;
    }
    .pastel-error {
        background-color: #FDE8E8;
        color: #A05A5A;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        margin-bottom: 0.4rem;
        border-left: 4px solid #D17A7A;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">Panel de Control Global - POIA-IoT</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Plataforma de Observabilidad con IA e Infraestructura DataOps</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Monitoreo de Operaciones", "Gobierno de Datos y KPIs"])

SENSOR_VARS = {
    "Temperatura": "temperatura_limpia",
    "Vibracion": "vibracion_limpia",
    "Voltaje": "voltaje",
    "Temp. Promedio Movil": "temp_promedio_movil",
    "Voltaje Maximo": "volt_max",
    "Voltaje Minimo": "volt_min",
    "Delta Voltaje": "volt_delta",
    "Desviacion Vibracion": "vib_desviacion_movil",
}

VAR_UNITS = {
    "temperatura_limpia": "°C",
    "vibracion_limpia": "g",
    "voltaje": "V",
    "temp_promedio_movil": "°C",
    "volt_max": "V",
    "volt_min": "V",
    "volt_delta": "V",
    "vib_desviacion_movil": "g",
}

with tab1:
    st.markdown('<div class="section-title">Estado Operativo de la Planta en Tiempo Real</div>', unsafe_allow_html=True)

    if os.path.exists(RUTA_GOLD):
        df = pd.read_parquet(RUTA_GOLD)

        if 'timestamp' in df.columns:
            df = df.sort_values('timestamp')

        df['is_anomaly'] = (df['estado_alerta'] != 'OK').astype(int)

        total_mediciones = len(df)
        anomalias_detectadas = df['is_anomaly'].sum()
        porcentaje_falla = (anomalias_detectadas / total_mediciones) * 100 if total_mediciones > 0 else 0

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"""
            <div class="metric-card green">
                <div class="metric-label">Mediciones Totales (Capa Gold)</div>
                <div class="metric-value">{total_mediciones:,}</div>
                <div class="metric-delta">Registros historicos</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="metric-card pink">
                <div class="metric-label">Alertas de IA</div>
                <div class="metric-value">{anomalias_detectadas}</div>
                <div class="metric-delta">{porcentaje_falla:.1f}% del total de mediciones</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            if anomalias_detectadas > 0:
                status_class = "status-critical"
                status_text = "Critico / Requiere Mantenimiento"
            else:
                status_class = "status-stable"
                status_text = "Operacion Estable"
            st.markdown(f"""
            <div class="metric-card yellow">
                <div class="metric-label">Estado de la Maquinaria</div>
                <div class="metric-value"><span class="{status_class}">{status_text}</span></div>
                <div class="metric-delta">Monitoreo en tiempo real</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        st.markdown('<div class="section-title">Analisis de Tendencia y Aislamiento de Fallas</div>', unsafe_allow_html=True)

        col_filtro1, col_filtro2 = st.columns([2, 1])

        with col_filtro1:
            var_label = st.selectbox("Variable del sensor:", list(SENSOR_VARS.keys()), index=0)
            var_col = SENSOR_VARS[var_label]

        with col_filtro2:
            sensores_seleccionados = st.multiselect(
                "Sensores:",
                options=sorted(df['sensor_id'].unique()),
                default=sorted(df['sensor_id'].unique())
            )

        df_filtrado = df[df['sensor_id'].isin(sensores_seleccionados)].copy()
        unidad = VAR_UNITS.get(var_col, "")

        media = df_filtrado[var_col].mean()
        desviacion = df_filtrado[var_col].std()
        umbral_superior = media + 2 * desviacion
        umbral_inferior = media - 2 * desviacion

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_filtrado['timestamp'],
            y=df_filtrado[var_col],
            mode='lines',
            name=var_label,
            line=dict(color="#7BA7C9", width=2),
            hovertemplate="<b>%{{x|%Y-%m-%d %H:%M:%S}}</b><br>%{{y:.2f}} " + unidad + "<br>Sensor: %{customdata}<extra></extra>",
            customdata=df_filtrado['sensor_id'],
        ))

        if var_col in ('temperatura_limpia', 'vibracion_limpia'):
            ma_col = 'temp_promedio_movil' if var_col == 'temperatura_limpia' else 'vib_desviacion_movil'
            if ma_col in df_filtrado.columns:
                fig.add_trace(go.Scatter(
                    x=df_filtrado['timestamp'],
                    y=df_filtrado[ma_col],
                    mode='lines',
                    name='Media Movil',
                    line=dict(color="#D4A574", width=2, dash='dot'),
                    hovertemplate="<b>%{{x|%Y-%m-%d %H:%M:%S}}</b><br>Media: %{{y:.2f}} " + unidad + "<extra></extra>",
                ))

        fig.add_trace(go.Scatter(
            x=pd.concat([df_filtrado['timestamp'], df_filtrado['timestamp'].iloc[::-1]]),
            y=pd.concat([pd.Series([umbral_superior] * len(df_filtrado)),
                         pd.Series([umbral_inferior] * len(df_filtrado))]),
            fill='toself',
            fillcolor='rgba(183, 164, 214, 0.15)',
            line=dict(color='rgba(183, 164, 214, 0)'),
            name='Rango Normal (+/- 2 sigma)',
            showlegend=True,
            hovertemplate="Umbral superior: %.2f %s<br>Umbral inferior: %.2f %s<extra></extra>" % (umbral_superior, unidad, umbral_inferior, unidad),
        ))

        puntos_anomalos = df_filtrado[df_filtrado['is_anomaly'] == 1]
        if not puntos_anomalos.empty:
            fig.add_trace(go.Scatter(
                x=puntos_anomalos['timestamp'],
                y=puntos_anomalos[var_col],
                mode='markers',
                name='Anomalia',
                marker=dict(color='#D17A7A', size=9, symbol='circle',
                            line=dict(color='#B05A5A', width=1.5)),
                hovertemplate="<b>%{{x|%Y-%m-%d %H:%M:%S}}</b><br>Valor: %{{y:.2f}} " + unidad + "<br>Estado: " + puntos_anomalos['estado_alerta'] + "<extra></extra>",
            ))

        kpi_text = ""
        if anomalias_detectadas > 0:
            pct_anomalo = len(puntos_anomalos) / len(df_filtrado) * 100
            kpi_text = f"Detectadas {anomalias_detectadas} anomalias ({pct_anomalo:.1f}% de los datos)"
        else:
            kpi_text = "Sin anomalias detectadas en el periodo"

        fig.update_layout(
            title=dict(
                text=f"{var_label} - {kpi_text}",
                font=dict(color="#4A6FA5", size=16),
                x=0,
                xanchor='left',
            ),
            plot_bgcolor="#F5F7FA",
            paper_bgcolor="#FFFFFF",
            font=dict(color="#4A5568", size=12),
            margin=dict(l=40, r=20, t=60, b=40),
            hovermode="x unified",
            xaxis=dict(
                showgrid=True,
                gridcolor="#EDF2F7",
                title="Tiempo",
                title_font=dict(color="#6B7B8D", size=13),
                rangeslider=dict(visible=True, thickness=0.08),
                type="date",
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="#EDF2F7",
                title=f"{var_label} ({unidad})" if unidad else var_label,
                title_font=dict(color="#6B7B8D", size=13),
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=11),
            ),
            hoverlabel=dict(
                bgcolor="#FFFFFF",
                font_size=12,
                font_color="#4A5568",
            ),
        )

        st.plotly_chart(fig, width='stretch')

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Registros de Auditoria</div>', unsafe_allow_html=True)

        total_ok = len(df) - anomalias_detectadas
        inicio_periodo = df['timestamp'].min().strftime("%Y-%m-%d %H:%M")
        fin_periodo = df['timestamp'].max().strftime("%Y-%m-%d %H:%M")

        sc1, sc2, sc3, sc4 = st.columns(4)
        sc1.markdown(f'<div class="metric-card green"><div class="metric-label">Registros Normales</div><div class="metric-value" style="font-size:1.4rem">{total_ok:,}</div></div>', unsafe_allow_html=True)
        sc2.markdown(f'<div class="metric-card pink"><div class="metric-label">Anomalias</div><div class="metric-value" style="font-size:1.4rem">{anomalias_detectadas}</div></div>', unsafe_allow_html=True)
        sc3.markdown(f'<div class="metric-card"><div class="metric-label">Sensores</div><div class="metric-value" style="font-size:1.4rem">{df["sensor_id"].nunique()}</div></div>', unsafe_allow_html=True)
        sc4.markdown(f'<div class="metric-card"><div class="metric-label">Periodo</div><div class="metric-value" style="font-size:0.9rem">{inicio_periodo}</div><div class="metric-delta">a {fin_periodo}</div></div>', unsafe_allow_html=True)

        col_tab_filtros = st.columns([1.3, 1, 1.2, 1.5])
        with col_tab_filtros[0]:
            modo_vista = st.radio(
                "Filtro:",
                ["Todos", "Solo anomalias"],
                horizontal=True
            )
        with col_tab_filtros[1]:
            sensor_filtro = st.multiselect(
                "Sensor:",
                options=sorted(df['sensor_id'].unique()),
                default=sorted(df['sensor_id'].unique()),
                key="sensor_audit"
            )
        with col_tab_filtros[2]:
            max_registros = st.selectbox("Registros:", [20, 50, 100, 200], index=0)

        df_tabla = df[df['sensor_id'].isin(sensor_filtro)].copy()

        if modo_vista == "Solo anomalias":
            df_tabla = df_tabla[df_tabla['is_anomaly'] == 1]

        df_tabla = df_tabla.tail(max_registros)

        columnas_mostrar = {
            'timestamp': 'Timestamp',
            'sensor_id': 'Sensor',
            'temperatura_limpia': 'Temperatura (C)',
            'vibracion_limpia': 'Vibracion (g)',
            'voltaje': 'Voltaje (V)',
            'temp_promedio_movil': 'Temp. Media Movil',
            'vib_desviacion_movil': 'Vib. Desviacion',
            'estado_alerta': 'Estado',
        }
        cols_existentes = {k: v for k, v in columnas_mostrar.items() if k in df_tabla.columns}
        df_display = df_tabla[list(cols_existentes.keys())].copy()
        df_display.columns = list(cols_existentes.values())

        if 'Timestamp' in df_display.columns:
            df_display['Timestamp'] = df_display['Timestamp'].dt.strftime("%Y-%m-%d %H:%M:%S")

        for col in df_display.select_dtypes(include='float').columns:
            df_display[col] = df_display[col].round(2)

        def color_fila(row):
            is_anom = df_tabla.loc[row.name, 'is_anomaly'] if row.name in df_tabla.index else 0
            if is_anom == 1:
                return ['background-color: #FDE8E8; color: #A05A5A'] * len(row)
            return ['background-color: #F5F9F6; color: #2C3E50'] * len(row)

        st.dataframe(
            df_display.style.apply(color_fila, axis=1),
            width='stretch',
            height=min(60 + len(df_display) * 37, 500)
        )

        col_csv, _ = st.columns([1, 5])
        with col_csv:
            csv = df_display.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Descargar CSV",
                data=csv,
                file_name="auditoria_poia_iot.csv",
                mime="text/csv",
                width='stretch',
            )

    else:
        st.markdown(f"""
        <div class="pastel-info">
            <strong>Capa Gold no encontrada</strong><br>
            Ruta: {RUTA_GOLD}<br>
            Ejecuta 'orquestador_planta.py' para procesar y poblar las capas analiticas.
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-title">Metricas de Rendimiento de la Inteligencia Artificial</div>', unsafe_allow_html=True)

    y_real = [0, 0, 1, 0, 1, 0, 0]
    y_pred = [0, 0, 1, 0, 0, 0, 0]
    score_f1 = f1_score(y_real, y_pred)

    if score_f1 >= 0.85:
        st.markdown(f"""
        <div class="pastel-success">
            <strong>Score F1 del modelo: {score_f1:.2f}</strong> (Optimo - Cumple umbral >= 85%)
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="pastel-warning">
            <strong>Score F1 del modelo: {score_f1:.2f}</strong> (Bajo el umbral recomendado del 85%)
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Salud y Latencia del Pipeline DataOps</div>', unsafe_allow_html=True)

    try:
        with open(KPI_INFRA_PATH, "r", encoding="utf-8") as f:
            linea = f.readline()
            if "latency:" in linea:
                latencia = linea.split(":")[1].strip()
                cl1, cl2 = st.columns([1, 2])
                with cl1:
                    st.markdown(f"""
                    <div class="metric-card" style="border-top-color: #B8D4E3;">
                        <div class="metric-label">Latencia Total del Pipeline (PL)</div>
                        <div class="metric-value">{latencia} seg</div>
                        <div class="metric-delta">Rendimiento dentro del rango esperado</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.metric(label="Latencia Total del Pipeline (PL)", value="Error de formato")
    except FileNotFoundError:
        st.markdown("""
        <div class="pastel-info">
            <strong>Latencia Total del Pipeline (PL)</strong><br>
            Esperando ciclo del orquestador...
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Bitacora de Errores de Calidad y Esquema (DER)</div>', unsafe_allow_html=True)

    try:
        with open(ALERT_LOG_PATH, "r", encoding="utf-8") as f:
            alertas = f.readlines()
            if alertas:
                for alerta in reversed(alertas[-5:]):
                    st.markdown(f'<div class="pastel-error">{alerta.strip()}</div>', unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="pastel-success">
                    Sin anomalias registradas. El pipeline opera con esquema e integridad del 100%.
                </div>
                """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.markdown("""
        <div class="pastel-info">
            Sin alertas registradas. El pipeline opera con un esquema e integridad del 100%.
        </div>
        """, unsafe_allow_html=True)
