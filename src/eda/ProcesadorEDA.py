import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

class ProcesadorEDA:
    def __init__(self, dfs: dict):
        self.dfs = dfs

    def info_general_df(self, nombre, df):
        st.subheader(f" Información general - {nombre}")
        st.text(f"Shape: {df.shape}")
        st.write("Tipos de datos:", df.dtypes)
        st.write("Valores nulos:", df.isnull().sum())
        st.dataframe(df.head())

    def estadisticas_df(self, nombre, df):
        st.subheader(f" Estadísticas - {nombre}")
        st.dataframe(df.describe(include="all"))

    def histograma_df(self, nombre, df):
        num_cols = df.select_dtypes(include="number").columns
        if len(num_cols) == 0: return
        st.subheader(f" Histogramas - {nombre}")
        fig = df[num_cols].hist(bins=30, figsize=(12, 8))
        st.pyplot(fig[0][0].figure)

    def boxplot_df(self, nombre, df):
        num_cols = df.select_dtypes(include="number").columns
        if len(num_cols) == 0: return
        st.subheader(f" Boxplots - {nombre}")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(data=df[num_cols], ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    def correlacion_df(self, nombre, df):
        num_cols = df.select_dtypes(include="number").columns
        if len(num_cols) == 0: return
        st.subheader(f" Matriz de correlación - {nombre}")
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
        st.pyplot(fig)

    def analisis_temporal(self, freq="D", fecha_col="fecha", variable="PM2.5"):
        st.subheader(f" Serie temporal {variable} ({freq})")
        for nombre, df in self.dfs.items():
            if fecha_col not in df.columns or variable not in df.columns:
                continue
            df[fecha_col] = pd.to_datetime(df[fecha_col], errors="coerce")
            serie = df.set_index(fecha_col)[variable].resample(freq).mean()
            fig, ax = plt.subplots(figsize=(12, 6))
            serie.plot(ax=ax)
            ax.set_title(f"{variable} - {nombre} ({freq})")
            st.pyplot(fig)
