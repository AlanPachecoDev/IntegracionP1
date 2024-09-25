import os
import csv
import random
from datetime import datetime

# Variable global para mantener el contador de IdTransaccion
contador_id_transaccion = 0

# Función para generar un ID de transacción autoincremental
def generar_id_transaccion():
    global contador_id_transaccion
    id_transaccion = contador_id_transaccion
    contador_id_transaccion += 1
    return id_transaccion

# Función para generar una fecha aleatoria dentro de un rango de 2 años
def generar_fecha():
    start_date = datetime.now().replace(year=datetime.now().year - 2)
    end_date = datetime.now()
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime('%Y-%m-%d %H:%M:%S')

# Función para generar un ID de categoría aleatorio (suponiendo un rango de 1 a 10)
def generar_id_categoria():
    return random.randint(1, 10)

# Función para generar un ID de producto aleatorio (suponiendo un rango de 1 a 100)
def generar_id_producto():
    return random.randint(1, 100)

# Función para generar un nombre de producto aleatorio
def generar_producto():
    productos = ["Producto A", "Producto B", "Producto C", "Producto D", "Producto E"]
    return random.choice(productos)

# Función para generar una cantidad aleatoria
def generar_cantidad():
    return random.randint(1, 100)

# Función para generar un precio unitario aleatorio
def generar_precio_unitario():
    return round(random.uniform(10, 1000), 2)

# Función para calcular el total de la venta
def calcular_total_venta(cantidad, precio_unitario):
    return round(cantidad * precio_unitario, 2)

# Función para generar un nombre de archivo único en una carpeta específica
def generar_nombre_archivo(nombre_base, carpeta_destino):
    contador = 1
    nombre_archivo = nombre_base + ".csv"
    while os.path.exists(os.path.join(carpeta_destino, nombre_archivo)):
        nombre_archivo = nombre_base + "_" + str(contador) + ".csv"
        contador += 1
    return os.path.join(carpeta_destino, nombre_archivo)

# Función para generar y escribir los datos en el archivo CSV
def generar_csv(nombre_archivo, num_registros=10):
    with open(nombre_archivo, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter='|')
        writer.writerow(["IdTransaccion", "Fecha", "IdCategoria", "IdProducto", "Producto", "Cantidad", "PrecioUnitario", "TotalVenta"])
        for _ in range(num_registros):
            id_transaccion = generar_id_transaccion()
            fecha = generar_fecha()
            id_categoria = generar_id_categoria()
            id_producto = generar_id_producto()
            producto = generar_producto()
            cantidad = generar_cantidad()
            precio_unitario = generar_precio_unitario()
            total_venta = calcular_total_venta(cantidad, precio_unitario)
            writer.writerow([id_transaccion, fecha, id_categoria, id_producto, producto, cantidad, precio_unitario, total_venta])

# Ejemplo de uso: generar un archivo CSV en una carpeta específica con un nombre único y 10 registros
carpeta_destino = "../transaccionesVarias"
nombre_base = "transaccion"
nombre_archivo = generar_nombre_archivo(nombre_base, carpeta_destino)
generar_csv(nombre_archivo)
print("Se ha generado el archivo:", nombre_archivo)
