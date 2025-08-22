# Clase ModeloML: entrena y evalúa modelos supervisados (regresión o clasificación).


import pandas as pd
import numpy as np
from sklearn import model_selection
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold, train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

# ================================
# 1. Cargar datos
# ================================
df_data = pd.read_csv("data/processed/air_quality_merged.csv")

# Variable objetivo: clasificación ICA (ejemplo)
y = df_data["categoria_ica"]

# Variables predictoras
df_X = df_data.drop(["categoria_ica"], axis=1)

# Convertir variables categóricas a dummies
df_X = pd.get_dummies(df_X)

# ================================
# 2. Train/Test Split
# ================================
X = df_X.values
y = y.values
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ================================
# 3. Escalado
# ================================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ================================
# 4. Benchmarking modelos
# ================================
models = [
    ("LR", LogisticRegression(max_iter=1000)),
    ("LDA", LinearDiscriminantAnalysis()),
    ("KNN", KNeighborsClassifier()),
    ("CART", DecisionTreeClassifier()),
    ("NB", GaussianNB()),
    ("SVM", SVC())
]

results = []
names = []
print(" Resultados Benchmarking:")
for name, model in models:
    kf = KFold(n_splits=10, shuffle=True, random_state=42)
    cv_results = model_selection.cross_val_score(model, X_scaled, y, cv=kf)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)

# ================================
# 5. Selección de mejor modelo (ejemplo con SVM)
# ================================
svc = SVC()
param_grid = {"C": [0.1, 1, 10], "gamma": [0.01, 0.1, 1]}
svc_cv = GridSearchCV(svc, param_grid, cv=5)
svc_cv.fit(X_train, y_train)

print(" Mejor modelo SVM:", svc_cv.best_params_)
print(" Accuracy (CV):", svc_cv.best_score_)

# ================================
# 6. Predicción sobre nuevos datos
# ================================
df_new = pd.read_csv("data/processed/nuevos_datos.csv")
df_X_new = pd.get_dummies(df_new)
X_new = df_X_new.values
y_prediction = svc_cv.predict(X_new)

print(" Predicciones:", y_prediction)