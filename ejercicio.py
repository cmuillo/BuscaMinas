# =============================================================================
# CLASE: SUMA DE TODOS LOS ELEMENTOS DE UNA MATRIZ
#        Recursión por PILA vs Recursión por COLA
# =============================================================================
#
# ¿Qué es una matriz?
#   Una tabla de números organizada en FILAS y COLUMNAS.
#   En Python se representa como una lista de listas.
#
#   Ejemplo de matriz 2×2:
#       [ [1, 2],      Fila 0
#         [3, 4] ]     Fila 1
#
# =============================================================================
# isinstance() — VALIDACIÓN DE TIPOS
# =============================================================================
#
# isinstance(objeto, tipo) devuelve True si 'objeto' es del tipo indicado.
#
# Lo usamos para verificar que la entrada sea realmente una matriz válida
# ANTES de entrar a la recursión, evitando errores difíciles de rastrear.
#
# Ejemplos de isinstance():
#   isinstance([1, 2], list)       → True
#   isinstance("hola", list)       → False
#   isinstance(3, (int, float))    → True   ← acepta int O float
#   isinstance("3", (int, float))  → False
#
# En nuestra validación comprobamos:
#   1. Que la matriz sea una lista              → isinstance(matriz, list)
#   2. Que no esté vacía                        → len(matriz) > 0
#   3. Que cada fila sea una lista              → isinstance(fila, list)
#   4. Que cada elemento sea int o float        → isinstance(elem, (int, float))
# =============================================================================


def validar_matriz(matriz):
    """
    Verifica con isinstance() que 'matriz' sea una lista de listas de números.
    Lanza TypeError con un mensaje claro si algo no cumple.
    """

    # ① ¿Es una lista?
    if not isinstance(matriz, list) or len(matriz) == 0:
        raise TypeError(f"Se esperaba una lista no vacía, pero se recibió: {type(matriz).__name__}")

    for i, fila in enumerate(matriz):

        # ② ¿Cada fila es una lista?
        if not isinstance(fila, list) or len(fila) == 0:
            raise TypeError(f"La fila {i} debe ser una lista no vacía, pero es: {type(fila).__name__}")

        for j, elemento in enumerate(fila):

            # ③ ¿Cada elemento es un número (int o float)?
            if not isinstance(elemento, (int, float)):
                raise TypeError(
                    f"El elemento [{i}][{j}] debe ser int o float, "
                    f"pero es: {type(elemento).__name__} (valor: {elemento!r})"
                )

# =============================================================================
# TIPO 1 — RECURSIÓN POR PILA (stack recursion)
# =============================================================================
#
# ¿CUÁNDO ocurre?
#   Cuando después de la llamada recursiva todavía queda una operación
#   pendiente (en este caso, una suma).  El programa guarda esa operación
#   en la PILA DE LLAMADAS (call stack) hasta que regresa el resultado.
#
# Señal que lo identifica en el código:
#   return fila[col] + suma_fila_pila(fila, col + 1)
#                  ↑
#   Hay un "+ fila[col]" FUERA de la llamada recursiva → pendiente en la pila.
#
# Cómo crece la pila para [1, 2]:
#   Llamada 1 → espera: 1 + ???
#     Llamada 2 → espera: 2 + ???
#       Llamada 3 → caso base: devuelve 0
#     Llamada 2 devuelve: 2 + 0 = 2
#   Llamada 1 devuelve: 1 + 2 = 3
#
# Desventaja: si la matriz es muy grande, la pila puede desbordarse
#             (RecursionError en Python).
# =============================================================================


def suma_fila_pila(fila, col=0):
    """Suma los elementos de una fila — estilo PILA (operación pendiente tras la llamada)."""

    # CASO BASE: no quedan columnas → suma parcial es 0
    if col == len(fila):
        return 0

    # CASO RECURSIVO: primero se resuelve suma_fila_pila(...),
    # LUEGO se suma fila[col]. Esa suma queda PENDIENTE en la pila.
    return fila[col] + suma_fila_pila(fila, col + 1)
    #      ↑─────────────────────────────────────────
    #      Operación pendiente guardada en la pila de llamadas


def suma_matriz_pila(matriz, fila=0):
    """Suma todos los elementos de la matriz — estilo PILA.
    En la primera llamada (fila=0) valida los tipos con isinstance().
    """

    # Validación solo en la llamada inicial (no en cada nivel recursivo)
    if fila == 0:
        validar_matriz(matriz)   # ← isinstance() aquí

    # CASO BASE: no quedan filas
    if fila == len(matriz):
        return 0

    # CASO RECURSIVO: suma fila actual + resultado de las filas siguientes (pendiente en pila)
    return suma_fila_pila(matriz[fila]) + suma_matriz_pila(matriz, fila + 1)


