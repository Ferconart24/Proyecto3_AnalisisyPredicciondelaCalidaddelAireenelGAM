 #Clase GestorBaseDatos: conecta con SQLite, MySQL, PostgreSQL o SQL Server y permite ejecutar consultas.

import pyodbc
import pandas as pd

class GestorBaseDatos:
    def __init__(self, server, database):
        """
        Inicializa la conexión usando Windows Authentication.
        """
        self.conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};DATABASE={database};Trusted_Connection=yes;"
        )
        self.conn = None

    def conectar(self):
        """Conecta a SQL Server usando Windows Authentication."""
        try:
            self.conn = pyodbc.connect(self.conn_str)
            print("✅ Conexión establecida con SQL Server (Windows Authentication)")
        except Exception as e:
            self.conn = None
            print("❌ Error en la conexión:", e)

    def crear_tabla_desde_dataframe(self, df, tabla):
        """Crea una tabla automáticamente según el DataFrame"""
        if not self.conn:
            print("❌ No hay conexión activa.")
            return

        cursor = self.conn.cursor()

        # Tipos de datos básicos
        tipo_sql = {
            "int64": "INT",
            "float64": "FLOAT",
            "object": "NVARCHAR(255)",
            "bool": "BIT",
            "datetime64[ns]": "DATETIME"
        }

        # Ajustes especiales para tus CSV
        columnas_sql = []
        for col, dtype in df.dtypes.items():
            if col.lower() == "fecha":
                columnas_sql.append(f"[{col}] DATE")
            elif col.lower() == "hora":
                columnas_sql.append(f"[{col}] INT")
            else:
                columnas_sql.append(f"[{col}] {tipo_sql.get(str(dtype), 'NVARCHAR(255)')}")

        columnas_sql_str = ", ".join(columnas_sql)

        query = f"""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = '{tabla}')
        CREATE TABLE {tabla} (
            id INT IDENTITY(1,1) PRIMARY KEY,
            {columnas_sql_str}
        )
        """
        cursor.execute(query)
        self.conn.commit()
        print(f"🛠️ Tabla '{tabla}' creada/verificada en SQL Server")

    def insertar_dataframe(self, df, tabla):
        """Inserta un DataFrame completo en la tabla (optimizado con executemany)"""
        if not self.conn:
            print("❌ No hay conexión activa.")
            return

        cursor = self.conn.cursor()
        columnas = ",".join([f"[{c}]" for c in df.columns])
        placeholders = ",".join("?" * len(df.columns))
        query = f"INSERT INTO {tabla} ({columnas}) VALUES ({placeholders})"

        data = [tuple(row) for row in df.to_numpy()]
        cursor.executemany(query, data)

        self.conn.commit()
        print(f"✅ {len(df)} registros insertados en '{tabla}'")

    def consultar(self, query):
        """Ejecuta una consulta y devuelve un DataFrame"""
        if not self.conn:
            print("❌ No hay conexión activa.")
            return pd.DataFrame()
        return pd.read_sql(query, self.conn)

    def cerrar(self):
        """Cierra la conexión si existe"""
        if self.conn:
            self.conn.close()
            self.conn = None
            print("🔒 Conexión cerrada")
        else:
            print("ℹ️ No había conexión activa para cerrar")
