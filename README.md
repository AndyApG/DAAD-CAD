# Proyecto integrador DAAD + CAD

Breve descripción del proyecto: qué hace, para qué sirve y a quién está dirigido.
Este proyecto se  realiza un análisis del rendimiento de  funciones que permiten leer, validar, limpiar, transformar y analizar un conjunto de datos de estudiantes de escuelas públicas y privadas. Se compara el rendimiento de funciones implementadas con pandas y otras hechas de manera directa.
## Estructura del proyecto

El proyecto está representado en el siguiente diagrama:

```text

Proyecto_Primer_Parcial/
├── data/              # Datos de entrada y salida en archivos de csv
├── logs/              # Archivos de registro de commits
├── outputs/           # Resultados generados (archivos de resultados de experimentos y gráficas)
├── src/               # Código fuente principal
│   └── ...            # Módulos y scripts
├── .gitignore         # Archivos/carpetas ignorados por Git
├── main.py            # Script principal de ejecución
├── README.md          # Documentación del proyecto
└── requirements.txt   # Dependencias del entorno

```
## Requerimientos de reproducibilidad

Este proyecto requiere **Python 3.14.7** (o superior).  
Para garantizar que cualquier persona pueda reproducir los resultados, se deben seguir estos pasos:

1. **Verificar versión de Python**
```bash
python --version 
```

2. **Crear un entorno virtual de Python en tu carpeta raíz del proyecto**

```bash 
 python -m venv venv
```

3. **Activar el entorno virtual**

**Windows**
```bash
.\venv\Scripts\activate
```

**Linux o Mac**
```bash
source venv/bin/activate
```

4. **Instalación de requerimientos**
``` bash
pip install -r requirements.txt
```