# =============================================================================
# TIPO 2 — RECURSIÓN POR COLA (tail recursion)
# =============================================================================
#
# ¿CUÁNDO ocurre?
#   Cuando la llamada recursiva es LO ÚLTIMO que hace la función: no queda
#   ninguna operación pendiente después de ella.
#   El resultado parcial se pasa como parámetro extra llamado ACUMULADOR.
#
# Señal que lo identifica en el código:
#   return suma_fila_cola(fila, col + 1, acum + fila[col])
#          ↑──────────────────────────────────────────────
#   La llamada recursiva es TODA la instrucción return → nada pendiente.
#
# Cómo avanza el acumulador para [1, 2]:
#   Llamada 1 → col=0, acum=0  → pasa acum=0+1=1
#   Llamada 2 → col=1, acum=1  → pasa acum=1+2=3
#   Llamada 3 → col=2          → caso base: devuelve acum=3  ✓
#
# Ventaja: el lenguaje (o el compilador) puede optimizarla para no apilar
#          marcos. Python NO aplica esa optimización automáticamente,
#          pero el patrón sigue siendo válido y más explícito.
# =============================================================================


def suma_fila_cola(fila, col=0, acum=0):
    """Suma los elementos de una fila — estilo COLA (acumulador, nada pendiente)."""

    # CASO BASE: no quedan columnas → devuelve el acumulador (resultado final)
    if col == len(fila):
        return acum                        # ← ya tenemos todo, nada pendiente

    # CASO RECURSIVO: la suma se hace ANTES de la llamada (en el argumento acum),
    # por eso después de la llamada no queda ninguna operación pendiente.
    return suma_fila_cola(fila, col + 1, acum + fila[col])
    #                                    ↑──────────────
    #                  La suma se incorpora al acumulador ANTES de llamar


def suma_matriz_cola(matriz, fila=0, acum=0):
    """Suma todos los elementos de la matriz — estilo COLA.
    En la primera llamada (fila=0) valida los tipos con isinstance().
    """

    # Validación solo en la llamada inicial
    if fila == 0:
        validar_matriz(matriz)   # ← isinstance() aquí

    # CASO BASE: no quedan filas → devuelve el acumulador
    if fila == len(matriz):
        return acum

    # CASO RECURSIVO: suma la fila actual al acumulador y avanza
    # (la llamada recursiva es lo ÚLTIMO, nada pendiente después)
    return suma_matriz_cola(matriz, fila + 1, acum + suma_fila_cola(matriz[fila]))


# =============================================================================
# PRUEBAS — ambas versiones producen el mismo resultado
# =============================================================================

matriz = [
    [1, 2],
    [3, 4]
]

print("── Recursión por PILA ──")
print("Resultado:", suma_matriz_pila(matriz))   # 10

print("── Recursión por COLA ──")
print("Resultado:", suma_matriz_cola(matriz))   # 10


# =============================================================================
# EJERCICIO 1: Sumar una sola fila con AMBOS estilos
# =============================================================================
#
# Enunciado: Dada la lista [5, 10, 15], obtén la suma con cada enfoque.
#
# ── Por pila ──
#   suma_fila_pila([5,10,15], col=0)
#     = 5 + suma_fila_pila([5,10,15], col=1)   ← 5 queda pendiente en pila
#         = 10 + suma_fila_pila([5,10,15], col=2) ← 10 queda pendiente
#             = 15 + suma_fila_pila([5,10,15], col=3)
#                 = 0  ← caso base
#             = 15     ← se resuelve en orden inverso
#         = 25
#     = 30
#
# ── Por cola ──
#   suma_fila_cola([5,10,15], col=0, acum=0)
#     → col=1, acum=5   (0+5)
#     → col=2, acum=15  (5+10)
#     → col=3, acum=30  (15+15)
#     → caso base: devuelve 30  ← directo, sin retroceder
# =============================================================================

print("\n── Ejercicio 1: fila [5, 10, 15] ──")
fila_simple = [5, 10, 15]
print("Por pila:", suma_fila_pila(fila_simple))   # 30
print("Por cola:", suma_fila_cola(fila_simple))   # 30


# =============================================================================
# EJERCICIO 2: Matriz identidad 3×3 con AMBOS estilos
# =============================================================================
#
# Enunciado: Suma todos los elementos de la matriz identidad.
#
#   identidad = [ [1, 0, 0],
#                 [0, 1, 0],
#                 [0, 0, 1] ]
#
# ── Por pila ──
#   suma_matriz_pila(id, fila=0)
#     = suma_fila_pila([1,0,0]) + suma_matriz_pila(id, fila=1)  ← pendiente en pila
#     = 1 + (suma_fila_pila([0,1,0]) + suma_matriz_pila(id, fila=2))
#     = 1 + (1 + (suma_fila_pila([0,0,1]) + 0))
#     = 1 + 1 + 1 = 3  ← se resuelve al volver de la recursión más profunda
#
# ── Por cola ──
#   suma_matriz_cola(id, fila=0, acum=0)
#     → fila=1, acum=1  (0 + suma_fila_cola([1,0,0]) = 1)
#     → fila=2, acum=2  (1 + suma_fila_cola([0,1,0]) = 1)
#     → fila=3, acum=3  (2 + suma_fila_cola([0,0,1]) = 1)
#     → caso base: devuelve 3  ← directo
# =============================================================================

