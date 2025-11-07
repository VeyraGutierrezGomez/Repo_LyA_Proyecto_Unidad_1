#esta linea importa tkinter con el alias tk para construir la interfaz
import tkinter as tk
#esta linea trae messagebox para mostrar cuadros de dialogo simples
from tkinter import messagebox
#esta linea importa la clase Image y ImageTk para cargar y usar imagenes en tkinter
from PIL import Image, ImageTk
#esta linea permite construir rutas relativas al archivo actual
from pathlib import Path
#esta linea importa funciones para generar numeros aleatorios
import random
#esta linea importa time para medir tiempos y usar sleep en la animacion
import time
#esta linea importa heapq para usar colas con prioridad en dijkstra
import heapq
#esta linea importa deepcopy para clonar estructuras sin referencia compartida
from copy import deepcopy

#esta funcion centra la ventana en la pantalla segun ancho y alto dados
def centrar_ventana(ventana, ancho, alto):
    #actualiza tareas pendientes de tkinter antes de medir
    ventana.update_idletasks()
    #calcula la posicion x para centrar horizontalmente
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    #calcula la posicion y para centrar verticalmente
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    #aplica la geometria que pone tamaño y posicion a la ventana
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


#clase que representa un grafo usando listas de adyacencia
class Grafo:
    #constructor que inicializa la estructura de adyacencia vacia
    def __init__(self):
        #diccionario donde cada clave es un nodo y el valor es lista de tuplas (destino,peso)
        #ejemplo: {'CDMX': [('Cancun',3), ('Guadalajara',1)], ...}
        self.adyacencia = {}

    #agrega una arista dirigida origen->destino con un peso
    def agregar_arista(self, origen, destino, peso):
        #si el origen no existe en el diccionario, crear lista vacia
        if origen not in self.adyacencia:
            self.adyacencia[origen] = []
        #añadir la tupla (destino,peso) a la lista del origen
        self.adyacencia[origen].append((destino, peso))

    #devuelve la lista de vertices del grafo (tanto claves como destinos)
    def obtener_vertices(self):
        #usar un set para evitar duplicados
        vertices = set(self.adyacencia.keys())
        #recorrer todas las listas de destinos y agregarlos al set
        for destinos in self.adyacencia.values():
            for v, _ in destinos:
                vertices.add(v)
        #convertir a lista y devolver
        return list(vertices)

    #metodo bellman-ford que tambien devuelve el diccionario prev para reconstruir caminos
    def bellman_ford_con_prev(self, inicio):
        """
        Ejecuta Bellman-Ford: devuelve (dist, prev) o (None, None) si detecta ciclo negativo.
        dist: dict nodo -> distancia mínima desde inicio
        prev: dict nodo -> predecesor en camino mínimo
        """
        #obtener todos los vertices presentes en el grafo
        vertices = self.obtener_vertices()
        #inicializar distancias con infinito para todos los vertices
        dist = {v: float("inf") for v in vertices}
        #inicializar predecesores en None
        prev = {v: None for v in vertices}
        #si el nodo inicio no esta en el grafo, devolver diccionarios vacios
        if inicio not in dist:
            #inicio no en grafo
            return {}, {}

        #distancia al inicio es cero
        dist[inicio] = 0

        #relajar las aristas V-1 veces para propagar distancias
        for _ in range(len(vertices) - 1):
            #bandera para detectar si hubo algun cambio en una iteracion
            cambio = False
            #recorrer cada nodo que tiene lista de adyacencia
            for u in self.adyacencia:
                #si la distancia a u es infinita no se puede relajar sus aristas
                if dist[u] == float("inf"):
                    continue
                #para cada arista u->v con peso, intentar relajar
                for v, peso in self.adyacencia[u]:
                    #si pasando por u llegamos a v con menor costo, actualizar
                    if dist[u] + peso < dist[v]:
                        dist[v] = dist[u] + peso
                        prev[v] = u
                        cambio = True
            #si en una pasada no hubo cambios, ya convergio y podemos salir
            if not cambio:
                break

        #una iteracion extra para detectar ciclo negativo: si se puede relajar, hay ciclo negativo
        for u in self.adyacencia:
            #si u no fue alcanzable, ignorarlo
            if dist[u] == float("inf"):
                continue
            for v, peso in self.adyacencia[u]:
                if dist[u] + peso < dist[v]:
                    #retornar None para indicar deteccion de ciclo negativo
                    return None, None  # ciclo negativo

        #devolver distancias y predecesores
        return dist, prev

    #metodo dijkstra que devuelve dist y prev (no valido si hay pesos negativos)
    def dijkstra_con_prev(self, inicio):
        """
        Ejecuta Dijkstra (solo válido si no hay aristas con peso negativo).
        devuelve (dist, prev).
        """
        #obtener vertices y preparar diccionarios
        vertices = self.obtener_vertices()
        dist = {v: float("inf") for v in vertices}
        prev = {v: None for v in vertices}
        #si inicio no esta en el grafo devolver diccionarios vacios
        if inicio not in dist:
            return {}, {}

        #distancia al inicio es cero
        dist[inicio] = 0
        #crear heap de prioridad con la tupla (dist,nodo)
        heap = [(0, inicio)]
        #conjunto para marcar nodos ya procesados
        visited = set()

        #mientras queden nodos en la cola
        while heap:
            #sacar el nodo con menor distancia conocida
            d_u, u = heapq.heappop(heap)
            #si ya fue procesado, saltarlo
            if u in visited:
                continue
            #marcar como procesado
            visited.add(u)
            #si el valor obtenido es mayor que el guardado, ignorar
            if d_u > dist[u]:
                continue
            #si u no tiene vecinos seguir con la siguiente iteracion
            if u not in self.adyacencia:
                continue
            #recorrer vecinos de u
            for v, peso in self.adyacencia[u]:
                #nota: si peso es negativo dijkstra puede fallar, aqui se usa solo para comparar
                nd = dist[u] + peso
                #si al pasar por u se mejora la distancia a v, actualizar y encolar
                if nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(heap, (nd, v))

        #devolver distancias y predecesores
        return dist, prev


