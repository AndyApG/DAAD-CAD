def limpieza_texto(str):
    """Quita espacios en blanco al final e inicio
      de un str, convierte en minusculas y remplaza 
      espacios entre palabras por _"""
    texto_minusculas = str.strip().lower()
    return texto_minusculas.replace(" ", "_")



if __name__ == '__main__':
    import sys
    print(f"Cadena original: { sys.argv[1]} \nCadena limpia: {limpieza_texto(str(sys.argv[1]))}")




