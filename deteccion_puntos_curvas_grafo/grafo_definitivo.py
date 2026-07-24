import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from PIL import Image
import matplotlib.lines as mlines


# Definimos una función para obtener cuadrados de tamaño fijo en una matriz
def obtener_cuadrados(matriz, tamano):
    cuadrados = []
    pos_cuadrados = []
    for fila in range(len(matriz) - tamano + 1):
        for columna in range(len(matriz[0]) - tamano + 1):
            cuadrado = []
            pos_cuadrado = []
            for i in range(tamano):
                fila_actual = fila + i
                fila_cuadrado = []
                coord_cuadrado = []
                for j in range(tamano):
                    columna_actual = columna + j
                    fila_cuadrado.append(matriz[fila_actual][columna_actual])
                    coord_cuadrado.append([fila_actual, columna_actual])
                cuadrado.append(fila_cuadrado)
                pos_cuadrado.append(coord_cuadrado)
            cuadrados.append(cuadrado)
            pos_cuadrados.append(pos_cuadrado)
    return cuadrados, pos_cuadrados


matriz = np.array([[7, 6, 9, 3],
                   [9, 5, 7, 4],
                   [8, 4, 8, 6],
                   [5, 3, 5, 4],
                   [6, 7, 0, 3]])

# matriz = np.array([[78, 99, 50, 70, 90, 55, 77, 66, 43],
#                    [54, 54, 49, 77, 88, 81, 80, 72, 41],
#                    [57, 12, 13, 52, 63, 54, 71, 32, 14]])
#
# matriz = np.array([
#         [78, 99, 50],
#         [54, 54, 49],
#         [57, 12, 13]
#     ])

# matriz = np.array([[7, 6, 8, 3],
#                    [9, 1, 7, 4],
#                    [8, 3, 8, 6],
#                    [5, 2, 5, 4],
#                    [6, 7, 0, 3]])

# matriz = np.array([[7, 6, 12, 3],
#                    [9, 5, 7, 4],
#                    [8, 4, 3, 6],
#                    [5, -2, 5, 4],
#                    [6, 7, 2, 3]])
#
#
# matriz = np.array([[7, 6, 9, 3],
#                    [9, 5, 7, 4],
#                    [8, 4, 8, 6],
#                    [5, 7, 0, 4],
#                    [6, 3, 5, 3]])
#
#
# plt.figure(figsize=(15, 15), dpi=300)
#
# img = Image.open('picaso.png').convert('L')
# matriz = np.asarray(img)
#
# matriz = np.array([[3, 25, 10],
#                    [15, 30, 40],
#                    [28, 7, 51]])
#
# matriz = np.array([
#         [78, 99, 50],
#         [54, 54, 49],
#         [57, 12, 13]
#     ])

filas = matriz.shape[0]
columnas = matriz.shape[1]
G = nx.grid_2d_graph(filas, columnas)  # Crea un grafo 2D del tamaño deseado

# Creamos los nodos del grafo, correspondientes a las posiciones de la matriz
# A cada nodo le añadimos las etiquetas correspondientes (su valor)

for i in range(filas):
    for j in range(columnas):
        G.add_node((i, j), value=matriz[i][j])

# Creamos listas para almacenar los nodos correspondientes a máximos, mínimos y puntos de silla

maximos = []
minimos = []
sillas = []
sillas_borde = []

for node in G.nodes:
    vecinos = G.neighbors(node)  # G.neighbors recoge los nodos en orden: arriba, abajo, izquierda, derecha
    valores = [G.nodes[n]["value"] for n in vecinos]
    print(f"Los valores de los vecinos son: {valores}")
    if G.nodes[node]["value"] > max(valores):
        maximos.append(node)
    if G.nodes[node]["value"] < min(valores):
        minimos.append(node)
    if len(valores) == 4:
        if valores[0] > G.nodes[node]["value"] and \
                valores[1] > G.nodes[node]["value"]:
            if valores[2] < G.nodes[node]["value"] and  \
                    valores[3] < G.nodes[node]["value"]:
                sillas.append(node)
        if valores[0] < G.nodes[node]["value"] and \
                valores[1] < G.nodes[node]["value"]:
            if valores[2] > G.nodes[node]["value"] and \
                    valores[3] > G.nodes[node]["value"]:
                sillas.append(node)
    if len(valores) == 3:
        if node[0] == 0 or node[0] == filas-1:
            if valores[0] > G.nodes[node]["value"] > valores[1] and \
                    valores[2] > G.nodes[node]["value"]:
                sillas_borde.append(node)
            if valores[0] < G.nodes[node]["value"] < valores[2] and \
                    valores[1] > G.nodes[node]["value"]:
                sillas_borde.append(node)

        if node[1] == 0 or node[1] == columnas-1:
            if valores[0] > G.nodes[node]["value"] > valores[2] and \
                    valores[1] > G.nodes[node]["value"]:
                sillas_borde.append(node)
            if valores[0] < G.nodes[node]["value"] < valores[2] and \
                    valores[1] < G.nodes[node]["value"]:
                sillas_borde.append(node)

