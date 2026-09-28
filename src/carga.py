import csv
import pandas as pd

"""CARGA MANUAL"""

""" Esta funcion recibe la direccion del archivo que se desea carga
    regresa como resultado las columnas del archivo
"""
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

def lectura_pandas(archivo):
    df = pd.read_csv(archivo)
    return df.columns, df






