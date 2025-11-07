import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path
import random
import time
import heapq
from copy import deepcopy

# --------------------------------------------------
# Función para centrar una ventana en la pantalla
# --------------------------------------------------
def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


# --------------------------------------------------
# Clase Grafo: Representa un grafo usando listas de adyacencia
# --------------------------------------------------
class Grafo:
    def __init__(self):
        # Diccionario: { nodo: [(destino, peso), ...] }
        self.adyacencia = {}

    def agregar_arista(self, origen, destino, peso):
        # Agrega una arista dirigida al grafo con su peso
        if origen not in self.adyacencia:
            self.adyacencia[origen] = []
        self.adyacencia[origen].append((destino, peso))

    def obtener_vertices(self):
        # Obtiene una lista con todos los nodos del grafo
        vertices = set(self.adyacencia.keys())
        for destinos in self.adyacencia.values():
            for v, _ in destinos:
                vertices.add(v)
        return list(vertices)

    def bellman_ford_con_prev(self, inicio):
        """
        Ejecuta Bellman-Ford: devuelve (dist, prev) o (None, None) si detecta ciclo negativo.
        dist: dict nodo -> distancia mínima desde inicio
        prev: dict nodo -> predecesor en camino mínimo
        """
        vertices = self.obtener_vertices()
        dist = {v: float("inf") for v in vertices}
        prev = {v: None for v in vertices}
        if inicio not in dist:
            # inicio no en grafo
            return {}, {}

        dist[inicio] = 0

        # Relajar V-1 veces
        for _ in range(len(vertices) - 1):
            cambio = False
            for u in self.adyacencia:
                # si u tiene distancia infinita no puede relajar
                if dist[u] == float("inf"):
                    continue
                for v, peso in self.adyacencia[u]:
                    if dist[u] + peso < dist[v]:
                        dist[v] = dist[u] + peso
                        prev[v] = u
                        cambio = True
            if not cambio:
                break

        # Iteración extra para detectar ciclo negativo
        for u in self.adyacencia:
            if dist[u] == float("inf"):
                continue
            for v, peso in self.adyacencia[u]:
                if dist[u] + peso < dist[v]:
                    return None, None  # ciclo negativo

        return dist, prev

    def dijkstra_con_prev(self, inicio):
        """
        Ejecuta Dijkstra (solo válido si no hay aristas con peso negativo).
        devuelve (dist, prev).
        """
        vertices = self.obtener_vertices()
        dist = {v: float("inf") for v in vertices}
        prev = {v: None for v in vertices}
        if inicio not in dist:
            return {}, {}

        dist[inicio] = 0
        # heap de (dist, nodo)
        heap = [(0, inicio)]
        visited = set()

        while heap:
            d_u, u = heapq.heappop(heap)
            if u in visited:
                continue
            visited.add(u)
            # si el valor sacado es mayor que el guardado, ignorar
            if d_u > dist[u]:
                continue
            # iterar vecinos
            if u not in self.adyacencia:
                continue
            for v, peso in self.adyacencia[u]:
                # si peso negativo, dijkstra puede dar resultados incorrectos,
                # pero lo ejecutamos igual para la comparación.
                nd = dist[u] + peso
                if nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(heap, (nd, v))

        return dist, prev


# ----------------------------
# Ventana inicial (tipo de mapa)
# ----------------------------
class VentanaInicio:
    def __init__(self, root):
        self.root = root
        self.root.title("Tipo de Vuelo")
        centrar_ventana(root, 400, 250)
        #self.root.geometry("400x250")
        self.root.configure(bg="#f0f0f0")

        tk.Label(self.root, text="¿Mapa Nacional o Internacional?",
                 font=("Arial", 13, "bold"), bg="#f0f0f0").pack(pady=30)

        tk.Button(self.root, text="Vuelo Nacional", width=18, bg="#4CAF50", fg="white",
                  command=lambda: VentanaOrigenDestino("nacional")).pack(pady=10)
        tk.Button(self.root, text="Vuelo Internacional", width=18, bg="#2196F3", fg="white",
                  command=lambda: VentanaOrigenDestino("internacional")).pack(pady=10)


