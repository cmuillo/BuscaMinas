# =============================================================================
# EXAMEN - IC-1802 Introducción a la Programación
# =============================================================================
# Restricciones generales:
#   - Sin ciclos for/while
#   - Sin módulos
#   - Solo recursividad (pila o cola según indique cada ejercicio)
# =============================================================================

# =============================================================================
# ANÁLISIS DE INCOHERENCIA CON EL NIVEL DEL CURSO
#
# Para un estudiante que ve Python por primera vez, este examen plantea
# conceptos que normalmente se estudian en cursos posteriores (2do o 3er año):
#
# 1. Recursividad de PILA vs COLA: Distinguir entre ambos tipos de recursión
#    es un concepto de Estructuras de Datos / Algoritmos avanzados. En un
#    primer curso introductorio rara vez se hace esa distinción formal.
#
# 2. Ejercicio 1 sin .split(): Para un principiante, .split() es la herramienta
#    natural y correcta. Sin ella, hay que parsear caracter por caracter para
#    encontrar las palabras, combinando indexación, slicing y recursión al mismo
#    tiempo — una complejidad desproporcionada para el nivel declarado.
#
# 3. Cero ciclos + solo recursión: Un curso introductorio típicamente enseña
#    ciclos ANTES de introducir recursión. Prohibir for/while y exigir recursión
#    pura desde el primer examen elimina los andamios básicos de aprendizaje.
#
# 4. Ejercicio 2 "sin funciones adicionales": Implementar recursión de cola
#    sin una función auxiliar exige el uso de parámetros con valores por defecto
#    (indice=0) — técnica que no suele enseñarse en primeros cursos.
#
# 5. Ejercicio 3 "solo listas": Sin poder usar sets ni diccionarios, la
#    deduplicación requiere una búsqueda lineal implícitamente O(n²) que
#    combina recursión anidada — complejidad algorítmica inadecuada para
#    alguien que recién conoce las estructuras de datos.
#
# 6. Puntaje inconsistente: El Ejercicio 1 fue tachado de 45 pts a 40 pts
#    en el enunciado físico, lo que sugiere ajustes de último momento.
# =============================================================================


# =============================================================================
# EJERCICIO 1 (40 pts): Invertir orden de palabras
# Tipo de recursión requerida: PILA (stack)
#
# Qué es recursividad de PILA:
#   El llamado recursivo NO es la última operación. Al regresar, todavía
#   hay trabajo pendiente (en este caso, concatenar la primera palabra).
#   Las llamadas se van "apilando" en memoria y se resuelven de atrás hacia adelante.
# =============================================================================

def _encontrar_espacio(oracion, indice=0):
    """
    Auxiliar recursiva (de cola) que devuelve el índice del PRIMER espacio
    en 'oracion', o -1 si no hay ninguno.

    Se necesita porque no podemos usar .split() ni [::-1] para separar palabras,
    así que buscamos manualmente el espacio caracter por caracter.
    """
    if indice >= len(oracion):
        return -1                                       # No hay espacio: es la última (o única) palabra
    if oracion[indice] == ' ':
        return indice                                   # Encontramos el espacio
    return _encontrar_espacio(oracion, indice + 1)      # Seguir buscando (cola: nada más que hacer aquí)


def invertir_oracion(oracion):
    """
    Invierte el orden de las palabras en una oración usando recursividad de PILA.

    Estrategia:
      1. Encontrar dónde termina la PRIMERA palabra (primer espacio).
      2. Llamar recursivamente para invertir el RESTO de la oración.
      3. DESPUÉS de que retorna la llamada, concatenar la primera palabra AL FINAL.
         → Eso es lo que hace que sea recursividad de PILA: hay trabajo pendiente
           luego del retorno recursivo.

    Traza para "Python es poderoso":
      invertir_oracion("Python es poderoso")
        → invertir_oracion("es poderoso") + " " + "Python"   ← espera en la pila
          → invertir_oracion("poderoso") + " " + "es"        ← espera en la pila
            → "poderoso"   (caso base: no hay espacio)
          → "poderoso" + " " + "es"  = "poderoso es"
        → "poderoso es" + " " + "Python" = "poderoso es Python"
    """
    pos = _encontrar_espacio(oracion)

    # Caso base: sin espacio → solo hay una palabra, se devuelve tal cual
    if pos == -1:
        return oracion

    primera_palabra = oracion[:pos]     # Ej: "Python"
    resto = oracion[pos + 1:]           # Ej: "es poderoso"

    # PILA: el retorno recursivo ocurre primero; la concatenación ocurre DESPUÉS
    return invertir_oracion(resto) + ' ' + primera_palabra


# =============================================================================
# EJERCICIO 2 (30 pts): Lista ordenada
# Tipo de recursión requerida: COLA (tail), sin funciones adicionales
#
# Qué es recursividad de COLA:
#   El llamado recursivo ES la última operación de la función; no hay nada
#   pendiente después de que retorna. Esto permite optimizaciones en memoria
#   porque no hay que "recordar" nada entre llamadas.
# =============================================================================