#ventana inicial que pregunta tipo de mapa (nacional o internacional)
class VentanaInicio:
    #constructor que recibe la ventana raiz de tkinter
    def __init__(self, root):
        #guardar referencia a la ventana raiz
        self.root = root
        #poner titulo en la ventana principal
        self.root.title("Tipo de Vuelo")
        #centrar la ventana en pantalla con tamaño 400x250
        centrar_ventana(root, 400, 250)
        #configurar color de fondo de la ventana principal
        #self.root.geometry("400x250")
        self.root.configure(bg="#f0f0f0")

        #crear una etiqueta que pregunta si el mapa es nacional o internacional
        tk.Label(self.root, text="¿Mapa Nacional o Internacional?",
                 font=("Arial", 13, "bold"), bg="#f0f0f0").pack(pady=30)

        #boton que abre la ventana de origen/destino con opciones nacionales
        tk.Button(self.root, text="Vuelo Nacional", width=18, bg="#4CAF50", fg="white",
                  command=lambda: VentanaOrigenDestino("nacional")).pack(pady=10)
        #boton que abre la ventana de origen/destino con opciones internacionales
        tk.Button(self.root, text="Vuelo Internacional", width=18, bg="#2196F3", fg="white",
                  command=lambda: VentanaOrigenDestino("internacional")).pack(pady=10)


