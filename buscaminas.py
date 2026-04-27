# =============================================================================
# BUSCAMINAS - Proyecto #2 - Ingeniería de Sistemas 2026
# =============================================================================
# Descripción: Implementación completa del juego Buscaminas con interfaz
#              gráfica Tkinter. Usa matrices como estructura de datos principal.
# Lenguaje:    Python 3
# Librerías:   tkinter (GUI), random (minas), json (archivos), time (timer)
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import json
import os
import time
from datetime import datetime


# =============================================================================
# CONSTANTE: NIVELES
# Diccionario con la configuración predefinida de cada nivel de dificultad.
# Formato: 'NombreNivel': (filas, columnas, num_minas)
# =============================================================================
NIVELES = {
    'Fácil':    (8,  8,  10),
    'Medio':    (10, 10, 15),
    'Difícil':  (12, 12, 25),
    'Experto':  (15, 15, 40),
}

# Directorio donde se guardan los archivos JSON de puntajes
DIRECTORIO_PUNTAJES = 'puntajes'

# =============================================================================
# CONSTANTE: COLORES_NUMEROS
# Colores estándar del Buscaminas clásico para los dígitos 1-8.
# Cada número indica cuántas minas hay en las celdas adyacentes.
# =============================================================================
COLORES_NUMEROS = {
    1: '#0000FF',   # 1 = Azul
    2: '#008000',   # 2 = Verde
    3: '#FF0000',   # 3 = Rojo
    4: '#000080',   # 4 = Azul oscuro
    5: '#800000',   # 5 = Marrón
    6: '#008080',   # 6 = Cian
    7: '#000000',   # 7 = Negro
    8: '#808080',   # 8 = Gris
}


