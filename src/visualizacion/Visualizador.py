from src.eda.ProcesadorEDA import ProcesadorEDA
import pandas as pd
from pathlib import Path

def main():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = BASE_DIR / "data" / "processed"
    if not DATA_DIR.exists(): return

    csv_files = [f for f in DATA_DIR.iterdir() if f.suffix == ".csv"]
    if not csv_files: return

    dfs = {}
    for archivo in csv_files:
        try:
            df = pd.read_csv(archivo)
            dfs[archivo.stem] = df
        except Exception as e:
            print(f"❌ No se pudo cargar {archivo.name}: {e}")

    eda = ProcesadorEDA(dfs)
    resumen = []

    for nombre, df in dfs.items():
        print("\n" + "="*60)
        print(f"{'ANÁLISIS DE DATOS: ' + nombre:^60}")
        print("="*60)

        # Info y estadísticas
        print("➡️ Información general")
        eda.info_general_df(nombre, df)

        print("➡️ Estadísticas descriptivas")
        eda.estadisticas_df(nombre, df)

        # Gráficos principales
        print("➡️ Gráficos principales")
        eda.histograma_df(nombre, df)
        eda.boxplot_df(nombre, df)
        eda.correlacion_df(nombre, df)
        eda.analisis_anual()  # gráficos por año

        # Correlaciones especiales y dispersión
        print("➡️ Correlaciones y dispersión")
        if nombre in ["FlujoVehicular", "Contaminantes"]:
            eda.correlacion_trafico_contaminantes()
        eda.dispersion_meteo_contaminantes()
        eda.analisis_temporal(freq="D")
        eda.analisis_temporal(freq="W")

        # Heatmap solo para Contaminantes
        if nombre == "Contaminantes":
            eda.mapa_calor_zonas(df_name="Contaminantes", zona_col="zona")

        resumen.append((nombre, df.shape[0], df.shape[1]))

    # Resumen final
    print("\n" + "="*60)
    print(f"{'RESUMEN FINAL':^60}")
    print("="*60)
    print(f"{'CSV':<20}{'Filas':<10}{'Columnas':<10}")
    for r in resumen:
        print(f"{r[0]:<20}{r[1]:<10}{r[2]:<10}")

if __name__ == "__main__":
    main()
