import joblib
from pathlib import Path
import pandas as pd

# Ruta al modelo (sube 2 niveles desde src/modelos)
project_root = Path(__file__).resolve().parents[2]
modelo_path = project_root / "models" / "modelo_calidad_aire.pkl"

# Cargar modelo
modelo = joblib.load(modelo_path)

# Crear ejemplo de entrada
ejemplo = pd.DataFrame([{
    "hora": 8,
    "flujo_vehicular": 1500,
    "pm10": 45.0,
    "co": 0.9,
    "no2": 70,
    "o3": 120,
    "temperatura": 25.0,
    "humedad": 80,
    "viento": 10.0,
    "precipitacion": 2.0
}])

# Predicción
pred = modelo.predict(ejemplo)
print(f"✅ Predicción de PM2.5: {pred[0]:.2f}")