#ventana para elegir origen y destino usando menus desplegables
class VentanaOrigenDestino:
    #constructor que recibe el tipo ("nacional" o "internacional")
    def __init__(self, tipo):
        #guardar tipo en la instancia
        self.tipo = tipo
        #crear una ventana secundaria (toplevel)
        self.win = tk.Toplevel()
        #poner titulo que incluye el tipo seleccionado
        self.win.title(f"Origen y Destino ({tipo.capitalize()})")
        #centrar la ventana secundaria
        centrar_ventana(self.win, 420, 260)
        #self.win.geometry("420x260")
        #fondo de la ventana secundaria
        self.win.configure(bg="#f8f8f8")

        #etiqueta que indica seleccionar origen y destino
        tk.Label(self.win, text=f"Selecciona origen y destino ({tipo})",
                 font=("Arial", 12, "bold"), bg="#f8f8f8").pack(pady=12)

        #segun el tipo, crear la lista de lugares disponibles
        if tipo == "nacional":
            lugares = ["CDMX", "Guadalajara", "Monterrey", "Cancún", "Tijuana",
                       "Los Cabos", "Guanajuato", "Culiacan", "Puerto Vallarta", "Merida"]
        else:
            lugares = ["México", "USA", "Inglaterra", "Francia", "Japón", "Dubai", "Colombia", "Chile"]

        #crear un frame para organizar los widgets dentro de la ventana
        frame = tk.Frame(self.win, bg="#f8f8f8")
        frame.pack(pady=8)

        #etiqueta y menu desplegable para el origen
        tk.Label(frame, text="Origen:", bg="#f8f8f8").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        #variable que guarda la opcion seleccionada de origen
        self.var_origen = tk.StringVar(value=lugares[0])
        #crear el optionmenu para origen y colocarlo en la grilla
        tk.OptionMenu(frame, self.var_origen, *lugares).grid(row=0, column=1, padx=6, pady=6)

        #etiqueta y menu desplegable para el destino
        tk.Label(frame, text="Destino:", bg="#f8f8f8").grid(row=1, column=0, padx=6, pady=6, sticky="e")
        #variable que guarda la opcion seleccionada de destino
        self.var_destino = tk.StringVar(value=lugares[1])
        #crear el optionmenu para destino y colocarlo en la grilla
        tk.OptionMenu(frame, self.var_destino, *lugares).grid(row=1, column=1, padx=6, pady=6)

        #boton que al presionarlo abre la ventana del grafo con origen y destino elegidos
        tk.Button(self.win, text="Visualizar", bg="#4CAF50", fg="white", width=14,
                  command=self.abrir_grafo).pack(pady=18)

    #metodo que se ejecuta al presionar "Visualizar"
    def abrir_grafo(self):
        #obtener valores seleccionados en los optionmenu
        origen = self.var_origen.get()
        destino = self.var_destino.get()
        #crear la ventana que mostrara el grafo y la animacion
        VentanaGrafo(origen, destino, self.tipo)


