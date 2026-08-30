import numpy as np


def generar_matriz_medida(filas, columnas, s=20):
    """
    Genera una matriz aleatoria de tamaño (filas, columnas) y la imprime
    en formatos listos para copiar a Python y MATLAB.
    """
    # Generamos la matriz con valores simulando píxeles (entre 10 y 255)
    matriz = np.random.randint(10, 255, size=(filas, columnas))

    print(f"\n{'=' * 40}")
    print(f" MATRIZ ALTURA {filas}, ANCHURA {columnas}")
    print(f"{'=' * 40}\n")

    # Formato Python
    print("**Python:**")
    print("image = np.array([")
    for i, fila in enumerate(matriz):
        fila_str = ", ".join(map(str, fila))
        if i < filas - 1:
            print(f"    [{fila_str}],")
        else:
            print(f"    [{fila_str}]")
    print("])")
    print(f"s = {s}\n")

    # Formato MATLAB
    filas_matlab = [" ".join(map(str, fila)) for fila in matriz]
    matlab_str = ";".join(filas_matlab)  # Unión estricta con punto y coma

    print("**MATLAB:**")
    print(f"image=[{matlab_str}];")
    print(f"width={s};\n")


if __name__ == "__main__":

    generar_matriz_medida(146, 134, s=134)
