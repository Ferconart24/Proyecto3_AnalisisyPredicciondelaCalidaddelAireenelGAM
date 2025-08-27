# Clase Utilidades: contiene funciones auxiliares reutilizables para validaciones, formateo, etc.



# src/helpers/Utilidades.py
import os
import unidecode
import pandas as pd
from pathlib import Path


class Utilidades:
    """
    Funciones auxiliares reutilizables para el proyecto:
    - Normalización de texto y columnas
    - Manejo de rutas y archivos
    - Funciones con fechas
    """

    # ===============================
    # TEXTOS Y COLUMNAS
    # ===============================
    @staticmethod
    def normalizar_texto(texto: str) -> str:
        """Quita tildes, pasa a minúsculas y elimina espacios extras"""
        return unidecode.unidecode(str(texto)).strip().lower()

    @staticmethod
    def normalizar_columnas(df: pd.DataFrame) -> pd.DataFrame:
        """Normaliza los nombres de las columnas de un DataFrame"""
        df = df.copy()
        df.columns = [Utilidades.normalizar_texto(col) for col in df.columns]
        return df

    # ===============================
    # RUTAS Y ARCHIVOS
    # ===============================
    @staticmethod
    def asegurar_directorio(path: str | Path):
        """Crea directorio si no existe"""
        Path(path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def validar_archivo(path: str | Path) -> bool:
        """Valida si un archivo existe"""
        return Path(path).exists()

    # ===============================
    # FECHAS
    # ===============================
    @staticmethod
    def extraer_anio(df: pd.DataFrame, col_fecha="fecha") -> pd.DataFrame:
        """Agrega columna 'anio' a partir de una columna de fecha"""
        if col_fecha in df.columns:
            df[col_fecha] = pd.to_datetime(df[col_fecha], errors="coerce")
            df["anio"] = df[col_fecha].dt.year
        return df

    @staticmethod
    def extraer_mes(df: pd.DataFrame, col_fecha="fecha") -> pd.DataFrame:
        """Agrega columna 'mes' a partir de una columna de fecha"""
        if col_fecha in df.columns:
            df[col_fecha] = pd.to_datetime(df[col_fecha], errors="coerce")
            df["mes"] = df[col_fecha].dt.month
        return df

    @staticmethod
    def extraer_dia_semana(df: pd.DataFrame, col_fecha="fecha") -> pd.DataFrame:
        """Agrega columna 'dia_semana' (0=Lunes, 6=Domingo)"""
        if col_fecha in df.columns:
            df[col_fecha] = pd.to_datetime(df[col_fecha], errors="coerce")
            df["dia_semana"] = df[col_fecha].dt.dayofweek
        return df
