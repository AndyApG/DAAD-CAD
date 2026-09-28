"""
3.5 Análisis y distribución de resultados.

Cada resultado tiene dos versiones:
  * *_manual : recibe `datos` (lista de listas) y `columnas` (lista con los nombres).
  * *_pd     : recibe un DataFrame de pandas.

Las funciones buscan las columnas POR NOMBRE, así que no importa el orden en que
vengan. Columnas requeridas en los datos limpios:
    id_estudiante, calificacion, institucion, tipo_institucion, tipo_examen

IMPORTANTE: las calificaciones deben estar ya normalizadas a la escala 0-10
(paso 3 de la limpieza) antes de llamar estas funciones.
"""
import math
import unicodedata

import matplotlib
matplotlib.use("Agg")          # solo guarda a archivo, no abre ventanas
import matplotlib.pyplot as plt
import pandas as pd

RANGOS = [f"{i}-{i + 1}" for i in range(10)]     # 0-1, 1-2, ..., 9-10

def _tipo(valor):
    """'Pública' / 'PUBLICA ' -> 'publica' (sin acentos, minúsculas)."""
    s = unicodedata.normalize("NFD", str(valor))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.strip().lower()


def _es_calificacion_valida(x):
    return isinstance(x, (int, float)) and not math.isnan(x) and 0 <= x <= 10


def _indices(columnas, *nombres):
    columnas = list(columnas)
    return [columnas.index(n) for n in nombres]

"""MANUAL"""
def instituciones_por_tipo_manual(datos, columnas):
    """Número y porcentaje de instituciones (distintas) públicas y privadas.
    Regresa: [(tipo, num_instituciones, porcentaje), ...]"""
    i_inst, i_tipo = _indices(columnas, "institucion", "tipo_institucion")
    por_tipo = {}
    for fila in datos:
        por_tipo.setdefault(_tipo(fila[i_tipo]), set()).add(fila[i_inst])

    total = sum(len(s) for s in por_tipo.values())
    if total == 0:
        return []
    return [(t, len(s), len(s) / total * 100) for t, s in sorted(por_tipo.items())]


def estudiantes_por_tipo_manual(datos, columnas):
    """Número de estudiantes (distintos) asociados a cada tipo de institución.
    Regresa: [(tipo, num_estudiantes), ...]"""
    i_id, i_tipo = _indices(columnas, "id_estudiante", "tipo_institucion")
    por_tipo = {}
    for fila in datos:
        por_tipo.setdefault(_tipo(fila[i_tipo]), set()).add(fila[i_id])
    return [(t, len(s)) for t, s in sorted(por_tipo.items())]


def promedio_institucion_examen_manual(datos, columnas):
    """Promedio de calificaciones por institución y por tipo de examen.
    Regresa: [(institucion, tipo_examen, promedio, n_registros), ...]"""
    i_inst, i_exa, i_cal = _indices(columnas, "institucion", "tipo_examen", "calificacion")
    acum = {}                                   # (inst, examen) -> [suma, conteo]
    for fila in datos:
        cal = fila[i_cal]
        if not _es_calificacion_valida(cal):
            continue
        clave = (fila[i_inst], fila[i_exa])
        if clave not in acum:
            acum[clave] = [0.0, 0]
        acum[clave][0] += cal
        acum[clave][1] += 1
    return [(inst, exa, s / n, n) for (inst, exa), (s, n) in sorted(acum.items())]


def promedio_tipo_institucion_examen_manual(datos, columnas):
    """Promedio por tipo de institución y tipo de examen (resumen para graficar).
    Regresa: [(tipo_institucion, tipo_examen, promedio, n_registros), ...]"""
    i_tipo, i_exa, i_cal = _indices(columnas, "tipo_institucion", "tipo_examen", "calificacion")
    acum = {}
    for fila in datos:
        cal = fila[i_cal]
        if not _es_calificacion_valida(cal):
            continue
        clave = (_tipo(fila[i_tipo]), fila[i_exa])
        if clave not in acum:
            acum[clave] = [0.0, 0]
        acum[clave][0] += cal
        acum[clave][1] += 1
    return [(t, exa, s / n, n) for (t, exa), (s, n) in sorted(acum.items())]