def ordenada(lista, indice=0):
    """
    Determina si 'lista' está ordenada de menor a mayor usando recursividad de COLA.

    El parámetro 'indice' lleva la cuenta de qué par estamos comparando ahora.
    Empieza en 0 por defecto, así la función se llama simplemente: ordenada([1,2,3]).

    Estrategia:
      - Comparar lista[indice] con lista[indice+1].
      - Si lista[indice] > lista[indice+1] → ya no está ordenada → False.
      - Si llegamos al penúltimo índice sin problema → True.
      - Si todo bien → avanzar al siguiente par (llamada de cola).

    Es de COLA porque `return ordenada(lista, indice + 1)` es la ÚLTIMA
    instrucción; no hay ninguna operación pendiente después de ese retorno.
    """
    # Caso base: comparamos todos los pares consecutivos sin problemas → True
    if indice >= len(lista) - 1:
        return True

    # Si el elemento actual es mayor que el siguiente → no está ordenada
    if lista[indice] > lista[indice + 1]:
        return False

    # COLA: avanzar al siguiente par; nada más que hacer después de retornar
    return ordenada(lista, indice + 1)


# =============================================================================
# EJERCICIO 3 (30 pts): Eliminar duplicados
# Restricción: SOLO listas como estructura de datos (sin sets, dicts, tuplas).
# Puede usar recursividad de pila o de cola.
# =============================================================================

def _esta_en_lista(elemento, lista, indice=0):
    """
    Auxiliar recursiva (de cola) que verifica si 'elemento' ya existe
    en 'lista'. Reemplaza el operador 'in' o el uso de un set.

    Solo trabaja con listas y parámetros simples, cumpliendo la restricción.
    """
    if indice >= len(lista):
        return False                                            # Llegamos al final sin encontrarlo
    if lista[indice] == elemento:
        return True                                             # Lo encontramos
    return _esta_en_lista(elemento, lista, indice + 1)          # Cola: seguir buscando


def sin_duplicados(lista, resultado=None):
    """
    Elimina elementos repetidos de 'lista' conservando el orden de primera
    aparición. Solo usa listas como estructura de datos.

    El parámetro 'resultado' es un acumulador: va guardando los elementos
    únicos que ya procesamos. Empieza vacío.

    Nota técnica: se usa resultado=None en vez de resultado=[] para evitar
    el problema clásico de Python donde un argumento mutable por defecto
    se comparte entre todas las llamadas a la función.

    Estrategia (recursividad de cola):
      - Si la lista original está vacía → devolver lo acumulado.
      - Si el primer elemento YA está en 'resultado' → ignorarlo.
      - Si NO está → agregarlo a 'resultado'.
      - Llamar recursivamente con el resto de la lista.

    Traza para [1,2,2,3]:
      sin_duplicados([1,2,2,3], [])
        → sin_duplicados([2,2,3], [1])       # 1 es nuevo → lo agregamos
          → sin_duplicados([2,3], [1,2])     # 2 es nuevo → lo agregamos
            → sin_duplicados([3], [1,2])     # 2 ya está  → lo ignoramos
              → sin_duplicados([], [1,2,3])  # 3 es nuevo → lo agregamos
                → [1,2,3]                   # caso base: lista vacía
    """
    if resultado is None:
        resultado = []

    # Caso base: lista vacía → ya procesamos todos los elementos
    if len(lista) == 0:
        return resultado

    primero = lista[0]
    resto = lista[1:]

    if _esta_en_lista(primero, resultado):
        # Ya existe en el resultado → omitirlo y continuar (cola)
        return sin_duplicados(resto, resultado)
    else:
        # Es nuevo → agregarlo al resultado y continuar (cola)
        return sin_duplicados(resto, resultado + [primero])


# =============================================================================
# PRUEBAS
# =============================================================================
if __name__ == '__main__':
    print("=== Ejercicio 1: Invertir orden de palabras ===")
    print(invertir_oracion("Python es poderoso"))    # → "poderoso es Python"
    print(invertir_oracion("hola"))                  # → "hola"
    print(invertir_oracion("uno dos tres cuatro"))   # → "cuatro tres dos uno"

    print("\n=== Ejercicio 2: Lista ordenada ===")
    print(ordenada([1, 2, 3, 4, 5]))   # → True
    print(ordenada([1, 3, 2, 4, 5]))   # → False
    print(ordenada([5, 4, 3, 2, 1]))   # → False
    print(ordenada([1]))               # → True  (un solo elemento siempre está ordenado)

    print("\n=== Ejercicio 3: Eliminar duplicados ===")
    print(sin_duplicados([1, 2, 2, 2, 3, 1, 4]))   # → [1, 2, 3, 4]
    print(sin_duplicados(['a', 'b', 'a', 'c']))     # → ['a', 'b', 'c']
    print(sin_duplicados([1, 1, 1, 1]))             # → [1]
    print(sin_duplicados([]))                        # → []
