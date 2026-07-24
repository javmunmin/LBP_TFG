import numpy as np


def contract_jmm(darts):
    # Encontrar índices donde darts(3,:) == 0
    darts_0 = np.where(darts[2, :] == 0)[0]  # Indices con base 0
    darts_remove = np.zeros(len(darts_0), dtype=int)
    d_afec = np.zeros(len(darts_0), dtype=int)
    con = 0  # en Python será 0, no como en Matlab (índice 1)

    for i in range(len(darts_0)):
        v = darts_0[i]
        t = (v+1) % 2
        # en matlab es t = mod(v,2), siendo v el índice de cada posición donde darts(3,:) == 0.
        # Sumamos 1 al índice para igualar

        if (t == 1) and darts[2, v+1] == 0:
            darts_remove[con] = v
            d_afec[con] = np.where(darts[1, :] == v+1)[0][0]
            con = con + 1
        if (t == 0) and darts[2, v-1] == 0:
            darts_remove[con] = v
            d_afec[con] = np.where(darts[1, :] == v+1)[0][0]
            con = con + 1

    darts_remove = darts_remove[:con]
    d_afec = d_afec[:con]
    phis = darts[1, darts_remove]
    darts_cotract = darts.copy()
    # Antes de calcular la intersección, sumamos 1 a cada elemento de darts_remove,
    # ya que en matlab usan índices sobre 1
    darts_remove = darts_remove + 1
    tem, a, b = np.intersect1d(phis, darts_remove, return_indices=True)
    # Restamos el 1 sumado anteriormente para volver a los valores de índices deseados
    darts_remove = darts_remove - 1
    phis[a] = darts[1, tem-1]

    for i in range(len(phis)):
        darts_cotract[1, d_afec[i]] = phis[i]
    darts_cotract[:, darts_remove] = -1

    return darts_cotract


if __name__ == "__main__":
    # Resultado esperado con s = 3
    # darts = np.array([
    #     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
    #      25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48],
    #     [25, 3, 31, 5, 37, 43, 27, 32, 33, 38, 39, 44, 29, 34, 35, 40, 41, 46, 30, 36, 20, 42, 22, 48,
    #      1, 7, 26, 13, 28, 19, 2, 9, 8, 15, 14, 21, 4, 11, 10, 17, 16, 23, 6, 45, 12, 47, 18, 24],
    #     [-1, -1, -1, -1, -1, -1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, -1, -1, -1, -1, -1, -1,
    #      -1, -1, -1, -1, -1, -1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, -1, -1, -1, -1, -1, -1]
    # ])

    # resultado esperado con s = 4
    darts = np.array([
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
         28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54,
         55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80],
        [41, 3, 49, 5, 57, 7, 65, 73, 43, 50, 51, 58, 59, 66, 67, 74, 45, 52, 53, 60, 61, 68, 69, 76, 47, 54, 55, 62,
         63, 70, 71, 78, 48, 56, 34, 64, 36, 72, 38, 80, 1, 9, 42, 17, 44, 25, 46, 33, 2, 11, 10, 19, 18, 27, 26,
         35, 4, 13, 12, 21, 20, 29, 28, 37, 6, 15, 14, 23, 22, 31, 30, 39, 8, 75, 16, 77, 24, 79, 32, 40],
        [-1, -1, -1, -1, -1, -1, -1, -1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, -1,
         -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
         0, 0, 1, 0, 1, 0, 1, -1, -1, -1, -1, -1, -1, -1, -1]
    ])

    # Ejecutar la función
    result = contract_jmm(darts)
    # print(result)