def distribucion_calificaciones_manual(datos, columnas):
    """Distribución (histograma en rangos de 1 punto) de las calificaciones de
    cada tipo de examen (Conocimiento General e Idiomas).
    Regresa: [(tipo_examen, rango, frecuencia, porcentaje), ...]"""
    i_exa, i_cal = _indices(columnas, "tipo_examen", "calificacion")
    conteos = {}                                # examen -> [10 contadores]
    for fila in datos:
        cal = fila[i_cal]
        if not _es_calificacion_valida(cal):
            continue
        if fila[i_exa] not in conteos:
            conteos[fila[i_exa]] = [0] * 10
        conteos[fila[i_exa]][min(int(cal), 9)] += 1     # el 10 cae en el rango 9-10

    resultado = []
    for exa in sorted(conteos):
        total = sum(conteos[exa])
        for rango, frec in zip(RANGOS, conteos[exa]):
            resultado.append((exa, rango, frec, frec / total * 100))
    return resultado


def estudiantes_ambos_tipos_manual(datos, columnas):
    """Estudiantes que aparecen ligados a instituciones públicas Y privadas.
    Regresa: (num_estudiantes_ambos, [ids])"""
    i_id, i_tipo = _indices(columnas, "id_estudiante", "tipo_institucion")
    tipos_por_est = {}
    for fila in datos:
        tipos_por_est.setdefault(fila[i_id], set()).add(_tipo(fila[i_tipo]))
    ids = sorted(e for e, t in tipos_por_est.items() if len(t) > 1)
    return len(ids), ids


def calcular_estadisticas_manual(datos, columnas):
    """Corre todos los resultados de la sección 3.5 (versión manual)."""
    n_ambos, ids_ambos = estudiantes_ambos_tipos_manual(datos, columnas)
    return {
        "instituciones_por_tipo": instituciones_por_tipo_manual(datos, columnas),
        "estudiantes_por_tipo": estudiantes_por_tipo_manual(datos, columnas),
        "promedio_institucion_examen": promedio_institucion_examen_manual(datos, columnas),
        "promedio_tipo_examen": promedio_tipo_institucion_examen_manual(datos, columnas),
        "distribucion": distribucion_calificaciones_manual(datos, columnas),
        "n_estudiantes_ambos_tipos": n_ambos,
        "ids_estudiantes_ambos_tipos": ids_ambos,
    }

"""PANDAS"""

def _df_valido(df):
    
    d = df.copy()
    d["tipo_institucion"] = d["tipo_institucion"].map(_tipo)
    return d[d["calificacion"].between(0, 10)]


def instituciones_por_tipo_pd(df):
    d = df.copy()
    d["tipo_institucion"] = d["tipo_institucion"].map(_tipo)
    res = (d.groupby("tipo_institucion")["institucion"].nunique()
             .rename("num_instituciones").reset_index())
    res["porcentaje"] = res["num_instituciones"] / res["num_instituciones"].sum() * 100
    return res


def estudiantes_por_tipo_pd(df):
    d = df.copy()
    d["tipo_institucion"] = d["tipo_institucion"].map(_tipo)
    return (d.groupby("tipo_institucion")["id_estudiante"].nunique()
              .rename("num_estudiantes").reset_index())


def promedio_institucion_examen_pd(df):
    return (_df_valido(df).groupby(["institucion", "tipo_examen"])["calificacion"]
            .agg(promedio="mean", n_registros="count").reset_index())


def promedio_tipo_institucion_examen_pd(df):
    return (_df_valido(df).groupby(["tipo_institucion", "tipo_examen"])["calificacion"]
            .agg(promedio="mean", n_registros="count").reset_index())


