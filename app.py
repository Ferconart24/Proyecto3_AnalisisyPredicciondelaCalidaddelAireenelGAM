import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

from src.visualizacion.Visualizador import Visualizador
# from src.modelos.ModeloML import ModeloML
# from src.eda.ProcesadorEDA import ProcesadorEDA

# ---------------- CONFIGURACIÓN ----------------
st.set_page_config(page_title="Calidad del Aire en el GAM", layout="wide")

# ---------------- MENÚ LATERAL ----------------
with st.sidebar:

    menu = option_menu(
        "Menú del Proyecto",
        [
            "Carga de Datos",
            "EDA",
            "Visualizaciones",
            "Modelos",
            "Base de Datos",
            "Acerca de"
        ],
        icons=["folder", "bar-chart", "globe", "cpu", "database", "info-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "transparent"},
            "icon": {"color": "black", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "5px",
                "border-radius": "8px",
                "border": "1px solid #ccc",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#2b8a3e", "color": "white"},
        },
    )

# ---------------- CARGA DE DATOS ----------------
if menu == "Carga de Datos":
    st.title("Carga de Datos del Proyecto")

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
    st.title("Análisis Exploratorio de Datos")

    if "contaminantes" in st.session_state and "flujo" in st.session_state:
        df_cont = st.session_state["contaminantes"]
        df_flujo = st.session_state["flujo"]

        # eda = ProcesadorEDA(df_cont, df_flujo)
        st.info("Aquí irán las funciones del EDA (distribuciones, correlaciones, temporales)")
    else:
        st.warning("Primero carga los datos en 'Carga de Datos'.")

# ---------------- VISUALIZACIONES ----------------
elif menu == "Visualizaciones":
    st.title("Visualizaciones")

    if "contaminantes" in st.session_state and "flujo" in st.session_state and "clima" in st.session_state:
        df_cont = st.session_state["contaminantes"]
        df_flujo = st.session_state["flujo"]
        df_clima = st.session_state["clima"]

        vis = Visualizador(df_cont, df_flujo, df_clima)

        st.subheader("1️⃣ Consumo por hora y día")
        vis.consumo_hora_dia()

        st.subheader("2️⃣ Demanda bajo distintas condiciones climáticas")
        vis.demanda_condiciones()

        st.subheader("3️⃣ Correlaciones entre contaminantes y clima")
        vis.correlaciones_clima()
    else:
        st.warning("⚠️ Primero carga los datos en 'Carga de Datos'.")

# ---------------- MODELOS ----------------
elif menu == "Modelos":
    st.title("Modelo")

    st.subheader("Regresión")
    st.write("Predicción de concentración de PM2.5 (ejemplo con Regresión Lineal, KNN, Random Forest).")

    st.subheader("Clasificación")
    st.write("Clasificación de calidad del aire según ICA (Buena, Moderada, Mala, Muy Mala).")

# ---------------- BASE DE DATOS ----------------
elif menu == "Base de Datos":
    st.title("Conexión a la Base de Datos")

    try:
        import pyodbc

        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;DATABASE=CalidadAire;UID=sa;PWD=tu_password"
        )
        st.success("✅ Conexión exitosa a la base de datos SQL Server")

        query = "SELECT TOP 5 * FROM Contaminantes"
        df_sql = pd.read_sql(query, conn)
        st.dataframe(df_sql)

        conn.close()
    except Exception as e:
        st.error(f"❌ Error en la conexión: {e}")

# ---------------- ACERCA DE ----------------
elif menu == "Acerca de":
    st.title("Acerca del Proyecto")

    st.markdown("""
    ## 🎯 Objetivo
    Diseñar y desarrollar un proyecto de **Ciencia de Datos en Python** enfocado en una problemática relevante para Costa Rica, como lo es el (análisis sobre la Calidad del Aire en el GAM), integrando diversas fuentes de datos como bases de datos relacionales, APIs públicas costarricenses e internacionales, y archivos csv reales. El proyecto incluirán un análisis exploratorio de datos (EDA), visualización de datos y la aplicación de algoritmos de machine learning supervisado. Todo el desarrollo se estructurará utilizando principios de programación orientada a objetos para fomentar buenas prácticas de diseño y mantenimiento del código.
    ## 👥 Integrantes
    - **Fernando Contreras Artavia**
    - **Victor Rojas Navarro**
    - **Johel Barquero Carvajal**
    ## 🛠️ Herramientas
    - **Python** (pandas, scikit-learn, matplotlib, seaborn, plotly, streamlit)
    - **SQL Server** para almacenamiento de datos
    - **Git/GitHub** para control de versiones
    ## 🚀 Conclusión
    El sistema integra **EDA, visualización avanzada, modelos ML y base de datos**
    en una aplicación interactiva con **Streamlit**.
    """)