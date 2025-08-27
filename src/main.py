import os
from src.api.ClienteAPI import ClienteAPI
from src.datos.GestorDatos import GestorDatos
from src.basedatos.GestorBaseDatos import GestorBaseDatos
from src.modelos.ModeloML import entrenar_modelo


def main():
    # ------------------- RUTAS -------------------
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(BASE_DIR, "data", "raw")
    processed_dir = os.path.join(BASE_DIR, "data", "processed")

    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)

    # ------------------- 1. DESCARGAR DATOS DE APIs -------------------
    print("\n🔹 Paso 1: Descargando datos de APIs...")
    api = ClienteAPI()
    try:
        df_air = api.descargar_air_quality("2024-08-15", "2024-08-22")
        api.guardar_csv(df_air, "air_quality_clean.csv")

        df_clima_hist = api.descargar_clima_historico("2024-08-15", "2024-08-22")
        api.guardar_csv(df_clima_hist, "clima_historico.csv")
    except Exception as e:
        print(f"⚠️ Error al descargar desde API: {e}")
        print("Continuando solo con archivos locales...")

    # ------------------- 2. PROCESAR ARCHIVOS CSV -------------------
    print("\n🔹 Paso 2: Procesando CSVs locales...")
    gd = GestorDatos(ruta_raw=raw_dir, ruta_processed=processed_dir)

    df_flujo = gd.procesar_archivo("flujo_vehicular.csv")
    df_contaminantes = gd.procesar_archivo("contaminantes.csv")
    df_clima = gd.procesar_archivo("clima.csv")

    # ------------------- 3. CONEXIÓN A SQL SERVER -------------------
    print("\n🔹 Paso 3: Conexión a SQL Server...")
    gestor_db = GestorBaseDatos(
        server=r"DESKTOP-GQ1EGAS\JOHEL",   # 🔧 Ajusta con tu servidor SQL
        database="ContaminacionAire"       # 🔧 Ajusta con tu base de datos
    )
    gestor_db.conectar()

    # ------------------- 4. CREAR TABLAS -------------------
    print("\n🔹 Paso 4: Creando tablas...")
    gestor_db.crear_tabla_desde_dataframe(df_flujo, "FlujoVehicular")
    gestor_db.crear_tabla_desde_dataframe(df_contaminantes, "Contaminantes")
    gestor_db.crear_tabla_desde_dataframe(df_clima, "Clima")

    # ------------------- 5. INSERTAR DATOS -------------------
    print("\n🔹 Paso 5: Insertando datos...")
    gestor_db.insertar_dataframe(df_flujo, "FlujoVehicular")
    gestor_db.insertar_dataframe(df_contaminantes, "Contaminantes")
    gestor_db.insertar_dataframe(df_clima, "Clima")

    # ------------------- 6. CREAR TABLA UNIFICADA -------------------
    print("\n🔹 Paso 6: Creando Tabla Unificada...")
    df_unificado = df_flujo.merge(df_contaminantes, on=["fecha", "hora"]) \
                           .merge(df_clima, on=["fecha", "hora"])

    gestor_db.crear_tabla_desde_dataframe(df_unificado, "TablaUnificada")
    gestor_db.insertar_dataframe(df_unificado, "TablaUnificada")

    output_path = os.path.join(processed_dir, "TablaUnificada.csv")
    df_unificado.to_csv(output_path, index=False)

    print(f"✅ Archivo 'TablaUnificada.csv' guardado en {output_path}")
    print("✅ Inserción completada en la base de datos ContaminacionAire.")

    # ------------------- 7. ENTRENAR MODELO -------------------
    print("\n🔹 Paso 7: Entrenando modelo...")
    entrenar_modelo(csv_path=output_path)

    # ------------------- 8. CERRAR CONEXIÓN -------------------
    gestor_db.cerrar()


if __name__ == "__main__":
    main()


    
