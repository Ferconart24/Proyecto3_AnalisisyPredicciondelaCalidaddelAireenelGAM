# Proyecto3_AnalisisyPredicciondelaCalidaddelAireenelGAM
 Analizar la calidad del aire en el Gran Área Metropolitana  correlacionándola con datos de tráfico vehicular y condiciones meteorológicas  para predecir niveles de contaminación.

## ️Estructura del Proyecto
- `src/eda/`: clase **ProcesadorEDA** (EDA básico: estadísticas, correlaciones, histogramas, boxplots, etc).  
- `src/visualizacion/`: clase **Visualizador** (comparaciones por zona, relación clima-contaminantes, consumo por hora, correlaciones globales).  
- `src/modelos/`: modelos entrenados y script de prueba.  
- `data/processed/`: datasets procesados.  
- `models/`: modelos entrenados en formato `.pkl`.  
- `app.py`: aplicación central con **Streamlit**.  
- **Notebooks:**  
  1. `Entrenamiento_Modelos.ipynb`: Regresión y Clasificación (muestra los resultados de forma interactiva).  
  2. `exploracion_inicial.ipynb`  
  3. `Guia_ModeloML.ipynb`: Información rápida de los datasets.  
  4. `Predicciones_CalidadAire.ipynb`: Realizar predicciones desde un notebook.  
  5. `SQL Server.ipynb`: Demostración de cómo se crearon las tablas en SQL Server.

---
##  Variables de entrada para las predicciones

- `hora`
- `flujo_vehicular`
- `temperatura`
- `humedad`
- `viento`️
- `pm10: Material particulado fino `  ️
- `co: Monóxido de carbono` ️
- `no2: Dióxido de nitrógeno`
- `o3: Ozono a nivel del suelo` ️  

    ---

## Modelos de Machine Learning

- **Calidad del Aire** → predicción numérica de contaminación (ejemplo: 40.8).  
- **Regresión (PM2.5)** → concentración estimada de partículas PM2.5.  
- **Clasificación (ICA)** → categoría de calidad del aire:
  - `Buena`: Aire limpio.
  - `Moderada`: Aceptable.
  - `Mala`: Riesgo.
  - `Muy Mala`: Riesgo para toda la población. 