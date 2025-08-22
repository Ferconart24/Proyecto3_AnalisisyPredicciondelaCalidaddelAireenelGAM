#Clase GestorDatos: encargada de cargar, transformar y exportar archivos CSV, Excel, etc.

import pandas as pd
import unidecode
import os

class GestorDatos:
    def __init__(self, ruta_raw="../data/raw", ruta_processed="../data/processed"):
        self.ruta_raw = ruta_raw
        self.ruta_processed = ruta_processed

    def cargar_csv(self, nombre_archivo):
        path = os.path.join(self.ruta_raw, nombre_archivo)
        df = pd.read_csv(path)
        return df

    def normalizar_texto(self, texto):
        """Quita tildes, pasa a minúsculas y elimina espacios extras"""
        return unidecode.unidecode(str(texto)).strip().lower()

    def limpiar_dataframe(self, df):
        # Normalizar nombres de columnas
        df.columns = [self.normalizar_texto(col) for col in df.columns]

        # Normalizar ubicación si existe
        if "ubicacion" in df.columns:
            df["ubicacion"] = df["ubicacion"].apply(lambda x: self.normalizar_texto(x))

        # Convertir fecha a datetime si existe
        if "fecha" in df.columns:
            df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

        # Convertir hora a int
        if "hora" in df.columns:
            df["hora"] = pd.to_numeric(df["hora"], errors="coerce").fillna(0).astype(int)

        # Manejo de valores fuera de rango
        if "humedad" in df.columns:
            df = df[df["humedad"].between(0, 100)]

        if "pm2_5" in df.columns:
            df = df[df["pm2_5"] >= 0]

        if "pm10" in df.columns:
            df = df[df["pm10"] >= 0]

        return df

    def guardar_csv(self, df, nombre_archivo):
        path = os.path.join(self.ruta_processed, nombre_archivo)
        df.to_csv(path, index=False)
        print(f"✅ Archivo limpio guardado en {path}")

    def procesar_archivo(self, nombre_archivo):
        df = self.cargar_csv(nombre_archivo)
        df_limpio = self.limpiar_dataframe(df)
        self.guardar_csv(df_limpio, nombre_archivo)
        return df_limpio
