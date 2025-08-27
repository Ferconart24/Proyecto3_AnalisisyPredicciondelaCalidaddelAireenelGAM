# src/visualizacion/Visualizador.py
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd

class Visualizador:
    def __init__(self, df_cont, df_flujo, df_clima):
        self.df_cont = df_cont
        self.df_flujo = df_flujo
        self.df_clima = df_clima

    def consumo_hora_dia(self):
        if "hora" in self.df_cont.columns and "pm2_5" in self.df_cont.columns:
            promedio = self.df_cont.groupby("hora")["pm2_5"].mean()
            fig, ax = plt.subplots(figsize=(10, 6))
            promedio.plot(kind="bar", ax=ax, color="skyblue")
            ax.set_ylabel("PM2.5")
            st.pyplot(fig)

    def demanda_condiciones(self):
        if "temperatura" in self.df_clima.columns and "pm2_5" in self.df_cont.columns:
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.scatterplot(
                x=self.df_clima["temperatura"],
                y=self.df_cont["pm2_5"],
                alpha=0.6, ax=ax
            )
            st.pyplot(fig)

    def correlaciones_clima(self):
        try:
            df = self.df_cont.merge(self.df_flujo, on="fecha", how="inner").merge(
                self.df_clima, on="fecha", how="inner"
            )
            num_cols = df.select_dtypes(include="number").columns
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.heatmap(df[num_cols].corr(), annot=False, cmap="viridis", ax=ax)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"❌ Error al generar correlación: {e}")


