# -*- coding: utf-8 -*-
# MATRICES — Rotar imagen 90° a la derecha
# Pasos: 1) Transponer  2) Invertir cada fila


# PASO 1 — transponer: transpuesta[j][i] = matriz[i][j]
def transponer(matriz):
    n = len(matriz)
    transpuesta = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            transpuesta[j][i] = matriz[i][j]  # intercambia i ↔ j
    return transpuesta

# PASO 2 — invertir cada fila con [::-1]
def rotar_90_derecha(matriz):
    return [fila[::-1] for fila in transponer(matriz)]


if __name__ == "__main__":
    imagen = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    rotada = rotar_90_derecha(imagen)
    print("Original:", imagen)
    print("Rotada:  ", rotada)
    # Esperado: [[7,4,1], [8,5,2], [9,6,3]]