# =============================================================================
# CLASE: Tablero
# =============================================================================
# Gestiona TODA la lógica interna del juego Buscaminas mediante TRES matrices:
#
#   matriz_minas   → bool[][]  : True si la celda contiene una mina
#   matriz_numeros → int[][]   : número de minas adyacentes (−1 si es mina)
#   matriz_estado  → str[][]   : estado visual de cada celda:
#                                  'tapada'      → celda sin descubrir
#                                  'descubierta' → celda visible
#                                  'bandera'     → jugador marcó con bandera
#
# Esta clase NO depende de Tkinter; solo maneja datos y reglas del juego.
# =============================================================================
class Tablero:
    def __init__(self, filas: int, columnas: int, num_minas: int):
        """
        Inicializa el tablero con tres matrices vacías.

        Args:
            filas:     número de filas del tablero
            columnas:  número de columnas del tablero
            num_minas: total de minas que se colocarán
        """
        self.filas = filas
        self.columnas = columnas
        self.num_minas = num_minas

        # --- Matrices principales (listas de listas) ---
        # Indica si hay mina en cada celda (se rellena en colocar_minas)
        self.matriz_minas = [[False] * columnas for _ in range(filas)]

        # Guarda el número de minas vecinas de cada celda (−1 = es mina)
        self.matriz_numeros = [[0] * columnas for _ in range(filas)]

        # Estado actual visible de cada celda para la interfaz gráfica
        self.matriz_estado = [['tapada'] * columnas for _ in range(filas)]

        # --- Variables de control del juego ---
        self.primera_jugada = True        # Las minas se colocan DESPUÉS del 1er click
        self.juego_terminado = False      # True si ganó o perdió
        self.ganado = False               # True solo si completó el tablero
        self.minas_marcadas = 0           # Contador de banderas colocadas
        self.celdas_descubiertas = 0      # Celdas seguras ya reveladas
        self.celdas_sin_mina = filas * columnas - num_minas  # Meta para ganar

    # -------------------------------------------------------------------------
    def colocar_minas(self, fila_excluida: int, col_excluida: int):
        """
        Distribuye las minas aleatoriamente en el tablero usando random.sample.

        La celda clicada primero (fila_excluida, col_excluida) se excluye del
        sorteo para garantizar que el jugador nunca pierde en el primer turno.

        Args:
            fila_excluida: fila de la primera celda clicada (protegida)
            col_excluida:  columna de la primera celda clicada (protegida)
        """
        # Construimos lista de todas las posiciones disponibles, excluyendo la elegida
        posiciones_disponibles = [
            (f, c)
            for f in range(self.filas)
            for c in range(self.columnas)
            if not (f == fila_excluida and c == col_excluida)
        ]

        # Selección aleatoria sin reemplazo (librería random)
        minas_elegidas = random.sample(posiciones_disponibles, self.num_minas)

        # Marcar cada posición de mina en la matriz correspondiente
        for f, c in minas_elegidas:
            self.matriz_minas[f][c] = True
            self.matriz_numeros[f][c] = -1   # −1 indica que ES mina

        # Ya con las minas puestas, calculamos los números
        self.calcular_numeros()

    # -------------------------------------------------------------------------
    def calcular_numeros(self):
        """
        Recorre el tablero y asigna a cada celda (que no sea mina) el número
        de minas que tiene en sus 8 vecinos (o menos en los bordes).

        Se itera sobre los 8 desplazamientos (−1, 0, +1) × (−1, 0, +1) para
        cubrir todas las diagonales, horizontales y verticales.
        """
        desplazamientos = [(-1, -1), (-1, 0), (-1, 1),
                           ( 0, -1),           ( 0, 1),
                           ( 1, -1), ( 1, 0), ( 1, 1)]

        for f in range(self.filas):
            for c in range(self.columnas):
                # Las minas no necesitan número
                if self.matriz_minas[f][c]:
                    continue

                contador = 0
                for df, dc in desplazamientos:
                    nf, nc = f + df, c + dc
                    # Verificar que el vecino está dentro de los límites
                    if 0 <= nf < self.filas and 0 <= nc < self.columnas:
                        if self.matriz_minas[nf][nc]:
                            contador += 1

                self.matriz_numeros[f][c] = contador

    # -------------------------------------------------------------------------
    def descubrir_celda(self, fila: int, col: int) -> bool:
        """
        Intenta descubrir la celda indicada.

        Si es el primer click, primero llama a colocar_minas() para garantizar
        que la primera celda tocada nunca sea una mina.

        Si la celda descubierta es una mina:
            → marca el juego como terminado y retorna False

        Si es una celda segura:
            → llama a _expandir() para el efecto de revelado automático
            → retorna True

        Args:
            fila: fila de la celda a descubrir
            col:  columna de la celda a descubrir

        Returns:
            True  → el juego continúa
            False → el jugador pisó una mina
        """
        # En el primer click se colocan las minas (la celda clickeada está protegida)
        if self.primera_jugada:
            self.colocar_minas(fila, col)
            self.primera_jugada = False

        # Ignorar celdas ya descubiertas o marcadas con bandera
        if self.matriz_estado[fila][col] != 'tapada':
            return True

        # ¡Mina! → perder
        if self.matriz_minas[fila][col]:
            self.matriz_estado[fila][col] = 'descubierta'
            self.juego_terminado = True
            return False

        # Celda segura: expandir recursivamente
        self._expandir(fila, col)
        return True

    # -------------------------------------------------------------------------
    def _expandir(self, fila: int, col: int):
        """
        Algoritmo de relleno (flood fill / BFS recursivo) que descubre
        automáticamente todas las celdas vacías (número 0) conectadas.

        Cuando una celda con 0 minas vecinas es revelada, se revelan también
        sus 8 vecinos, y así sucesivamente hasta encontrar bordes numéricos.

        Args:
            fila: fila de la celda a expandir
            col:  columna de la celda a expandir
        """
        # Condición de parada: ya descubierta o es bandera
        if self.matriz_estado[fila][col] != 'tapada':
            return

        # Descubrir esta celda
        self.matriz_estado[fila][col] = 'descubierta'
        self.celdas_descubiertas += 1

        # Verificar victoria: se descubrieron todas las celdas sin minas
        if self.celdas_descubiertas >= self.celdas_sin_mina:
            self.ganado = True
            self.juego_terminado = True

        # Si la celda es 0, expandir a los 8 vecinos
        if self.matriz_numeros[fila][col] == 0:
            desplazamientos = [(-1, -1), (-1, 0), (-1, 1),
                               ( 0, -1),           ( 0, 1),
                               ( 1, -1), ( 1, 0), ( 1, 1)]
            for df, dc in desplazamientos:
                nf, nc = fila + df, col + dc
                if 0 <= nf < self.filas and 0 <= nc < self.columnas:
                    if self.matriz_estado[nf][nc] == 'tapada':
                        self._expandir(nf, nc)

    # -------------------------------------------------------------------------
    def marcar_bandera(self, fila: int, col: int):
        """
        Alterna el marcador de bandera en una celda tapada.

        Bandera: el jugador cree que hay una mina. Solo funciona en celdas
        que aún están tapadas (no descubiertas).

        Args:
            fila: fila de la celda
            col:  columna de la celda
        """
        if self.matriz_estado[fila][col] == 'tapada':
            self.matriz_estado[fila][col] = 'bandera'
            self.minas_marcadas += 1
        elif self.matriz_estado[fila][col] == 'bandera':
            self.matriz_estado[fila][col] = 'tapada'
            self.minas_marcadas -= 1

    # -------------------------------------------------------------------------
    def revelar_todo(self):
        """
        Revela todas las minas del tablero al perder la partida.
        Se usa para mostrar la ubicación de todas las minas en pantalla.
        """
        for f in range(self.filas):
            for c in range(self.columnas):
                if self.matriz_minas[f][c]:
                    self.matriz_estado[f][c] = 'descubierta'


