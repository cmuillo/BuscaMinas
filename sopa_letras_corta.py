# Version corta: busca una palabra en linea recta (arriba, abajo, izquierda, derecha)

def existe_palabra_corta(matriz, palabra):
    if not palabra:
        return True
    if not matriz or not matriz[0]:
        return False

    filas, columnas = len(matriz), len(matriz[0])
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for f in range(filas):
        for c in range(columnas):
            for df, dc in direcciones:
                ok = True
                for i, letra in enumerate(palabra):
                    nf, nc = f + i * df, c + i * dc
                    if nf < 0 or nf >= filas or nc < 0 or nc >= columnas or matriz[nf][nc] != letra:
                        ok = False
                        break
                if ok:
                    return True
    return False


if __name__ == "__main__":
    sopa = [
        ['C', 'A', 'S', 'A'],
        ['X', 'Z', 'S', 'O'],
        ['Q', 'W', 'L', 'L']
    ]
    print('"SOL" ->', existe_palabra_corta(sopa, "SOL"))  # False
    print('"CAS" ->', existe_palabra_corta(sopa, "CAS"))  # True
