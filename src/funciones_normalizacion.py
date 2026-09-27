from text_to_num import text2num
import math

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

def texto_numero(cadena):
    try:
        
        coma = cadena.replace(",", ".")
        punto = coma.replace("punto",".")
        espacio = punto.replace("_", " ")
        return float(espacio)
    except ValueError:
        try:
            if len(espacio) >= 4 :
                if "." in espacio:
                    entero, decimal = list(espacio.split(" . "))
                    numero = float(text2num(entero, "es")) + float(text2num(decimal, "es"))/10
                    return numero 
                elif " y " in espacio:
                    decena, unidad = list(espacio.split(" y "))
                    numero = float(text2num(decena, "es")) + float(text2num(unidad, "es"))
                    return numero
                else: 
                    return float(text2num(espacio, "es"))
        except Exception as e:
            print(espacio)
            return math.nan

            

def escala_calificacion(nota):
    try:
        if abs(nota) > 10 :
            return round(abs(nota) / 10, 1)
        else :
            return round( abs(nota), 1)

    except Exception as e:
        print("Error: ", e)
        return math.nan

if __name__ == '__main__':
    import sys

    try:
        
        print(f"Cadena original: {sys.argv[1]} \nCadena limpia: {texto_minusculas(str(sys.argv[1]))}")
        print(f"La cadena de salida es {nulos_none(texto_minusculas(str(sys.argv[1])))}")
        print(f"Texto a numero: {texto_numero(str(sys.argv[1]))}")


    except Exception as e:
        print("Error: ", e)
    
        




