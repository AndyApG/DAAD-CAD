import csv
import pandas as pd


"""CARGA MANUAL"""

def lectura_csv(archivo):
    datos = []
    with open(archivo, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Guardar columnas
        columnas = reader.fieldnames
        
        # Recorrer cada fila y convertir a lista
        for fila in reader:
            fila_filtrada = [fila[col] for col in columnas]
            datos.append(fila_filtrada)
    
    return columnas, datos
        

"""CARGA CON PANDAS"""

def lecturapandas(archivo):
    df = pd.read_csv(archivo)
    return df.columns, df






