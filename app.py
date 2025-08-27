import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from pathlib import Path

# ---------------- Rutas ----------------
project_root = Path(__file__).resolve().parent
model_dir = project_root / "models"

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
        icons=["folder", "bar-chart", "bar-chart-line", "cpu", "database", "info-circle"],
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

        st.success(" Datasets cargados desde 'data/processed/'")
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
        st.error(" No se encontraron los archivos procesados.")

# ---------------- EDA ----------------
elif menu == "EDA":
    st.title(" Análisis Exploratorio de Datos (EDA)")

    if "contaminantes" in st.session_state and "flujo" in st.session_state and "clima" in st.session_state:
        from src.eda.ProcesadorEDA import ProcesadorEDA

        dfs = {
            "Contaminantes": st.session_state["contaminantes"],
            "FlujoVehicular": st.session_state["flujo"],
            "Clima": st.session_state["clima"]
        }

        # Crear tabla unificada
        df_unificado = dfs["Contaminantes"].merge(
            dfs["FlujoVehicular"], on="fecha", how="inner"
        ).merge(
            dfs["Clima"], on="fecha", how="inner"
        )
        dfs["TablaUnificada"] = df_unificado

        eda = ProcesadorEDA(dfs)

        dataset = st.selectbox(" Selecciona un dataset para analizar:", list(dfs.keys()))
        df = dfs[dataset]

        # Análisis clásico de EDA
        eda.info_general_df(dataset, df)
        eda.estadisticas_df(dataset, df)
        eda.histograma_df(dataset, df)
        eda.boxplot_df(dataset, df)
        eda.correlacion_df(dataset, df)

        eda.analisis_temporal(freq="D")
        eda.analisis_temporal(freq="W")

    else:
        st.warning("️ Primero carga los datos en 'Carga de Datos'.")

# ---------------- VISUALIZACIONES ----------------
elif menu == "Visualizaciones":
    st.title(" Visualizaciones personalizadas")

    if "contaminantes" in st.session_state and "flujo" in st.session_state and "clima" in st.session_state:
        df_cont = st.session_state["contaminantes"]
        df_flujo = st.session_state["flujo"]
        df_clima = st.session_state["clima"]

        from src.visualizacion.Visualizador import Visualizador
        vis = Visualizador(df_cont, df_flujo, df_clima)

        # Consumo promedio por hora
        st.markdown("### Promedio de contaminantes por hora del día")
        vis.consumo_hora_dia()

        #  Relación clima vs contaminantes
        st.markdown("###  Relación entre clima y contaminantes")
        vis.demanda_condiciones()

        # Correlaciones entre todas las variables
        st.markdown("###  Correlación entre clima, flujo vehicular y contaminantes")
        vis.correlaciones_clima()


    else:
        st.warning("️ Primero carga los datos en 'Carga de Datos'.")
        
# ---------------- MODELOS ----------------
elif menu == "Modelos":
    st.title("Modelos de Machine Learning")

    import joblib
    modelos = {
        "Calidad del Aire": "modelo_calidad_aire.pkl",
        "Regresión (PM2.5)": "modelo_regresion.pkl",
        "Clasificación (ICA)": "modelo_clasificacion.pkl"
    }

    st.subheader(" Ingresa los datos para la predicción")

    hora = st.slider("Hora del día", 0, 23, 12)
    flujo = st.number_input("Flujo vehicular", min_value=0, value=1800)
    temp = st.number_input("Temperatura (°C)", min_value=0.0, value=25.0)
    humedad = st.slider("Humedad (%)", 0, 100, 70)
    viento = st.number_input("Velocidad del viento (km/h)", min_value=0.0, value=7.0)
    pm10 = st.number_input("PM10", min_value=0.0, value=50.0)
    co = st.number_input("CO", min_value=0.0, value=1.0)
    no2 = st.number_input("NO2", min_value=0.0, value=80.0)
    o3 = st.number_input("O3", min_value=0.0, value=100.0)

    ejemplo = pd.DataFrame([{
        "hora": hora,
        "flujo_vehicular": flujo,
        "temperatura": temp,
        "humedad": humedad,
        "viento": viento,
        "pm10": pm10,
        "co": co,
        "no2": no2,
        "o3": o3
    }])

    if st.button(" Predecir"):
        for nombre, archivo in modelos.items():
            path = model_dir / archivo
            if path.exists():
                modelo = joblib.load(path)

                if hasattr(modelo, "feature_names_in_"):
                    for col in modelo.feature_names_in_:
                        if col not in ejemplo.columns:
                            ejemplo[col] = 0.0
                    ejemplo = ejemplo[modelo.feature_names_in_]

                pred = modelo.predict(ejemplo)[0]
                st.success(f" {nombre} → **{pred}**")
            else:
                st.error(f" Modelo no encontrado: {archivo}")

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
# Análisis y Predicción de la Calidad del Aire - GAM Costa Rica

