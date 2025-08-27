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

    # ==============================
    # 1. PM2.5 promedio por hora del día
    # ==============================
    def consumo_hora_dia(self):
        if "hora" in self.df_cont.columns and "pm2_5" in self.df_cont.columns:
            promedio = self.df_cont.groupby("hora")["pm2_5"].mean()
            fig, ax = plt.subplots(figsize=(10, 6))
            promedio.plot(kind="bar", ax=ax, color="skyblue")
            ax.set_title("Promedio de PM2.5 por hora del día")
            ax.set_xlabel("Hora")
            ax.set_ylabel("PM2.5 (µg/m³)")
            st.pyplot(fig)

    # ==============================
    # 2. Dispersión PM2.5 vs Temperatura
    # ==============================
    def demanda_condiciones(self):
        if "temperatura" in self.df_clima.columns and "pm2_5" in self.df_cont.columns:
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.scatterplot(
                x=self.df_clima["temperatura"],
                y=self.df_cont["pm2_5"],
                alpha=0.6, ax=ax
            )
            ax.set_title("Relación entre Temperatura y PM2.5")
            ax.set_xlabel("Temperatura (°C)")
            ax.set_ylabel("PM2.5 (µg/m³)")
            st.pyplot(fig)

    # ==============================
    # 3. Heatmap de correlaciones entre variables numéricas
    # ==============================
    def correlaciones_clima(self):
        try:
            df = self.df_cont.merge(self.df_flujo, on="fecha", how="inner").merge(
                self.df_clima, on="fecha", how="inner"
            )
            num_cols = df.select_dtypes(include="number").columns
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.heatmap(df[num_cols].corr(), annot=False, cmap="viridis", ax=ax)
            ax.set_title("Matriz de correlaciones")
            st.pyplot(fig)
        except Exception as e:
            st.error(f" Error al generar correlación: {e}")

    # ==============================
    # 4. Promedio de flujo vehicular por ubicación
    # ==============================
    def flujo_por_ubicacion(self):
        if "ubicacion" in self.df_flujo.columns and "flujo_vehicular" in self.df_flujo.columns:
            promedio_ubicacion = self.df_flujo.groupby("ubicacion")["flujo_vehicular"].mean()

            fig, ax = plt.subplots(figsize=(8, 6))
            promedio_ubicacion.sort_values().plot(kind="barh", ax=ax, color="salmon")
            ax.set_title("Promedio de flujo vehicular por ubicación")
            ax.set_xlabel("Flujo vehicular promedio")
            ax.set_ylabel("Ubicación")
            st.pyplot(fig)
        else:
            st.warning("️ No existe la columna 'ubicacion' en flujo vehicular.")
