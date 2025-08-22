# src/eda/ProcesadorEDA.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


class ProcesadorEDA:
    def __init__(self, dfs: dict):
        self.dfs = dfs

    # ===============================
    # INFO GENERAL Y ESTADÍSTICAS
    # ===============================
    def info_general_df(self, nombre, df):
        st.subheader(f"📄 Información general - {nombre}")
        st.text(f"Shape: {df.shape}")
        st.write("Tipos de datos:")
        st.write(df.dtypes)
        st.write("Valores nulos:")
        st.write(df.isnull().sum())
        st.dataframe(df.head())

    def estadisticas_df(self, nombre, df):
        st.subheader(f"📊 Estadísticas descriptivas - {nombre}")
        st.dataframe(df.describe(include="all"))

    # ===============================
    # VISUALIZACIONES
    # ===============================
    def histograma_df(self, nombre, df):
        num_cols = df.select_dtypes(include="number").columns
        if len(num_cols) == 0:
            return
        st.subheader(f"📈 Histogramas - {nombre}")
        fig, ax = plt.subplots(figsize=(12, 8))
        df[num_cols].hist(ax=ax, bins=30)
        st.pyplot(fig)

    def boxplot_df(self, nombre, df):
        num_cols = df.select_dtypes(include="number").columns
        if len(num_cols) == 0:
            return
        st.subheader(f"📦 Boxplots - {nombre}")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(data=df[num_cols], ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    def correlacion_df(self, nombre, df):
        num_cols = df.select_dtypes(include="number").columns
        if len(num_cols) == 0:
            return
        st.subheader(f"🔗 Matriz de correlación - {nombre}")
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
        st.pyplot(fig)

    # ===============================
    # ANÁLISIS TEMPORAL
    # ===============================
    def analisis_temporal(self, freq="D", fecha_col="fecha", variable="PM2.5"):
        st.subheader(f"📈 Análisis temporal ({freq}) - {variable}")
        for nombre, df in self.dfs.items():
            if fecha_col not in df.columns or variable not in df.columns:
                continue
            df[fecha_col] = pd.to_datetime(df[fecha_col])
            serie = df.set_index(fecha_col)[variable].resample(freq).mean()
            fig, ax = plt.subplots(figsize=(12, 6))
            serie.plot(ax=ax)
            ax.set_title(f"{variable} - {nombre} ({freq})")
            st.pyplot(fig)

    # ===============================
    # HEATMAP POR ZONAS
    # ===============================
    def mapa_calor_zonas(self, df_name="Contaminantes", zona_col="zona", variable="PM2.5"):
        st.subheader("🗺️ Mapa de calor por zonas")
        if df_name not in self.dfs:
            return
        df = self.dfs[df_name]
        if zona_col not in df.columns or variable not in df.columns or "fecha" not in df.columns:
            return

        df["fecha"] = pd.to_datetime(df["fecha"])
        tabla = df.pivot_table(values=variable, index=df["fecha"].dt.month, columns=zona_col, aggfunc="mean")

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(tabla, cmap="coolwarm", annot=True, fmt=".1f", ax=ax)
        ax.set_title(f"Mapa de calor {variable} por zonas y meses")
        st.pyplot(fig)