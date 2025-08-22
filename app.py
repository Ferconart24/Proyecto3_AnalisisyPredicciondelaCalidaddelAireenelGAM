import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

#from src.visualizacion.Visualizador import Visualizador
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

    if "contaminantes" in st.session_state and "flujo" in st.session_state and "clima" in st.session_state:
        dfs = {
            "Contaminantes": st.session_state["contaminantes"],
            "FlujoVehicular": st.session_state["flujo"],
            "Clima": st.session_state["clima"]
        }

        # ✅ Crear tabla unificada
        df_unificado = dfs["Contaminantes"].merge(
            dfs["FlujoVehicular"], on="fecha", how="inner"
        ).merge(
            dfs["Clima"], on="fecha", how="inner"
        )
        dfs["TablaUnificada"] = df_unificado

        from src.eda.ProcesadorEDA import ProcesadorEDA
        eda = ProcesadorEDA(dfs)

        # Selección de dataset
        dataset = st.selectbox("📂 Selecciona un dataset para analizar:", list(dfs.keys()))
        df = dfs[dataset]

        # Mostrar análisis
        st.subheader(f"📊 Análisis del dataset: {dataset}")
        eda.info_general_df(dataset, df)
        eda.estadisticas_df(dataset, df)
        eda.histograma_df(dataset, df)
        eda.boxplot_df(dataset, df)
        eda.correlacion_df(dataset, df)

        # 📈 Solo análisis temporal
        eda.analisis_temporal(freq="D")
        eda.analisis_temporal(freq="W")

    else:
        st.warning("Primero carga los datos en 'Carga de Datos'.")

# ---------------- VISUALIZACIONES ----------------
elif menu == "Visualizaciones":
    st.title("📊 Visualizaciones Interactivas - Calidad del Aire")

    try:
        # Cargar el dataset unificado
        df = pd.read_csv("data/processed/TablaUnificada.csv", parse_dates=["fecha"])

        st.success("✅ Datos cargados correctamente desde TablaUnificada.csv")
        st.dataframe(df.head())

        import plotly.express as px

        # --- Gráfico 1: Correlación flujo vehicular vs PM2.5 ---
        st.subheader(" Flujo vehicular vs PM2.5")
        fig1 = px.scatter(df, x="flujo_vehicular", y="pm2_5", color="ubicacion",
                          title="Correlación entre flujo vehicular y PM2.5",
                          trendline="ols")
        st.plotly_chart(fig1, use_container_width=True)

        # --- Gráfico 2: Correlación flujo vehicular vs NO2 ---
        st.subheader(" Flujo vehicular vs NO2")
        fig2 = px.scatter(df, x="flujo_vehicular", y="no2", color="ubicacion",
                          title="Correlación entre flujo vehicular y NO2",
                          trendline="ols")
        st.plotly_chart(fig2, use_container_width=True)

        # --- Gráfico 3: Análisis temporal de PM2.5 y NO2 ---
        st.subheader(" Evolución temporal de PM2.5 y NO2")
        df_temp = df.groupby("fecha")[["pm2_5", "no2"]].mean().reset_index()
        fig3 = px.line(df_temp, x="fecha", y=["pm2_5", "no2"],
                       title="Tendencia diaria de PM2.5 y NO2")
        st.plotly_chart(fig3, use_container_width=True)

        # --- Gráfico 4: Mapa de calor por ubicación (PM2.5) ---
        st.subheader(" Mapa de calor de PM2.5 por ubicación")
        df_heat = df.groupby(["ubicacion", "fecha"])["pm2_5"].mean().reset_index()
        fig4 = px.density_heatmap(df_heat, x="fecha", y="ubicacion", z="pm2_5",
                                  color_continuous_scale="YlOrRd",
                                  title="Mapa de calor de PM2.5")
        st.plotly_chart(fig4, use_container_width=True)

        # --- Gráfico 5: Dispersión clima vs contaminantes ---
        st.subheader("️ Dispersión clima vs PM2.5")
        fig5 = px.scatter(df, x="temperatura", y="pm2_5", color="humedad",
                          title="PM2.5 en función de Temperatura y Humedad")
        st.plotly_chart(fig5, use_container_width=True)

        st.subheader("️ Dispersión clima vs NO2")
        fig6 = px.scatter(df, x="temperatura", y="no2", color="humedad",
                          title="NO2 en función de Temperatura y Humedad")
        st.plotly_chart(fig6, use_container_width=True)

    except FileNotFoundError:
        st.error("❌ No se encontró el archivo TablaUnificada.csv en data/processed/")
