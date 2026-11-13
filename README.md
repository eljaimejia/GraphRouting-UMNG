# GraphRouting UMNG

**Universidad Militar Nueva Granada**  
**Programa de Matemáticas Aplicadas y Computacionales**

<p align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="72" alt="Python"/>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://img.shields.io/badge/Matplotlib-3.x-11557C?style=for-the-badge&logo=matplotlib&logoColor=white" height="42" alt="Matplotlib"/>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://img.shields.io/badge/Tkinter-stdlib-FFD43B?style=for-the-badge&logo=python&logoColor=black" height="42" alt="Tkinter"/>
</p>

<p align="center">
  <i>Aplicación de escritorio para calcular rutas óptimas y estimar tiempos de recorrido<br/>en el Campus Cajicá de la UMNG.</i>
</p>

---

## ¿Por qué este proyecto?

Caminar por el campus no debería ser un problema de optimización, pero lo es.
Entre dos ubicaciones cualesquiera suele haber varios caminos posibles, con
longitudes distintas, y no siempre es obvio cuál combinación de senderos
minimiza la distancia total. Cualquiera que haya tenido que llegar de un
bloque al otro lado del campus en cinco minutos entiende la situación.

Ese es, en esencia, un **problema de camino mínimo sobre un grafo ponderado**,
uno de los tópicos centrales del programa de Matemáticas Aplicadas y
Computacionales. Nos propusimos entonces construir una herramienta que,
dado un origen y un destino, calcule la ruta más corta entre dos puntos del
campus y, de paso, estime el tiempo de desplazamiento a partir de mediciones
reales del usuario.

El proyecto se enmarca en la categoría **SoftLab** del Proyecto Fin de
Asignatura. Por eso el énfasis no está puesto en la interfaz gráfica ni en
la cantidad de funcionalidades, sino en el **análisis del problema**, la
**organización lógica del sistema** y la **justificación técnica** de las
decisiones que fuimos tomando en el camino.

---

## ¿Qué hace la aplicación?

- Carga el grafo del campus desde `CSV/Grafo_UMNG_Final.csv`.
- Permite seleccionar origen y destino con listas desplegables restringidas
  a los nodos existentes en el grafo.
- Calcula la ruta más corta con el algoritmo de **Dijkstra**.
- Registra el tiempo real de recorrido y ajusta un modelo de
  **regresión lineal simple** para predecir el tiempo de rutas nuevas.
- Muestra un gráfico con las mediciones registradas y la recta de regresión.

Todo el núcleo lógico está construido con la **biblioteca estándar de
Python** (`csv`, `tkinter`, `pathlib`); la única dependencia externa es
`matplotlib`, y se usa exclusivamente para visualizar los datos.


---

## Metodología

### 1. Modelado del problema

Representamos el campus como un **grafo no dirigido y ponderado**:

$$
G = (V, E, w)
$$

donde $V$ es el conjunto de ubicaciones (bloques, cafetería, biblioteca,
etc.), $E$ el conjunto de caminos peatonales, y $w : E \to \mathbb{R}^{+}$
la función que asigna a cada arista su longitud en metros.

Dados un origen $s \in V$ y un destino $t \in V$, el objetivo es encontrar
el camino

$$
P^{*} = \arg\min_{P \in \mathcal{P}(s,t)} \; \sum_{(u,v) \in P} w(u,v)
$$

siendo $\mathcal{P}(s,t)$ el conjunto de todos los caminos simples entre
$s$ y $t$.

### 2. Algoritmo de Dijkstra

Para cada nodo $v$ mantenemos una cota superior $d(v)$ de la distancia
mínima desde el origen, inicializada como:

$$
d(s) = 0, \qquad d(v) = +\infty \quad \forall \, v \neq s
$$

En cada iteración se extrae el nodo no visitado con menor $d(u)$ y se
**relajan** sus aristas salientes:

$$
d(v) \;\leftarrow\; \min\bigl(d(v),\; d(u) + w(u,v)\bigr)
\qquad \forall \, (u,v) \in E
$$

