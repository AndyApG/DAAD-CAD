import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ARCHIVOS = {
    "carga": "datos_experimento_carga",
    "nulos": "datos_experimento_conteo_nulos",
    "limpieza": "datos_experimento_limpieza",
    "estadisticas": "datos_experimento_estadisticas", 
}

OPERACIONES_GRAFICA = ["carga", "nulos", "limpieza", "estadisticas_total"]


def _leer_tiempos(ruta_csv, nombre_operacion, n_tamano):
    df = pd.read_csv(ruta_csv)
    if "Operacion" not in df.columns:
        df["Operacion"] = nombre_operacion
    if "N" not in df.columns:
        df["N"] = n_tamano
    return df[["Operacion", "Pandas", "Tiempo", "N"]]


def calcular_metricas(carpeta_archivos, tamanos):
   
    renglones = []
    for sufijo, n_tamano in tamanos:
        for operacion, prefijo in ARCHIVOS.items():
            ruta = os.path.join(carpeta_archivos, f"{prefijo}_{sufijo}.csv")
            if not os.path.exists(ruta):
                print(f"[metricas] No existe {ruta}, se omite.")
                continue
            datos = _leer_tiempos(ruta, operacion, n_tamano)
            for op, sub in datos.groupby("Operacion", sort=False):
                t_pd = sub.loc[sub["Pandas"] == 1, "Tiempo"].mean()
                t_man = sub.loc[sub["Pandas"] == 0, "Tiempo"].mean()
                n = int(sub["N"].iloc[0])
                renglones.append({
                    "operacion": op,
                    "tamano": sufijo,
                    "N": n,
                    "T_manual_s": t_man,
                    "T_pandas_s": t_pd,
                    "speedup": t_man / t_pd,
                    "reduccion_pct": (t_man - t_pd) / t_man * 100,
                    "throughput_manual_reg_s": n / t_man,
                    "throughput_pandas_reg_s": n / t_pd,
                })
    return pd.DataFrame(renglones)


def grafica_tiempos(tabla, ruta_salida, operaciones=OPERACIONES_GRAFICA):
    """Gráfica de tiempo de ejecución manual vs pandas contra el tamaño N."""
    fig, ax = plt.subplots(figsize=(8, 5))
    for op in operaciones:
        sub = tabla[tabla["operacion"] == op].sort_values("N")
        if sub.empty:
            continue
        linea, = ax.plot(sub["N"], sub["T_manual_s"], marker="o", linestyle="--", label=f"{op} (manual)")
        ax.plot(sub["N"], sub["T_pandas_s"], marker="s", color=linea.get_color(), label=f"{op} (pandas)")
    ax.set_yscale("log")
    ax.set_xlabel("Número de registros (N)")
    ax.set_ylabel("Tiempo promedio (s, escala log)")
    ax.set_title("Tiempo de ejecución: implementación manual vs pandas")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=150)
    plt.close()


def grafica_speedup(tabla, ruta_salida, operaciones=OPERACIONES_GRAFICA):
    """Gráfica de speedup (T_manual / T_pandas) contra el tamaño N."""
    fig, ax = plt.subplots(figsize=(8, 5))
    for op in operaciones:
        sub = tabla[tabla["operacion"] == op].sort_values("N")
        if sub.empty:
            continue
        ax.plot(sub["N"], sub["speedup"], marker="o", label=op)
    ax.axhline(1, color="gray", linestyle="--", label="S = 1 (mismo tiempo)")
    ax.set_xlabel("Número de registros (N)")
    ax.set_ylabel("Speedup  S = T_manual / T_pandas")
    ax.set_title("Speedup de pandas respecto a la implementación manual")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=150)
    plt.close()


def generar_reporte(carpeta_archivos, carpeta_graficas, lotes, n_total):
    tamanos = [(f"lote_{n}", n) for n in lotes] + [("total", n_total)]
    tabla = calcular_metricas(carpeta_archivos, tamanos)

    tabla.to_csv(os.path.join(carpeta_archivos, "tabla_comparativa_rendimiento.csv"), index=False)
    grafica_tiempos(tabla, os.path.join(carpeta_graficas, "tiempo_ejecucion.png"))
    grafica_speedup(tabla, os.path.join(carpeta_graficas, "speedup.png"))
    return tabla
