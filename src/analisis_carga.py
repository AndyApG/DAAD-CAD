import time
import carga
import csv

"""Comparación del tiempo de lectura entre la función 
    implementada y la función de la libreria pandas"""

n = 5 #Número de repeticiones de cada experimento
ruta_archivo = "data\\raw\\calificaciones_medio_superior_practica2.csv"
ruta_experimento1 = "outputs\\archivos\\experimento1.csv"


"""Experimento 1: Lectura de los archivos e impresión tamaño de los datos
    nombre de columnas y 5 primeros registros y se guarda en un archivo csv"""

# Definir encabezados solo una vez
headers = ["Pandas","Iteración", "Tiempo", "Num_filas", "Num_columnas"]

# Crear archivo y escribir encabezados
with open(ruta_experimento1, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(headers)


for i in range(n):
    tiempo_inicio = time.perf_counter()
        
    # lectura con pandas
    columnas, datos = carga.lecturapandas(ruta_archivo)

    tiempo_fin = time.perf_counter()

    # medir tiempo
    tiempo = tiempo_fin - tiempo_inicio
    
    # número de filas y columnas
    num_filas = datos.shape[0]
    num_col = datos.shape[1]
    

    # Guardar resultados en el archivo
    with open(ruta_experimento1, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([1,i, tiempo, num_filas, num_col])
    


for i in range(n):
    tiempo_inicio = time.perf_counter()
    
    # lectura sin pandas
    columnas, datos = carga.lectura_csv(ruta_archivo)

    tiempo_fin = time.perf_counter()

    # medir tiempo
    tiempo = tiempo_fin - tiempo_inicio
    
    
    # número de filas y columnas
    num_filas = len(datos)
    num_col = len(columnas)
   
        
    

    with open(ruta_experimento1, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([0,i, tiempo, num_filas, num_col])
    

    