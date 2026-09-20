from tabulate import tabulate
import src.carga as carga


ruta_archivo = "data\\raw\\calificaciones_medio_superior_practica2.csv"

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
        print("\nTipos de datos de las columnas:")
        datos.info()

    except Exception as e:
        print("Ocurrió un error al cargar los datos:", e)

            
    
    