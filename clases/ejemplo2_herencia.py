# ============================================================
#  EJEMPLO 2 - Herencia en Python
#  Temática: Videojuego (continuación del ejemplo 1)
#
#  Qué aprenderás aquí:
#    - Qué es la HERENCIA: una clase que "extiende" otra
#    - Cómo reutilizar código del padre en el hijo
#    - Cómo agregar comportamiento nuevo en la clase hija
#    - super() para llamar al constructor del padre
# ============================================================


# -- CLASE BASE (PADRE) --
# Igual que el ejemplo 1: define lo común a todos los personajes.

class Personaje:

    def __init__(self, nombre, vida, ataque):
        self.nombre  = nombre
        self.vida    = vida
        self.ataque  = ataque

    def atacar(self, objetivo):
        objetivo.vida -= self.ataque
        print(f"{self.nombre} ataca a {objetivo.nombre} "
              f"por {self.ataque} de daño.")

    def mostrar_estado(self):
        print(f"[{self.nombre}]  Vida: {self.vida}  Ataque: {self.ataque}")


# -- CLASE HIJA: Mago --
# Hereda TODO de Personaje (no hay que repetir el código).
# Agrega un atributo extra (mana) y un método nuevo (lanzar_hechizo).

class Mago(Personaje):       # <-- entre paréntesis va la clase padre

    # Constructor del hijo
    def __init__(self, nombre, vida, ataque, mana):
        # super() llama al constructor del padre para inicializar
        # los atributos comunes (nombre, vida, ataque).
        super().__init__(nombre, vida, ataque)
        self.mana = mana     # Atributo NUEVO, exclusivo del Mago


    # Método NUEVO exclusivo del Mago
    def lanzar_hechizo(self, objetivo):
        costo_mana = 20       # Cada hechizo cuesta 20 de maná
        daño_magico = self.ataque * 2   # El hechizo hace el doble de daño

        # Verificamos si tiene suficiente maná
        if self.mana >= costo_mana:
            objetivo.vida -= daño_magico
            self.mana     -= costo_mana
            print(f"{self.nombre} lanza un HECHIZO a {objetivo.nombre} "
                  f"por {daño_magico} de daño mágico. "
                  f"Maná restante: {self.mana}")
        else:
            print(f"{self.nombre} no tiene suficiente maná.")


    # Sobreescribimos mostrar_estado para incluir el maná
    # (esto se llama SOBREESCRITURA o override)
    def mostrar_estado(self):
        print(f"[{self.nombre}]  Vida: {self.vida}  "
              f"Ataque: {self.ataque}  Maná: {self.mana}")


# ============================================================
#  PROGRAMA PRINCIPAL
# ============================================================

# Creamos un Guerrero (Personaje normal) y un Mago (clase hija)
guerrero = Personaje("Guerrero", 120, 12)
mago     = Mago("Gandalf", 70, 20, 100)   # Necesita el parámetro mana

print("=== Estado inicial ===")
guerrero.mostrar_estado()
mago.mostrar_estado()       # Muestra también el maná por el override

print("\n=== Combate ===")
mago.lanzar_hechizo(guerrero)   # Usa el método nuevo del hijo
guerrero.atacar(mago)           # Usa el método heredado del padre

print("\n=== Estado final ===")
guerrero.mostrar_estado()
mago.mostrar_estado()
