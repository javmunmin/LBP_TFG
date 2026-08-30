import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def analizar_diferencias(img_py_path, img_mat_path):
    # Cargamos imágenes
    img_py = cv2.imread(img_py_path)
    img_mat = cv2.imread(img_mat_path)

    if img_py is None or img_mat is None:
        print("Error: No se encuentran las imágenes.")
        return

    # Definimos diccionario de colores (BGR para OpenCV)
    colores_bgr = {
        "Min (Negro)": (0, 0, 0),
        "Max (Blanco)": (255, 255, 255),
        "Slope (Gris)": (125, 125, 125),
        "Saddle (Azul)": (255, 0, 0),
        "Plateau (Rojo)": (0, 0, 255)
    }

    # Función auxiliar para convertir imagen a etiquetas numéricas
    def imagen_a_etiquetas(img):
        h, w, _ = img.shape
        etiquetas = np.zeros((h, w), dtype=int) - 1

        for i, (nombre, color) in enumerate(colores_bgr.items()):
            lower = np.array(color, dtype="uint8")
            upper = np.array(color, dtype="uint8")
            mask = cv2.inRange(img, lower, upper)
            etiquetas[mask > 0] = i
        return etiquetas, list(colores_bgr.keys())

    labels_py, nombres_clases = imagen_a_etiquetas(img_py)
    labels_mat, _ = imagen_a_etiquetas(img_mat)

    # 3. Calcular Matriz de Confusión
    num_clases = len(nombres_clases)
    confusion = np.zeros((num_clases, num_clases), dtype=int)

    total_pixels = labels_py.size
    errores = 0

    mask_validos = (labels_py != -1) & (labels_mat != -1)

    for real, pred in zip(labels_mat[mask_validos], labels_py[mask_validos]):
        confusion[real, pred] += 1
        if real != pred:
            errores += 1

    # Reporte de Texto
    print("\n" + "=" * 40)
    print(" REPORTE DE ERRORES POR CATEGORÍA")
    print("=" * 40)
    print(f"Total Píxeles: {total_pixels}")
    print(f"Total Errores: {errores}")
    print(f"Precisión Global: {(1 - errores / total_pixels) * 100:.4f}%\n")

    print("DETALLE DE CONFUSIONES:")
    print(f"{'Matlab dice...':<20} | {'Python dice...':<20} | {'Cantidad':<10}")
    print("-" * 56)

    indices = np.unravel_index(np.argsort(confusion, axis=None)[::-1], confusion.shape)
    for r, c in zip(indices[0], indices[1]):
        if r != c and confusion[r, c] > 0:
            print(f"{nombres_clases[r]:<20} | {nombres_clases[c]:<20} | {confusion[r, c]:<10}")

    # Generamos imagen con diferencias con colores con leyenda dinámica
    diff_map = np.ones((img_py.shape[0], img_py.shape[1], 3), dtype=np.uint8) * 255

    # Paleta de 20 colores distintos en formato RGB (para cubrir todas las permutaciones posibles)
    paleta_rgb = [
        (230, 25, 75), (60, 180, 75), (255, 225, 25), (67, 99, 216),
        (245, 130, 48), (145, 30, 180), (70, 240, 240), (240, 50, 230),
        (188, 246, 12), (250, 190, 190), (0, 128, 128), (230, 190, 255),
        (154, 99, 36), (255, 250, 200), (128, 0, 0), (170, 255, 195),
        (128, 128, 0), (255, 216, 177), (0, 0, 117), (50, 50, 50)
    ]

    errores_presentes = {}  # Mapeará (idx_matlab, idx_python) -> color_bgr
    leyenda_patches = [mpatches.Patch(color='white', label='Correcto')]

    color_idx = 0
    # Asignamos colores a las confusiones reales que han ocurrido
    for r in range(num_clases):
        for c in range(num_clases):
            if r != c and confusion[r, c] > 0:
                # Extraemos color de la paleta
                r_color, g_color, b_color = paleta_rgb[color_idx % len(paleta_rgb)]
                color_bgr = (b_color, g_color, r_color)

                # Guardamos en diccionario para pintar luego
                errores_presentes[(r, c)] = color_bgr

                # Creamos entrada para la leyenda (Matplotlib usa RGB normalizado 0-1)
                color_norm = (r_color / 255.0, g_color / 255.0, b_color / 255.0)

                # Limpiamos el nombre para que la leyenda no sea gigante (ej: "Plateau (Rojo)" -> "Plateau")
                nombre_mat = nombres_clases[r].split(' ')[0]
                nombre_py = nombres_clases[c].split(' ')[0]

                label_texto = f"{nombre_mat} -> {nombre_py} ({confusion[r, c]} px)"
                leyenda_patches.append(mpatches.Patch(color=color_norm, label=label_texto))

                color_idx += 1

    # Coloreamos la imagen mapeando las diferencias
    diff_indices = np.where(labels_py != labels_mat)
    for y, x in zip(diff_indices[0], diff_indices[1]):
        l_mat = labels_mat[y, x]
        l_py = labels_py[y, x]

        if l_mat == -1 or l_py == -1: continue

        if (l_mat, l_py) in errores_presentes:
            diff_map[y, x] = errores_presentes[(l_mat, l_py)]

    # Mostramos por pantalla con Matplotlib
    plt.figure(figsize=(14, 7))

    # Imagen Python
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(img_py, cv2.COLOR_BGR2RGB))
    plt.title("Salida Python")
    plt.axis("off")

    # Imagen Matlab
    plt.subplot(1, 3, 2)
    plt.imshow(cv2.cvtColor(img_mat, cv2.COLOR_BGR2RGB))
    plt.title("Salida Matlab")
    plt.axis("off")

    # Mapa de errores
    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(diff_map, cv2.COLOR_BGR2RGB))
    plt.title("Mapa de Errores Detallado")
    plt.axis("off")

    # Configuración leyenda (con fuente un poco más pequeña para que quepan todos)
    plt.legend(handles=leyenda_patches, bbox_to_anchor=(1.05, 1), loc='upper left',
               borderaxespad=0., fontsize=8, title="Confusiones (Matlab -> Py)")

    plt.tight_layout()
    plt.show()


analizar_diferencias("3096_definitiva_python.png", "3096_definitiva_matlab.png")
# analizar_diferencias("picaso_15x13_python.png", "picaso_15x13_matlab.png")