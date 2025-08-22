# src/modelos/ModeloML.py
import os
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib


def _resolve_csv_path(csv_path: str | None) -> Path:
    """
    Resolve the CSV path robustly.
    - If csv_path is given, use it (after resolving to absolute).
    - Otherwise, try common locations:
        1) <project_root>/data/processed/TablaUnificada.csv
        2) <src>/data/processed/TablaUnificada.csv (legacy fallback)
    """
    if csv_path:
        p = Path(csv_path).expanduser().resolve()
        if p.exists():
            return p
        raise FileNotFoundError(f"No se encontró el archivo CSV en la ruta especificada: {p}")

    here = Path(__file__).resolve()
    # here.parents[0] = .../src/modelos
    # here.parents[1] = .../src
    # here.parents[2] = .../<project_root>
    project_root = here.parents[2]
    candidates = [
        project_root / "data" / "processed" / "TablaUnificada.csv",
        here.parents[1] / "data" / "processed" / "TablaUnificada.csv",  # fallback: src/data/processed
    ]
    for c in candidates:
        if c.exists():
            return c

    raise FileNotFoundError(
        "No se encontró el archivo 'TablaUnificada.csv' en las ubicaciones esperadas:\n"
        f"- {candidates[0]}\n"
        f"- {candidates[1]}\n\n"
        "Sugerencias:\n"
        "1) Genere el CSV procesado con su pipeline de datos y ubíquelo en data/processed/TablaUnificada.csv (en la raíz del proyecto).\n"
        "2) O llame entrenar_modelo(csv_path='ruta/al/archivo.csv') para proveer la ruta explícitamente."
    )


def entrenar_modelo(csv_path: str | None = None):
    # 1) Resolver ruta del CSV
    csv_file = _resolve_csv_path(csv_path)

    # 2) Cargar el CSV combinado
    df = pd.read_csv(csv_file)

    # 3) Validar columnas requeridas antes de entrenar
    required_cols = [
        "hora", "flujo_vehicular", "pm10", "co", "no2", "o3",
        "temperatura", "humedad", "viento", "precipitacion", "pm2_5"
    ]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(
            "Faltan columnas requeridas en el CSV para entrenar el modelo: "
            f"{missing}. Asegúrese de que el proceso de limpieza/unificación "
            "genere estas columnas con los nombres correctos."
        )

    # 4) Variables de entrada (X) y salida (y)
    X = df[[
        "hora", "flujo_vehicular", "pm10", "co", "no2", "o3",
        "temperatura", "humedad", "viento", "precipitacion"
    ]]
    y = df["pm2_5"]

    # 5) Partición de datos
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 6) Modelo
    modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    # 7) Evaluación
    y_pred = modelo.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"MSE: {mse:.2f}")
    print(f"R²: {r2:.2f}")

    # 8) Guardar modelo en <project_root>/models/modelo_calidad_aire.pkl
    project_root = Path(__file__).resolve().parents[2]
    model_dir = project_root / "models"
    model_dir.mkdir(parents=True, exist_ok=True)
    modelo_path = model_dir / "modelo_calidad_aire.pkl"
    joblib.dump(modelo, modelo_path)
    print(f"✅ Modelo guardado en {modelo_path}")
