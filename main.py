from tabulate import tabulate
import src.carga as carga
import src.nulos as nulos
import src.funciones_normalizacion as f
import csv
import pandas as pd

ruta_archivo = "data\\raw\\calificaciones_medio_superior_practica2.csv"
ruta_salida_nulos= "outputs\\archivos\\nulos.csv"

if __name__ == "__main__":
    print("== Proyecto 1: Diseño de Aplicaciones para Análisis de Datos ==")

    try:

        print("Leyendo archivo ...\n")
        columnas, datos = carga.lectura_pandas(ruta_archivo)
        print("Los datos se han cargado correctamente.\n")

        print("Comenzando la limpieza...")
        print("1. Eliminando espacios en blanco y convirtiendo a miusculas....")
        datos_minusculas = datos.map(lambda x: f.nulos_none(f.texto_minusculas(x) if isinstance(x,str) else x))

        print("2. Contando Nulos ....")
        conteo_nulos1 = nulos.nulos_pandas(datos_minusculas)
        df_nulos1 = pd.DataFrame([conteo_nulos1])
        # Crear archivo y escribir encabezados
        print("Almacenando nulos en outputs\\archivos\\nulos.csv")
        df_nulos1.to_csv(ruta_salida_nulos, encoding="utf-8-sig")

        print("Iniciando experimentación .....")
        
    except Exception as e:
        print("Ocurrió un error al cargar los datos:", e)

            
    
    