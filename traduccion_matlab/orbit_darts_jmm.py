import numpy as np

def orbit_darts_jmm(darts_cotract):
    num_darts = darts_cotract.shape[1]
    orbit_Darts = [[] for _ in range(num_darts)]
    max_iter = 10000

    for i in range(num_darts):
        if darts_cotract[0, i] != -1:
            t = darts_cotract[0, i] % 2
            tem = darts_cotract[0, i]
            phi = 0
            orbit = []
            ind = i
            count = 0
            while phi != tem:
                if count > max_iter:
                    print(f"Bucle infinito en i={i}, detenido tras {max_iter} iteraciones")
                    break
                if t == 1:
                    phi = darts_cotract[1, ind+1]  # phi del alpha
                    # print(f"phi es {phi} en el bucle {count}")
                    orbit.append(darts_cotract[2, phi-1])
                    ind = phi - 1
                if t == 0:
                    phi = darts_cotract[1, darts_cotract[0, ind-1]-1]
                    # print(f"phi es {phi} en el bucle {count}")
                    orbit.append(darts_cotract[2, phi-1])
                    ind = phi - 1
                t = phi % 2
                count = count + 1
        else:
            orbit = []
            count = 0
        orbit_Darts[i] = orbit
        # print(f"Bucle nº {i}, pasos: {count}, órbita: {orbit}")

    return orbit_Darts


if __name__ == "__main__":

    # darts_cotract = np.array([
    #     [1, 2, 3, 4, 5, 6, 7, 8, -1, -1, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
    #      31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48],
    #     [25, 3, 31, 5, 37, 43, 27, 32, -1, -1, 39, 44, 29, 34, 35, 40, 41, 46, 30, 36, 20, 42, 22, 48, 1, 7, 26, 13, 28,
    #      19, 2, 33, 8, 15, 14, 21, 4, 11, 38, 17, 16, 23, 6, 45, 12, 47, 18, 24],
    #     [-1, -1, -1, -1, -1, -1, 0, 1, -1, -1, 1, 0, 1, 0, 1, 0, 0, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    #      0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, -1, -1, -1, -1, -1, -1]
    # ])

    darts_cotract = np.array([
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, -1, -1, -1, -1, 15, 16, -1, -1, -1, -1, -1, -1, -1, -1, 25, 26, 27, 28, 29,
         30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,
         -1, -1, -1, -1, -1, -1, -1, -1, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80],
        [41, 3, 49, 5, 4, 7, 65, 73, 43, 50, -1, -1, -1, -1, 67, 74, -1, -1, -1, -1, -1, -1, -1, -1, 47, 54, 55, 29,
         28, 70, 71, 78, 48, 56, 34, 37, 36, 72, 38, 80, 1, 9, 42, 45, 44, 25, 46, 33, 2, 51, 10, 53, 52, 27, 26, 35,
         -1, -1, -1, -1, -1, -1, -1, -1, 6, 15, 66, 69, 68, 31, 30, 39, 8, 75, 16, 77, 76, 79, 32, 40],
        [-1, -1, -1, -1, -1, -1, -1, -1, 0, 1, -1, -1, -1, -1, 1, 0, -1, -1, -1, -1, -1, -1, -1, -1, 1, 0, 1, 0, 1, 0,
         0, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 1, 0, 1, 0, 1, 0, 1, -1, -1, -1, -1,
         -1, -1, -1, -1, 1, 0, 0, 1, 0, 1, 0, 1, -1, -1, -1, -1, -1, -1, -1, -1]
    ])

    orbits = orbit_darts_jmm(darts_cotract)

    # Mostramos las órbitas encontradas
    # for i, orb in enumerate(orbits):
    #     if orb is not None:
    #         print(f"Órbita {i+1}: {orb}")
    #
    # print(orbits)
