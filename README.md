# Simulador de Rutas Aéreas con Bellman-Ford y Dijkstra

## Descripción

Este proyecto es una **simulación interactiva de rutas de vuelo** desarrollada en **Python (versión 3.13)** con interfaz gráfica mediante **Tkinter** y procesamiento de imágenes con **Pillow (PIL)**.

El sistema modela una **red de aeropuertos** donde los vuelos tienen tiempos asociados (pesos).
Implementa los algoritmos **Bellman-Ford** y **Dijkstra** para calcular las rutas más cortas entre ciudades, demostrando que **Bellman-Ford sigue funcionando incluso con pesos negativos (descuentos o ajustes)**.

El programa cuenta con una **interfaz visual animada**, donde el usuario elige tipo de vuelo (nacional o internacional), selecciona origen y destino, y observa el recorrido del avión en un mapa.
Además, compara el rendimiento y exactitud de ambos algoritmos.

## Objetivos

* Implementar el **algoritmo Bellman-Ford** con detección de **ciclos negativos**.
* Comparar su funcionamiento y tiempos de ejecución con el algoritmo **Dijkstra**.
* Simular una **red de aeropuertos** con diferentes costos (positivos y negativos).
* Visualizar gráficamente las rutas y el recorrido más corto.
* Mostrar advertencias al detectar un ciclo negativo en el grafo.
* Desarrollar una interfaz interactiva con selección de vuelo, origen y destino.

## Tecnologías utilizadas

* **Lenguaje:** Python 3.13
* **Bibliotecas:**

  * `tkinter` (interfaz gráfica)
  * `PIL` (Pillow, para manejo de imágenes)
  * `heapq`, `random`, `time` (para algoritmos y animación)
* **IDE recomendado:** Visual Studio Code
* **Imágenes:**

  * `mapa_mexicoo.png` (vuelos nacionales)
  * `mapa_mundo.png` (vuelos internacionales)

## Instalación y configuración

### 1. Instalar Python

1.1 Descarga **Python 3.13** desde la página oficial:
   👉 [https://www.python.org/downloads/](https://www.python.org/downloads/)
1.2 Durante la instalación, **marca la casilla** “Add Python to PATH”.
1.3 Espera a que termine la instalación.
1.4 Verifica que esté instalado correctamente abriendo **PowerShell o CMD** y escribiendo:

   ```bash
   python --version
   ```

### 2. Instalar la biblioteca Pillow

2.1 Abre una terminal en tu computadora (PowerShell o CMD).
2.2 Copia y ejecuta el siguiente comando (tu ruta de instalación puede variar):

   ```bash
   C:\Users\usuario1\AppData\Local\Programs\Python\Python313\python.exe -m pip install pillow
   ```
2.3 Espera a que finalice la instalación.
   Si se instaló correctamente, verás un mensaje como:

   ```
   Successfully installed pillow-x.x.x
   ```
### 3. Archivos requeridos

3.1 Guarda las siguientes imágenes en la **misma carpeta** donde tengas tu archivo `aeropuerto.py`:

* `mapa_mexicoo.png`
* `mapa_mundo.png`

> Si no existen las imágenes, el programa mostrará un mensaje de error y no cargará el mapa.

### 4. Ejecutar el programa

Puedes ejecutar el programa de dos maneras:

#### Opción 1: Desde VS Code

• Abre la carpeta del proyecto en **Visual Studio Code**.
• Abre el archivo `aeropuerto.py`.
• Haz clic en el botón **▶️ “Correr”** en la esquina superior derecha.
• Espera a que se abra la ventana del programa.

#### Opción 2: Desde PowerShell o CMD

• Abre una terminal en la carpeta donde está tu archivo.
• Escribe:

   ```bash
   python aeropuerto.py
   ```
• Presiona **Enter** y se ejecutará el programa.

## Funcionamiento general

1. **Ventana de Inicio:**
   El usuario elige si desea un vuelo **nacional o internacional**.

2. **Selección de Origen y Destino:**
   Se muestran menús desplegables con ciudades según el tipo de vuelo.

3. **Visualización de Mapa:**

   * Se dibuja el **grafo de aeropuertos** con sus conexiones y tiempos.
   * Se aplica **Bellman-Ford** para hallar la ruta más corta.
   * Se anima un **avión** siguiendo el camino óptimo.

4. **Comparación de Algoritmos:**
   Al cerrar la ventana del mapa, el sistema:

   • Ejecuta **Bellman-Ford** y **Dijkstra**.
   • Mide tiempos de ejecución.
   • Muestra un mensaje comparando sus resultados.
   • Advierte si existe un **ciclo negativo**.

## Funcionalidades principales

• Simulación de rutas de vuelo nacionales e internacionales.
• Visualización gráfica del grafo con animación del recorrido.
• Cálculo del **camino más corto** entre ciudades.
• Detección y alerta de **ciclos negativos**.
• Comparación de rendimiento entre **Bellman-Ford y Dijkstra**.

## Interfaz gráfica

El programa utiliza **Tkinter** y se compone de tres ventanas principales:

• **Inicio:** Selección del tipo de vuelo (nacional o internacional)         
• **Origen/Destino:** Elección de ciudades para el recorrido                         
• **Mapa/Grafo:** Visualización del grafo, animación y comparación de algoritmos 


## Autores

Proyecto académico desarrollado por:

• Rubi Maria Cobos Ramos
• Ingridh Maricela Gracia Flores
• Veyra Maria Gutierrez Gomez
• Jesus Emmanuel Lopez Zuñiga
• Jennifer Elizabeth Yepez Lopez

