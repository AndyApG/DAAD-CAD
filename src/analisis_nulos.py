import time
import csv
import pandas as pd
import nulos
import funciones_normalizacion as f

"""Comparación del tiempo de calculo de valores nulos entre la función 
    implementada sin pandas y la función implementada con la libreria pandas"""

n = 5 #Número de repeticiones de cada experimento
ruta_archivo = "data\\raw\\calificaciones_medio_superior_practica2.csv"
ruta_experimento = "outputs\\archivos\\experimento2.csv"

#Leer archivo pandas
df = pd.read_csv(ruta_archivo)
df = df.map(lambda x: f.nulos_none(f.texto_minusculas(x) if isinstance(x,str) else x))

datos = []
with open(ruta_archivo, newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    columnas = reader.fieldnames
    for fila in reader:
        fila_filtrada = [fila[col] for col in columnas]
        datos.append(fila_filtrada)



# Definir encabezados solo una vez
headers = ["Pandas","Iteración", "Tiempo"]
[headers.append(i+"_nulos") for i in list(df.columns) ]

# Crear archivo y escribir encabezados
with open(ruta_experimento, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(headers)


for i in range(n):
    tiempo_inicio = time.perf_counter()
        
    #nulos con pandas
    nulo = nulos.nulos_pandas(df)
    tiempo_final = time.perf_counter()
    tiempo = tiempo_final-tiempo_inicio
    l = list(nulo.values())
    lista = [1,i, tiempo]

    [lista.append(i) for i in l]

    print(lista)
    with open(ruta_experimento, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(lista)


for i in range(n):
    tiempo_inicio = time.perf_counter()
        
    #nulos con pandas
    nul = nulos.nulos_sin_pandas(datos,df.columns)
    tiempo_final = time.perf_counter()

    tiempo = tiempo_final-tiempo_inicio
    l = list(nul.values())
    lista = [0,i, tiempo]

    [lista.append(i) for i in l]

    print(lista)
    with open(ruta_experimento, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(lista)