## Objetivo
Desarrollar un sistema de análisis de datos para monitorear y predecir la calidad del aire en el Gran Área Metropolitana de Costa Rica, 
utilizando técnicas de ciencia de datos, machine learning y visualización interactiva.

## Equipo de Desarrollo
- **Fernando Contreras Artavia**
- **Victor Rojas Navarro** 
- **Johel Barquero Carvajal**

---

## ️Estructura del Proyecto
- `src/eda/`: clase **ProcesadorEDA** (EDA básico: estadísticas, correlaciones, histogramas, boxplots, etc).  
- `src/visualizacion/`: clase **Visualizador** (comparaciones por zona, relación clima-contaminantes, consumo por hora, correlaciones globales).  
- `src/modelos/`: modelos entrenados y script de prueba.  
- `data/processed/`: datasets procesados.  
- `models/`: modelos entrenados en formato `.pkl`.  
- `app.py`: aplicación central con **Streamlit**.  
- **Notebooks:**  
  1. `Entrenamiento_Modelos.ipynb`: Regresión y Clasificación (muestra los resultados de forma interactiva).  
  2. `exploracion_inicial.ipynb`  
  3. `Guia_ModeloML.ipynb`: Información rápida de los datasets.  
  4. `Predicciones_CalidadAire.ipynb`: Realizar predicciones desde un notebook.  
  5. `SQL Server.ipynb`: Demostración de cómo se crearon las tablas en SQL Server.

---
##  Variables de entrada para las predicciones

- `hora`
- `flujo_vehicular`
- `temperatura`
- `humedad`
- `viento`️
- `pm10: Material particulado fino `  ️
- `co: Monóxido de carbono` ️
- `no2: Dióxido de nitrógeno`
- `o3: Ozono a nivel del suelo` ️  

    ---

## Modelos de Machine Learning

- **Calidad del Aire** → predicción numérica de contaminación (ejemplo: 40.8).  
- **Regresión (PM2.5)** → concentración estimada de partículas PM2.5.  
- **Clasificación (ICA)** → categoría de calidad del aire:
  - `Buena`: Aire limpio.
  - `Moderada`: Aceptable.
  - `Mala`: Riesgo.
  - `Muy Mala`: Riesgo para toda la población.   

    ---

    ## Base de Datos
    - Clase `GestorBaseDatos` para conexión a **SQL Server** vía ODBC.  
    - Funcionalidades:
        - Conexión con autenticación Windows.  
        - Creación automática de tablas desde DataFrames.  
        - Inserción masiva de registros.  
        - Consultas SQL directas.  

    ---

    ## Conclusión
    Este proyecto integra en una **aplicación web interactiva**:
    - **EDA** (estadísticas y exploración de datos).    
    - **Modelos de Machine Learning** para predicciones.  
    - **Gestión de base de datos** en SQL Server.  

    Todo esto permite el **monitoreo y la predicción de la calidad del aire en Costa Rica.**  
    """)