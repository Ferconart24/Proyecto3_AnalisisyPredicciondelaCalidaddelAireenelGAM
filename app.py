import streamlit as st
import pandas as pd
from src.eda.ProcesadorEDA import ProcesadorEDA

# from src.visualizacion.Visualizador import Visualizador
# from src.modelos.ModeloML import ModeloML

st.set_page_config(page_title="Calidad del Aire en el GAM", layout="wide")

menu = st.sidebar.radio(
    "Menú del Proyecto",
    [
        "Carga de Datos",
        "EDA",
        "Visualizaciones",
        "Modelos",
        "Conclusiones"
    ]
)

# ---------------- CARGA DE DATOS ----------------
if menu == "Carga de Datos":
    st.title("📂 Carga de Datos del Proyecto")

    try:
        df_cont = pd.read_csv("data/processed/contaminantes.csv", parse_dates=["fecha"])
        df_flujo = pd.read_csv("data/processed/flujo_vehicular.csv", parse_dates=["fecha"])
        df_clima = pd.read_csv("data/processed/clima.csv", parse_dates=["fecha"])

        st.success("✅ Datasets cargados desde 'data/processed/'")
        st.subheader("Contaminantes")
        st.dataframe(df_cont.head())
        st.subheader("Flujo Vehicular")
        st.dataframe(df_flujo.head())
        st.subheader("Clima")
        st.dataframe(df_clima.head())

        # Guardar en sesión
        st.session_state["contaminantes"] = df_cont
        st.session_state["flujo"] = df_flujo
        st.session_state["clima"] = df_clima

    except FileNotFoundError:
        st.error("❌ No se encontraron los archivos procesados.")

# ---------------- EDA ----------------
elif menu == "EDA":
    st.title("📊 Análisis Exploratorio de Datos")

    if "contaminantes" in st.session_state and "flujo" in st.session_state:
        df_cont = st.session_state["contaminantes"]
        df_flujo = st.session_state["flujo"]

        eda = ProcesadorEDA(df_cont)

        st.subheader("Distribución de contaminantes")
        eda.distribuciones(["pm2_5", "pm10", "co", "no2", "o3"])

        st.subheader("Correlaciones entre variables")
        eda.correlaciones()

        st.subheader("Patrones temporales de PM2.5")
        eda.temporal("pm2_5")

    else:
        st.warning("Primero carga los datos en 'Carga de Datos'.")

# ---------------- VISUALIZACIONES ----------------
elif menu == "Visualizaciones":
    st.title("🌍 Visualizaciones Avanzadas")
    st.info("Aquí se mostrarán mapas de calor y gráficos interactivos según ubicaciones de la GAM.")

    # -> Aquí integrarás tu clase Visualizador
    # Ejemplo: mapa de calor con plotly o folium

# ---------------- MODELOS ----------------
elif menu == "Modelos":
    st.title("🤖 Modelos Supervisados")

    st.subheader("Regresión")
    st.write("Predicción de concentración de PM2.5 (ejemplo con Regresión Lineal, KNN, Random Forest).")

    st.subheader("Clasificación")
    st.write("Clasificación de calidad del aire según ICA (Buena, Moderada, Mala, Muy Mala).")

    # -> Aquí irán tus modelos ML cuando estén implementados

# ---------------- CONCLUSIONES ----------------
elif menu == "Conclusiones":
    st.title("📑 Conclusiones del Proyecto")

    st.markdown("""
    - **Mayor contaminación** detectada en horas pico y zonas de alto flujo vehicular.
    - **Variables críticas**: flujo vehicular y condiciones meteorológicas (humedad y viento).
    - **Modelos ML** permitirán predecir la concentración de PM2.5 y categorizar la calidad del aire.
    """)