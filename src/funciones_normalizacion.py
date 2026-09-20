def texto_minusculas(cadena):
    """Quita espacios en blanco al final e inicio
      de un str, convierte en minusculas y remplaza 
      espacios entre palabras por _"""
    if len(cadena) == 0:
        return cadena
    else:
        texto_minusculas = cadena.strip().lower()
        return texto_minusculas.replace(" ", "_")

def nulos_none(cadena, nulos=["", "na", "n/a", "null", "none", "nan", "n/c", "s/c"]):
    """Convierte los valores que se encuentran el vector nulos a None"""
    if cadena in nulos:
        return None
    else:
        return cadena


if __name__ == '__main__':
    import sys

    try:
        print(f"Cadena original: {sys.argv[1]} \nCadena limpia: {texto_minusculas(str(sys.argv[1]))}")
        print(f"La cadena de salida es {nulos_none(texto_minusculas(str(sys.argv[1])))}")
    except Exception as e:
        print("Error: ", e)
    
        




