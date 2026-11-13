import csv
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from pathlib import Path


class AppRutas(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GraphRouting UMNG")
        self.geometry("900x600")

        self.azul = "#003865"
        self.amarillo = "#F2C700"
        self.carpeta_datos = Path(__file__).resolve().parent.parent / "CSV"
        self.grafo = {}
        self.nodos = set()

        self.cargar_datos()
        self.pantalla_inicio()

    def cargar_datos(self):
        archivo = self.carpeta_datos / "Grafo_UMNG_Final.csv"
        try:

            with archivo.open("r", encoding="utf-8-sig") as datos:
                lector = csv.DictReader(datos)
                for fila in lector:
                    origen = fila["Nodo Origen"].strip()
                    destino = fila["Nodo Destino"].strip()
                    distancia = float(fila["Distancia (metros)"])

                    self.nodos.add(origen)
                    self.nodos.add(destino)

                    if origen not in self.grafo:
                        self.grafo[origen] = {}
                    if destino not in self.grafo:
                        self.grafo[destino] = {}

                    self.grafo[origen][destino] = distancia
                    self.grafo[destino][origen] = distancia
            print(f"{len(self.nodos)} nodos cargados")
        except OSError as error:
            messagebox.showerror("Error", f"No se pudo abrir el CSV:\n{error}")

    def pantalla_inicio(self):
        self.frame_actual = tk.Frame(self, bg=self.azul)
        self.frame_actual.pack(expand=True, fill="both")
        tk.Label(self.frame_actual, text="GraphRouting UMNG", font=("Arial", 28, "bold"), bg=self.azul, fg="white").pack(pady=(150, 10))
        tk.Label(self.frame_actual, text="Enrutador del Campus Cajicá", font=("Arial", 14), bg=self.azul, fg=self.amarillo).pack(pady=(0, 40))
        tk.Button(self.frame_actual, text="Ingresar", font=("Arial", 12, "bold"), bg=self.amarillo, fg=self.azul, command=self.pantalla_mapa).pack(ipadx=20, ipady=5)

    def pantalla_mapa(self):
        self.frame_actual.destroy()
        self.frame_actual = tk.Frame(self, bg="white")
        self.frame_actual.pack(expand=True, fill="both")

        frame_izq = tk.Frame(self.frame_actual, bg="white")
        frame_izq.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        tk.Label(frame_izq, text="Mapa del Campus", font=("Arial", 14, "bold"), bg="white", fg=self.azul).pack(pady=10)

        try:
            ruta_img = self.carpeta_datos.parent / "Images" / "ImgUni.png"
            imagen = tk.PhotoImage(file=str(ruta_img))
            # La imagen original es grande; así cabe en la ventana.
            imagen = imagen.subsample(4, 4)
            self.foto = imagen
            tk.Label(frame_izq, image=self.foto, bg="white").pack()
        except (tk.TclError, OSError):
            tk.Label(frame_izq, text="[No se pudo abrir ImgUni.png]", bg="white", fg="red").pack()

        frame_der = tk.Frame(self.frame_actual, bg=self.azul, width=300)
        frame_der.pack(side="right", fill="y")
        frame_der.pack_propagate(False)
        tk.Label(frame_der, text="Buscar Ruta", font=("Arial", 16, "bold"), bg=self.azul, fg=self.amarillo).pack(pady=20)
        tk.Label(frame_der, text="Origen:", bg=self.azul, fg="white", font=("Arial", 10, "bold")).pack(anchor="w", padx=20)
        lugares = sorted(self.nodos)
        # Solo permite escoger lugares que existen en el CSV.
        self.ent_origen = ttk.Combobox(frame_der, values=lugares, state="readonly", font=("Arial", 11))
        self.ent_origen.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_der, text="Destino:", bg=self.azul, fg="white", font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=(10, 0))
        self.ent_destino = ttk.Combobox(frame_der, values=lugares, state="readonly", font=("Arial", 11))
        self.ent_destino.pack(fill="x", padx=20, pady=5)

        tk.Button(frame_der, text="Calcular", bg=self.amarillo, fg=self.azul, font=("Arial", 11, "bold"), command=self.calcular).pack(fill="x", padx=20, pady=20)
        self.txt_resultado = tk.Text(frame_der, height=10, width=30, font=("Arial", 10), bg="white", fg="black")
        self.txt_resultado.pack(padx=20, pady=10)
        self.txt_resultado.insert(tk.END, "Aquí saldrá tu ruta...")
        self.txt_resultado.config(state="disabled")
        tk.Button(frame_der, text="Volver", bg="white", fg=self.azul, command=self.volver_inicio).pack(side="bottom", pady=20)

    def volver_inicio(self):
        self.frame_actual.destroy()
        self.pantalla_inicio()

    def buscar_camino_dijkstra(self, origen, destino):
        distancias = {nodo: float("inf") for nodo in self.grafo}
        anteriores = {}
        pendientes = set(self.grafo)
        distancias[origen] = 0

        while pendientes:
            # Dijkstra continúa desde el nodo pendiente más cercano.
            actual = min(pendientes, key=lambda nodo: distancias[nodo])
            if distancias[actual] == float("inf"):
                break
            if actual == destino:
                break

            pendientes.remove(actual)
            for vecino, distancia in self.grafo[actual].items():
                nueva_distancia = distancias[actual] + distancia
                if vecino in pendientes and nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    anteriores[vecino] = actual

        if distancias[destino] == float("inf"):
            return None, float("inf")

        camino = [destino]
        while camino[-1] != origen:
            camino.append(anteriores[camino[-1]])
        camino.reverse()
        return camino, distancias[destino]

    def calcular(self):
        origen = self.ent_origen.get()
        destino = self.ent_destino.get()
        if not origen or not destino:
            messagebox.showwarning("Falta", "Selecciona el origen y el destino de las listas.")
            return

        camino, distancia = self.buscar_camino_dijkstra(origen, destino)
        if camino is None:
            messagebox.showerror("Error", "No hay camino a ese destino.")
            return

        self.mostrar_resultado(camino, distancia)
        tiempo_real = simpledialog.askfloat(
            "Registro de datos",
            "¿Cuántos minutos te demoraste en realidad?\n\nCancela si no quieres guardar el dato.",
            minvalue=0,
        )
        if tiempo_real is not None:
            self.guardar_tiempo(distancia, tiempo_real)
            self.mostrar_resultado(camino, distancia)
            self.mostrar_grafica()
            messagebox.showinfo("Guardado", "Dato guardado. La gráfica muestra los tiempos registrados.")

    def mostrar_resultado(self, camino, distancia):
        prediccion = self.predecir_tiempo(distancia)
        texto = f"Ruta:\n{' -> '.join(camino)}\n\nDistancia: {distancia:.1f} m\n"
        if prediccion is None:
            texto += "Tiempo aprox.: registra tiempos en dos distancias distintas.\n"
        else:
            texto += f"Tiempo aproximado: {max(0, prediccion):.1f} min\n"

        self.txt_resultado.config(state="normal")
        self.txt_resultado.delete("1.0", tk.END)
        self.txt_resultado.insert(tk.END, texto)
        self.txt_resultado.config(state="disabled")

    def leer_tiempos(self):
        archivo = self.carpeta_datos / "Tiempos_Reales.csv"
        mediciones = []
        try:
            with archivo.open("r", encoding="utf-8") as datos:
                lector = csv.DictReader(datos)
                for fila in lector:
                    distancia = float(fila["Distancia (m)"])
                    tiempo = float(fila["Tiempo Real (min)"])
                    mediciones.append((distancia, tiempo))
        except FileNotFoundError:
            return []
        return mediciones

    def predecir_tiempo(self, distancia):
        mediciones = self.leer_tiempos()
        if len(mediciones) < 2:
            return None

        cantidad = len(mediciones)
        suma_distancias = sum(dato[0] for dato in mediciones)
        suma_tiempos = sum(dato[1] for dato in mediciones)
        suma_multiplicaciones = sum(dato[0] * dato[1] for dato in mediciones)
        suma_distancias_cuadradas = sum(dato[0] ** 2 for dato in mediciones)

        # Fórmula de mínimos cuadrados usando las sumas de x, y, xy y x².
        denominador = cantidad * suma_distancias_cuadradas - suma_distancias ** 2
        if denominador == 0:
            return None

        pendiente = (cantidad * suma_multiplicaciones - suma_distancias * suma_tiempos) / denominador
        intercepto = (suma_tiempos - pendiente * suma_distancias) / cantidad
        return pendiente * distancia + intercepto

    def guardar_tiempo(self, distancia, tiempo):
        archivo = self.carpeta_datos / "Tiempos_Reales.csv"
        nuevo = not archivo.exists()
        with archivo.open("a", newline="", encoding="utf-8") as datos:
            escritor = csv.writer(datos)
            if nuevo:
                escritor.writerow(["Distancia (m)", "Tiempo Real (min)"])
            escritor.writerow([distancia, tiempo])

    def mostrar_grafica(self):
        mediciones = self.leer_tiempos()
        if not mediciones:
            return

        distancias = [dato[0] for dato in mediciones]
        tiempos = [dato[1] for dato in mediciones]
        plt.scatter(distancias, tiempos, label="Mediciones")
        menor_distancia = min(distancias)
        mayor_distancia = max(distancias)
        if menor_distancia < mayor_distancia:
            tiempos_recta = [self.predecir_tiempo(menor_distancia), self.predecir_tiempo(mayor_distancia)]
            plt.plot([menor_distancia, mayor_distancia], tiempos_recta, color="red", label="Regresión lineal")
        plt.xlabel("Distancia (m)")
        plt.ylabel("Tiempo (min)")
        plt.title("Tiempo real según la distancia")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    AppRutas().mainloop()
