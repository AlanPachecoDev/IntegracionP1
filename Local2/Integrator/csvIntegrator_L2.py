import os
import pandas as pd
import mysql.connector
from mysql.connector import Error
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuración de la conexión a la base de datos MySQL
def conectar_mysql():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            database='bdd_integracion_1p',
            user='root',
            password='Elfossinsangre511214!'
        )
        if conexion.is_connected():
            print("Conexión exitosa a MySQL")
            return conexion
    except Error as e:
        print("Error al conectar a MySQL:", e)

# Función para cargar un archivo CSV a una tabla específica en la base de datos
def cargar_csv_a_mysql(conexion, archivo, tabla, id_local, carpeta_destino):
    try:
        df = pd.read_csv(archivo, delimiter='|')
        df['IdLocal'] = id_local  # Agrega la columna IdLocal con el valor proporcionado
        df.drop(columns=['Producto'], inplace=True)  # Elimina la columna 'Producto'
        cursor = conexion.cursor()
        for index, row in df.iterrows():
            # Selecciona las columnas que coinciden con las de la tabla en MySQL
            query = f"INSERT INTO {tabla} (IdTransaccion, Fecha, IdCategoria, IdProducto, Cantidad, PrecioUnitario, TotalVenta, IdLocal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            # Inserta los valores de cada fila en la tabla
            cursor.execute(query, (row['IdTransaccion'], row['Fecha'], row['IdCategoria'], row['IdProducto'], row['Cantidad'], row['PrecioUnitario'], row['TotalVenta'], row['IdLocal']))
        conexion.commit()
        print(f"Archivo {archivo} cargado correctamente en la tabla {tabla}")
        # Mover el archivo CSV a la carpeta de destino
        nombre_archivo = os.path.basename(archivo)
        os.rename(archivo, os.path.join(carpeta_destino, nombre_archivo))
        print(f"Archivo {archivo} movido a la carpeta {carpeta_destino}")
    except Error as e:
        print("Error al cargar el archivo CSV a MySQL:", e)

# Observador de eventos de cambios en archivos
class EventHandler(FileSystemEventHandler):
    def __init__(self, conexion, id_local):
        super().__init__()
        self.conexion = conexion
        self.id_local = id_local

    def on_modified(self, event):
        if event.is_directory:
            return
        print(f"Archivo modificado: {event.src_path}")
        cargar_csv_a_mysql(self.conexion, event.src_path, "ventas_consolidadas", self.id_local, "../../respaldos")

    def on_created(self, event):
        if event.is_directory:
            return
        print(f"Archivo creado: {event.src_path}")
        cargar_csv_a_mysql(self.conexion, event.src_path, "ventas_consolidadas", self.id_local, "../../respaldos")

if __name__ == "__main__":
    directorio = "../transacciones"
    id_local = 2  # El ID se cambia dependiendo del local en el que se esté

    conexion_mysql = conectar_mysql()
    if conexion_mysql:
        # Cargar archivos CSV existentes
        for archivo in os.listdir(directorio):
            if archivo.endswith('.csv'):
                archivo_path = os.path.join(directorio, archivo)
                cargar_csv_a_mysql(conexion_mysql, archivo_path, "ventas_consolidadas", id_local, "../../respaldos")

        # Observar cambios en la carpeta
        event_handler = EventHandler(conexion_mysql, id_local)
        observer = Observer()
        observer.schedule(event_handler, directorio, recursive=False)
        observer.start()
        print(f"Observando cambios en la carpeta {directorio}...")

        try:
            while True:
                pass
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
