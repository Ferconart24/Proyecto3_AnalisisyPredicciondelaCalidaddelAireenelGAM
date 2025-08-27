# src/datos/GestorDatos.py
import pandas as pd
import os
from src.helpers.Utilidades import Utilidades


class GestorDatos:
    """
    Clase encargada de:
    - Cargar archivos CSV desde data/raw o data/processed
    - Limpiar cada dataset (normalización de nombres, fechas, valores)
    - Unificar clima, flujo vehicular y contaminantes en una sola tabla
    """

    def __init__(self, ruta_raw: str = "data/raw", ruta_processed: str = "data/processed"):
        self.ruta_raw = ruta_raw
        self.ruta_processed = ruta_processed
        Utilidades.asegurar_directorio(self.ruta_raw)
        Utilidades.asegurar_directorio(self.ruta_processed)

    # ===============================
    # 1. Limpieza general
    # ===============================
    def limpiar_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normaliza columnas y aplica reglas básicas de limpieza"""
        df = Utilidades.normalizar_columnas(df)

        # Normalizar ubicación si existe
        if "ubicacion" in df.columns:
            df["ubicacion"] = df["ubicacion"].astype(str).apply(Utilidades.normalizar_texto)

        # Convertir fecha
        if "fecha" in df.columns:
            df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

        # Convertir hora
        if "hora" in df.columns:
            df["hora"] = pd.to_numeric(df["hora"], errors="coerce").fillna(0).astype(int)

        # Filtrar humedad
        if "humedad" in df.columns:
            df = df[df["humedad"].between(0, 100)]

        # Filtrar contaminantes negativos
        for col in ["pm2_5", "pm10", "co", "no2", "o3"]:
            if col in df.columns:
                df = df[df[col] >= 0]

        return df

    def guardar_csv(self, df: pd.DataFrame, nombre_archivo: str):
        path = os.path.join(self.ruta_processed, nombre_archivo)
        df.to_csv(path, index=False)
        print(f"✅ Archivo limpio guardado en {path}")

    # ===============================
    # 2. Carga de archivos
    # ===============================
    def cargar_csv(self, nombre_archivo: str, procesar: bool = True) -> pd.DataFrame:
        """
        Carga un CSV desde data/raw o data/processed.
        Si procesar=True, aplica limpieza.
        """
        path_raw = os.path.join(self.ruta_raw, nombre_archivo)
        path_proc = os.path.join(self.ruta_processed, nombre_archivo)

        path = path_raw if os.path.exists(path_raw) else path_proc
        if not os.path.exists(path):
            raise FileNotFoundError(f"❌ No se encontró {nombre_archivo} en raw ni processed")

        df = pd.read_csv(path)
        if procesar:
            df = self.limpiar_dataframe(df)
        return df

    # ===============================
    # 3. Procesamiento completo de un archivo
    # ===============================
    def procesar_archivo(self, nombre_archivo: str) -> pd.DataFrame:
        """
        Carga, limpia y guarda un CSV desde data/raw hacia data/processed.
        Retorna el DataFrame limpio.
        """
        df = self.cargar_csv(nombre_archivo)
        df_limpio = self.limpiar_dataframe(df)
        self.guardar_csv(df_limpio, nombre_archivo)
        return df_limpio

    # ===============================
    # 4. Unificación de datasets
    # ===============================
    def unificar(self, incluir_api: bool = True) -> pd.DataFrame:
        """
        Une flujo_vehicular + contaminantes + clima.
        Opcionalmente incluye clima_historico y air_quality_clean si existen.
        """
        try:
            df_flujo = self.cargar_csv("flujo_vehicular.csv")
            df_cont = self.cargar_csv("contaminantes.csv")
            df_clima = self.cargar_csv("clima.csv")
        except Exception as e:
            print("❌ Error cargando CSVs base:", e)
            return pd.DataFrame()

        # Merge principal por fecha y hora
        df_unificado = (
            df_flujo.merge(df_cont, on=["fecha", "hora"], how="inner")
                    .merge(df_clima, on=["fecha", "hora"], how="inner")
        )

        # Si existen, incluir datasets de API
        if incluir_api:
            try:
                df_air = self.cargar_csv("air_quality_clean.csv")
                if "time" in df_air.columns:
                    df_air = df_air.rename(columns={"time": "fecha"})
                df_unificado = df_unificado.merge(df_air, on="fecha", how="left")
            except FileNotFoundError:
                print("ℹ️ No se encontró air_quality_clean.csv")

            try:
                df_hist = self.cargar_csv("clima_historico.csv")
                if "time" in df_hist.columns:
                    df_hist = df_hist.rename(columns={"time": "fecha"})
                df_unificado = df_unificado.merge(df_hist, on="fecha", how="left")
            except FileNotFoundError:
                print("ℹ️ No se encontró clima_historico.csv")

        # Guardar tabla final
        self.guardar_csv(df_unificado, "TablaUnificada.csv")
        return df_unificado