print("\n── Ejercicio 2: matriz identidad 3×3 ──")
identidad = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 8, 1]
]
print("Por pila:", suma_matriz_pila(identidad))   # 10
print("Por cola:", suma_matriz_cola(identidad))   # 10


# =============================================================================
# RESPUESTA A LA REFLEXIÓN: Máximo de la matriz
# =============================================================================
#
# ¿Qué cambia respecto a la suma?
#   Solo DOS cosas:
#   1. La OPERACIÓN: en vez de "+" se usa "max()"
#   2. El NEUTRO del acumulador:
#      - Para suma  → acum empieza en 0         (0 + x = x para cualquier x)
#      - Para máximo → acum empieza en float('-inf')  (-inf es menor que todo)
#
# ─────────────────────────────────────────────────────────────────────────────
# MÁXIMO — Por PILA
# ─────────────────────────────────────────────────────────────────────────────
# El caso base devuelve el ÚLTIMO elemento (no hay neutro en la pila).
# max() reemplaza a + al combinar los resultados.

def max_fila_pila(fila, col=0):
    """Devuelve el máximo de una fila — estilo PILA."""

    # CASO BASE: último elemento de la fila (no hay siguiente)
    if col == len(fila) - 1:
        return fila[col]

    # CASO RECURSIVO: compara el elemento actual con el máximo del resto
    return max(fila[col], max_fila_pila(fila, col + 1))
    #      ↑── max() en vez de +


def max_matriz_pila(matriz, fila=0):
    """Devuelve el máximo de la matriz — estilo PILA."""

    # CASO BASE: última fila
    if fila == len(matriz) - 1:
        return max_fila_pila(matriz[fila])

    # CASO RECURSIVO: compara el máximo de la fila actual con el del resto
    return max(max_fila_pila(matriz[fila]), max_matriz_pila(matriz, fila + 1))


# ─────────────────────────────────────────────────────────────────────────────
# MÁXIMO — Por COLA
# ─────────────────────────────────────────────────────────────────────────────
# El acumulador arranca en float('-inf'):
#   cualquier número real es mayor que -infinito,
#   por lo que el primer elemento siempre lo reemplazará.
# max(acum, elemento) reemplaza a acum + elemento.

def max_fila_cola(fila, col=0, acum=float('-inf')):
    """Devuelve el máximo de una fila — estilo COLA."""

    # CASO BASE: no quedan columnas → el acumulador tiene el máximo
    if col == len(fila):
        return acum

    # CASO RECURSIVO: actualiza el acumulador con el mayor entre acum y fila[col]
    return max_fila_cola(fila, col + 1, max(acum, fila[col]))
    #                                   ↑── max(acum, ...) en vez de acum + ...


def max_matriz_cola(matriz, fila=0, acum=float('-inf')):
    """Devuelve el máximo de la matriz — estilo COLA."""

    # CASO BASE: no quedan filas → el acumulador tiene el máximo global
    if fila == len(matriz):
        return acum

    # CASO RECURSIVO: actualiza el acumulador con el máximo de la fila actual
    return max_matriz_cola(matriz, fila + 1, max(acum, max_fila_cola(matriz[fila])))


# ─────────────────────────────────────────────────────────────────────────────
# Prueba máximo
# ─────────────────────────────────────────────────────────────────────────────

print("\n── Máximo de la matriz [[1,2],[3,4]] ──")
print("Por pila:", max_matriz_pila(matriz))    # 4
print("Por cola:", max_matriz_cola(matriz))    # 4

print("\n── Máximo de la identidad 3×3 ──")
print("Por pila:", max_matriz_pila(identidad))  # 1
print("Por cola:", max_matriz_cola(identidad))  # 1


# =============================================================================
# PRUEBAS DE isinstance() — qué pasa si la entrada es incorrecta
# =============================================================================
#
# validar_matriz() se llama automáticamente al inicio de suma_matriz_pila
# y suma_matriz_cola. Si los datos no son válidos, lanza un TypeError claro.

print("\n── Pruebas de isinstance() ──")

# Caso válido: lista de listas de números → sin error
try:
    validar_matriz([[1, 2], [3, 4]])
    print("✓ [[1,2],[3,4]]       → válida")
except TypeError as e:
    print("✗", e)

# Error: la matriz es un string, no una lista
try:
    validar_matriz("hola")
except TypeError as e:
    print("✗", e)

# Error: una fila contiene un string en vez de número
try:
    validar_matriz([[1, 2], [3, "cuatro"]])
except TypeError as e:
    print("✗", e)

# Error: se pasó un número suelto en vez de una lista de listas
try:
    validar_matriz(42)
except TypeError as e:
    print("✗", e)