# ----------------------------
# Ventana para elegir origen/destino (OptionMenu)
# ----------------------------
class VentanaOrigenDestino:
    def __init__(self, tipo):
        self.tipo = tipo
        self.win = tk.Toplevel()
        self.win.title(f"Origen y Destino ({tipo.capitalize()})")
        centrar_ventana(self.win, 420, 260)
        #self.win.geometry("420x260")
        self.win.configure(bg="#f8f8f8")

        tk.Label(self.win, text=f"Selecciona origen y destino ({tipo})",
                 font=("Arial", 12, "bold"), bg="#f8f8f8").pack(pady=12)

        if tipo == "nacional":
            lugares = ["CDMX", "Guadalajara", "Monterrey", "Cancún", "Tijuana",
                       "Los Cabos", "Guanajuato", "Culiacan", "Puerto Vallarta", "Merida"]
        else:
            lugares = ["México", "USA", "Inglaterra", "Francia", "Japón", "Dubai", "Colombia", "Chile"]

        frame = tk.Frame(self.win, bg="#f8f8f8")
        frame.pack(pady=8)

        tk.Label(frame, text="Origen:", bg="#f8f8f8").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        self.var_origen = tk.StringVar(value=lugares[0])
        tk.OptionMenu(frame, self.var_origen, *lugares).grid(row=0, column=1, padx=6, pady=6)

        tk.Label(frame, text="Destino:", bg="#f8f8f8").grid(row=1, column=0, padx=6, pady=6, sticky="e")
        self.var_destino = tk.StringVar(value=lugares[1])
        tk.OptionMenu(frame, self.var_destino, *lugares).grid(row=1, column=1, padx=6, pady=6)

        tk.Button(self.win, text="Visualizar", bg="#4CAF50", fg="white", width=14,
                  command=self.abrir_grafo).pack(pady=18)

    def abrir_grafo(self):
        origen = self.var_origen.get()
        destino = self.var_destino.get()
        VentanaGrafo(origen, destino, self.tipo)


