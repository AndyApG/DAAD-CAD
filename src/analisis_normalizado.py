import time
import csv
from src.limpieza_manual import limpieza_manual
from src.limpieza_pandas import limpieza_pandas

"""Comparación del tiempo de calculo de valores nulos entre la función 
    implementada sin pandas y la función implementada con la libreria pandas"""

def experimento(nombre_archivo_entrada, nombre_archivo_salida, n = 5):

    # Definir encabezados solo una vez
    headers = ["Pandas","Iteración", "Tiempo", "longitud"]
    
    # Crear archivo y escribir encabezados
    with open(nombre_archivo_salida, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)


    for i in range(n):
        tiempo_inicio = time.perf_counter()
        df = limpieza_pandas(nombre_archivo_entrada)
        tiempo_final = time.perf_counter()
        tiempo = tiempo_final-tiempo_inicio
        l = len(df)
        lista = [1,i, tiempo,l]

        with open(nombre_archivo_salida, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(lista)

    for i in range(n):
        tiempo_inicio = time.perf_counter()
        df = limpieza_manual(nombre_archivo_entrada)
        tiempo_final = time.perf_counter()
        tiempo = tiempo_final-tiempo_inicio
        l = len(df)
        lista = [0,i, tiempo,l]
        
        with open(nombre_archivo_salida, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(lista)

