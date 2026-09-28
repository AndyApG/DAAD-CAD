import math
from src.carga import lectura_csv
from src.funciones_normalizacion import *

# Posiciones de las columnas del CSV original
ID_EST, TIPO_EXAMEN, CALIF, INSTITUCION, TIPO_INST, MODALIDAD, FECHA, ANIO = 1, 4, 5, 6, 7, 8, 9, 10

# Columnas del resultado (mismo orden que limpieza_pandas)
COLUMNAS_LIMPIAS = ["id_estudiante", "calificacion", "institucion", "tipo_institucion",
                    "tipo_examen", "modalidad", "anio_aplicacion"]


def limpieza_manual(ruta):
    """Limpieza sin pandas. Regresa una lista de listas con las columnas
    COLUMNAS_LIMPIAS (mismo contenido y orden que limpieza_pandas)."""

    columnas, datos = lectura_csv(ruta)

    # 1. Minusculas, sin espacios y nulos como None
    registros = [
        [nulos_none(texto_minusculas(str(v))) for v in fila]
        for fila in datos
    ]

    # 2. Imputacion del tipo de institucion usando el diccionario institucion -> tipo
    instituciones_dic = {}
    for fila in registros:
        if fila[INSTITUCION] is not None and fila[TIPO_INST] is not None:
            instituciones_dic[fila[INSTITUCION]] = fila[TIPO_INST]

    for fila in registros:
        if fila[TIPO_INST] is None and fila[INSTITUCION] in instituciones_dic:
            fila[TIPO_INST] = instituciones_dic[fila[INSTITUCION]]

    # 3. Idiomas: quitar duplicados (id_estudiante, fecha_aplicacion), conservar el primero
    idiomas_unicos = []
    vistos = set()
    for fila in registros:
        if fila[TIPO_EXAMEN] == "idiomas":
            clave = (fila[ID_EST], fila[FECHA])
            if clave not in vistos:
                vistos.add(clave)
                idiomas_unicos.append(fila)

    # 4. Conocimiento general: un registro por estudiante, el de fecha mas reciente
    #    (las fechas vacias quedan al final, igual que sort_values de pandas)
    conocimiento = [fila for fila in registros if fila[TIPO_EXAMEN] == "conocimiento_general"]
    con_fecha = [f for f in conocimiento if f[FECHA] is not None]
    sin_fecha = [f for f in conocimiento if f[FECHA] is None]
    con_fecha.sort(key=lambda f: f[FECHA], reverse=True)

    conocimiento_unicos = []
    vistos = set()
    for fila in con_fecha + sin_fecha:
        if fila[ID_EST] not in vistos:
            vistos.add(fila[ID_EST])
            conocimiento_unicos.append(fila)

    filtrado = idiomas_unicos + conocimiento_unicos

    # 5. Calificacion a numero
    for fila in filtrado:
        if fila[CALIF] is not None:
            fila[CALIF] = texto_numero(str(fila[CALIF]))

    # 6. Seleccionar columnas y eliminar filas con nulos (None o nan)
    orden = [ID_EST, CALIF, INSTITUCION, TIPO_INST, TIPO_EXAMEN, MODALIDAD, ANIO]

    def es_nulo(v):
        return v is None or (isinstance(v, float) and math.isnan(v))

    resultado = []
    for fila in filtrado:
        nueva = [fila[c] for c in orden]
        if not any(es_nulo(v) for v in nueva):
            resultado.append(nueva)

    return resultado