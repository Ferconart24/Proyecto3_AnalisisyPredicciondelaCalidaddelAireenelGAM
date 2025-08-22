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