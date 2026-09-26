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

    # lectura con pandas
    try:
        columnas, datos = carga.lectura_pandas(ruta_archivo)
        print("Los datos se han cargado correctamente.\n")

        # número de filas y columnas
        print("Filas y columnas del archivo:")
        num_filas = datos.shape[0]
        num_col = datos.shape[1]
        print("Número de filas:", num_filas)
        print("Número de columnas:", num_col)

        # muestra de datos
        print("\nMuestra de datos:")
        print(datos.head(5))

        # Tipos de los datos
        print("\n Tipos de datos de las columnas:")
        datos.info()

    

        datos_minusculas = datos.map(lambda x: f.nulos_none(f.texto_minusculas(x) if isinstance(x,str) else x))
        conteo_nulos = nulos.nulos_pandas(datos_minusculas)
        df_nulos = pd.DataFrame([conteo_nulos])
        # Crear archivo y escribir encabezados
        df_nulos.to_csv(ruta_salida_nulos, encoding="utf-8-sig")

        print(df_nulos)



        # Valores unicos en los tipos de examen calificacion institucion, tipo de institucion y modalidad
        print(datos.iloc[0:5,4:9].nunique())

    except Exception as e:
        print("Ocurrió un error al cargar los datos:", e)

            
    
    