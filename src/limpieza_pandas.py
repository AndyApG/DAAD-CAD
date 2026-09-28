import pandas as pd
from src.funciones_normalizacion import *

def limpieza_pandas(ruta):
    df_original = pd.read_csv(ruta)

    # Uniformizar a minusculas, quitar acentos y escribir nulos como None

    df = df_original.copy().map(lambda x : nulos_none(texto_minusculas(str(x))))

    # Conteo nulos 
    seguimiento_nulos ={"df_inicial" : df.isnull().sum().to_list()}

    # Instituciones con su tipo y frecuencia
    instituciones = df[["institucion","tipo_institucion"]].value_counts().reset_index(name="conteo_total")
    instituciones_dic = dict(list(zip(instituciones["institucion"],instituciones["tipo_institucion"])))

    # Imputación tipo de institucion con el nombre de la institucion
    df["tipo_institucion"] = df[["institucion", "tipo_institucion"]] \
        .apply(lambda x: instituciones_dic[x["institucion"]] 
                        if x["institucion"] in instituciones_dic 
                        else x["tipo_institucion"], axis=1)

    #instituciones["conteo_imputado"] = df[["institucion","tipo_institucion","modalidad"]].value_counts().reset_index(name="conteo_inicial")

    #seguimiento_nulos["imputacion_tipo_institucion" ]= df.isnull().sum().to_list()

    # Registros con id, nombre duplicados de idiomas

    duplicados_id_fecha = df.loc[df["tipo_examen"]=="idiomas", 
                                        ["id_estudiante","fecha_aplicacion"]] \
                                    .duplicated(keep="first")

    # Filtrar las filas duplicadas
    df_idiomas_unico = df.loc[df["tipo_examen"]=="idiomas"].loc[~duplicados_id_fecha]

    #Esta linea es equivalente a la de arriba
    #df_idiomas_unicos = df.loc[df["tipo_examen"]=="idiomas"].drop_duplicates(subset=["id_estudiante","fecha_aplicacion"])

    df_conocimiento_unicos = (
        df.loc[df["tipo_examen"]=="conocimiento_general", df.columns]
        .sort_values(by="fecha_aplicacion", ascending=False)   
        .drop_duplicates(subset="id_estudiante", keep="first") 
    )

    df_filtrado = pd.concat([df_idiomas_unico, df_conocimiento_unicos], ignore_index= True)
    #print(df_filtrado.isna().sum())

    #seguimiento_nulos["df_sin_duplicados"] = df_filtrado.isnull().sum().to_list()

    #La linea de abajo equivale a la de arriba
    #print(df[(df["tipo_examen"]== "conocimiento_general") & (~df.sort_values(by=["anio_aplicacion"], ascending= False).duplicated(subset=["id_estudiante","tipo_examen"],keep="first"))])
    df_filtrado["calificacion"] = df_filtrado["calificacion"].map(lambda x : texto_numero(str(x)))
    #seguimiento_nulos["df_calficacion_numero"] = df_filtrado.isnull().sum().to_list()
    

    df_sin_na = df_filtrado[["id_estudiante","calificacion", "institucion", "tipo_institucion", "tipo_examen", "modalidad", "anio_aplicacion"]]

    df_sin_na = df_sin_na.dropna()

    return df_sin_na 




"""
valoresunicos = pd.DataFrame([ len(list(df_original[i].unique())) for i in df_original.columns], df_original.columns.to_list())
print(valoresunicos)
print("NULOS EN DATA SET ORIGINAL")
nulo_original = df_original.isna().sum()
print(nulo_original)
print("----------")



df = df_original.copy().map(lambda x : nulos_none(texto_minusculas(str(x))))
valoresunicos = pd.DataFrame([ len(list(df[i].unique())) for i in df.columns], df.columns.to_list())
print(valoresunicos)
print("NULOS EN DATA SET  EN MINUSCULAS SIN ESPACIO")
nulo_original_minusculas = df.isna().sum()
print(nulo_original_minusculas)



df["calificacion"] = df["calificacion"].map(lambda x : texto_numero(str(x)))
cal_uni_minus=list(df["calificacion"].unique())
valoresunicos = pd.DataFrame([ len(list(df[i].unique())) for i in df.columns], df.columns.to_list())
print(valoresunicos)
df["calificacion"] = df["calificacion"].map(lambda x : escala_calificacion(x))
cal_uni_esca=list(df["calificacion"].unique())
valoresunicos = pd.DataFrame([ len(list(df[i].unique())) for i in df.columns], df.columns.to_list())
print(valoresunicos)
print("NULOS EN DATA SET CALIFICACION ENTRE 0 Y 10")
nulo_original_calificacion = df.isna().sum()
print(nulo_original_calificacion)

valoresunicos_tipo_examen = pd.DataFrame(list(df["tipo_examen"].unique()))
print(valoresunicos_tipo_examen)

valoresunicos_institucion = pd.DataFrame(list(df["institucion"].unique()))
print(valoresunicos_institucion)

valoresunicos_modalidad = pd.DataFrame(list(df["modalidad"].unique()))
print(valoresunicos_modalidad)

valoresunicos_tipo_institucion = pd.DataFrame(list(df["tipo_institucion"].unique()))
print(valoresunicos_tipo_institucion)

# diccionario de escuelas públicas
print("---")
data = df[["institucion","tipo_institucion"]].value_counts().to_frame()

print(data)

df_examen_idiomas = df[df["tipo_examen"] == "idiomas"]
filtro = df_examen_idiomas.sort_values(by="anio_aplicacion", ascending = True).duplicated(subset=["id_estudiante","nombre","apellido","tipo_examen"],keep="first")
duplicados_idiomas = df_examen_idiomas[filtro]
print(duplicados_idiomas[["id_estudiante","nombre","apellido"]].value_counts().to_frame())








print(df[df.sort_values(by=["anio_aplicacion"], ascending= False).duplicated(subset=["id_estudiante","nombre","apellido","tipo_examen"],keep="last")])

data = df[["institucion","tipo_institucion"]].value_counts().to_frame()
print(data)



"""

