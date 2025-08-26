# Clase ClienteAPI: realiza peticiones a APIs públicas y transforma los resultados en DataFrames.
# src/api/ClienteAPI.py
import requests
import pandas as pd
from pathlib import Path


class ClienteAPI:
    """
    Cliente para descargar datos de calidad del aire y clima histórico
    desde Open-Meteo (no requiere API key).
    """

    def __init__(self, base_dir: str = "data/processed", lat: float = 9.9281, lon: float = -84.0907):
        self.lat = lat
        self.lon = lon
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def descargar_air_quality(self, start: str, end: str) -> pd.DataFrame:
        """
        Descarga calidad del aire horario (PM10, PM2.5, CO, NO2, O3).
        Formato fechas: 'YYYY-MM-DD'
        """
        url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        params = {
            "latitude": self.lat,
            "longitude": self.lon,
            "hourly": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone",
            "start_date": start,
            "end_date": end,
            "timezone": "America/Costa_Rica"
        }
        r = requests.get(url, params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
        df = pd.DataFrame(data["hourly"])
        df["time"] = pd.to_datetime(df["time"], errors="coerce")
        return df.dropna()

    def descargar_clima_historico(self, start: str, end: str) -> pd.DataFrame:
        """
        Descarga clima histórico (temperatura, humedad, precipitación, viento).
        Formato fechas: 'YYYY-MM-DD'
        """
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": self.lat,
            "longitude": self.lon,
            "start_date": start,
            "end_date": end,
            "hourly": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
            "timezone": "America/Costa_Rica"
        }
        r = requests.get(url, params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
        df = pd.DataFrame(data["hourly"])
        df["time"] = pd.to_datetime(df["time"], errors="coerce")
        return df.dropna()

    def guardar_csv(self, df: pd.DataFrame, nombre: str) -> Path:
        """
        Guarda un DataFrame en data/processed.
        """
        path = self.base_dir / nombre
        df.to_csv(path, index=False, encoding="utf-8")
        print(f"✅ Archivo guardado en {path}")
        return path
