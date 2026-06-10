# =============================================================
#  Laboratorio Semana 15 - POO: Sistema de Membresía de Gimnasio
#  Curso: Programación
# =============================================================

# ¿Qué es una CLASE?
# Una clase es como un "molde" o "plano" para crear objetos.
# Imagina que la clase es el diseño de una casa: define cuántas
# habitaciones tiene, de qué color es, etc. Cada casa construida
# a partir de ese plano es un OBJETO (también llamado instancia).

class Membresia:
    """
    Clase que representa una membresía de gimnasio.
    Cada objeto creado a partir de esta clase será una membresía diferente.
    """

    # ---------------------------------------------------------------
    # CONSTRUCTOR (__init__)
    # Este método especial se ejecuta automáticamente cada vez que
    # creamos un nuevo objeto. Aquí definimos los ATRIBUTOS del objeto,
    # que son las variables propias de cada membresía.
    # 'self' hace referencia al propio objeto que se está creando.
    # ---------------------------------------------------------------
    def __init__(self, numero, nombre):
        self.numero = numero                  # Número único de la membresía
        self.nombre = nombre                  # Nombre del cliente

        # Contadores de sesiones
        self.sesiones_disponibles = 0         # Cuántas sesiones puede usar ahora
        self.total_sesiones_compradas = 0     # Acumulado histórico de sesiones compradas
        self.cantidad_compras = 0             # Cuántas veces ha comprado sesiones

        # Contadores de uso
        self.total_sesiones_utilizadas = 0    # Acumulado histórico de sesiones usadas
        self.cantidad_usos = 0                # Cuántas veces ha usado una sesión

        # Estado inicial siempre es Activa
        self.estado = "Activa"


    # ---------------------------------------------------------------
    # MÉTODO: comprar_sesiones
    # Permite añadir sesiones a la membresía.
    # Recibe 'cantidad': el número de sesiones que se quieren comprar.
    # ---------------------------------------------------------------
    def comprar_sesiones(self, cantidad):
        # Primero verificamos que la membresía esté activa
        if self.estado == "Suspendida":
            return "Membresía suspendida"

        # Si está activa, actualizamos los tres contadores correspondientes
        self.sesiones_disponibles += cantidad          # Sube el saldo disponible
        self.total_sesiones_compradas += cantidad      # Sube el acumulado histórico
        self.cantidad_compras += 1                     # Registra una compra más
        return f"Se compraron {cantidad} sesiones. Disponibles: {self.sesiones_disponibles}"


    # ---------------------------------------------------------------
    # MÉTODO: utilizar_sesion
    # Descuenta una sesión del saldo disponible.
    # No recibe parámetros extra porque siempre se usa 1 sesión a la vez.
    # ---------------------------------------------------------------
    def utilizar_sesion(self):
        # Revisamos si la membresía está activa
        if self.estado == "Suspendida":
            return "Membresía suspendida"

        # Revisamos si hay sesiones disponibles antes de descontar
        if self.sesiones_disponibles == 0:
            return "Sesiones insuficientes"

        # Si todo está bien, descontamos y registramos el uso
        self.sesiones_disponibles -= 1             # Baja el saldo disponible
        self.total_sesiones_utilizadas += 1        # Sube el acumulado histórico
        self.cantidad_usos += 1                    # Registra un uso más
        return f"Sesión utilizada. Sesiones restantes: {self.sesiones_disponibles}"


    # ---------------------------------------------------------------
    # MÉTODO: ver_sesiones_disponibles
    # Solo retorna cuántas sesiones tiene disponibles ahora mismo.
    # ---------------------------------------------------------------
    def ver_sesiones_disponibles(self):
        return self.sesiones_disponibles


    # ---------------------------------------------------------------
    # MÉTODO: ver_informacion
    # Retorna TODOS los datos de la membresía en un solo texto.
    # Usamos un f-string de varias líneas para que quede legible.
    # ---------------------------------------------------------------
    def ver_informacion(self):
        return (
            f"\n{'='*40}\n"
            f"  MEMBRESÍA #{self.numero}\n"
            f"{'='*40}\n"
            f"  Nombre          : {self.nombre}\n"
            f"  Estado          : {self.estado}\n"
            f"  Sesiones disp.  : {self.sesiones_disponibles}\n"
            f"  Total compradas : {self.total_sesiones_compradas}\n"
            f"  Compras hechas  : {self.cantidad_compras}\n"
            f"  Total usadas    : {self.total_sesiones_utilizadas}\n"
            f"  Usos realizados : {self.cantidad_usos}\n"
            f"{'='*40}"
        )


    # ---------------------------------------------------------------
    # MÉTODO: suspender
    # Cambia el estado a "Suspendida".
    # ---------------------------------------------------------------
    def suspender(self):
        self.estado = "Suspendida"
        return "Membresía suspendida correctamente."


    # ---------------------------------------------------------------
    # MÉTODO: activar
    # Cambia el estado a "Activa".
    # ---------------------------------------------------------------
    def activar(self):
        self.estado = "Activa"
        return "Membresía activada correctamente."