# ---------------- MODELOS ----------------
elif menu == "Modelos":
    st.title("Modelo")

    st.subheader("Regresión")
    st.write("Predicción de concentración de PM2.5 (ejemplo con Regresión Lineal, KNN, Random Forest).")

    st.subheader("Clasificación")
    st.write("Clasificación de calidad del aire según ICA (Buena, Moderada, Mala, Muy Mala).")

# ---------------- BASE DE DATOS ----------------
elif menu == "Base de Datos":
    st.title("Código de Conexión a la Base de Datos")

    codigo_sql = """import pyodbc
import pandas as pd

class GestorBaseDatos:
    def __init__(self, server, database):
        self.conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};DATABASE={database};Trusted_Connection=yes;"
        )
        self.conn = None

    def conectar(self):
        try:
            self.conn = pyodbc.connect(self.conn_str)
            print("✅ Conexión establecida con SQL Server (Windows Authentication)")
        except Exception as e:
            self.conn = None
            print("❌ Error en la conexión:", e)

    def crear_tabla_desde_dataframe(self, df, tabla):
        if not self.conn:
            print("❌ No hay conexión activa.")
            return

        cursor = self.conn.cursor()
        tipo_sql = {
            "int64": "INT",
            "float64": "FLOAT",
            "object": "NVARCHAR(255)",
            "bool": "BIT",
            "datetime64[ns]": "DATETIME"
        }

        columnas_sql = []
        for col, dtype in df.dtypes.items():
            if col.lower() == "fecha":
                columnas_sql.append(f"[{col}] DATE")
            elif col.lower() == "hora":
                columnas_sql.append(f"[{col}] INT")
            else:
                columnas_sql.append(f"[{col}] {tipo_sql.get(str(dtype), 'NVARCHAR(255)')}")

        columnas_sql_str = ", ".join(columnas_sql)
        query = f\"\"\" 
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = '{tabla}')
        CREATE TABLE {tabla} (
            id INT IDENTITY(1,1) PRIMARY KEY,
            {columnas_sql_str}
        )
        \"\"\"
        cursor.execute(query)
        self.conn.commit()

    def insertar_dataframe(self, df, tabla):
        if not self.conn:
            print("❌ No hay conexión activa.")
            return
        cursor = self.conn.cursor()
        columnas = ",".join([f"[{c}]" for c in df.columns])
        placeholders = ",".join("?" * len(df.columns))
        query = f"INSERT INTO {tabla} ({columnas}) VALUES ({placeholders})"
        data = [tuple(row) for row in df.to_numpy()]
        cursor.executemany(query, data)
        self.conn.commit()

    def consultar(self, query):
        if not self.conn:
            print("❌ No hay conexión activa.")
            return pd.DataFrame()
        return pd.read_sql(query, self.conn)

    def cerrar(self):
        if self.conn:
            self.conn.close()
            self.conn = None
"""

    # Mostrar el código en Streamlit con formato Python
    st.code(codigo_sql, language="python")

# ---------------- ACERCA DE ----------------
elif menu == "Acerca de":
    st.title("Acerca del Proyecto")

    st.markdown("""
    # ️ Análisis de Calidad del Aire - GAM Costa Rica

    ##  Objetivo
    Desarrollar un sistema de análisis de datos para monitorear y predecir la calidad del aire en el Gran Área Metropolitana de Costa Rica, utilizando técnicas de ciencia de datos y machine learning.

    ##  Equipo de Desarrollo
    - **Fernando Contreras Artavia**
    - **Victor Rojas Navarro** 
    - **Johel Barquero Carvajal**

    ##  Tecnologías Utilizadas
    - **Python**: pandas, scikit-learn, matplotlib, seaborn, plotly, streamlit
    - **Base de Datos**: SQL Server
    - **Control de Versiones**: Git/GitHub
    - **APIs**: Datos ambientales públicos de Costa Rica 

    ##  Características del Proyecto
    - **Análisis Exploratorio de Datos (EDA)** de calidad del aire
    - **Visualizaciones interactivas** con gráficos y mapas
    - **Modelos de Machine Learning** para predicciones
    - **Integración de múltiples fuentes** de datos 
    - **Aplicación web** desarrollada con Streamlit

    ##  Impacto
    Este proyecto busca proporcionar herramientas accesibles para el monitoreo ambiental, contribuyendo a la toma de decisiones informadas sobre la calidad del aire en Costa Rica.

    ##  Conclusión
    El sistema integra **análisis exploratorio de datos (EDA)**, **visualización avanzada**, **modelos de machine learning** y **gestión de base de datos** en una aplicación interactiva desarrollada con **Streamlit**. Esta solución completa permite el monitoreo y la predicción de la calidad del aire.

    """)