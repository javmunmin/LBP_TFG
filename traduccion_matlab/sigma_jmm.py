import numpy as np


def sigma_jll(darts_jmm, darts_bypixel):
    M = len(darts_bypixel)
    N = len(darts_bypixel[0])
    NumDarts_jmm = darts_jmm.shape[1]
    verdart = M * 2 * (N + 1)

    for i in range(M):
        for j in range(N):
            darts = darts_bypixel[i][j]
            # print(f"Los dardos en la posición i={i}, j={j} son:\n{darts}")
            a, b, c, d = darts

            if j+1 <= N-1:
                phi_a = darts_bypixel[i][j + 1][3]  # d
                # print(f"En {i},{j}, phi_a es {phi_a}")
                darts_jmm[1, a - 1] = phi_a

            if i+1 <= M-1:
                phi_b = darts_bypixel[i + 1][j][0]  # a
                # print(f"En {i},{j}, phi_b es {phi_b}")
                darts_jmm[1, b - 1] = phi_b

            if j-1 >= 0:
                phi_c = darts_bypixel[i][j - 1][1]  # b
                # print(f"En {i},{j}, phi_c es {phi_c}")
                darts_jmm[1, c - 1] = phi_c

            if i-1 >= 0:
                phi_d = darts_bypixel[i - 1][j][2]  # c
                # print(f"En {i},{j}, phi_d es {phi_d}")
                darts_jmm[1, d - 1] = phi_d

    # Dardos horizontales borde izquierdo
    i = np.arange(0, M * 2, 2)
    n = np.arange(verdart + 1, verdart + 1 + (N * 2) * M, N * 2)
    darts_jmm[1, i] = n

    # Dardos horizontales borde derecho
    i = np.arange(verdart - (M - 1) * 2 - 1, verdart + 1, 2)
    n = np.arange(verdart + N * 4, NumDarts_jmm + 1, N * 2)
    darts_jmm[1, i] = n

    # Dardos verticales borde arriba
    i = np.arange(verdart + 1 + 1 - 1, verdart + N * 2 + 1, 2)
    n = np.arange((M * 2) + 1, (M * 2) * N + 2, M * 2)
    darts_jmm[1, i] = n

    # Dardos verticales borde abajo
    i = np.arange(verdart + N * 2 * M + 1 - 1, NumDarts_jmm + 1 - 1, 2)
    n = np.arange(M * 2, verdart, M * 2)
    darts_jmm[1, i] = n

    # Cierre borde izquierdo
    i = np.arange(1, M * 2 - 1, 2)
    n = i + 1 + 1
    darts_jmm[1, i] = n

    # Esquinas
    darts_jmm[1, M * 2 - 1] = NumDarts_jmm - N * 2 + 1
    darts_jmm[1, verdart - M * 2] = verdart + N * 2
    darts_jmm[1, verdart] = 1
    darts_jmm[1, verdart - 1] = NumDarts_jmm
    darts_jmm[1, NumDarts_jmm - 1] = verdart - 1 + 1

    # Rebote borde inferior
    i = np.arange(NumDarts_jmm - N * 2 + 1, NumDarts_jmm - 1, 2)
    n = i + 1 + 1
    darts_jmm[1, i] = n

    # Rebote borde superior
    i = np.arange(verdart + 2, verdart + N * 2, 2)
    n = i - 1 + 1
    darts_jmm[1, i] = n

    # Rebote borde derecha
    i = np.arange((verdart - M * 2) + 2, verdart, 2)
    n = i - 1 + 1
    darts_jmm[1, i] = n

    return darts_jmm


if __name__ == "__main__":
    # Entradas cuando s = 3
    # darts_jmm = np.array([
    #     list(range(1, 49)),
    #     [0] * 48,
    #     [-1, -1, -1, -1, -1, -1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0,
    #      1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 1,
    #      0, 1, 0, 1, 1, 0, 0, 1, 0, 1, -1, -1, -1, -1, -1, -1]
    # ])
    #
    # darts_bypixel = [
    #     [[7, 32, 2, 25], [13, 34, 8, 27], [19, 36, 14, 29]],
    #     [[9, 38, 4, 31], [15, 40, 10, 33], [21, 42, 16, 35]],
    #     [[11, 44, 6, 37], [17, 46, 12, 39], [23, 48, 18, 41]]
    # ]

    # Entradas cuando s = 4
    darts_jmm = np.array([
        list(range(1, 81)),
        [0] * 80,
        [-1, -1, -1, -1, -1, -1, -1, -1, 0, 1, 0, 0, 0, 0, 1, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, -1, -1, -1, -1,
         -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 1, 0, 1, 0,
         1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, -1, -1,
         -1, -1, -1, -1, -1, -1]
    ])
    # print(darts_jmm)

    darts_bypixel = [
        [[9, 50, 2, 41], [17, 52, 10, 43], [25, 54, 18, 45], [33, 56, 26, 47]],
        [[11, 58, 4, 49], [19, 60, 12, 51], [27, 62, 20, 53], [35, 64, 28, 55]],
        [[13, 66, 6, 57], [21, 68, 14, 59], [29, 70, 22, 61], [37, 72, 30, 63]],
        [[15, 74, 8, 65], [23, 76, 16, 67], [31, 78, 24, 69], [39, 80, 32, 71]]
    ]
    # print(darts_bypixel)
    darts_bypixel = np.array(darts_bypixel)
    # print(darts_bypixel)

    # Call function
    updated_darts_jmm = sigma_jll(darts_jmm.copy(), darts_bypixel)
    # print(f"darts_jmm is now:\n{updated_darts_jmm}")