# =============================================================
#  FUNCIONES DEL MENÚ
#  Estas funciones manejan la interacción con el usuario.
#  Están separadas de la clase para mantener la lógica limpia.
# =============================================================

def buscar_membresia(lista, numero):
    """
    Recorre la lista de membresías y retorna el objeto que coincide
    con el número dado. Si no existe, retorna None.
    """
    for m in lista:
        if m.numero == numero:
            return m
    return None


def crear_membresia(lista):
    """Solicita datos al usuario y crea una nueva membresía."""
    print("\n-- CREAR NUEVA MEMBRESÍA --")
    numero = int(input("Número de membresía: "))

    # Verificamos que el número no esté ya en uso
    if buscar_membresia(lista, numero):
        print("⚠ Ya existe una membresía con ese número.")
        return

    nombre = input("Nombre del cliente: ")
    nueva = Membresia(numero, nombre)    # Creamos el objeto usando la clase
    lista.append(nueva)                  # Lo añadimos a la lista general
    print(f"✓ Membresía #{numero} creada para {nombre}.")


def mostrar_todas(lista):
    """Muestra la información de todas las membresías registradas."""
    if not lista:
        print("\nNo hay membresías registradas.")
        return
    for m in lista:
        print(m.ver_informacion())


def seleccionar_membresia(lista):
    """
    Pide al usuario un número de membresía y retorna el objeto.
    Si no existe, imprime un aviso y retorna None.
    """
    numero = int(input("Número de membresía: "))
    m = buscar_membresia(lista, numero)
    if not m:
        print("⚠ Membresía no encontrada.")
    return m


def mostrar_menu():
    """Imprime las opciones del menú principal."""
    print("\n" + "="*40)
    print("   SISTEMA DE MEMBRESÍAS - GIMNASIO")
    print("="*40)
    print("1. Crear nueva membresía")
    print("2. Ver todas las membresías")
    print("3. Comprar sesiones")
    print("4. Utilizar sesión")
    print("5. Ver sesiones disponibles")
    print("6. Ver información de una membresía")
    print("7. Suspender membresía")
    print("8. Activar membresía")
    print("9. Salir")
    print("="*40)


# =============================================================
#  PROGRAMA PRINCIPAL
#  Aquí inicia la ejecución. El bucle while mantiene el menú
#  activo hasta que el usuario elige la opción 9 (Salir).
# =============================================================

def main():
    # Lista donde guardaremos todos los objetos Membresia
    membresias = []

    # Bucle principal: se repite hasta que el usuario quiera salir
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            crear_membresia(membresias)

        elif opcion == "2":
            mostrar_todas(membresias)

        elif opcion == "3":
            # Comprar sesiones en una membresía específica
            print("\n-- COMPRAR SESIONES --")
            m = seleccionar_membresia(membresias)
            if m:
                cantidad = int(input("¿Cuántas sesiones desea comprar? "))
                print(m.comprar_sesiones(cantidad))

        elif opcion == "4":
            # Usar una sesión de una membresía
            print("\n-- UTILIZAR SESIÓN --")
            m = seleccionar_membresia(membresias)
            if m:
                print(m.utilizar_sesion())

        elif opcion == "5":
            # Consultar sesiones disponibles
            print("\n-- SESIONES DISPONIBLES --")
            m = seleccionar_membresia(membresias)
            if m:
                print(f"Sesiones disponibles: {m.ver_sesiones_disponibles()}")

        elif opcion == "6":
            # Ver toda la información de una membresía
            print("\n-- INFORMACIÓN DE MEMBRESÍA --")
            m = seleccionar_membresia(membresias)
            if m:
                print(m.ver_informacion())

        elif opcion == "7":
            # Suspender membresía
            print("\n-- SUSPENDER MEMBRESÍA --")
            m = seleccionar_membresia(membresias)
            if m:
                print(m.suspender())

        elif opcion == "8":
            # Activar membresía
            print("\n-- ACTIVAR MEMBRESÍA --")
            m = seleccionar_membresia(membresias)
            if m:
                print(m.activar())

        elif opcion == "9":
            print("\n¡Hasta luego!")
            break   # Sale del bucle while y termina el programa

        else:
            print("⚠ Opción no válida. Intente de nuevo.")


# Este bloque garantiza que main() solo se ejecute cuando corremos
# este archivo directamente, no cuando se importa desde otro archivo.
if __name__ == "__main__":
    main()
