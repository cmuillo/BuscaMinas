# -*- coding: utf-8 -*-
# ÁRBOLES — Recorridos de un árbol binario
#
#        Ana          inorden   → izq, raíz, der  → orden alfabético en BST
#       /   \         preorden  → raíz, izq, der  → copiar árbol
#    Bruno  Carla     postorden → izq, der, raíz  → eliminar nodos
#    /  \       \
# Diego  Eva  Felipe

class Nodo:
    def __init__(self, valor):
        self.valor     = valor
        self.izquierdo = None
        self.derecho   = None

# Construir el árbol manualmente
raiz = Nodo("Ana")
raiz.izquierdo = Nodo("Bruno")
raiz.derecho   = Nodo("Carla")
raiz.izquierdo.izquierdo = Nodo("Diego")
raiz.izquierdo.derecho   = Nodo("Eva")
raiz.derecho.derecho     = Nodo("Felipe")

# Inorden: izq → raíz → der
def inorden(nodo, res=None):
    if res is None: res = []
    if nodo is None: return res       # caso base
    inorden(nodo.izquierdo, res)
    res.append(nodo.valor)
    inorden(nodo.derecho, res)
    return res

# Preorden: raíz → izq → der
def preorden(nodo, res=None):
    if res is None: res = []
    if nodo is None: return res
    res.append(nodo.valor)
    preorden(nodo.izquierdo, res)
    preorden(nodo.derecho, res)
    return res

# Postorden: izq → der → raíz
def postorden(nodo, res=None):
    if res is None: res = []
    if nodo is None: return res
    postorden(nodo.izquierdo, res)
    postorden(nodo.derecho, res)
    res.append(nodo.valor)
    return res

# Altura: 1 + max(altura_izq, altura_der)
def altura(nodo):
    if nodo is None: return 0         # caso base
    return 1 + max(altura(nodo.izquierdo), altura(nodo.derecho))


if __name__ == "__main__":
    print("Inorden:  ", inorden(raiz))    # ['Diego','Bruno','Eva','Ana','Carla','Felipe']
    print("Preorden: ", preorden(raiz))   # ['Ana','Bruno','Diego','Eva','Carla','Felipe']
    print("Postorden:", postorden(raiz))  # ['Diego','Eva','Bruno','Felipe','Carla','Ana']
    print("Altura:   ", altura(raiz))     # 3
