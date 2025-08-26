# src/modelos/ModeloML.py
import os
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib


def _resolve_csv_path(csv_path: str | None = None) -> Path:
    if csv_path:
        p = Path(csv_path).expanduser().resolve()
        if p.exists():
            return p
        raise FileNotFoundError(f"No se encontró el archivo CSV en la ruta especificada: {p}")

    here = Path(__file__).resolve()
    project_root = here.parents[2]
    candidates = [
        project_root / "data" / "processed" / "TablaUnificada.csv",
        here.parents[1] / "data" / "processed" / "TablaUnificada.csv",
    ]
    for c in candidates:
        if c.exists():
            return c

    raise FileNotFoundError("No se encontró el archivo 'TablaUnificada.csv' en las ubicaciones esperadas.")


def entrenar_modelo(csv_path: str | None = None):
    # 1) Resolver ruta del CSV
    csv_file = _resolve_csv_path(csv_path)

    # 2) Cargar datos
    df = pd.read_csv(csv_file)

    # 3) Features y target
    X = df[[
        "hora", "flujo_vehicular", "pm10", "co", "no2", "o3",
        "temperatura", "humedad", "viento", "precipitacion"
    ]]
    y = df["pm2_5"]

    # 4) Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 5) Modelo
    modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    # 6) Evaluación
    y_pred = modelo.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("📊 Resultados del modelo Random Forest")
    print(f"➡️ MSE: {mse:.2f}")
    print(f"➡️ R²: {r2:.2f}")

    # 7) Guardar modelo
    project_root = Path(__file__).resolve().parents[2]
    model_dir = project_root / "models"
    model_dir.mkdir(parents=True, exist_ok=True)
    modelo_path = model_dir / "modelo_calidad_aire.pkl"
    joblib.dump(modelo, modelo_path)

    print(f"✅ Modelo guardado en {modelo_path}")
    return modelo


if __name__ == "__main__":
    entrenar_modelo()
