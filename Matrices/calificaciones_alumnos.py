# -*- coding: utf-8 -*-
# MATRICES — Tabla de calificaciones
# Filas = alumnos | Columnas = asignaturas

ALUMNOS     = ["Ana", "Bruno", "Carla", "Diego"]
ASIGNATURAS = ["Mates", "Física", "Historia"]

calificaciones = [
    [90, 75, 85],  # Ana
    [60, 80, 70],  # Bruno
    [95, 88, 92],  # Carla
    [70, 65, 78],  # Diego
]

# Promedio por alumno — recorrer FILAS con enumerate
def promedios_alumnos(matriz, nombres):
    resultado = []
    for i, fila in enumerate(matriz):
        promedio = sum(fila) / len(fila)
        resultado.append((nombres[i], promedio))
    resultado.sort(key=lambda t: t[1], reverse=True)  # mayor a menor
    return resultado

# Promedio por asignatura — recorrer COLUMNAS con zip(*)
def promedios_asignaturas(matriz, asignaturas):
    resultado = []
    for j, columna in enumerate(zip(*matriz)):  # zip(*) agrupa por columna
        resultado.append((asignaturas[j], sum(columna) / len(columna)))
    resultado.sort(key=lambda t: t[1])  # menor a mayor (más difícil primero)
    return resultado

# Nota máxima global — doble bucle anidado
def nota_maxima(matriz, nombres, asignaturas):
    max_nota, fila_max, col_max = -1, 0, 0
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] > max_nota:
                max_nota, fila_max, col_max = matriz[i][j], i, j
    return max_nota, nombres[fila_max], asignaturas[col_max]


if __name__ == "__main__":
    print("Promedios alumnos:", promedios_alumnos(calificaciones, ALUMNOS))
    print("Promedios asig.:  ", promedios_asignaturas(calificaciones, ASIGNATURAS))
    nota, alumno, asig = nota_maxima(calificaciones, ALUMNOS, ASIGNATURAS)
    print(f"Nota máxima: {nota} — {alumno} en {asig}")
