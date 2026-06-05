# -*- coding: utf-8 -*-
"""
Flood Fill - versión fácil de estudiar.

Objetivo:
- Dada una matriz y una posición inicial (fila, columna), cambiar todos los
  elementos conectados (arriba, abajo, izquierda, derecha) que tengan el mismo
  valor inicial por un nuevo valor.

Esta versión está pensada para explicar claramente el uso de variables.
"""


def flood_fill_facil(matriz, fila_inicial, columna_inicial, nuevo_valor):
    """
    Aplica Flood Fill y devuelve una NUEVA matriz modificada.

    Uso de variables principales:
    - matriz_resultado: copia de la matriz original para no modificar el dato de entrada.
    - filas: cantidad de filas en la matriz.
    - columnas: cantidad de columnas en la matriz.
    - valor_inicial: valor que tiene la celda desde la que empieza el relleno.
    - pendientes: lista de celdas por revisar (funciona como pila LIFO).
    - fila_actual, columna_actual: coordenadas de la celda que se está procesando.
    """
    if not matriz:
        return []

    # 1) Preparar datos básicos
    filas = len(matriz)
    columnas = len(matriz[0])

    # Si la posición de inicio no existe, devolvemos copia sin cambios
    if fila_inicial < 0 or fila_inicial >= filas or columna_inicial < 0 or columna_inicial >= columnas:
        return [fila[:] for fila in matriz]

    valor_inicial = matriz[fila_inicial][columna_inicial]

    # Si ya tiene el nuevo valor, no hace falta hacer nada
    if valor_inicial == nuevo_valor:
        return [fila[:] for fila in matriz]

    # Copia de trabajo
    matriz_resultado = [fila[:] for fila in matriz]

    # 2) Estructura para recorrer celdas conectadas
    pendientes = [(fila_inicial, columna_inicial)]

    # 3) Procesar celdas hasta vaciar la pila
    while pendientes:
        fila_actual, columna_actual = pendientes.pop()

        # Validar límites de la celda actual
        if fila_actual < 0 or fila_actual >= filas or columna_actual < 0 or columna_actual >= columnas:
            continue

        # Solo cambiamos celdas que todavía tengan el valor inicial
        if matriz_resultado[fila_actual][columna_actual] != valor_inicial:
            continue

        # Reemplazar por el nuevo valor
        matriz_resultado[fila_actual][columna_actual] = nuevo_valor

        # Agregar vecinos (4 direcciones)
        pendientes.append((fila_actual - 1, columna_actual))  # arriba
        pendientes.append((fila_actual + 1, columna_actual))  # abajo
        pendientes.append((fila_actual, columna_actual - 1))  # izquierda
        pendientes.append((fila_actual, columna_actual + 1))  # derecha

    return matriz_resultado


if __name__ == "__main__":
    # Ejemplo del enunciado
    matriz_ejemplo = [
        [1, 1, 1],
        [1, 2, 2],
        [1, 1, 2],
    ]

    fila_inicio = 0
    columna_inicio = 0
    reemplazo = 9

    print("Matriz original:")
    for fila in matriz_ejemplo:
        print(fila)

    resultado = flood_fill_facil(matriz_ejemplo, fila_inicio, columna_inicio, reemplazo)

    print("\nResultado flood fill:")
    for fila in resultado:
        print(fila)

    # Esperado:
    # [9, 9, 9]
    # [9, 2, 2]
    # [9, 9, 2]
