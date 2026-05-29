"""Ejercicio 1: validar simbolos de agrupacion en una expresion matematica.

Soporta: (), [] y {}
"""


def validacion_expresion_matematica(expresion_matematica):
	"""Retorna True si la expresion esta balanceada; False en caso contrario."""
	simbolos_apertura = "([{"
	simbolos_cierre = ")]}"
	pares = {")": "(", "]": "[", "}": "{"}

	pila = []

	for simbolo in expresion_matematica:
		if simbolo in simbolos_apertura:
			pila.append(simbolo)
		elif simbolo in simbolos_cierre:
			if not pila:
				return False
			ultimo_abierto = pila.pop()
			if pares[simbolo] != ultimo_abierto:
				return False

	return len(pila) == 0


if __name__ == "__main__":
	expresion_ok = "3 + [(2 * 5) - {8 / (4 - 2)}]"
	expresion_error = "3 + [(2 * 5) - {8 / (4 - 2)]}"

	print("Expresion:", expresion_ok)
	print("Balanceada:", validacion_expresion_matematica(expresion_ok))
	print()

	print("Expresion:", expresion_error)
	print("Balanceada:", validacion_expresion_matematica(expresion_error))
