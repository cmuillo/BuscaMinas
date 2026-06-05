# -*- coding: utf-8 -*-
"""
Conteo de Islas - ejercicio de matrices.

Definición:
- Una ISLA es un grupo de celdas con valor 1 que están conectadas
  entre sí (arriba, abajo, izquierda, derecha).
- Las celdas con valor 0 representan agua.

Objetivo:
- Dada una matriz binaria, devolver el NÚMERO TOTAL DE ISLAS.

Ejemplo:
  Entrada:
    [[1, 1, 0, 0],
     [1, 0, 0, 1],
     [0, 0, 0, 1],
     [0, 1, 1, 0]]

  Salida: 3  (hay tres grupos de 1s desconectados entre sí)

Estrategia:
- Recorrer cada celda.
- Cuando encontremos un 1 que aún no fue visitado:
    -> contamos una nueva isla
    -> usamos Flood Fill para marcar toda esa isla como visitada
       (así no la contamos dos veces)
"""


def contar_islas(matriz):
    """
    Recorre la matriz y cuenta cuántas islas (regiones de 1s conectadas) hay.

    Variables:
    - filas, columnas: tamaño de la matriz.
    - visitado: matriz de booleanos para no contar la misma isla dos veces.
    - contador: número de islas encontradas hasta ahora.
    """
    if not matriz or not matriz[0]:
        return 0

    filas = len(matriz)
    columnas = len(matriz[0])

    # Marcamos aquí qué celdas ya fueron procesadas
    visitado = [[False] * columnas for _ in range(filas)]

    contador = 0  # aquí acumulamos el número de islas

    for f in range(filas):
        for c in range(columnas):
            # Si encontramos tierra (1) que aún no visitamos -> nueva isla
            if matriz[f][c] == 1 and not visitado[f][c]:
                contador += 1
                # Inundar (flood fill) toda la isla para marcarla visitada
                inundar(matriz, visitado, f, c, filas, columnas)

    return contador


def inundar(matriz, visitado, fila, columna, filas, columnas):
    """
    Marca como visitadas todas las celdas de la isla
    que empieza en (fila, columna), usando una pila (DFS iterativo).

    Esto evita que la isla sea contada múltiples veces.
    """
    pila = [(fila, columna)]

    while pila:
        f, c = pila.pop()

        # Ignorar si está fuera de la matriz
        if f < 0 or f >= filas or c < 0 or c >= columnas:
            continue
        # Ignorar si ya fue visitada o es agua
        if visitado[f][c] or matriz[f][c] == 0:
            continue

        # Marcar como visitada
        visitado[f][c] = True

        # Agregar los 4 vecinos para seguir expandiendo la isla
        pila.append((f - 1, c))  # arriba
        pila.append((f + 1, c))  # abajo
        pila.append((f, c - 1))  # izquierda
        pila.append((f, c + 1))  # derecha


if __name__ == "__main__":
    pruebas = [
        (
            [[1, 1, 0, 0],
             [1, 0, 0, 1],
             [0, 0, 0, 1],
             [0, 1, 1, 0]],
            "Ejemplo principal"
        ),
        (
            [[1, 1, 1],
             [1, 1, 1],
             [1, 1, 1]],
            "Toda tierra -> 1 isla"
        ),
        (
            [[0, 0, 0],
             [0, 0, 0]],
            "Toda agua -> 0 islas"
        ),
        (
            [[1, 0, 1],
             [0, 0, 0],
             [1, 0, 1]],
            "4 islas en esquinas"
        ),
    ]

    for mat, desc in pruebas:
        print(f"{desc}: {contar_islas(mat)} isla(s)")
