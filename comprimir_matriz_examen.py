def comprimir_matriz(m):
    r, act, cnt = [], None, 0
    for fila in m:
        for x in fila:
            if act is None:
                act, cnt = x, 1
            elif x == act:
                cnt += 1
            else:
                r.append((act, cnt))
                act, cnt = x, 1
    if act is not None:
        r.append((act, cnt))
    return r


if __name__ == "__main__":
    ejemplo = [[1, 1, 1], [2, 2, 3]]
    print(comprimir_matriz(ejemplo))