#ventana que muestra el mapa, el grafo y la ruta mas corta encontrada
class VentanaGrafo:
    #constructor que recibe origen, destino y tipo de mapa
    def __init__(self, origen, destino, tipo):
        #guardar parametros en la instancia
        self.origen = origen
        self.destino = destino
        self.tipo = tipo

        #crear la ventana toplevel para la visualizacion
        self.win = tk.Toplevel()
        #titulo de la ventana
        self.win.title("Visualización del Grafo")
        #centrar la ventana grande en pantalla
        centrar_ventana(self.win, 820, 600)
        #self.win.geometry("820x600")
        #color de fondo blanco para la ventana del grafo
        self.win.configure(bg="#ffffff")

        #etiqueta que muestra el origen y destino elegidos
        tk.Label(self.win, text=f"Origen: {origen}    →    Destino: {destino}",
                 font=("Arial", 12, "bold"), bg="#ffffff").pack(pady=8)

        #canvas donde se dibuja el mapa y el grafo encima
        self.canvas = tk.Canvas(self.win, width=780, height=450, bg="white", highlightthickness=0)
        self.canvas.pack(pady=6)

        #determinar la ruta del archivo de imagen relativo al script actual
        base = Path(__file__).parent
        #si el tipo es nacional usar el mapa de mexico, si no usar mapa mundo
        if tipo == "nacional":
            ruta = base / "mapa_mexicoo.png"
        else:
            ruta = base / "mapa_mundo.png"

        #intentar abrir y mostrar la imagen del mapa en el canvas
        try:
            #abrir la imagen y redimensionarla al tamano del canvas
            mapa = Image.open(ruta).resize((780, 450))
            #convertir a objeto compatible con tkinter
            self.bg_img = ImageTk.PhotoImage(mapa)
            #dibujar la imagen en la esquina superior izquierda del canvas
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_img)
            #mantener referencia: self.bg_img
        except Exception as e:
            #si ocurre un error al cargar la imagen, mostrar un mensaje de error
            messagebox.showerror("Error", f"No se pudo cargar la imagen del mapa:\n{e}")
            #seguir sin imagen (la aplicacion sigue funcionando sin fondo)

        #construir la estructura del grafo y definir posiciones en pantalla
        self.grafo = Grafo()
        #diccionario que guarda coordenadas (x,y) para cada nodo
        self.posiciones = {}
        #llamar al metodo que agrega las aristas base y asigna posiciones
        self.crear_grafo_y_posiciones()

        #aplicar una variacion aleatoria a los pesos para simular cambios en tiempos
        self.aplicar_variacion_aleatoria()

        #ejecutar bellman-ford para calcular rutas iniciales y poder animar el camino
        dist, prev = self.grafo.bellman_ford_con_prev(self.origen)
        #si bellman devolvio None significa que detecto ciclo negativo
        if dist is None:
            #mostrar error de ciclo negativo y permitir que el usuario cierre la ventana
            messagebox.showerror("Error", "Se detectó un ciclo negativo. No es posible calcular ruta.")
            #aun asi permitimos cerrar la ventana para ver la comparacion en on_close
        else:
            #dibujar todas las aristas en gris con sus pesos
            self.dibujar_aristas_con_pesos()
            #dibujar los nodos encima del mapa
            self.dibujar_nodos()
            #reconstruir el camino desde el diccionario prev devuelto por bellman-ford
            camino = self.reconstruir_camino(prev, self.origen, self.destino)
            #si la lista camino tiene longitud menor o igual a 1 significa que no hay ruta valida
            if len(camino) <= 1:
                #mostrar advertencia de que no existe ruta entre origen y destino
                messagebox.showwarning("Sin ruta", "No existe una ruta entre origen y destino.")
            else:
                #calcular el tiempo total sumando pesos entre nodos consecutivos del camino
                total_horas = sum(self.obtener_peso_entre(camino[i], camino[i+1]) for i in range(len(camino)-1))
                #iniciar la animacion del avion despues de 100 ms para que todo ya este dibujado
                self.win.after(100, lambda: self.animar_camino(camino))
                #crear un pequeño panel informativo que muestra la ruta y el tiempo total
                info_frame = tk.Frame(self.win, bg="#e0f7fa", bd=2, relief="groove")
                info_frame.pack(pady=10)
                #etiqueta que indica que se encontro la ruta mas corta
                tk.Label(info_frame, text="Ruta más corta encontrada", font=("Arial", 11, "bold"), bg="#e0f7fa").pack()
                #etiqueta que muestra los nodos del camino separados por flechas
                tk.Label(info_frame, text=f"{' → '.join(camino)}", font=("Arial", 10), bg="#e0f7fa").pack()
                #etiqueta que muestra el tiempo total calculado
                tk.Label(info_frame, text=f"Tiempo total: {total_horas} h", font=("Arial", 10, "bold"), bg="#e0f7fa").pack()

        #cuando el usuario cierre la ventana, ejecutar el metodo on_close para comparar algoritmos
        self.win.protocol("WM_DELETE_WINDOW", self.on_close)

    #metodo que agrega las aristas base y asigna posiciones en el canvas
    def crear_grafo_y_posiciones(self):
        #aqui se definen las aristas base (tiempos en horas) y las posiciones de cada nodo
        #ajusta coordenadas si necesitas mover puntos en el mapa
        if self.tipo == "nacional":
            #aristas base (orientadas): cada una indica origen, destino y tiempo estimado
            self.grafo.agregar_arista("Tijuana", "Los Cabos", 2)
            self.grafo.agregar_arista("Tijuana", "Monterrey", 6)
            self.grafo.agregar_arista("Los Cabos", "Culiacan", 1)
            self.grafo.agregar_arista("Culiacan", "Puerto Vallarta", 2)
            self.grafo.agregar_arista("Puerto Vallarta", "Los Cabos", 6)
            self.grafo.agregar_arista("Culiacan", "Monterrey", 2)
            self.grafo.agregar_arista("Culiacan", "Tijuana", 3)
            self.grafo.agregar_arista("Monterrey", "CDMX", 4)
            self.grafo.agregar_arista("Monterrey", "Guadalajara", 3)
            self.grafo.agregar_arista("Guadalajara", "CDMX", 1)
            self.grafo.agregar_arista("Guadalajara", "Puerto Vallarta", 2)
            self.grafo.agregar_arista("CDMX", "Cancún", 3)
            self.grafo.agregar_arista("Merida", "Guanajuato", 3)
            self.grafo.agregar_arista("Merida", "CDMX", 4)
            self.grafo.agregar_arista("Cancún", "Merida", 1)
            self.grafo.agregar_arista("Guanajuato", "Monterrey", 2)

            #asignar coordenadas x,y para cada ciudad en el canvas
            self.posiciones = {
                "Tijuana": (95, 95),
                "Monterrey": (440, 180),
                "CDMX": (470, 325),
                "Guadalajara": (390, 295),
                "Cancún": (735, 280),
                "Culiacan": (270, 205),
                "Los Cabos": (215, 230),
                "Guanajuato": (430, 280),
                "Merida": (690, 285),
                "Puerto Vallarta": (330, 270)
            }
        else:
            #version internacional: agregar aristas entre paises y asignar posiciones aproximadas
            self.grafo.agregar_arista("Chile", "México", 10)
            self.grafo.agregar_arista("Colombia", "Chile", 6)
            self.grafo.agregar_arista("Colombia", "México", 8)
            self.grafo.agregar_arista("México", "USA", 5)
            self.grafo.agregar_arista("México", "Colombia", 8)
            self.grafo.agregar_arista("México", "Chile", 10)
            self.grafo.agregar_arista("USA", "México", 5)
            self.grafo.agregar_arista("USA", "Inglaterra", 9)
            self.grafo.agregar_arista("Inglaterra", "Francia", 2)
            self.grafo.agregar_arista("Inglaterra", "Japón", 12)
            self.grafo.agregar_arista("Francia", "Japón", 12)
            self.grafo.agregar_arista("Francia", "USA", 9)
            self.grafo.agregar_arista("Japón", "Dubai", 10)
            self.grafo.agregar_arista("Dubai", "Francia", 10)

            #posiciones aproximadas para cada pais/region en el canvas
            self.posiciones = {
                "USA": (150, 115),     #este de ee.uu
                "Inglaterra": (309, 78),        #reino unido
                "Francia": (317, 95),          #francia
                "Japón": (605, 127),           #japon
                "Dubai": (430, 165),           #dubai
                "Chile": (158, 330),           #chile
                "Colombia": (145, 215),        #colombia
                "México": (85, 170)           #mexico
            }

    #aplica una variacion aleatoria a cada peso para simular cambios en tiempos
    def aplicar_variacion_aleatoria(self):
        #recorrer cada origen en la adyacencia (usar list para evitar modificar mientras iteras)
        for u in list(self.grafo.adyacencia.keys()):
            #lista temporal que guardara nuevas tuplas (destino,nuevo_peso)
            nuevas = []
            for v, w in self.grafo.adyacencia[u]:
                #generar un delta aleatorio entre -2 y 2 horas
                delta = random.randint(-2, 2)
                #calcular el nuevo peso sumando delta
                nuevo = w + delta
                #si prefieres evitar tiempos negativos descomenta la siguiente linea en tu codigo original
                #nuevo = max(1, nuevo)
                #agregar la nueva tupla a la lista temporal
                nuevas.append((v, nuevo))
            #reemplazar la lista original por la lista con variacion
            self.grafo.adyacencia[u] = nuevas

    #dibuja todas las aristas en gris y muestra su peso en horas
    def dibujar_aristas_con_pesos(self):
        #recorrer cada origen en la adyacencia
        for u in self.grafo.adyacencia:
            #si no existe posicion para el origen saltarla
            if u not in self.posiciones:
                continue
            #obtener coordenadas del origen
            x1, y1 = self.posiciones[u]
            #recorrer cada destino y peso desde u
            for v, peso in self.grafo.adyacencia[u]:
                #si no existe posicion para el destino saltarlo
                if v not in self.posiciones:
                    continue
                #coordenadas del destino
                x2, y2 = self.posiciones[v]
                #dibujar linea con flecha que representa la arista
                self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="#777777", width=1.5)
                #calcular punto medio para colocar el texto del peso
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                #desplazar un poco el texto para que no coincida con la flecha
                self.canvas.create_text(mx, my - 12, text=f"{peso} h", font=("Arial", 9, "bold"), fill="black")

    #dibuja los nodos (ciudades) encima del mapa
    def dibujar_nodos(self):
        #recorrer el diccionario de posiciones
        for ciudad, (x, y) in self.posiciones.items():
            #dibujar un pequeño oval rojo para representar el nodo
            self.canvas.create_oval(x-6, y-6, x+6, y+6, fill="#ff4d4d", outline="black")
            #dibujar el nombre de la ciudad encima del nodo
            self.canvas.create_text(x, y-14, text=ciudad, font=("Arial", 9, "bold"), fill="black")

    #devuelve el peso de la arista u->v si existe, sino None
    def obtener_peso_entre(self, u, v):
        #si u no esta en adyacencia no hay aristas desde u
        if u not in self.grafo.adyacencia:
            return None
        #buscar entre las tuplas (destino,peso)
        for dest, peso in self.grafo.adyacencia[u]:
            if dest == v:
                return peso
        #si no se encontro la arista devolver None
        return None

    #reconstruye el camino desde el diccionario prev retornado por los algoritmos
    def reconstruir_camino(self, prev, origen, destino):
        #lista que ira guardando el camino invertido
        camino = []
        #empezar desde el destino y seguir prev hasta None o inicio
        cur = destino
        #si destino no esta en prev o no fue alcanzado, el loop terminara en None
        while cur is not None:
            #insertar al inicio para construir camino en orden correcto
            camino.insert(0, cur)
            #avanzar al predecesor
            cur = prev.get(cur, None)
        #validar que el primer nodo del camino sea el origen esperado
        if len(camino) == 0 or camino[0] != origen:
            #si no coincide, devolver lista con solo el origen para indicar ausencia de camino real
            return [origen]  # indicar "sin camino real"
        #devolver la lista con el camino correcto
        return camino

    #anima el avion por el camino resaltando las aristas en rojo
    def animar_camino(self, camino):
        #primero dibujar lineas rojas sobre cada arista del camino para resaltarlas
        for i in range(len(camino)-1):
            u, v = camino[i], camino[i+1]
            #si alguna ciudad no tiene posicion saltarla
            if u not in self.posiciones or v not in self.posiciones:
                continue
            #obtener coordenadas inicio y fin
            x1, y1 = self.posiciones[u]
            x2, y2 = self.posiciones[v]
            #sobrescribir la arista con una linea mas gruesa y roja
            self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="#cc0000", width=3)
        #crear el avion como un oval azul en el primer nodo del camino
        start = camino[0]
        x0, y0 = self.posiciones[start]
        avion = self.canvas.create_oval(x0-5, y0-5, x0+5, y0+5, fill="#0000cc", outline="white")

        #mover el avion suavemente por cada segmento del camino
        for i in range(len(camino)-1):
            u, v = camino[i], camino[i+1]
            #si faltan posiciones, saltar ese segmento
            if u not in self.posiciones or v not in self.posiciones:
                continue
            #coordenadas de inicio y fin del segmento
            x1, y1 = self.posiciones[u]
            x2, y2 = self.posiciones[v]
            #numero de pasos para interpolar la posicion del avion
            pasos = 80
            #iterar cada paso y actualizar las coordenadas del oval que representa el avion
            for t in range(pasos + 1):
                x = x1 + (x2 - x1) * (t / pasos)
                y = y1 + (y2 - y1) * (t / pasos)
                #mover el oval a la nueva posicion calculada
                self.canvas.coords(avion, x-6, y-6, x+6, y+6)
                #forzar actualizacion de la ventana para que se vea el movimiento
                self.win.update()
                #pequeña pausa para controlar la velocidad de animacion
                time.sleep(0.015)  # velocidad de la animacion (ajustable)

    #metodo que se ejecuta al cerrar la ventana y compara dijkstra vs bellman-ford
    def on_close(self):
        """
        cuando se cierra la ventana, ejecuta dijkstra y bellman-ford en:
         1) grafo forzado sin pesos negativos (cada peso = max(1, peso_actual))
         2) grafo con los pesos actuales (puede contener negativos)
        mide tiempos y muestra comparación, además comprueba si los resultados coinciden.
        """
        try:
            #base: clonar el grafo actual (puede contener negativos)
            grafo_neg = Grafo()
            #usar deepcopy para que no compartan referencias internas
            grafo_neg.adyacencia = deepcopy(self.grafo.adyacencia)

            #crear una version del grafo donde los pesos se fuerzan a ser no negativos
            grafo_nonneg = Grafo()
            grafo_nonneg.adyacencia = {}
            #recorrer cada origen y su lista de aristas
            for u, lista in self.grafo.adyacencia.items():
                nueva_lista = []
                for v, w in lista:
                    #forzar minimo 1 hora para evitar negativos en esta copia
                    w_nn = max(1, w)  # fuerza no negativo (al menos 1)
                    nueva_lista.append((v, w_nn))
                #asignar la lista modificada al grafo sin negativos
                grafo_nonneg.adyacencia[u] = nueva_lista

            #guardar origen y destino actuales para pasar a los algoritmos
            origen = self.origen
            destino = self.destino

            #funcion auxiliar que ejecuta un metodo (bellman o dijkstra) y mide su tiempo
            def ejecutar_y_medir(grafo_obj, metodo_nombre):
                #marcar tiempo de inicio con alta precision
                start = time.perf_counter()
                #elegir metodo segun nombre
                if metodo_nombre == "bellman":
                    dist, prev = grafo_obj.bellman_ford_con_prev(origen)
                else:
                    dist, prev = grafo_obj.dijkstra_con_prev(origen)
                #marcar tiempo de fin y calcular duracion
                end = time.perf_counter()
                dur = end - start
                #devolver dist, prev y tiempo empleado
                return dist, prev, dur

            #1) ejecutar ambos algoritmos en la version sin negativos
            bf_dist_nn, bf_prev_nn, bf_time_nn = ejecutar_y_medir(grafo_nonneg, "bellman")
            dj_dist_nn, dj_prev_nn, dj_time_nn = ejecutar_y_medir(grafo_nonneg, "dijkstra")

            #preparar variables para comparar resultados en la version sin negativos
            iguales_nn = False
            ruta_bf_nn = []
            ruta_dj_nn = []
            #si bellman devolvio resultados validos y dijkstra tambien
            if bf_dist_nn is not None and bf_dist_nn != {} and dj_dist_nn != {}:
                #reconstruir rutas usando prev
                ruta_bf_nn = self.reconstruir_camino(bf_prev_nn, origen, destino)
                ruta_dj_nn = self.reconstruir_camino(dj_prev_nn, origen, destino)
                #obtener valores numericos de distancia al destino (si existen)
                val_bf = bf_dist_nn.get(destino, float("inf"))
                val_dj = dj_dist_nn.get(destino, float("inf"))
                #comparar valores con tolerancia muy pequeña
                iguales_nn = abs((val_bf if val_bf != float("inf") else float("inf")) - (val_dj if val_dj != float("inf") else float("inf"))) < 1e-9

            #2) ejecutar ambos algoritmos en el grafo con pesos actuales (puede tener negativos)
            bf_dist_neg, bf_prev_neg, bf_time_neg = ejecutar_y_medir(grafo_neg, "bellman")
            dj_dist_neg, dj_prev_neg, dj_time_neg = ejecutar_y_medir(grafo_neg, "dijkstra")

            #comprobar si bellman detecto ciclo negativo (en cuyo caso bf_dist_neg es None)
            bf_neg_detected = (bf_dist_neg is None)

            #inicializar variables para la comparacion en grafo con negativos
            iguales_neg = False
            ruta_bf_neg = []
            ruta_dj_neg = []
            #si bellman no detecto ciclo negativo y ambos devolvieron diccionarios
            if not bf_neg_detected and bf_dist_neg != {} and dj_dist_neg != {}:
                #reconstruir rutas desde prev para cada algoritmo
                ruta_bf_neg = self.reconstruir_camino(bf_prev_neg, origen, destino)
                ruta_dj_neg = self.reconstruir_camino(dj_prev_neg, origen, destino)
                #obtener valores numericos de distancia al destino en ambos casos
                val_bf_n = bf_dist_neg.get(destino, float("inf"))
                val_dj_n = dj_dist_neg.get(destino, float("inf"))
                #comparar si coinciden (si dijkstra no fallo)
                iguales_neg = abs((val_bf_n if val_bf_n != float("inf") else float("inf")) - (val_dj_n if val_dj_n != float("inf") else float("inf"))) < 1e-9

            #construir una lista de lineas que serviran como resumen para mostrar en un messagebox
            msg_lines = []
            msg_lines.append("Comparación de tiempos y resultados:")
            msg_lines.append("")
            msg_lines.append("GRAFO SIN PESOS NEGATIVOS (se forzaron pesos >= 1):")
            #añadir linea con tiempo de bellman-ford en la version sin negativos
            msg_lines.append(f"  Bellman-Ford: {bf_time_nn:.6f} s")
            #añadir linea con tiempo de dijkstra en la version sin negativos
            msg_lines.append(f"  Dijkstra:     {dj_time_nn:.6f} s")
            #si bellman regreso None informar deteccion de ciclo negativo (caso inesperado aqui)
            if bf_dist_nn is None:
                msg_lines.append("  Bellman-Ford: detectó ciclo negativo (inexplicable en versión sin negativos).")
            else:
                #obtener distancias finales al destino para mostrarlas
                bf_val = bf_dist_nn.get(destino, None)
                dj_val = dj_dist_nn.get(destino, None)
                msg_lines.append(f"  distancia (Bellman-Ford) al destino '{destino}': {bf_val}")
                msg_lines.append(f"  distancia (Dijkstra)       al destino '{destino}': {dj_val}")
                msg_lines.append(f"  rutas reconstruidas BF: {' → '.join(ruta_bf_nn) if ruta_bf_nn else '(no hay)'}")
                msg_lines.append(f"  rutas reconstruidas DJ: {' → '.join(ruta_dj_nn) if ruta_dj_nn else '(no hay)'}")
                msg_lines.append(f"  ¿Resultados iguales? {'Sí' if iguales_nn else 'No'}")


            msg_lines.append("")
            msg_lines.append("GRAFO CON PESOS ACTUALES (puede tener negativos):")
            msg_lines.append("")
            #explicacion breve y sencilla sobre por que dijkstra no es valido con negativos
            msg_lines.append("En este caso, el grafo conserva sus pesos originales, por lo que pueden existir aristas con pesos negativos.")
            msg_lines.append("Dijkstra no puede manejar correctamente pesos negativos, ya que asume que una vez que se encuentra")
            msg_lines.append("la ruta más corta hacia un nodo, esta no puede mejorar. Si existen pesos negativos, podría aparecer un")
            msg_lines.append("camino más corto después, pero Dijkstra no lo revisará nuevamente, produciendo resultados incorrectos.")
            msg_lines.append("")
            msg_lines.append("Bellman-Ford, en cambio, sí admite pesos negativos porque relaja todas las aristas repetidamente,")
            msg_lines.append("ajustando las distancias aunque se descubra un camino más corto más adelante. Además, puede detectar")
            msg_lines.append("la presencia de ciclos negativos.")
            msg_lines.append("")

            #mostrar el resumen en un cuadro de dialogo (messagebox) con las lineas unidas por saltos
            messagebox.showinfo("Comparación Dijkstra vs Bellman-Ford", "\n".join(msg_lines))
        except Exception as e:
            #si ocurre cualquier error durante la comparacion, mostrar mensaje de error con la excepcion
            messagebox.showerror("Error en comparación", f"Ocurrió un error al comparar:\n{e}")
        finally:
            #en cualquier caso, intentar cerrar la ventana visual del grafo
            try:
                self.win.destroy()
            except:
                #si ocurre error al destruir la ventana, se ignora para evitar bloquear la aplicacion
                pass


#bloque principal que arranca la aplicacion cuando se ejecute el script directamente
if __name__ == "__main__":
    #crear la ventana raiz
    root = tk.Tk()
    #crear la instancia de la ventana inicial que contiene los botones de tipo de mapa
    app = VentanaInicio(root)
    #iniciar el bucle principal de eventos de tkinter
    root.mainloop()
