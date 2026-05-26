# ============================================================
#  RECURSIVIDAD - Ejemplos para examen escrito
#  Concepto clave: una función recursiva se llama a sí misma
#  con un problema MÁS PEQUEÑO, hasta llegar al CASO BASE
#  (condición de parada que NO se llama a sí misma).
# ============================================================


# ------------------------------------------------------------
# EJEMPLO 1: FACTORIAL
# factorial(n) = n * (n-1) * (n-2) * ... * 1
# Por ejemplo: factorial(4) = 4 * 3 * 2 * 1 = 24
# ------------------------------------------------------------

def factorial(n):
    # --- CASO BASE ---
    # Cuando n llega a 0 ó 1, ya no hay nada más que multiplicar.
    # Sin esto la función se llamaría infinitamente → error.
    if n == 0 or n == 1:
        return 1

    # --- LLAMADA RECURSIVA ---
    # Reducimos el problema: pedimos el factorial de (n-1)
    # y multiplicamos el resultado por n.
    return n * factorial(n - 1)

# ¿Cómo se ejecuta factorial(4) paso a paso?
#
#  factorial(4)
#    └─ 4 * factorial(3)
#           └─ 3 * factorial(2)
#                  └─ 2 * factorial(1)
#                         └─ devuelve 1   ← caso base
#                  └─ devuelve 2 * 1 = 2
#           └─ devuelve 3 * 2 = 6
#    └─ devuelve 4 * 6 = 24

print("--- FACTORIAL ---")
print("factorial(0) =", factorial(0))   # 1
print("factorial(1) =", factorial(1))   # 1
print("factorial(4) =", factorial(4))   # 24
print("factorial(5) =", factorial(5))   # 120


# ------------------------------------------------------------
# EJEMPLO 2: SUMA DE LOS PRIMEROS N NÚMEROS NATURALES
# suma(n) = n + (n-1) + (n-2) + ... + 1
# Por ejemplo: suma(4) = 4 + 3 + 2 + 1 = 10
# ------------------------------------------------------------

def suma(n):
    # --- CASO BASE ---
    # La suma de los primeros 0 números es 0.
    if n == 0:
        return 0

    # --- LLAMADA RECURSIVA ---
    # Sumamos n al resultado de la suma de los anteriores.
    return n + suma(n - 1)

# ¿Cómo se ejecuta suma(4) paso a paso?
#
#  suma(4)
#    └─ 4 + suma(3)
#              └─ 3 + suma(2)
#                        └─ 2 + suma(1)
#                                  └─ 1 + suma(0)
#                                              └─ devuelve 0  ← caso base
#                                  └─ devuelve 1 + 0 = 1
#                        └─ devuelve 2 + 1 = 3
#              └─ devuelve 3 + 3 = 6
#    └─ devuelve 4 + 6 = 10

print("\n--- SUMA DE NATURALES ---")
print("suma(0) =", suma(0))   # 0
print("suma(1) =", suma(1))   # 1
print("suma(4) =", suma(4))   # 10
print("suma(5) =", suma(5))   # 15


# ------------------------------------------------------------
# EJEMPLO 3: SUMA DE TODOS LOS ELEMENTOS DE UNA LISTA
# Recorre la lista tomando un elemento a la vez de forma recursiva.
# Por ejemplo: suma_lista([3, 1, 4, 2]) = 3 + 1 + 4 + 2 = 10
# ------------------------------------------------------------

def suma_lista(lista):
    # --- CASO BASE ---
    # Si la lista está vacía, no hay nada que sumar → devolvemos 0.
    if len(lista) == 0:
        return 0

    # --- LLAMADA RECURSIVA ---
    # Tomamos el PRIMER elemento:  lista[0]
    # Llamamos de nuevo con el RESTO de la lista: lista[1:]
    #   lista[1:]  devuelve todos los elementos menos el primero.
    #   Ejemplo: si lista = [3, 1, 4, 2]
    #            lista[0]  →  3
    #            lista[1:] →  [1, 4, 2]
    return lista[0] + suma_lista(lista[1:])

# ¿Cómo se ejecuta suma_lista([3, 1, 4, 2]) paso a paso?
#
#  suma_lista([3, 1, 4, 2])
#    └─ 3 + suma_lista([1, 4, 2])
#                └─ 1 + suma_lista([4, 2])
#                           └─ 4 + suma_lista([2])
#                                      └─ 2 + suma_lista([])
#                                                  └─ devuelve 0  ← caso base
#                                      └─ devuelve 2 + 0 = 2
#                           └─ devuelve 4 + 2 = 6
#                └─ devuelve 1 + 6 = 7
#    └─ devuelve 3 + 7 = 10

print("\n--- SUMA DE LISTA ---")
print("suma_lista([])        =", suma_lista([]))          # 0
print("suma_lista([5])       =", suma_lista([5]))         # 5
print("suma_lista([3,1,4,2]) =", suma_lista([3, 1, 4, 2])) # 10


# ------------------------------------------------------------
# EJEMPLO 4: MÁXIMO DE UNA LISTA
# Recorre la lista comparando el primer elemento con el máximo
# del resto, y se queda con el mayor.
# Por ejemplo: maximo([3, 7, 1, 5]) → 7
# ------------------------------------------------------------

def maximo(lista):
    # --- CASO BASE ---
    # Si la lista tiene UN solo elemento, ese elemento ES el máximo.
    if len(lista) == 1:
        return lista[0]

    # --- LLAMADA RECURSIVA ---
    # Obtenemos el máximo del RESTO de la lista (sin el primero).
    max_resto = maximo(lista[1:])

    # Comparamos el primer elemento con el máximo del resto.
    # Devolvemos el mayor de los dos.
    if lista[0] > max_resto:
        return lista[0]
    else:
        return max_resto

# ¿Cómo se ejecuta maximo([3, 7, 1, 5]) paso a paso?
#
#  maximo([3, 7, 1, 5])
#    max_resto = maximo([7, 1, 5])
#                  max_resto = maximo([1, 5])
#                                max_resto = maximo([5])
#                                              └─ devuelve 5  ← caso base
#                                ¿1 > 5? No → devuelve 5
#                  ¿7 > 5? Sí  → devuelve 7
#    ¿3 > 7? No  → devuelve 7

print("\n--- MÁXIMO DE LISTA ---")
print("maximo([5])        =", maximo([5]))           # 5
print("maximo([3,7,1,5])  =", maximo([3, 7, 1, 5])) # 7
print("maximo([4,2,9,6])  =", maximo([4, 2, 9, 6])) # 9


# ============================================================
#  REGLAS DE ORO para el examen:
#
#  1. CASO BASE  → condición if que devuelve un valor directo
#                  (sin llamarse a sí misma). Sin él → bucle infinito.
#
#  2. LLAMADA RECURSIVA → se llama a sí misma con un argumento
#                         que se ACERCA al caso base en cada paso.
#
#  3. Cada llamada "espera" a que la siguiente termine para
#     poder calcular y devolver su propio resultado.
# ============================================================
