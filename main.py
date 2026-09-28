import pandas as pd
import os
from src import carga 
from src import nulos
from src import funciones_normalizacion as f
from src import analisis_carga as ac
from src import analisis_nulos as an
from src import analisis_normalizado as nor
from src import estadisticas as est
from src.limpieza_pandas import limpieza_pandas
from src import analisis_estadisticas as ae
from src import metricas

ruta_archivo = "data\\raw\\calificaciones_medio_superior_practica2.csv"
ruta_salida_nulos= "outputs\\archivos\\nulos.csv"


if __name__ == "__main__":
    print("== Proyecto 1: Diseño de Aplicaciones para Análisis de Datos ==")

    ruta_archivo = "data\\raw\\calificaciones_medio_superior_practica2.csv"
    ruta_salida_nulos = "outputs\\archivos\\nulos.csv"
    ruta_nulos_calif = "outputs\\archivos\\nulos_calificaciones.csv"
    ruta_duplicados = "outputs\\archivos\\duplicado.csv"
    ruta_clean = "data\\final\\clean.csv"
    ruta_graficas = "outputs\\graficas\\"   

    try:

        for carpeta in ["outputs\\archivos", "outputs\\graficas", "data\\final"]:
            os.makedirs(carpeta, exist_ok=True)

        print("Leyendo archivo ...\n")
        columnas, datos = carga.lectura_pandas(ruta_archivo)
        print("Los datos se han cargado correctamente.\n")

        print("Comenzando la limpieza...")
        print("1. Eliminando espacios en blanco y convirtiendo a minusculas....")
        datos_minusculas = datos.map(lambda x: f.nulos_none(f.texto_minusculas(x) if isinstance(x, str) else x))

        print("2. Contando Nulos ....")
        conteo_nulos1 = nulos.nulos_pandas(datos_minusculas)
        pd.DataFrame([conteo_nulos1]).to_csv(ruta_salida_nulos, index=False)
        print("Conteo de nulos en columnas en outputs\\archivos\\nulos.csv")

        print("3. Normalizando calificaciones de 0 a 10...")
        con_calif = datos_minusculas["calificacion"].notna()
        calif_num = datos_minusculas.loc[con_calif, "calificacion"].map(lambda x: f.texto_numero(str(x)))
        inconsistentes = datos_minusculas.loc[con_calif][calif_num.isna()]
        inconsistentes.to_csv(ruta_nulos_calif, index=False)
        print("Almacenando nulos por calificaciones inconsistentes en outputs\\archivos\\nulos_calificaciones.csv")

        print("4. Eliminando duplicados ....")
        idiomas = datos_minusculas[datos_minusculas["tipo_examen"] == "idiomas"]
        dup_idiomas = idiomas[idiomas.duplicated(["id_estudiante", "fecha_aplicacion"], keep="first")]
        conocimiento = (datos_minusculas[datos_minusculas["tipo_examen"] == "conocimiento_general"]
                        .sort_values("fecha_aplicacion", ascending=False))
        dup_conocimiento = conocimiento[conocimiento.duplicated("id_estudiante", keep="first")]
        pd.concat([dup_idiomas, dup_conocimiento]).to_csv(ruta_duplicados, index=False)
        print("Almacenando datos duplicados en outputs\\archivos\\duplicado.csv")

        print("5. Almacenando datos limpios")
        df_limpio = limpieza_pandas(ruta_archivo)
        df_limpio["calificacion"] = df_limpio["calificacion"].map(f.escala_calificacion)
        df_limpio = df_limpio.dropna()
        df_limpio.to_csv(ruta_clean, index=False)
        print("Data set limpio guardado en data\\final\\clean.csv")

        print("6. Calculando estadisticas...")
        res = est.calcular_estadisticas_pd(df_limpio)
        res["instituciones_por_tipo"].to_csv("outputs\\archivos\\instituciones_por_tipo.csv", index=False)
        res["estudiantes_por_tipo"].to_csv("outputs\\archivos\\estudiantes_por_tipo.csv", index=False)
        res["promedio_institucion_examen"].to_csv("outputs\\archivos\\promedio_institucion_examen.csv", index=False)
        res["distribucion"].to_csv("outputs\\archivos\\distribucion_calificaciones.csv", index=False)
        print(res["instituciones_por_tipo"])
        print(res["estudiantes_por_tipo"])
        print("Estudiantes ligados a ambos tipos de institución:", res["n_estudiantes_ambos_tipos"])

        print("7. Generando graficas ...")
        est.grafica_promedio_tipo_examen(res["promedio_tipo_examen"], ruta_graficas + "promedio_tipo_examen.png")
        est.grafica_distribucion_calificaciones(res["distribucion"], ruta_graficas + "distribucion_calificaciones.png")
        print("Gráficas guardadas en outputs\\graficas\\")



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
            archivo_experimento_carga = ruta_outputs + f"datos_experimento_carga_lote_{i}.csv"
            ac.experimento(archivo_almacenamiento_lotes, archivo_experimento_carga)

            print(f"Los resultados de la experimentacion de  tiempos de carga para el lote {i} se almacenaron en outputs\\archivos\\")

            print(f"Comparando calculo de nulos por lotes ...")
            archivo_experimento_nulos = ruta_outputs + f"datos_experimento_conteo_nulos_lote_{i}.csv"
            an.experimento(archivo_almacenamiento_lotes, archivo_experimento_nulos)
            print(f"Los resultados de la experimentacion de  conteo de nulos para el lote {i} se almacenaron en outputs\\archivos\\")
            
            print(f"Comparando limpieza de datos en el lote {i} ...")
            archivo_experimento_limpieza = ruta_outputs + f"datos_experimento_limpieza_lote_{i}.csv"
            nor.experimento(archivo_almacenamiento_lotes, archivo_experimento_limpieza)
            print(f"Los resultados de la experimentacion de  tiempos de limpieza para el lote {i} se almacenaron en outputs\\archivos\\")

            print(f"Comparando estadisticas en el lote {i} ...")
            archivo_experimento_estadisticas = ruta_outputs + f"datos_experimento_estadisticas_lote_{i}.csv"
            ae.experimento(archivo_almacenamiento_lotes, archivo_experimento_estadisticas)

        print ("Experimentacion datos completos...")
        print(f"Comparando carga de archivos en el lote...")
        archivo_experimento_carga_total = ruta_outputs + f"datos_experimento_carga_total.csv"
        ac.experimento(ruta_archivo, archivo_experimento_carga_total)
        
        print(f"Los resultados de la experimentacion de  tiempos de carga para el archivo completo se almacenaron en outputs\\archivos\\")
        
        print(f"Comparando calculo de nulos ...")
        archivo_experimento_nulos_total = ruta_outputs + f"datos_experimento_conteo_nulos_total.csv"
        an.experimento(ruta_archivo, archivo_experimento_nulos_total)
        print(f"Los resultados de la experimentacion de  conteo de nulos para total de datos se almacenaron en outputs\\archivos\\")
                    
        print("Comparando limpieza de datos en el total ...")
        archivo_experimento_limpieza_total = ruta_outputs + "datos_experimento_limpieza_total.csv"
        nor.experimento(ruta_archivo, archivo_experimento_limpieza_total)
        print("Los resultados de la experimentacion de tiempos de limpieza para el total de datos se almacenaron en outputs\\archivos\\")

                 

        print("Comparando estadisticas en el total ...")
        ae.experimento(ruta_archivo, ruta_outputs + "datos_experimento_estadisticas_total.csv")

        print("Generando tabla comparativa y graficas de rendimiento ...")
        tabla = metricas.generar_reporte(
            carpeta_archivos="outputs\\archivos",
            carpeta_graficas="outputs\\graficas",
            lotes=[50_000, 100_000, 150_000],
            n_total=len(datos),
        )
        

    except Exception as e:
        print("Ocurrió un error al cargar los datos:", e)

            
    
    