# ----------------------------
# Ventana de visualización (mapa + grafo)
# ----------------------------
class VentanaGrafo:
    def __init__(self, origen, destino, tipo):
        self.origen = origen
        self.destino = destino
        self.tipo = tipo

        # ventana
        self.win = tk.Toplevel()
        self.win.title("Visualización del Grafo")
        centrar_ventana(self.win, 820, 600)
        #self.win.geometry("820x600")
        self.win.configure(bg="#ffffff")

        tk.Label(self.win, text=f"Origen: {origen}    →    Destino: {destino}",
                 font=("Arial", 12, "bold"), bg="#ffffff").pack(pady=8)

        # canvas
        self.canvas = tk.Canvas(self.win, width=780, height=450, bg="white", highlightthickness=0)
        self.canvas.pack(pady=6)

        # cargar imagen de mapa (ruta relativa al archivo)
        base = Path(__file__).parent
        if tipo == "nacional":
            ruta = base / "mapa_mexicoo.png"
        else:
            ruta = base / "mapa_mundo.png"

        try:
            mapa = Image.open(ruta).resize((780, 450))
            self.bg_img = ImageTk.PhotoImage(mapa)
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_img)
            # mantener referencia: self.bg_img
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen del mapa:\n{e}")
            # seguir sin imagen (pero mejor avisar)

        # construir grafo (con pesos base) y posiciones en pantalla
        self.grafo = Grafo()
        self.posiciones = {}
        self.crear_grafo_y_posiciones()

        # aplicar variación aleatoria a los pesos (simular cambios de tiempo)
        self.aplicar_variacion_aleatoria()

        # ejecutar Bellman-Ford (primera vez para calcular ruta y animar)
        dist, prev = self.grafo.bellman_ford_con_prev(self.origen)
        if dist is None:
            messagebox.showerror("Error", "Se detectó un ciclo negativo. No es posible calcular ruta.")
            # aún así permitimos cerrar la ventana para ver la comparación en on_close
        else:
            # dibujar todas las aristas (grises) con pesos
            self.dibujar_aristas_con_pesos()
            # dibujar nodos encima
            self.dibujar_nodos()
            # reconstruir camino
            camino = self.reconstruir_camino(prev, self.origen, self.destino)
            # si no hay camino factible:
            if len(camino) <= 1:
                messagebox.showwarning("Sin ruta", "No existe una ruta entre origen y destino.")
            else:
                # resaltar y animar el camino óptimo (rojo)
                total_horas = sum(self.obtener_peso_entre(camino[i], camino[i+1]) for i in range(len(camino)-1))
                # animar el avión
                self.win.after(100, lambda: self.animar_camino(camino))
                # mostrar información de ruta sin cerrar el mapa
                info_frame = tk.Frame(self.win, bg="#e0f7fa", bd=2, relief="groove")
                info_frame.pack(pady=10)
                tk.Label(info_frame, text="Ruta más corta encontrada", font=("Arial", 11, "bold"), bg="#e0f7fa").pack()
                tk.Label(info_frame, text=f"{' → '.join(camino)}", font=("Arial", 10), bg="#e0f7fa").pack()
                tk.Label(info_frame, text=f"Tiempo total: {total_horas} h", font=("Arial", 10, "bold"), bg="#e0f7fa").pack()

        # capturar cierre de la ventana para mostrar la comparación
        self.win.protocol("WM_DELETE_WINDOW", self.on_close)

    # ----------------------------
    # Construcción del grafo y posiciones (mantener tu estructura)
    # ----------------------------
    def crear_grafo_y_posiciones(self):
        # Aquí definimos las aristas base (horas) y las posiciones de cada nodo en el canvas.
        # Ajusta coordenadas si necesitas mover puntos en el mapa.
        if self.tipo == "nacional":
            # aristas base (orientadas)
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

            # posiciones (coordenadas del mapa 780x500)
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
            # internacional
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

            self.posiciones = {
                "USA": (150, 115),     # Este de EE.UU
                "Inglaterra": (309, 78),        # Reino Unido
                "Francia": (317, 95),          # Francia
                "Japón": (605, 127),           # Japón
                "Dubai": (430, 165),           # Dubai
                "Chile": (158, 330),           # Chile
                "Colombia": (145, 215),        # Colombia
                "México": (85, 170)           # México
            }

    # ----------------------------
    # Aplicar variación aleatoria a los pesos
    # ----------------------------
    def aplicar_variacion_aleatoria(self):
        # Reemplazamos las listas en self.grafo.adyacencia por versiones con variación.
        for u in list(self.grafo.adyacencia.keys()):
            nuevas = []
            for v, w in self.grafo.adyacencia[u]:
                # variación entre -2 y +2 horas (puede generar negativos — Bellman-Ford lo soporta)
                delta = random.randint(-2, 2)
                nuevo = w + delta
                # si prefieres evitar tiempos negativos, descomenta la línea siguiente:
                # nuevo = max(1, nuevo)
                nuevas.append((v, nuevo))
            self.grafo.adyacencia[u] = nuevas

    # ----------------------------
    # Dibujar todas las aristas y pesos (gris)
    # ----------------------------
    def dibujar_aristas_con_pesos(self):
        for u in self.grafo.adyacencia:
            if u not in self.posiciones:
                continue
            x1, y1 = self.posiciones[u]
            for v, peso in self.grafo.adyacencia[u]:
                if v not in self.posiciones:
                    continue
                x2, y2 = self.posiciones[v]
                # línea con flecha gris
                self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="#777777", width=1.5)
                # peso al lado de la línea
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                # desplazar ligeramente para que no se sobreponga con la flecha
                self.canvas.create_text(mx, my - 12, text=f"{peso} h", font=("Arial", 9, "bold"), fill="black")

    # ----------------------------
    # Dibujar nodos encima del mapa
    # ----------------------------
    def dibujar_nodos(self):
        for ciudad, (x, y) in self.posiciones.items():
            self.canvas.create_oval(x-6, y-6, x+6, y+6, fill="#ff4d4d", outline="black")
            self.canvas.create_text(x, y-14, text=ciudad, font=("Arial", 9, "bold"), fill="black")

    # ----------------------------
    # Obtener peso entre u->v (si existe)
    # ----------------------------
    def obtener_peso_entre(self, u, v):
        if u not in self.grafo.adyacencia:
            return None
        for dest, peso in self.grafo.adyacencia[u]:
            if dest == v:
                return peso
        return None

    # ----------------------------
    # Reconstruir camino desde prev dict
    # ----------------------------
    def reconstruir_camino(self, prev, origen, destino):
        camino = []
        cur = destino
        # si destino no está en prev y no en vertices, devolvemos lista vacía
        # reconstrucción hasta inicio o None
        while cur is not None:
            camino.insert(0, cur)
            cur = prev.get(cur, None)
        # validar que el camino empiece en origen
        if len(camino) == 0 or camino[0] != origen:
            return [origen]  # indicar "sin camino real"
        return camino

    # ----------------------------
    # Animar el avión siguiendo el camino (resalta en rojo)
    # ----------------------------
    def animar_camino(self, camino):
        # dibujar líneas rojas del camino
        for i in range(len(camino)-1):
            u, v = camino[i], camino[i+1]
            if u not in self.posiciones or v not in self.posiciones:
                continue
            x1, y1 = self.posiciones[u]
            x2, y2 = self.posiciones[v]
            # sobrescribir la arista con rojo (más ancho)
            self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill="#cc0000", width=3)
        # crear avión en el primer nodo
        start = camino[0]
        x0, y0 = self.posiciones[start]
        avion = self.canvas.create_oval(x0-5, y0-5, x0+5, y0+5, fill="#0000cc", outline="white")

        # mover avión por cada segmento
        for i in range(len(camino)-1):
            u, v = camino[i], camino[i+1]
            if u not in self.posiciones or v not in self.posiciones:
                continue
            x1, y1 = self.posiciones[u]
            x2, y2 = self.posiciones[v]
            pasos = 80
            for t in range(pasos + 1):
                x = x1 + (x2 - x1) * (t / pasos)
                y = y1 + (y2 - y1) * (t / pasos)
                self.canvas.coords(avion, x-6, y-6, x+6, y+6)
                self.win.update()
                time.sleep(0.015)  # velocidad de la animación (ajustable)

    # ----------------------------
    # comparación al cerrar la ventana
    # ----------------------------
    def on_close(self):
        """
        cuando se cierra la ventana, ejecuta dijkstra y bellman-ford en:
         1) grafo forzado sin pesos negativos (cada peso = max(1, peso_actual))
         2) grafo con los pesos actuales (puede contener negativos)
        mide tiempos y muestra comparación, además comprueba si los resultados coinciden.
        """
        try:
            # base: grafo con pesos actuales (posible negativos)
            grafo_neg = Grafo()
            grafo_neg.adyacencia = deepcopy(self.grafo.adyacencia)

            # crear grafo sin negativos: forzar pesos a >= 1
            grafo_nonneg = Grafo()
            grafo_nonneg.adyacencia = {}
            for u, lista in self.grafo.adyacencia.items():
                nueva_lista = []
                for v, w in lista:
                    w_nn = max(1, w)  # fuerza no negativo (al menos 1)
                    nueva_lista.append((v, w_nn))
                grafo_nonneg.adyacencia[u] = nueva_lista

            origen = self.origen
            destino = self.destino

            # helper para ejecutar y medir
            def ejecutar_y_medir(grafo_obj, metodo_nombre):
                start = time.perf_counter()
                if metodo_nombre == "bellman":
                    dist, prev = grafo_obj.bellman_ford_con_prev(origen)
                else:
                    dist, prev = grafo_obj.dijkstra_con_prev(origen)
                end = time.perf_counter()
                dur = end - start
                return dist, prev, dur

            # 1) grafo sin negativos
            bf_dist_nn, bf_prev_nn, bf_time_nn = ejecutar_y_medir(grafo_nonneg, "bellman")
            dj_dist_nn, dj_prev_nn, dj_time_nn = ejecutar_y_medir(grafo_nonneg, "dijkstra")

            # comparar resultados (sin negativos dijkstra debería coincidir)
            iguales_nn = False
            ruta_bf_nn = []
            ruta_dj_nn = []
            if bf_dist_nn is not None and bf_dist_nn != {} and dj_dist_nn != {}:
                ruta_bf_nn = self.reconstruir_camino(bf_prev_nn, origen, destino)
                ruta_dj_nn = self.reconstruir_camino(dj_prev_nn, origen, destino)
                # comparar distancias al destino (si existe)
                val_bf = bf_dist_nn.get(destino, float("inf"))
                val_dj = dj_dist_nn.get(destino, float("inf"))
                iguales_nn = abs((val_bf if val_bf != float("inf") else float("inf")) - (val_dj if val_dj != float("inf") else float("inf"))) < 1e-9

            # 2) grafo con negativos (actual)
            bf_dist_neg, bf_prev_neg, bf_time_neg = ejecutar_y_medir(grafo_neg, "bellman")
            dj_dist_neg, dj_prev_neg, dj_time_neg = ejecutar_y_medir(grafo_neg, "dijkstra")

            # analizar si bellman detectó ciclo negativo
            bf_neg_detected = (bf_dist_neg is None)

            iguales_neg = False
            ruta_bf_neg = []
            ruta_dj_neg = []
            if not bf_neg_detected and bf_dist_neg != {} and dj_dist_neg != {}:
                ruta_bf_neg = self.reconstruir_camino(bf_prev_neg, origen, destino)
                ruta_dj_neg = self.reconstruir_camino(dj_prev_neg, origen, destino)
                val_bf_n = bf_dist_neg.get(destino, float("inf"))
                val_dj_n = dj_dist_neg.get(destino, float("inf"))
                iguales_neg = abs((val_bf_n if val_bf_n != float("inf") else float("inf")) - (val_dj_n if val_dj_n != float("inf") else float("inf"))) < 1e-9

            # construir mensaje resumen
            msg_lines = []
            msg_lines.append("Comparación de tiempos y resultados:")
            msg_lines.append("")
            msg_lines.append("GRAFO SIN PESOS NEGATIVOS (se forzaron pesos >= 1):")
            msg_lines.append(f"  Bellman-Ford: {bf_time_nn:.6f} s")
            msg_lines.append(f"  Dijkstra:     {dj_time_nn:.6f} s")
            if bf_dist_nn is None:
                msg_lines.append("  Bellman-Ford: detectó ciclo negativo (inexplicable en versión sin negativos).")
            else:
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
            msg_lines.append("En este caso, el grafo conserva sus pesos originales, por lo que pueden existir aristas con pesos negativos.")
            msg_lines.append("Dijkstra no puede manejar correctamente pesos negativos, ya que asume que una vez que se encuentra")
            msg_lines.append("la ruta más corta hacia un nodo, esta no puede mejorar. Si existen pesos negativos, podría aparecer un")
            msg_lines.append("camino más corto después, pero Dijkstra no lo revisará nuevamente, produciendo resultados incorrectos.")
            msg_lines.append("")
            msg_lines.append("Bellman-Ford, en cambio, sí admite pesos negativos porque relaja todas las aristas repetidamente,")
            msg_lines.append("ajustando las distancias aunque se descubra un camino más corto más adelante. Además, puede detectar")
            msg_lines.append("la presencia de ciclos negativos.")
            msg_lines.append("")


            # mostrar en un messagebox (multi-línea)
            messagebox.showinfo("Comparación Dijkstra vs Bellman-Ford", "\n".join(msg_lines))
        except Exception as e:
            messagebox.showerror("Error en comparación", f"Ocurrió un error al comparar:\n{e}")
        finally:
            # cerrar la ventana visual
            try:
                self.win.destroy()
            except:
                pass


# ----------------------------
# Ejecutar aplicación
# ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaInicio(root)
    root.mainloop()
