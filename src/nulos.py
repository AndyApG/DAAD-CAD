import math
import pandas as pd
valores_nulos = ["", "na", "n/a", "null", "none", "nan", "n/c", "s/c"]

"""CONTEO DE NUMERO DE VALORES NULOS POR COLUMNA SIN PANDAS"""
def nulos_sin_pandas(datos, columnas):
    conteo = {col: 0 for col in columnas}
    for fila in datos:
        for col, valor in zip(columnas, fila):
            val = str(valor).strip().lower()
            if val in valores_nulos or (isinstance(valor, float) and math.isnan(valor)):
                conteo[col] += 1
    return conteo


"""CONTEO DE NUMERO DE VALORES NULOS POR COLUMNA CON PANDAS"""

def nulos_pandas(datos):
    try:
     if isinstance(datos, pd.DataFrame):
        # Conteo de nulos por columna
        conteo = datos.isnull().sum().to_dict()
        return conteo
    
    except Exception as e:
        print("Los datos deben ser un DataFrame de pandas", e)
        return None

