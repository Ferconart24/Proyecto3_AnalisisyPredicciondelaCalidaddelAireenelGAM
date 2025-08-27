# src/modelos/ModeloML.py
import os
from pathlib import Path
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, f1_score

# Modelos
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

# Escalado y pipelines
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


# ---------- Utilidades ----------
def _resolve_csv_path(csv_path=None) -> Path:
    """Busca TablaUnificada.csv si no se pasa ruta."""
    if csv_path:
        return Path(csv_path).resolve()
    return Path(__file__).resolve().parents[2] / "data" / "processed" / "TablaUnificada.csv"


def _pm25_to_ica(pm25: float) -> str:
    """Convierte PM2.5 en categoría ICA."""
    if pm25 <= 12: return "Buena"
    elif pm25 <= 35.4: return "Moderada"
    elif pm25 <= 55.4: return "Mala"
    else: return "Muy Mala"


# ---------- Entrenamiento ----------
def entrenar_regresion(df: pd.DataFrame):
    X = df[["hora","flujo_vehicular","temperatura","humedad","viento","pm10","co","no2","o3"]]
    y = df["pm2_5"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelos = {
        "Lineal": Pipeline([
            ("scaler", StandardScaler()),
            ("model", LinearRegression())
        ]),
        "KNN": Pipeline([
            ("scaler", StandardScaler()),
            ("model", KNeighborsRegressor())
        ]),
        "Árbol": DecisionTreeRegressor(),
        "RandomForest": RandomForestRegressor(random_state=42),
    }

    resultados = {}
    mejor, mejor_score = None, -np.inf
    for nombre, modelo in modelos.items():
        modelo.fit(X_train, y_train)
        pred = modelo.predict(X_test)
        mse, r2 = mean_squared_error(y_test, pred), r2_score(y_test, pred)
        resultados[nombre] = {"MSE": mse, "R2": r2}
        if r2 > mejor_score:
            mejor, mejor_score = modelo, r2

    # Guardar modelo en carpeta raíz /models
    project_root = Path(__file__).resolve().parents[2]
    model_dir = project_root / "models"
    model_dir.mkdir(parents=True, exist_ok=True)
    modelo_path = model_dir / "modelo_regresion.pkl"

    joblib.dump(mejor, modelo_path)
    print("📊 Resultados regresión:", resultados)
    print(f"✅ Mejor regresor guardado en {modelo_path}")


def entrenar_clasificacion(df: pd.DataFrame):
    df["ica_categoria"] = df["pm2_5"].apply(_pm25_to_ica)
    X = df[["hora","flujo_vehicular","temperatura","humedad","viento","pm10","co","no2","o3"]]
    y = df["ica_categoria"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    modelos = {
        "Logística": Pipeline([
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=1000))  # más iteraciones
        ]),
        "KNN": Pipeline([
            ("scaler", StandardScaler()),
            ("model", KNeighborsClassifier())
        ]),
        "Árbol": DecisionTreeClassifier(),
        "RandomForest": RandomForestClassifier(random_state=42),
    }

    resultados = {}
    mejor, mejor_score = None, -np.inf
    for nombre, modelo in modelos.items():
        modelo.fit(X_train, y_train)
        pred = modelo.predict(X_test)
        acc, f1 = accuracy_score(y_test, pred), f1_score(y_test, pred, average="macro")
        resultados[nombre] = {"Accuracy": acc, "F1": f1}
        if acc > mejor_score:
            mejor, mejor_score = modelo, acc

    # Guardar modelo en carpeta raíz /models
    project_root = Path(__file__).resolve().parents[2]
    model_dir = project_root / "models"
    model_dir.mkdir(parents=True, exist_ok=True)
    modelo_path = model_dir / "modelo_clasificacion.pkl"

    joblib.dump(mejor, modelo_path)
    print("📊 Resultados clasificación:", resultados)
    print(f"✅ Mejor clasificador guardado en {modelo_path}")


# ---------- API principal ----------
def entrenar_modelo(csv_path=None, tarea="regresion"):
    df = pd.read_csv(_resolve_csv_path(csv_path))

    if tarea in ("regresion","ambos"):
        entrenar_regresion(df)
    if tarea in ("clasificacion","ambos"):
        entrenar_clasificacion(df)


# ---------- Ejecutar por consola ----------
if __name__ == "__main__":
    import sys
    tarea = sys.argv[1] if len(sys.argv) > 1 else "regresion"
    entrenar_modelo(tarea=tarea)
