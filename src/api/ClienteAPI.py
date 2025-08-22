# Clase ClienteAPI: realiza peticiones a APIs públicas y transforma los resultados en DataFrames.
'''
import requests
import pandas as pd

#Configuración
url = "https://air-quality-api.open-meteo.com/v1/air-quality" #url del API
params = {
    "latitude": 9.9281,
    "longitude": -84.0907,
    "hourly": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone",
    "appid": "d8d66d3c094782c020e3a2a9abdb1302"  # tu API key
}
#Descargar datos desde API
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print(" Datos descargados correctamente")
else:
    print(" Error en la solicitud:", response.status_code)
    exit()

df = pd.DataFrame(data["hourly"]) # Transformar a DataFrame


df["time"] = pd.to_datetime(df["time"], errors="coerce") # Convertir columna de tiempo a datetime


#Limpieza de datos nulos
print("Antes de limpieza:", df.shape)
df = df.dropna(how="any")  # eliminar filas con valores nulos
print("Después de limpieza:", df.shape)

#Guardar archivo limpio en data/processed
df.to_csv("data/processed/air_quality_clean.csv", index=False, encoding="utf-8")
print(" Archivo guardado en data/processed/air_quality_clean.csv")
import requests
import pandas as pd


#Configuración de open-meteo
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": 9.9281,
    "longitude": -84.0907,
    "start_date": "2024-08-15",
    "end_date": "2024-08-22",
    "hourly": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
}


#Descargar datos desde API
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print(" Datos descargados correctamente")
else:
    print("Error en la solicitud:", response.status_code)
    exit()


#Transformar a DataFrame
df = pd.DataFrame(data["hourly"])

#Convertir columna de tiempo a datetime
df["time"] = pd.to_datetime(df["time"], errors="coerce")

#Guardar archivo limpio
df.to_csv("data/processed/clima_historico.csv", index=False, encoding="utf-8")
print(" Archivo guardado en data/processed/clima_historico.csv")
'''