# Obtenemos todos los cuadrados de tamaño 2 en la matriz
[cuadrados, pos_cuadrados] = obtener_cuadrados(matriz, 2)

# Buscamos las hidden saddles
n = 0
hidden_saddles = []
nodos = []
for cuadrado in cuadrados:
    if cuadrado[0][0] < cuadrado[0][1] and \
            cuadrado[0][0] < cuadrado[1][0]:
        if cuadrado[1][1] < cuadrado[0][1] and \
                cuadrado[1][1] < cuadrado[1][0]:
            coord = pos_cuadrados[n]
            hidden_saddles.append(coord)
            nodo = (cuadrado[0][0] + cuadrado[0][1] +
                    cuadrado[1][0] + cuadrado[1][1] -
                    max(cuadrado[0][0], cuadrado[0][1], cuadrado[1][0], cuadrado[1][1]) -
                    min(cuadrado[0][0], cuadrado[0][1], cuadrado[1][0], cuadrado[1][1])) / 2
            nodos.append(nodo)
    if cuadrado[0][0] > cuadrado[0][1] and \
            cuadrado[0][0] > cuadrado[1][0]:
        if cuadrado[1][1] > cuadrado[0][1] and \
                cuadrado[1][1] > cuadrado[1][0]:
            coord = pos_cuadrados[n]
            hidden_saddles.append(coord)
            nodo = (cuadrado[0][0] + cuadrado[0][1] +
                    cuadrado[1][0] + cuadrado[1][1] -
                    max(cuadrado[0][0], cuadrado[0][1], cuadrado[1][0], cuadrado[1][1]) -
                    min(cuadrado[0][0], cuadrado[0][1], cuadrado[1][0], cuadrado[1][1])) / 2
            nodos.append(nodo)
    n = n + 1

m = 0
h_saddles = []
for lugar in hidden_saddles:
    x = (lugar[0][0][0] + lugar[1][0][0]) / 2
    y = (lugar[0][0][1] + lugar[0][1][1]) / 2
    G.add_node((x, y), value=nodos[m])
    G.add_edge((lugar[0][0][0], lugar[0][0][1]), (x, y))
    G.add_edge((lugar[0][1][0], lugar[0][1][1]), (x, y))
    G.add_edge((lugar[1][0][0], lugar[1][0][1]), (x, y))
    G.add_edge((lugar[1][1][0], lugar[1][1][1]), (x, y))
    h_saddles.append((x, y))
    m = m + 1

# Asignamos colores a los nodos según su categoría y los agregamos al grafo:

mapa_color = []

for node in G.nodes():
    if node in maximos:
        mapa_color.append('red')
    elif node in minimos:
        mapa_color.append('blue')
    elif node in sillas:
        mapa_color.append('green')
    elif node in h_saddles:
        mapa_color.append('purple')
    elif node in sillas_borde:
        mapa_color.append('yellow')
    else:
        mapa_color.append('gray')

valores_grafo = {n: G.nodes[n]["value"] for n in G.nodes}
pos = {(x, y): (y, -x) for x, y in G.nodes()}
nx.draw_networkx(G, pos=pos, labels=valores_grafo, font_size=20, with_labels=True, node_color=mapa_color)

# Para las curvas de nivel:
# X = [pos[nodo][0] for nodo in G.nodes()]
# Y = [pos[nodo][1] for nodo in G.nodes()]
# Z = [G.nodes[nodo]["value"] for nodo in G.nodes()]
#
# # Generamos la triangulación usando la librería matplotlib.tri, esto nos servirá para las curvas de nivel
# triangulacion = tri.Triangulation(X, Y)
#
# # Dibujamos las curvas de nivel con la librería matplotlib.plt.tricontour. Para ello necesitamos dar un número
# # de curvas de nivel, y usar la triangulación previamente calculada
# numero_niveles = np.max(matriz) - np.min(matriz) - 1
# curvas = plt.tricontour(triangulacion, Z, levels=numero_niveles,
#                         cmap='viridis', linewidths=1.5, alpha=0.6, zorder=0)
#
# # Añadimos etiquetas a las curvas con su valor
# plt.clabel(curvas, inline=True, fontsize=12, fmt='%1.1f')
#
# plt.gca().set_aspect('equal')

leyenda = [
    mlines.Line2D([0], [0], marker='o', color='w', label='Máximo',
                  markerfacecolor='red', markersize=10),
    mlines.Line2D([0], [0], marker='o', color='w', label='Mínimo',
                  markerfacecolor='blue', markersize=10),
    mlines.Line2D([0], [0], marker='o', color='w', label='Punto de silla',
                  markerfacecolor='green', markersize=10),
    mlines.Line2D([0], [0], marker='o', color='w', label='Hidden Saddle',
                  markerfacecolor='purple', markersize=10),
    mlines.Line2D([0], [0], marker='o', color='w', label='Silla de borde',
                  markerfacecolor='yellow', markersize=10),
    mlines.Line2D([0], [0], marker='o', color='w', label='Nodo normal',
                  markerfacecolor='gray', markersize=10)
]

plt.legend(handles=leyenda, loc='upper right', bbox_to_anchor=(1.3, 1.0))
plt.tight_layout()

plt.show()
