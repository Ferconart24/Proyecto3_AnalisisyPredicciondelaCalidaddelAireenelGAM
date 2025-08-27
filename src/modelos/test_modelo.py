# src/modelos/test_modelo.py
import joblib
from pathlib import Path
import pandas as pd

# Ruta al directorio de modelos
project_root = Path(__file__).resolve().parents[2]
model_dir = project_root / "models"


def probar_modelo(path, ejemplo, tipo):
    if path.exists():
        modelo = joblib.load(path)

        # Ajustar columnas automáticamente
        if hasattr(modelo, "feature_names_in_"):
            for col in modelo.feature_names_in_:
                if col not in ejemplo.columns:
                    ejemplo[col] = 0.0
            # reordenar columnas en el mismo orden del entrenamiento
            ejemplo = ejemplo[modelo.feature_names_in_]

        pred = modelo.predict(ejemplo)
        print(f"✅ {tipo} → Predicción: {pred[0]}")
    else:
        print(f"⚠️ No se encontró el modelo: {path.name}")


# ===========================
# 1. Probar modelo CALIDAD DEL AIRE
# ===========================
modelo_calidad_aire = model_dir / "modelo_calidad_aire.pkl"
ejemplo_calidad_aire = pd.DataFrame([{
    "hora": 12,
    "flujo_vehicular": 1800,
    "temperatura": 26.0,
    "humedad": 70,
    "viento": 7.0,
    "pm10": 50.0,
    "co": 1.0,
    "no2": 80,
    "o3": 100
}])
probar_modelo(modelo_calidad_aire, ejemplo_calidad_aire, "Calidad del Aire")


# ===========================
# 2. Probar REGRESIÓN (pm2_5)
# ===========================
modelo_regresion = model_dir / "modelo_regresion.pkl"
ejemplo_reg = pd.DataFrame([{
    "hora": 8,
    "flujo_vehicular": 1500,
    "temperatura": 25.0,
    "humedad": 80,
    "viento": 10.0,
    "pm10": 45.0,
    "co": 0.9,
    "no2": 70,
    "o3": 120
}])
probar_modelo(modelo_regresion, ejemplo_reg, "Regresión (PM2.5)")


# ===========================
# 3. Probar CLASIFICACIÓN (ICA)
# ===========================
modelo_clasificacion = model_dir / "modelo_clasificacion.pkl"
ejemplo_clf = pd.DataFrame([{
    "hora": 5,  #Se puede cambiar la hora para ver el comportamiento por ejemplo a las 18 es mala pero a las 5 es moderada
    "flujo_vehicular": 2200,
    "temperatura": 27.0,
    "humedad": 65,
    "viento": 5.0,
    "pm10": 80.0,
    "co": 1.2,
    "no2": 100,
    "o3": 90
}])
probar_modelo(modelo_clasificacion, ejemplo_clf, "Clasificación (ICA)")

