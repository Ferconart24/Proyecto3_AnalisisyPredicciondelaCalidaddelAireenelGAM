from src.datos.GestorDatos import GestorDatos

gd = GestorDatos()

# Procesar los 3 archivos
df_flujo = gd.procesar_archivo("flujo_vehicular.csv")
df_contaminantes = gd.procesar_archivo("contaminantes.csv")
df_clima = gd.procesar_archivo("clima.csv")
