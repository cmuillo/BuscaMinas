def flood_fill(m, sr, sc, nuevo):
    if not m or not m[0]: return []
    f, c = len(m), len(m[0])
    if sr < 0 or sr >= f or sc < 0 or sc >= c: return [x[:] for x in m]
    ori = m[sr][sc]
    if ori == nuevo: return [x[:] for x in m]
    r, pila = [x[:] for x in m], [(sr, sc)]
    while pila:
        i, j = pila.pop()
        if 0 <= i < f and 0 <= j < c and r[i][j] == ori:
            r[i][j] = nuevo
            pila += [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    return r

img = [[1,1,1],[1,2,2],[1,1,2]]
for fila in flood_fill(img, 0, 0, 9):
        print(fila)