# =============================================================================
# CLASE: GestorPuntajes
# =============================================================================
# Maneja la persistencia de puntajes usando archivos JSON.
# Un archivo por nivel de dificultad, almacenado en DIRECTORIO_PUNTAJES/.
#
# Formato del archivo JSON:
#   [
#     { "nombre": "Ana",  "tiempo": 45, "fecha": "2026-01-15 10:30" },
#     { "nombre": "Luis", "tiempo": 78, "fecha": "2026-01-16 09:00" },
#     ...
#   ]
# Ordenados de menor a mayor tiempo (mejor = más rápido).
# Se conservan únicamente los 10 mejores registros por nivel.
# =============================================================================
class GestorPuntajes:
    def __init__(self):
        """
        Crea el directorio de puntajes si no existe al iniciar la aplicación.
        """
        if not os.path.exists(DIRECTORIO_PUNTAJES):
            os.makedirs(DIRECTORIO_PUNTAJES)

    # -------------------------------------------------------------------------
    def _ruta_archivo(self, nivel: str) -> str:
        """
        Construye la ruta completa del archivo JSON para el nivel indicado.

        Convierte el nombre del nivel a minúsculas y reemplaza espacios por
        guiones bajos para nombres de archivo seguros.

        Args:
            nivel: nombre del nivel (ej. 'Fácil', 'Experto', 'Personalizado')

        Returns:
            Ruta relativa al archivo JSON del nivel
        """
        nombre_seguro = nivel.replace(' ', '_').lower()
        return os.path.join(DIRECTORIO_PUNTAJES, f'puntajes_{nombre_seguro}.json')

    # -------------------------------------------------------------------------
    def leer_puntajes(self, nivel: str) -> list:
        """
        Lee y retorna la lista de puntajes almacenada para el nivel dado.

        Si el archivo no existe o está corrupto, retorna una lista vacía
        en lugar de lanzar una excepción (manejo defensivo de archivos).

        Args:
            nivel: nombre del nivel de dificultad

        Returns:
            Lista de diccionarios con nombre, tiempo y fecha
        """
        ruta = self._ruta_archivo(nivel)
        if not os.path.exists(ruta):
            return []
        try:
            with open(ruta, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, IOError):
            return []

    # -------------------------------------------------------------------------
    def guardar_puntaje(self, nivel: str, nombre: str, tiempo: int):
        """
        Agrega un nuevo puntaje y conserva solo los 10 mejores para el nivel.

        El criterio de ordenamiento es el tiempo en segundos (menor = mejor).
        Usa json.dump con indent=2 para que el archivo sea legible por humanos.

        Args:
            nivel:  nombre del nivel (determina el archivo destino)
            nombre: nombre del jugador ingresado en el diálogo
            tiempo: tiempo en segundos que tardó en ganar
        """
        puntajes = self.leer_puntajes(nivel)

        # Nuevo registro con timestamp actual
        nuevo_registro = {
            'nombre': nombre,
            'tiempo': tiempo,
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        puntajes.append(nuevo_registro)

        # Ordenar por tiempo ascendente y conservar solo los mejores 10
        puntajes.sort(key=lambda x: x['tiempo'])
        puntajes = puntajes[:10]

        # Escribir en el archivo JSON
        ruta = self._ruta_archivo(nivel)
        with open(ruta, 'w', encoding='utf-8') as archivo:
            json.dump(puntajes, archivo, ensure_ascii=False, indent=2)


# =============================================================================
# CLASE: App (Ventana Principal / Controlador de Navegación)
# =============================================================================
# Hereda de tk.Tk (ventana raíz de Tkinter).
# Actúa como controlador de navegación: reemplaza el frame visible actual
# por el frame de la pantalla solicitada (patrón "frame container").
#
# Frames (pantallas) disponibles:
#   MenuPrincipal        → pantalla de inicio
#   SeleccionDificultad  → elección de nivel
#   TableroJuego         → tablero activo durante la partida
#   PuntajesAltos        → tabla de mejores tiempos
# =============================================================================
class App(tk.Tk):
    def __init__(self):
        """
        Configura la ventana principal y muestra el menú inicial.
        """
        super().__init__()
        self.title('💣 Buscaminas')
        self.resizable(False, False)
        self.configure(bg='#2c3e50')

        # Instancia única del gestor de puntajes compartida por todos los frames
        self.gestor_puntajes = GestorPuntajes()

        # Referencia al frame actualmente visible (None al iniciar)
        self._frame_actual = None

        # Mostrar pantalla inicial
        self.mostrar_menu_principal()

        # Centrar la ventana en la pantalla después de un ciclo de eventos
        self.after(10, self._centrar_ventana)

    # -------------------------------------------------------------------------
    def _centrar_ventana(self):
        """
        Calcula la posición x, y para centrar la ventana en el monitor.
        Se ejecuta con after() para esperar que Tkinter calcule el tamaño real.
        """
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth()  // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f'+{x}+{y}')

    # -------------------------------------------------------------------------
    def _mostrar_frame(self, ClaseFrame, **kwargs):
        """
        Destruye el frame actual y crea uno nuevo de la clase indicada.

        Args:
            ClaseFrame: clase del frame a instanciar (no una instancia)
            **kwargs:   argumentos adicionales pasados al constructor del frame
        """
        if self._frame_actual is not None:
            self._frame_actual.destroy()
        self._frame_actual = ClaseFrame(self, **kwargs)
        self._frame_actual.pack(fill='both', expand=True)
        # Recentrar la ventana cada vez que cambia el contenido
        self.after(10, self._centrar_ventana)

    # -------------------------------------------------------------------------
    def mostrar_menu_principal(self):
        """Navega a la pantalla del menú principal."""
        self._mostrar_frame(MenuPrincipal)

    def mostrar_seleccion_dificultad(self):
        """Navega a la pantalla de selección de dificultad."""
        self._mostrar_frame(SeleccionDificultad)

    def mostrar_tablero(self, nivel: str, filas: int = None,
                        columnas: int = None, minas: int = None):
        """
        Navega a la pantalla del tablero de juego.

        Args:
            nivel:    nombre del nivel seleccionado
            filas:    filas para nivel personalizado (None para niveles predefinidos)
            columnas: columnas para nivel personalizado
            minas:    minas para nivel personalizado
        """
        self._mostrar_frame(TableroJuego, nivel=nivel,
                            filas=filas, columnas=columnas, minas=minas)

    def mostrar_puntajes(self):
        """Navega a la pantalla de puntajes altos."""
        self._mostrar_frame(PuntajesAltos)


# =============================================================================
# CLASE: MenuPrincipal (Frame)
# =============================================================================
# Primera pantalla que ve el usuario al iniciar el programa.
# Presenta las opciones principales: jugar, ver puntajes y salir.
# =============================================================================
class MenuPrincipal(tk.Frame):
    def __init__(self, master: App):
        """
        Construye el menú principal con título y tres botones de acción.

        Args:
            master: referencia a la instancia de App (ventana raíz)
        """
        super().__init__(master, bg='#2c3e50', padx=60, pady=40)
        self._construir_ui()

    # -------------------------------------------------------------------------
    def _construir_ui(self):
        """
        Crea y posiciona todos los widgets del menú principal:
        título decorativo y botones con estilo plano (relief='flat').
        """
        # Título del juego
        tk.Label(
            self,
            text='💣 BUSCAMINAS',
            font=('Arial', 36, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        ).pack(pady=(0, 10))

        # Subtítulo con créditos del proyecto
        tk.Label(
            self,
            text='Proyecto #2 — IS 2026',
            font=('Arial', 11),
            fg='#95a5a6',
            bg='#2c3e50'
        ).pack(pady=(0, 30))

        # Lista de (texto_botón, función_comando)
        opciones = [
            ('🎮  Nueva Partida',    self.master.mostrar_seleccion_dificultad),
            ('🏆  Puntajes Altos',   self.master.mostrar_puntajes),
            ('❌  Salir',            self.master.quit),
        ]

        for texto, comando in opciones:
            tk.Button(
                self,
                text=texto,
                font=('Arial', 13),
                width=22,
                command=comando,
                bg='#3498db',
                fg='white',
                activebackground='#2980b9',
                activeforeground='white',
                relief='flat',
                cursor='hand2',
                pady=9
            ).pack(pady=6)


# =============================================================================
# CLASE: SeleccionDificultad (Frame)
# =============================================================================
# Pantalla que permite al jugador elegir un nivel predefinido
# (Fácil, Medio, Difícil, Experto) o crear un nivel personalizado.
# =============================================================================
class SeleccionDificultad(tk.Frame):
    def __init__(self, master: App):
        """
        Construye la pantalla de selección de dificultad.

        Args:
            master: referencia a la instancia de App
        """
        super().__init__(master, bg='#2c3e50', padx=60, pady=30)
        self._construir_ui()

    # -------------------------------------------------------------------------
    def _construir_ui(self):
        """
        Crea botones para cada nivel predefinido y uno para nivel personalizado.
        Cada botón de nivel muestra la configuración: dimensiones y número de minas.
        """
        tk.Label(
            self,
            text='Seleccionar Dificultad',
            font=('Arial', 22, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        ).pack(pady=(0, 20))

        # Botones para cada nivel predefinido (iteramos sobre el diccionario NIVELES)
        COLORES_NIVEL = ['#27ae60', '#f39c12', '#e74c3c', '#8e44ad']
        for (nombre, (f, c, m)), color in zip(NIVELES.items(), COLORES_NIVEL):
            descripcion = f'{nombre}   ({f}×{c},  {m} minas)'
            tk.Button(
                self,
                text=descripcion,
                font=('Arial', 12),
                width=28,
                # Capturamos nombre por defecto para evitar cierre tardío (late binding)
                command=lambda n=nombre: self.master.mostrar_tablero(n),
                bg=color,
                fg='white',
                activebackground=color,
                activeforeground='white',
                relief='flat',
                cursor='hand2',
                pady=7
            ).pack(pady=5)

        # Separador visual
        tk.Frame(self, bg='#7f8c8d', height=1).pack(fill='x', pady=15)

        # Botón para nivel personalizado
        tk.Button(
            self,
            text='⚙️  Nivel Personalizado',
            font=('Arial', 12),
            width=28,
            command=self._solicitar_nivel_personalizado,
            bg='#16a085',
            fg='white',
            activebackground='#1abc9c',
            relief='flat',
            cursor='hand2',
            pady=7
        ).pack(pady=5)

        # Botón para volver al menú
        tk.Button(
            self,
            text='← Menú Principal',
            font=('Arial', 10),
            command=self.master.mostrar_menu_principal,
            bg='#7f8c8d',
            fg='white',
            relief='flat',
            cursor='hand2'
        ).pack(pady=(20, 0))

    # -------------------------------------------------------------------------
    def _solicitar_nivel_personalizado(self):
        """
        Abre una ventana modal (Toplevel) con tres campos de entrada para que
        el jugador defina filas, columnas y número de minas.

        Valida que:
          - Filas y columnas estén entre 4 y 30
          - Número de minas sea al menos 1 y como máximo (filas*columnas - 1)
        """
        ventana = tk.Toplevel(self)
        ventana.title('Nivel Personalizado')
        ventana.configure(bg='#2c3e50', padx=30, pady=20)
        ventana.resizable(False, False)
        ventana.grab_set()   # Bloqueamos la ventana padre mientras este diálogo esté abierto

        tk.Label(
            ventana,
            text='Configuración personalizada',
            font=('Arial', 14, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        ).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Definición de los campos del formulario: (etiqueta, clave_dict)
        campos_def = [
            ('Filas (4 – 30):', 'filas'),
            ('Columnas (4 – 30):', 'columnas'),
            ('Minas:', 'minas'),
        ]

        entradas = {}  # Diccionario para acceder a los Entry por clave

        for i, (etiqueta, clave) in enumerate(campos_def, start=1):
            tk.Label(
                ventana, text=etiqueta, font=('Arial', 11),
                fg='#ecf0f1', bg='#2c3e50', anchor='w'
            ).grid(row=i, column=0, sticky='w', pady=5)

            entrada = tk.Entry(ventana, font=('Arial', 11), width=8, justify='center')
            entrada.grid(row=i, column=1, padx=(10, 0), pady=5)
            entradas[clave] = entrada

        # ---- Función interna para validar y confirmar ----
        def confirmar():
            """Valida los datos ingresados y lanza la partida personalizada."""
            try:
                f = int(entradas['filas'].get())
                c = int(entradas['columnas'].get())
                m = int(entradas['minas'].get())
            except ValueError:
                messagebox.showerror('Error', 'Ingresa únicamente valores numéricos enteros.', parent=ventana)
                return

            # Validar rango de filas y columnas
            if not (4 <= f <= 30) or not (4 <= c <= 30):
                messagebox.showerror('Error', 'Filas y columnas deben estar entre 4 y 30.', parent=ventana)
                return

            # Validar número de minas
            max_minas = f * c - 1
            if not (1 <= m <= max_minas):
                messagebox.showerror(
                    'Error',
                    f'Las minas deben ser entre 1 y {max_minas} para un tablero de {f}×{c}.',
                    parent=ventana
                )
                return

            # Todo válido: cerrar diálogo e iniciar partida
            ventana.destroy()
            self.master.mostrar_tablero('Personalizado', filas=f, columnas=c, minas=m)

        tk.Button(
            ventana,
            text='🎮 Iniciar Partida',
            command=confirmar,
            font=('Arial', 12),
            bg='#27ae60',
            fg='white',
            relief='flat',
            cursor='hand2',
            pady=6
        ).grid(row=len(campos_def) + 1, column=0, columnspan=2, pady=(20, 0))

        # Vincular tecla Enter para confirmar sin click
        ventana.bind('<Return>', lambda e: confirmar())


# =============================================================================
# CLASE: TableroJuego (Frame)
# =============================================================================
# Pantalla principal durante la partida. Contiene:
#
#   • Barra superior con: botón menú, contador de minas, nivel, temporizador,
#                         botón reiniciar
#   • Grilla de botones Tkinter representando cada celda del tablero
#
# Cada botón está indexado en el diccionario self.botones[(fila, col)].
# Click izquierdo → descubrir celda
# Click derecho   → colocar/quitar bandera
#
# El temporizador usa self.after() de Tkinter para actualizarse cada segundo.
# =============================================================================
class TableroJuego(tk.Frame):
    # Tamaño base de celda en píxeles; se reduce automáticamente en tableros grandes
    TAMANO_CELDA_BASE = 36

    def __init__(self, master: App, nivel: str,
                 filas: int = None, columnas: int = None, minas: int = None):
        """
        Inicializa el tablero visual a partir de la configuración del nivel.

        Si el nivel está en NIVELES, usa sus dimensiones predefinidas.
        Si es 'Personalizado', usa los parámetros filas/columnas/minas.

        Args:
            master:   referencia a la instancia de App
            nivel:    nombre del nivel (clave de NIVELES o 'Personalizado')
            filas:    filas para nivel personalizado
            columnas: columnas para nivel personalizado
            minas:    minas para nivel personalizado
        """
        super().__init__(master, bg='#2c3e50')

        # Obtener configuración según tipo de nivel
        if nivel in NIVELES:
            f, c, m = NIVELES[nivel]
        else:
            f, c, m = filas, columnas, minas

        self.nivel = nivel

        # Instanciar la lógica del tablero (sin interfaz)
        self.tablero = Tablero(f, c, m)

        # Diccionario que mapea (fila, col) → tk.Button
        self.botones: dict = {}

        # Variables del temporizador
        self.tiempo_inicio = None
        self.tiempo_transcurrido = 0
        self.temporizador_activo = False
        self._id_after = None    # ID del callback de after() para poder cancelarlo

        # Ajustar tamaño de celda para tableros grandes
        self.tamano_celda = self._calcular_tamano_celda(f, c)

        self._construir_barra_superior()
        self._construir_tablero()

    # -------------------------------------------------------------------------
    def _calcular_tamano_celda(self, filas: int, columnas: int) -> int:
        """
        Reduce el tamaño de cada celda cuando el tablero es grande,
        para que quepa en pantallas de resolución estándar (1366×768).

        Args:
            filas:    número de filas del tablero
            columnas: número de columnas del tablero

        Returns:
            Tamaño en píxeles para cada celda
        """
        max_dim = max(filas, columnas)
        if max_dim <= 12:
            return 36
        elif max_dim <= 20:
            return 30
        else:
            return 24

    # -------------------------------------------------------------------------
    def _construir_barra_superior(self):
        """
        Crea la barra de información en la parte superior del tablero.
        Contiene: botón menú, contador de minas, nombre del nivel,
                  temporizador y botón de reinicio.
        """
        barra = tk.Frame(self, bg='#34495e', pady=8)
        barra.pack(fill='x')

        # Botón para volver al menú principal
        tk.Button(
            barra,
            text='← Menú',
            font=('Arial', 10),
            command=self._volver_menu,
            bg='#7f8c8d',
            fg='white',
            relief='flat',
            cursor='hand2'
        ).pack(side='left', padx=10)

        # Contador de minas sin marcar: minas_totales − banderas_colocadas
        self.lbl_minas = tk.Label(
            barra,
            text=f'💣 {self.tablero.num_minas}',
            font=('Arial', 14, 'bold'),
            fg='#e74c3c',
            bg='#34495e'
        )
        self.lbl_minas.pack(side='left', padx=15)

        # Etiqueta con el nombre del nivel actual
        tk.Label(
            barra,
            text=self.nivel,
            font=('Arial', 12, 'bold'),
            fg='#ecf0f1',
            bg='#34495e'
        ).pack(side='left', padx=10)

        # Botón para reiniciar la partida con la misma configuración
        tk.Button(
            barra,
            text='🔄 Reiniciar',
            font=('Arial', 10),
            command=self._reiniciar,
            bg='#e67e22',
            fg='white',
            relief='flat',
            cursor='hand2'
        ).pack(side='right', padx=10)

        # Temporizador: muestra el tiempo en segundos con 3 dígitos
        self.lbl_timer = tk.Label(
            barra,
            text='⏱ 000',
            font=('Arial', 14, 'bold'),
            fg='#2ecc71',
            bg='#34495e'
        )
        self.lbl_timer.pack(side='right', padx=15)

    # -------------------------------------------------------------------------
    def _construir_tablero(self):
        """
        Crea la grilla de botones Tkinter usando grid(), uno por cada celda
        del tablero (filas × columnas).

        Cada botón:
         - Se almacena en self.botones[(fila, col)] para acceso directo
         - Vincula <Button-1> (left click) → descubrir
         - Vincula <Button-3> (right click) → bandera
        """
        frame_grilla = tk.Frame(self, bg='#2c3e50', padx=8, pady=8)
        frame_grilla.pack()

        # Calcular ancho del botón en caracteres según tamaño de celda
        ancho_btn = 2 if self.tamano_celda >= 30 else 1
        font_size = 10 if self.tamano_celda >= 30 else 8

        for f in range(self.tablero.filas):
            for c in range(self.tablero.columnas):
                btn = tk.Button(
                    frame_grilla,
                    width=ancho_btn,
                    height=1,
                    font=('Arial', font_size, 'bold'),
                    relief='raised',
                    bg='#95a5a6',
                    activebackground='#bdc3c7',
                    cursor='hand2',
                    bd=1
                )
                btn.grid(row=f, column=c, padx=1, pady=1)

                # Uso de argumentos por defecto para capturar fi y ci en el closure
                btn.bind('<Button-1>', lambda evt, fi=f, ci=c: self._click_izquierdo(fi, ci))
                btn.bind('<Button-3>', lambda evt, fi=f, ci=c: self._click_derecho(fi, ci))

                self.botones[(f, c)] = btn

    # -------------------------------------------------------------------------
    def _click_izquierdo(self, fila: int, col: int):
        """
        Manejador del click izquierdo: descubre la celda seleccionada.

        Si es el primer click de la partida, lanza el temporizador.
        Luego llama a tablero.descubrir_celda() y actualiza la interfaz.
        Evalúa si el jugador ganó o perdió tras cada click.

        Args:
            fila: fila de la celda clickeada
            col:  columna de la celda clickeada
        """
        if self.tablero.juego_terminado:
            return   # No hacer nada si el juego ya terminó

        if self.tablero.matriz_estado[fila][col] in ('descubierta', 'bandera'):
            return   # Ignorar clicks en celdas ya procesadas

        # Iniciar el temporizador la primera vez que se hace click
        if self.tablero.primera_jugada:
            self._iniciar_temporizador()

        # Ejecutar lógica de juego
        juego_continua = self.tablero.descubrir_celda(fila, col)
        self._actualizar_grilla()

        if not juego_continua:
            # Perdió: revelar todas las minas y mostrar mensaje
            self.tablero.revelar_todo()
            self._actualizar_grilla()
            self._detener_temporizador()
            messagebox.showwarning(
                '💥 ¡Boom!',
                '¡Pisaste una mina!\nJuego terminado.'
            )
        elif self.tablero.ganado:
            # Ganó: detener timer y registrar puntaje
            self._detener_temporizador()
            self._registrar_victoria()

    # -------------------------------------------------------------------------
    def _click_derecho(self, fila: int, col: int):
        """
        Manejador del click derecho: coloca o quita una bandera en la celda.

        Las banderas sirven para marcar donde el jugador cree que hay minas.
        Solo funciona en celdas tapadas (no descubiertas) y mientras el juego
        no haya terminado.

        Args:
            fila: fila de la celda clickeada
            col:  columna de la celda clickeada
        """
        if self.tablero.juego_terminado:
            return
        if self.tablero.matriz_estado[fila][col] == 'descubierta':
            return

        self.tablero.marcar_bandera(fila, col)
        self._actualizar_grilla()

    # -------------------------------------------------------------------------
    def _actualizar_grilla(self):
        """
        Recorre todas las celdas y actualiza el texto, color y relieve
        de cada botón Tkinter según el estado actual en la matriz.

        Estados visuales:
          'tapada'      → botón gris elevado, sin texto
          'bandera'     → botón gris con emoji 🚩
          'descubierta' → si es mina: rojo con 💣
                          si es número: beige con dígito de color
                          si es 0: beige sin texto
        """
        # Actualizar contador de minas (minas_totales − banderas)
        minas_restantes = self.tablero.num_minas - self.tablero.minas_marcadas
        self.lbl_minas.config(text=f'💣 {minas_restantes}')

        for f in range(self.tablero.filas):
            for c in range(self.tablero.columnas):
                btn = self.botones[(f, c)]
                estado = self.tablero.matriz_estado[f][c]

                if estado == 'tapada':
                    btn.config(text='', bg='#95a5a6', relief='raised', fg='black')

                elif estado == 'bandera':
                    btn.config(text='🚩', bg='#95a5a6', relief='raised')

                elif estado == 'descubierta':
                    if self.tablero.matriz_minas[f][c]:
                        # Celda con mina explotada
                        btn.config(text='💣', bg='#e74c3c', relief='sunken', fg='black')
                    else:
                        numero = self.tablero.matriz_numeros[f][c]
                        color_texto = COLORES_NUMEROS.get(numero, '#2c3e50')
                        texto = str(numero) if numero > 0 else ''
                        btn.config(
                            text=texto,
                            bg='#d5dbdb',
                            relief='sunken',
                            fg=color_texto
                        )

    # -------------------------------------------------------------------------
    def _iniciar_temporizador(self):
        """
        Registra el momento de inicio y activa el ciclo de actualización
        del temporizador cada 1000 ms usando self.after().
        """
        self.tiempo_inicio = time.time()
        self.temporizador_activo = True
        self._ciclo_temporizador()

    # -------------------------------------------------------------------------
    def _ciclo_temporizador(self):
        """
        Calcula el tiempo transcurrido desde el inicio,
        actualiza el label y se reprograma a sí mismo cada segundo.

        Solo se ejecuta si temporizador_activo es True.
        """
        if self.temporizador_activo:
            self.tiempo_transcurrido = int(time.time() - self.tiempo_inicio)
            self.lbl_timer.config(text=f'⏱ {self.tiempo_transcurrido:03d}')
            # Reprogramar este mismo método en 1 segundo
            self._id_after = self.after(1000, self._ciclo_temporizador)

    # -------------------------------------------------------------------------
    def _detener_temporizador(self):
        """
        Desactiva el temporizador y cancela el callback pendiente de after()
        para evitar actualizaciones sobre un frame ya destruido.
        """
        self.temporizador_activo = False
        if self._id_after is not None:
            self.after_cancel(self._id_after)
            self._id_after = None

    # -------------------------------------------------------------------------
    def _registrar_victoria(self):
        """
        Muestra un diálogo de victoria, solicita el nombre del jugador
        y delega el guardado del puntaje al GestorPuntajes.

        Si el jugador no ingresa nombre, muestra el mensaje de victoria
        sin guardar puntaje.
        """
        nombre = simpledialog.askstring(
            '🏆 ¡Ganaste!',
            f'¡Felicidades! Tiempo: {self.tiempo_transcurrido} segundos\n\n'
            'Ingresa tu nombre para el ranking:',
            parent=self
        )
        if nombre and nombre.strip():
            nombre_limpio = nombre.strip()
            self.master.gestor_puntajes.guardar_puntaje(
                self.nivel, nombre_limpio, self.tiempo_transcurrido
            )
            messagebox.showinfo(
                '¡Puntaje guardado!',
                f'Se registró el puntaje de {nombre_limpio}.\n'
                f'Nivel: {self.nivel} — Tiempo: {self.tiempo_transcurrido}s'
            )
        else:
            messagebox.showinfo(
                '¡Ganaste!',
                f'Tiempo: {self.tiempo_transcurrido} segundos\n(Puntaje no registrado)'
            )

    # -------------------------------------------------------------------------
    def _reiniciar(self):
        """
        Cancela el temporizador actual y carga una nueva instancia de TableroJuego
        con la misma configuración (mismo nivel, mismas dimensiones y minas).
        """
        self._detener_temporizador()
        self.master.mostrar_tablero(
            self.nivel,
            filas=self.tablero.filas,
            columnas=self.tablero.columnas,
            minas=self.tablero.num_minas
        )

    # -------------------------------------------------------------------------
    def _volver_menu(self):
        """
        Cancela el temporizador y regresa a la pantalla del menú principal.
        """
        self._detener_temporizador()
        self.master.mostrar_menu_principal()


# =============================================================================
# CLASE: PuntajesAltos (Frame)
# =============================================================================
# Pantalla que muestra los mejores 10 tiempos para cada nivel de dificultad.
# Usa un ttk.Notebook con una pestaña por nivel.
# Lee los datos directamente desde los archivos JSON del GestorPuntajes.
# =============================================================================
class PuntajesAltos(tk.Frame):
    def __init__(self, master: App):
        """
        Construye la pantalla de puntajes con pestañas por nivel.

        Args:
            master: referencia a la instancia de App
        """
        super().__init__(master, bg='#2c3e50', padx=20, pady=20)
        self._construir_ui()

    # -------------------------------------------------------------------------
    def _construir_ui(self):
        """
        Crea el encabezado, el Notebook con pestañas y el botón de regreso.
        """
        tk.Label(
            self,
            text='🏆 Puntajes Altos',
            font=('Arial', 24, 'bold'),
            fg='#f1c40f',
            bg='#2c3e50'
        ).pack(pady=(0, 15))

        # Notebook de Tkinter: cada pestaña corresponde a un nivel
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        # Crear una pestaña para cada nivel (predefinido + personalizado)
        niveles_a_mostrar = list(NIVELES.keys()) + ['Personalizado']
        for nivel in niveles_a_mostrar:
            frame_tab = tk.Frame(notebook, bg='#34495e', padx=10, pady=10)
            notebook.add(frame_tab, text=f'  {nivel}  ')
            self._llenar_tabla(frame_tab, nivel)

        # Botón para regresar al menú
        tk.Button(
            self,
            text='← Menú Principal',
            font=('Arial', 11),
            command=self.master.mostrar_menu_principal,
            bg='#7f8c8d',
            fg='white',
            relief='flat',
            cursor='hand2'
        ).pack(pady=(15, 0))

    # -------------------------------------------------------------------------
    def _llenar_tabla(self, parent: tk.Frame, nivel: str):
        """
        Llena el frame de una pestaña con la tabla de puntajes del nivel.

        Muestra los encabezados y hasta 10 filas de resultados.
        Si no hay registros, muestra un mensaje informativo.

        Args:
            parent: frame contenedor de la pestaña
            nivel:  nombre del nivel para consultar sus puntajes
        """
        encabezados = ['#', 'Jugador', 'Tiempo (s)', 'Fecha']
        anchos = [4, 18, 12, 18]

        # Fila de encabezados
        for col, (enc, ancho) in enumerate(zip(encabezados, anchos)):
            tk.Label(
                parent,
                text=enc,
                font=('Arial', 11, 'bold'),
                fg='#f1c40f',
                bg='#2d3436',
                width=ancho,
                relief='flat',
                anchor='center'
            ).grid(row=0, column=col, padx=2, pady=(0, 5), sticky='nsew')

        # Leer puntajes del archivo JSON
        puntajes = self.master.gestor_puntajes.leer_puntajes(nivel)

        if not puntajes:
            # Mensaje cuando no hay registros en el archivo
            tk.Label(
                parent,
                text='Aún no hay puntajes registrados para este nivel.',
                font=('Arial', 10),
                fg='#95a5a6',
                bg='#34495e'
            ).grid(row=1, column=0, columnspan=len(encabezados), pady=20)
            return

        # Filas de datos: alternamos colores de fondo para mejor legibilidad
        for i, registro in enumerate(puntajes, start=1):
            color_fila = '#3d5166' if i % 2 == 0 else '#34495e'
            datos_fila = [str(i), registro['nombre'], str(registro['tiempo']), registro['fecha']]

            for col, (dato, ancho) in enumerate(zip(datos_fila, anchos)):
                tk.Label(
                    parent,
                    text=dato,
                    font=('Arial', 10),
                    fg='#ecf0f1',
                    bg=color_fila,
                    width=ancho,
                    anchor='center'
                ).grid(row=i, column=col, padx=2, pady=1, sticky='nsew')


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================
# El bloque if __name__ == '__main__' garantiza que la aplicación solo se
# ejecute cuando se corre directamente este archivo (no al importarlo como
# módulo en otro script).
# =============================================================================
if __name__ == '__main__':
    app = App()
    app.mainloop()
