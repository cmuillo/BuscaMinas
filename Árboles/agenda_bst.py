# -*- coding: utf-8 -*-
# ÁRBOLES — BST (Árbol Binario de Búsqueda) — Agenda telefónica
# Regla: nombre < nodo → izquierda | nombre > nodo → derecha
#
#         Mario
#        /     \
#      Ana     Pedro
#        \     /   \
#      Carlos Lucía Sofía
#      /
#  Beatriz


class Nodo:
    def __init__(self, nombre):
        self.nombre    = nombre
        self.izquierdo = None
        self.derecho   = None

class AgendaBST:
    def __init__(self):
        self.raiz = None

    # Insertar: bajar comparando hasta encontrar None
    def insertar(self, nombre):
        if self.raiz is None:
            self.raiz = Nodo(nombre)
        else:
            self._insertar(self.raiz, nombre)

    def _insertar(self, nodo, nombre):
        if nombre < nodo.nombre:
            if nodo.izquierdo is None:
                nodo.izquierdo = Nodo(nombre)    # hueco → insertar
            else:
                self._insertar(nodo.izquierdo, nombre)
        elif nombre > nodo.nombre:
            if nodo.derecho is None:
                nodo.derecho = Nodo(nombre)      # hueco → insertar
            else:
                self._insertar(nodo.derecho, nombre)
        # igual → ignorar (no duplicados)

    # Buscar: mismo recorrido que insertar, pero devuelve True/False
    def buscar(self, nombre):
        return self._buscar(self.raiz, nombre)

    def _buscar(self, nodo, nombre):
        if nodo is None: return False            # no existe
        if nombre == nodo.nombre: return True    # encontrado
        if nombre < nodo.nombre:
            return self._buscar(nodo.izquierdo, nombre)
        return self._buscar(nodo.derecho, nombre)

    # Listar en orden alfabético: inorden en BST → siempre ordenado
    def listar(self):
        lista = []
        self._inorden(self.raiz, lista)
        return lista

    def _inorden(self, nodo, lista):
        if nodo is None: return
        self._inorden(nodo.izquierdo, lista)
        lista.append(nodo.nombre)
        self._inorden(nodo.derecho, lista)


if __name__ == "__main__":
    agenda = AgendaBST()
    for nombre in ["Mario", "Ana", "Pedro", "Carlos", "Lucía", "Sofía", "Beatriz"]:
        agenda.insertar(nombre)

    print("Orden alfabético:", agenda.listar())
    print("Buscar Lucía:",     agenda.buscar("Lucía"))   # True
    print("Buscar Jorge:",     agenda.buscar("Jorge"))   # False
