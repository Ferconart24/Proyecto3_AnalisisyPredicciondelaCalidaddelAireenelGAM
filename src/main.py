from src.datos.GestorDatos import GestorDatos

gd = GestorDatos()

# Procesar los 3 archivos
df_flujo = gd.procesar_archivo("flujo_vehicular.csv")
df_contaminantes = gd.procesar_archivo("contaminantes.csv")
df_clima = gd.procesar_archivo("clima.csv")


'''
import requests

import pandas as pd

import os


class ClienteAPI:

    def __init__(self, lat=9.9281, lon=-84.0907, api_key=None):

        self.lat = lat

        self.lon = lon

        self.api_key = api_key

    def descargar_air_quality(self, ruta_salida="data/processed/air_quality_clean.csv"):

        """Descarga datos de calidad del aire y elimina nulos"""

        url = "https://air-quality-api.open-meteo.com/v1/air-quality"

        params = {

            "latitude": self.lat,

            "longitude": self.lon,

            "hourly": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone",

            "appid": self.api_key

        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise Exception(f"Error en API Air Quality: {response.status_code}")

        data = response.json()

        df = pd.DataFrame(data["hourly"])

        df["time"] = pd.to_datetime(df["time"], errors="coerce")

        # limpieza de nulos

        df = df.dropna(how="any")

        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

        df.to_csv(ruta_salida, index=False, encoding="utf-8")

        print(f" Air Quality guardado en {ruta_salida}")

    def descargar_clima_historico(self, start_date, end_date, ruta_salida="data/processed/clima_historico.csv"):

        """Descarga datos climáticos históricos sin limpieza adicional"""

        url = "https://archive-api.open-meteo.com/v1/archive"

        params = {

            "latitude": self.lat,

            "longitude": self.lon,

            "start_date": start_date,

            "end_date": end_date,

            "hourly": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"

        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise Exception(f"Error en API Archive: {response.status_code}")

        data = response.json()

        df = pd.DataFrame(data["hourly"])

        df["time"] = pd.to_datetime(df["time"], errors="coerce")

        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

        df.to_csv(ruta_salida, index=False, encoding="utf-8")

        print(f" Clima histórico guardado en {ruta_salida}")

if __name__ == "__main__":
    print("Proyecto iniciado")

    # Inicializar cliente

    cliente = ClienteAPI(api_key="d8d66d3c094782c020e3a2a9abdb1302")

    # Descargar Air Quality (con limpieza de nulos)

    cliente.descargar_air_quality()

    # Descargar clima histórico (rango de fechas ajustable)

    cliente.descargar_clima_historico(start_date="2024-08-15", end_date="2024-08-22")
'''