def distribucion_calificaciones_pd(df):
    d = _df_valido(df).copy()
    d["rango"] = d["calificacion"].floordiv(1).clip(upper=9).astype(int)
    frec = (d.groupby(["tipo_examen", "rango"]).size().unstack(fill_value=0)
              .reindex(columns=range(10), fill_value=0))
    frec.columns = RANGOS
    res = frec.stack().rename("frecuencia").reset_index()
    res.columns = ["tipo_examen", "rango", "frecuencia"]
    res["porcentaje"] = res["frecuencia"] / res.groupby("tipo_examen")["frecuencia"].transform("sum") * 100
    return res


def estudiantes_ambos_tipos_pd(df):
    d = df.copy()
    d["tipo_institucion"] = d["tipo_institucion"].map(_tipo)
    n_tipos = d.groupby("id_estudiante")["tipo_institucion"].nunique()
    ids = sorted(n_tipos[n_tipos > 1].index)
    return len(ids), ids


def calcular_estadisticas_pd(df):
    """Corre todos los resultados de la sección 3.5 (versión pandas)."""
    n_ambos, ids_ambos = estudiantes_ambos_tipos_pd(df)
    return {
        "instituciones_por_tipo": instituciones_por_tipo_pd(df),
        "estudiantes_por_tipo": estudiantes_por_tipo_pd(df),
        "promedio_institucion_examen": promedio_institucion_examen_pd(df),
        "promedio_tipo_examen": promedio_tipo_institucion_examen_pd(df),
        "distribucion": distribucion_calificaciones_pd(df),
        "n_estudiantes_ambos_tipos": n_ambos,
        "ids_estudiantes_ambos_tipos": ids_ambos,
    }

"""GRAFICAS"""
def _a_df(resultado, columnas):
    return resultado if isinstance(resultado, pd.DataFrame) else pd.DataFrame(resultado, columns=columnas)


def grafica_promedio_tipo_examen(promedios, ruta_salida):
    """Gráfica 1: barras agrupadas, promedio por tipo de institución y de examen."""
    df = _a_df(promedios, ["tipo_institucion", "tipo_examen", "promedio", "n_registros"])
    tabla = df.pivot(index="tipo_institucion", columns="tipo_examen", values="promedio")

    ax = tabla.plot(kind="bar", figsize=(7, 5), rot=0)
    for cont in ax.containers:
        ax.bar_label(cont, fmt="%.2f", padding=2)
    ax.set_title("Promedio de calificación por tipo de institución y de examen")
    ax.set_xlabel("Tipo de institución")
    ax.set_ylabel("Promedio (0-10)")
    ax.set_ylim(0, 10)
    ax.legend(title="Tipo de examen")
    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=150)
    plt.close()


def grafica_distribucion_calificaciones(distribucion, ruta_salida):
    """Gráfica 2: histograma de calificaciones, un panel por tipo de examen."""
    df = _a_df(distribucion, ["tipo_examen", "rango", "frecuencia", "porcentaje"])
    examenes = sorted(df["tipo_examen"].unique())

    fig, ejes = plt.subplots(1, len(examenes), figsize=(6 * len(examenes), 5), sharey=True, squeeze=False)
    for ax, exa in zip(ejes[0], examenes):
        sub = df[df["tipo_examen"] == exa]
        ax.bar(sub["rango"], sub["frecuencia"])
        ax.set_title(f"Distribución: {exa}")
        ax.set_xlabel("Rango de calificación")
        ax.tick_params(axis="x", rotation=45)
    ejes[0][0].set_ylabel("Número de registros")
    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=150)
    plt.close()


if __name__ == "__main__":
   
    cols = ["id_estudiante", "calificacion", "institucion", "tipo_institucion", "tipo_examen"]
    datos = [["e1", 8.5, "a", "publica", "idiomas"],
             ["e1", 7.0, "b", "privada", "conocimiento_general"],
             ["e2", 10.0, "b", "privada", "idiomas"]]
    print(calcular_estadisticas_manual(datos, cols))
    print(calcular_estadisticas_pd(pd.DataFrame(datos, columns=cols)))