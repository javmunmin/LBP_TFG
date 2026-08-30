import numpy as np


def imagen_jmm(darts_bypixel, LBP_values):
    # Definimos los colores (RGB). Cambiamos nombres para no pisar funciones nativas (min/max)
    color_max = np.array([255, 255, 255])   # 4, blanco
    color_min = np.array([0, 0, 0])         # 0, negro
    slope = np.array([125, 125, 125])       # 2, gris
    saddle = np.array([0, 0, 255])          # 3, azul
    plateaus = np.array([255, 0, 0])        # -1, rojo

    # Tamaño de la imagen_jmm (M filas, N columnas)
    M = len(darts_bypixel)
    N = len(darts_bypixel[0])

    # Imagen en 3 canales (M, N, 3). Es el formato estándar HWC para OpenCV/Matplotlib
    LBP_image = np.zeros((M, N, 3), dtype=np.uint8)

    # Recorremos la matriz
    for i in range(M):
        for j in range(N):
            a = LBP_values[darts_bypixel[i][j][0] - 1]

            # Inyectamos el vector RGB directamente en la tercera dimensión gracias a NumPy
            if a == 0:
                LBP_image[i, j] = color_min
            elif a == 4:
                LBP_image[i, j] = color_max
            elif a == 2:
                LBP_image[i, j] = slope
            elif a == 3:
                LBP_image[i, j] = saddle
            elif a == -1:
                LBP_image[i, j] = plateaus

    return LBP_image


if __name__ == "__main__":
    LBP_values = [-1, 2, -1, 2, -1, 2, -1, 4, 2, 4, -1, -1, -1, -1, 4, 0, -1, -1, -1, -1, -1, -1, -1, -1, 4, 2, 2, 2,
                  2, 2, 0, 2, 2, -1, 2, -1, 2, -1, 2, -1, 2, -1, 4, -1, 4, -1, 2, -1, 2, 2, 2, 4, 2, 4, 2, 2, -1, -1,
                  -1, -1, -1, -1, -1, -1, 4, 2, 0, 2, 0, 2, 2, 2, -1, 4, -1, 0, -1, 0, -1, 2]
    darts_bypixel = [
        [[9, 50, 2, 41], [17, 52, 10, 43], [25, 54, 18, 45], [33, 56, 26, 47]],
        [[11, 58, 4, 49], [19, 60, 12, 51], [27, 62, 20, 53], [35, 64, 28, 55]],
        [[13, 66, 6, 57], [21, 68, 14, 59], [29, 70, 22, 61], [37, 72, 30, 63]],
        [[15, 74, 8, 65], [23, 76, 16, 67], [31, 78, 24, 69], [39, 80, 32, 71]]
    ]

    LBP_img = imagen_jmm(darts_bypixel, LBP_values)

    # print(LBP_img)
