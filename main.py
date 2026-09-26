from tabulate import tabulate
import pandas as pd
from src import carga, nulos
from src import funciones_normalizacion as f
from src import analisis_carga as ac

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
        df_nulos1.to_csv("outputs\\archivos\\nulos.csv", index=False)
        print("Conteo de nulos en columnas en outputs\\archivos\\nulos.csv")

        print("3. Normalizando calificaciones de 0 a 10...")
        print("Almacenando nulos por calificaciones inconsistentes en outputs\\archivos\\nulos_calificaciones.csv")

        print("4. Eliminando duplicados ....")
        print("Almacenando datos  duplicados en outputs\\archivos\\duplicado.csv")

        print("5. Almacenando datos limpios")
        print("Data set limpio guardado en data\\final\\clean.csv")

        print("6. Calculando estadisticas...")

        print("7. Generando graficas ...")



        print("Iniciando experimentación por lotes.....")
        print("Dividiendo el conjunto de datos original ...")

        ruta_experimento_raw = "data\\raw\\"
        ruta_outputs = "outputs\\archivos\\"

        for i in [50_000, 100_000, 150_000]:
            data_set = datos.iloc[0:i,:]
            archivo_almacenamiento_lotes = ruta_experimento_raw + f"datos_{i}.csv"
            data_set.to_csv(archivo_almacenamiento_lotes, index=False)

            print(f"Los resultados de la division del lote con {i} datos se almacenaron en data\\raw\\")

            # Conteo de nulos
            print(f"Contando nulos el lote {i} ...")
            datos_minusculas = data_set.map(lambda x: f.nulos_none(f.texto_minusculas(x) if isinstance(x,str) else x))
            conteo_nulos1 = nulos.nulos_pandas(datos_minusculas)
            df_nulos1 = pd.DataFrame([conteo_nulos1])
            ruta_nulos = ruta_outputs + f"datos_nulos_lote_{i}.csv"
            df_nulos1.to_csv(ruta_nulos, index=False)

            print(f"Los resultados de el conteo de nulos en el lote {i} se almacenaron en outputs\\archivos\\")

            print(f"Comparando carga de archivos en el lote {i} ...")
            # Analisis de lectura de datos por lotes
            archivo_experimento_carga = ruta_outputs + f"datos_experimento_carga_lote_{i}.csv"
            ac.experimento(archivo_almacenamiento_lotes, archivo_experimento_carga)

            print(f"Los resultados de la experimentacion de  tiempos de carga para el lote {i} se almacenaron en outputs\\archivos\\")

            #analisis_null.


        

    




        
    except Exception as e:
        print("Ocurrió un error al cargar los datos:", e)

            
    
    