# Clase ProcesadorEDA: análisis estadístico, limpieza y exploración de datos
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class ProcesadorEDA:
    def __init__(self, dfs: dict, output_dir="reports/figures"):
        self.dfs = dfs
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    # --- Limpieza y exploración por CSV ---
    def info_general_df(self, nombre, df):
        print(f"\n📄 Información general - {nombre}")
        print("Shape:", df.shape)
        print("Tipos de datos:\n", df.dtypes)
        print("Valores nulos:\n", df.isnull().sum())
        print("Primeras filas:\n", df.head(3))

    def estadisticas_df(self, nombre, df):
        print(f"\n📊 Estadísticas descriptivas - {nombre}")
        print(df.describe(include="all"))

    # --- Gráficos por CSV ---
    def histograma_df(self, nombre, df):
        num_cols = df.select_dtypes(include="number").columns
        if len(num_cols) == 0: return
        df[num_cols].hist(bins=30, figsize=(12, 8))
        plt.suptitle(f"Histogramas - {nombre}")
        plt.savefig(os.path.join(self.output_dir, f"{nombre}_hist.png"))
        plt.show()

    def boxplot_df(self, nombre, df):
        num_cols = df.select_dtypes(include="number").columns
        if len(num_cols) == 0: return
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df[num_cols])
        plt.title(f"Boxplots - {nombre}")
        plt.xticks(rotation=45)
        plt.savefig(os.path.join(self.output_dir, f"{nombre}_boxplot.png"))
        plt.show()

    def correlacion_df(self, nombre, df):
        num_cols = df.select_dtypes(include="number").columns
        if len(num_cols) == 0: return
        plt.figure(figsize=(10, 8))
        sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f")
        plt.title(f"Matriz de Correlación - {nombre}")
        plt.savefig(os.path.join(self.output_dir, f"{nombre}_corr.png"))
        plt.show()

    # --- Gráficos por año ---
    def analisis_anual(self, fecha_col="fecha", contaminantes=["PM2.5","NO2"]):
        for nombre, df in self.dfs.items():
            if fecha_col not in df.columns: continue
            df[fecha_col] = pd.to_datetime(df[fecha_col])
            for cont in contaminantes:
                if cont in df.columns:
                    serie = df.groupby(df[fecha_col].dt.year)[cont].mean()
                    plt.figure(figsize=(12, 6))
                    serie.plot(marker="o")
                    plt.title(f"{cont} por Año - {nombre}")
                    plt.xlabel("Año")
                    plt.ylabel(cont)
                    plt.grid(True)
                    plt.savefig(os.path.join(self.output_dir, f"{nombre}_{cont}_anual.png"))
                    plt.show()

    # --- Correlaciones específicas ---
    def correlacion_trafico_contaminantes(self, flujo_col="flujo", contaminantes=["PM2.5","NO2"]):
        if "FlujoVehicular" not in self.dfs or "Contaminantes" not in self.dfs:
            print("⚠️ No se encontraron los datasets necesarios para correlación flujo-contaminantes")
            return

        df_flujo = self.dfs["FlujoVehicular"]
        df_cont = self.dfs["Contaminantes"]

        if "fecha" in df_flujo.columns and "fecha" in df_cont.columns:
            df_merged = pd.merge(df_flujo, df_cont, on="fecha")
        else:
            print("⚠️ No hay columna 'fecha' para unir Flujo y Contaminantes")
            return

        for cont in contaminantes:
            if cont in df_merged.columns and flujo_col in df_merged.columns:
                corr = df_merged[flujo_col].corr(df_merged[cont])
                print(f"📊 Correlación {flujo_col} vs {cont}: {corr:.2f}")
                sns.lmplot(x=flujo_col, y=cont, data=df_merged)
                plt.title(f"{flujo_col} vs {cont}")
                plt.savefig(os.path.join(self.output_dir, f"{flujo_col}_{cont}_scatter.png"))
                plt.show()
            else:
                print(f"⚠️ Columnas {flujo_col} o {cont} no encontradas")

    def dispersion_meteo_contaminantes(self, meteo_cols=["temperatura","humedad"], contaminantes=["PM2.5","NO2"]):
        for nombre, df in self.dfs.items():
            for met in meteo_cols:
                for cont in contaminantes:
                    if met in df.columns and cont in df.columns:
                        sns.lmplot(x=met, y=cont, data=df)
                        plt.title(f"{met} vs {cont} - {nombre}")
                        plt.savefig(os.path.join(self.output_dir, f"{nombre}_{met}_{cont}_scatter.png"))
                        plt.show()

    # --- Temporal ---
    def analisis_temporal(self, fecha_col="fecha", contaminantes=["PM2.5","NO2"], freq="D"):
        for nombre, df in self.dfs.items():
            if fecha_col not in df.columns: continue
            df[fecha_col] = pd.to_datetime(df[fecha_col])
            for cont in contaminantes:
                if cont in df.columns:
                    serie = df.groupby(pd.Grouper(key=fecha_col, freq=freq))[cont].mean()
                    plt.figure(figsize=(12, 6))
                    serie.plot()
                    plt.title(f"{cont} ({freq}) - {nombre}")
                    plt.xlabel("Tiempo")
                    plt.ylabel(cont)
                    plt.grid(True)
                    plt.savefig(os.path.join(self.output_dir, f"{nombre}_{cont}_time_{freq}.png"))
                    plt.show()

    # --- Espacial / Heatmap ---
    def mapa_calor_zonas(self, df_name="Contaminantes", zona_col="zona", contaminantes=["PM2.5","NO2"]):
        if df_name not in self.dfs:
            print(f"⚠️ No se encontró el DataFrame {df_name}")
            return
        df = self.dfs[df_name]
        if zona_col not in df.columns:
            print(f"⚠️ No se encontró la columna '{zona_col}' en {df_name}")
            return
        pivot = df.groupby(zona_col)[contaminantes].mean()
        plt.figure(figsize=(8, 6))
        sns.heatmap(pivot, annot=True, cmap="Reds", fmt=".1f")
        plt.title(f"Mapa de calor zonas - {df_name}")
        plt.savefig(os.path.join(self.output_dir, f"{df_name}_zonas_heat.png"))
        plt.show()
