# ============================================================
#  EJEMPLO 1 - Clases básicas en Python
#  Temática: Videojuego
#
#  Qué aprenderás aquí:
#    - Qué es una clase y cómo definirla
#    - Qué es el constructor __init__
#    - Qué es 'self'
#    - Cómo crear objetos y usar sus métodos
# ============================================================


# --- DEFINICIÓN DE LA CLASE ---
# La clase es el "molde" o "plano".
# A partir de ella podemos crear tantos personajes como queramos.

class Personaje:

    # -- CONSTRUCTOR --
    # Se ejecuta automáticamente al crear un objeto.
    # 'self' es la referencia al objeto que se está creando.
    # Los parámetros (nombre, vida, ataque) son los datos que
    # hay que pasar al crear el personaje.
    def __init__(self, nombre, vida, ataque):
        self.nombre  = nombre   # Nombre del personaje
        self.vida    = vida     # Puntos de vida
        self.ataque  = ataque   # Daño que hace por golpe


    # -- MÉTODO: atacar --
    # Recibe al 'objetivo' (otro objeto Personaje) y le resta
    # puntos de vida según el ataque de quien golpea.
    def atacar(self, objetivo):
        objetivo.vida -= self.ataque
        print(f"{self.nombre} ataca a {objetivo.nombre} "
              f"por {self.ataque} de daño.")


    # -- MÉTODO: mostrar_estado --
    # Solo imprime los datos actuales del personaje.
    def mostrar_estado(self):
        print(f"[{self.nombre}]  Vida: {self.vida}  Ataque: {self.ataque}")


# ============================================================
#  PROGRAMA PRINCIPAL
# ============================================================

# Creamos dos objetos a partir del mismo molde (clase Personaje).
# Cada uno tiene sus propios datos independientes.
heroe   = Personaje("Arthas",  100, 15)
enemigo = Personaje("Orco",     60, 10)

# Mostramos el estado inicial de cada uno
print("=== Estado inicial ===")
heroe.mostrar_estado()
enemigo.mostrar_estado()

# El héroe ataca al enemigo
print("\n=== Combate ===")
heroe.atacar(enemigo)    # enemigo.vida baja 15 puntos
enemigo.atacar(heroe)    # heroe.vida baja 10 puntos

# Mostramos el estado final
print("\n=== Estado final ===")
heroe.mostrar_estado()
enemigo.mostrar_estado()
