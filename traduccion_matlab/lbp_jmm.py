import numpy as np
import cv2
import matplotlib.pyplot as plt


def matlab_resize_nearest(imagen_original, nuevo_tam):
    """
    Replica exacta de imresize(imagen_original, [new_h, new_w], 'nearest') de MATLAB.
    nuevo_tam debe ser una tupla: (nuevo_alto, nuevo_ancho)
    """
    old_h, old_w = imagen_original.shape[:2]
    new_h, new_w = nuevo_tam

    # MATLAB mapea los índices usando esta lógica matemática:
    indices_filas = np.floor(((np.arange(1, new_h + 1) - 0.5) * (old_h / new_h)) + 0.5).astype(int) - 1
    indices_columnas = np.floor(((np.arange(1, new_w + 1) - 0.5) * (old_w / new_w)) + 0.5).astype(int) - 1

    # Evitamos salirnos de los bordes por redondeo
    indices_filas = np.clip(indices_filas, 0, old_h - 1)
    indices_columnas = np.clip(indices_columnas, 0, old_w - 1)

    return imagen_original[indices_filas, :][:, indices_columnas]


def lbp_jmm(image, s):
    """
    Función inicial. Como argumentos pasamos la imagen_jmm o matriz deseada, y devuelve
    la matriz de dardos inicializada, y una lista de listas con los dardos por píxel
    """
    if image.ndim == 3 and image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    image = image.astype(np.uint8)  # Igual que Matlab
    M, N = image.shape

    if s != N:
        M_orig, N_orig = image.shape
        N = s
        M = int(round((M_orig / N_orig) * N))

        # Usamos nuestra función para una interpolación al vecino más cercano semejante a la que realiza Matlab
        image = matlab_resize_nearest(image, (M, N))

    NumDarts_jmm = ((N + 1) * (M * 2)) + ((M + 1) * (N * 2))
    verdart = M * 2 * (N + 1)

    darts_jmm = np.zeros((3, NumDarts_jmm), dtype=int)
    darts_jmm[0, :] = np.arange(1, NumDarts_jmm + 1)
    darts_jmm[2, :] = -1

    darts_bypixel = [[None for _ in range(N)] for _ in range(M)]

    for i in range(M):
        for j in range(N):
            v = image[i, j]

            in1 = i + 1
            in2 = j + 1

            even_v = (M * 2) * (in2 - 1) + in1 * 2
            odd_v = even_v + M * 2 - 1

            odd_h = (N * 2) * (in1 - 1) + in2 * 2 + verdart - 1
            even_h = odd_h + N * 2 + 1

            if j + 1 < N:
                darts_jmm[2, odd_v - 1] = int(v > image[i, j + 1])
            if i + 1 < M:
                darts_jmm[2, even_h - 1] = int(v > image[i + 1, j])
            if j - 1 >= 0:
                darts_jmm[2, even_v - 1] = int(v > image[i, j - 1])
            if i - 1 >= 0:
                darts_jmm[2, odd_h - 1] = int(v > image[i - 1, j])

            darts_bypixel[i][j] = [odd_v, even_h, even_v, odd_h]

    return darts_jmm, darts_bypixel


if __name__ == "__main__":
    image = np.array([
        [78, 99, 50],
        [54, 54, 49],
        [57, 12, 13]
    ])

    s = 4

    darts_jmm, darts_bypixel = lbp_jmm(image, s)

    print("darts_jmm:\n", darts_jmm)

    print(f"Los dardos por píxel son:\n{darts_bypixel}")
    print(f"darts_bypixel[0][0] are\n{darts_bypixel[0][0]}")

    # Print darts_bypixel as flat list for visual match
    print("\nDarts by pixel:")
    i = 1
    j = 1
    for row in darts_bypixel:
        for cell in row:
            print(f"[{i}][{j}]")
            print(cell)
            j = j + 1
        i = i + 1
        if 9 < j < 18:
            j = j - 9
