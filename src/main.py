import os
from src.datos.GestorDatos import GestorDatos
from src.basedatos.GestorBaseDatos import GestorBaseDatos

def main():
    # ------------------- PROCESAR ARCHIVOS CSV -------------------
    gd = GestorDatos()

    df_flujo = gd.procesar_archivo("flujo_vehicular.csv")
    df_contaminantes = gd.procesar_archivo("contaminantes.csv")
    df_clima = gd.procesar_archivo("clima.csv")

    # ------------------- CONEXIÓN A SQL SERVER -------------------
    gestor_db = GestorBaseDatos(
        server=r"DESKTOP-GQ1EGAS\JOHEL",   # Servidor SQL
        database="ContaminacionAire"       # Base de datos destino
    )
    gestor_db.conectar()

    # ------------------- CREACIÓN DE TABLAS ORIGINALES -------------------
    gestor_db.crear_tabla_desde_dataframe(df_flujo, "FlujoVehicular")
    gestor_db.crear_tabla_desde_dataframe(df_contaminantes, "Contaminantes")
    gestor_db.crear_tabla_desde_dataframe(df_clima, "Clima")

    # ------------------- INSERCIÓN DE DATOS ORIGINALES -------------------
    gestor_db.insertar_dataframe(df_flujo, "FlujoVehicular")
    gestor_db.insertar_dataframe(df_contaminantes, "Contaminantes")
    gestor_db.insertar_dataframe(df_clima, "Clima")

    # ------------------- CREACIÓN DE TABLA UNIFICADA -------------------
    df_unificado = df_flujo.merge(df_contaminantes, on=["fecha", "hora"]) \
                           .merge(df_clima, on=["fecha", "hora"])

    gestor_db.crear_tabla_desde_dataframe(df_unificado, "TablaUnificada")
    gestor_db.insertar_dataframe(df_unificado, "TablaUnificada")

    # ------------------- GUARDAR TABLA UNIFICADA EN data/processed -------------------
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))   # sube un nivel desde src/
    output_path = os.path.join(BASE_DIR, "data", "processed", "TablaUnificada.csv")
    df_unificado.to_csv(output_path, index=False)

    print(f"✅ Archivo 'TablaUnificada.csv' guardado en {output_path}")
    print("✅ Inserción completada en la base de datos ContaminacionAire.")


if __name__ == "__main__":
    main()

    # main.py
    # main.py
    from src.modelos.ModeloML import entrenar_modelo


    def main():
        entrenar_modelo()


    if __name__ == "__main__":
        main()