El algoritmo termina cuando el nodo destino $t$ es extraído; en ese momento
$d(t)$ es la distancia mínima. El camino se reconstruye con un diccionario
de predecesores $\pi$:

$$
P^{*} = \langle s = v_0,\, v_1,\, \dots,\, v_k = t \rangle,
\qquad v_{i} = \pi(v_{i+1})
$$

**Complejidad.** La implementación usa `min()` sobre el conjunto de nodos
pendientes, con costo $O(V^2)$. Para el tamaño del grafo del campus
($\approx 30$ nodos) esta cota sobra, y evita depender de `heapq`,
manteniendo el núcleo lógico autocontenido.

### 3. Predicción del tiempo de recorrido

El cálculo de rutas se complementa con un modelo de **regresión lineal
simple** que estima el tiempo $y$ (en minutos) a partir de la distancia
$x$ (en metros):

$$
\hat{y}(x) = m x + b
$$

Los parámetros se estiman por **mínimos cuadrados ordinarios** a partir de
$n$ mediciones $(x_i, y_i)$:

$$
m = \frac{ n \displaystyle\sum_{i=1}^{n} x_i y_i
         - \left( \displaystyle\sum_{i=1}^{n} x_i \right)
           \left( \displaystyle\sum_{i=1}^{n} y_i \right)}
        { n \displaystyle\sum_{i=1}^{n} x_i^{2}
         - \left( \displaystyle\sum_{i=1}^{n} x_i \right)^{2} }
\qquad
b = \frac{ \displaystyle\sum_{i=1}^{n} y_i
         - m \displaystyle\sum_{i=1}^{n} x_i }{n}
$$

El modelo necesita al menos dos mediciones para estimarse. Si el denominador
de $m$ es nulo (todas las distancias iguales), la predicción no se calcula
y la interfaz lo informa.

---

## Referencias

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009).
  *Introduction to Algorithms* (3rd ed.). MIT Press. — Capítulo 24:
  Single-Source Shortest Paths.
- Montgomery, D. C., Peck, E. A., & Vining, G. G. (2012). *Introduction to
  Linear Regression Analysis* (5th ed.). Wiley.
- Documentación oficial de Python: https://docs.python.org/3/
- Documentación oficial de Matplotlib: https://matplotlib.org/stable/

---

## Estructura del proyecto

La organización del repositorio separa el código fuente, los datos del grafo,
la documentación y los recursos gráficos en directorios independientes:

```text
GraphRouting-UMNG/
│
├── Code/
│   └── Pro_RecorridoInformativoCampus.py
│
├── CSV/
│   ├── Grafo_UMNG_Final.csv
│   └── Tiempos_Reales.csv
│
├── Docs/
│   ├── Categoría SoftLab_V3.pdf
│   └── Rutas_Campus_UMNG.xlsx
│
├── Images/
│   └── ImgUni.png
│
├── requirements.txt
├── .gitignore
│
└── README.md
```

### Descripción de los directorios

| Directorio / archivo | Descripción |
|---|---|
| `Code/` | Contiene el código fuente de la aplicación en Python. |
| `CSV/` | Contiene el grafo del campus y los tiempos reales registrados. |
| `Images/` | Contiene el mapa del campus usado por la aplicación. |
| `requirements.txt` | Lista Matplotlib, la dependencia externa del proyecto. |
| `.gitignore` | Archivos y directorios que Git debe excluir del control de versiones. |
| `README.md` | Presenta: descripción, metodología, funcionamiento y documentación del proyecto. |

---

## Integrantes del proyecto

- Kevin Wilder Cardozo V.
- David Antonio Mora F.
- Juan José Peláez B.

**Docente:** Juan Carlos Torres Sandoval  
**Asignatura:** Programación II  
**Categoría:** SoftLab — Proyecto Fin de Asignatura 
**Programa de Matemáticas Aplicadas y Computacionales**
**Universidad Militar Nueva Granada**
