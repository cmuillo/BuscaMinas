import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import json
import os
import time
from datetime import datetime

# =============================================================
# GUIA RAPIDA PARA ESTUDIAR ESTE ARCHIVO (orden recomendado)
# =============================================================
# 1) Lee main() al final: ahi inicia todo.
# 2) Revisa cambiar_pantalla() y las funciones pantalla_*.
# 3) Revisa iniciar_partida() para ver como se resetea el estado.
# 4) Revisa click_izquierdo() y click_derecho() (eventos principales).
# 5) Revisa descubrir(), expandir() y calcular_numeros() (logica central).
# 6) Al final, revisa leer_puntajes()/guardar_puntaje().

# ==========================
# CONFIGURACION DEL JUEGO
# ==========================
NIVELES = {
    'Fácil': (8, 8, 10),
    'Medio': (10, 10, 15),
    'Difícil': (12, 12, 25),
    'Experto': (15, 15, 40),
}

COLORES_NUMEROS = {
    1: '#0000FF',
    2: '#008000',
    3: '#FF0000',
    4: '#000080',
    5: '#800000',
    6: '#008080',
    7: '#000000',
    8: '#808080',
}

DIRECTORIO_PUNTAJES = 'puntajes'

# ==========================
# ESTADO GLOBAL (didactico)
# ==========================
root = None
frame_actual = None

juego = {
    'nivel': None,
    'tablero': None,
    'botones': {},
    'lbl_minas': None,
    'lbl_timer': None,
    'tiempo_inicio': 0,
    'tiempo_transcurrido': 0,
    'temporizador_activo': False,
    'after_id': None,
}


# ==========================
# BLOQUE 1: LOGICA DE TABLERO
# ==========================
def crear_tablero(filas, columnas, minas):
    # FUNCION CLAVE 1: Inicializa toda la estructura base del juego en memoria.
    return {
        'filas': filas,
        'columnas': columnas,
        'minas': minas,
        'matriz_minas': [[False] * columnas for _ in range(filas)],
        'matriz_numeros': [[0] * columnas for _ in range(filas)],
        'matriz_estado': [['tapada'] * columnas for _ in range(filas)],
        'primera_jugada': True,
        'juego_terminado': False,
        'ganado': False,
        'minas_marcadas': 0,
        'celdas_descubiertas': 0,
        'celdas_sin_mina': filas * columnas - minas,
    }


def colocar_minas(tablero, fila_excluida, col_excluida):
    # Se arma una lista de celdas candidatas excluyendo la primera jugada,
    # para garantizar que el primer click nunca sea mina.
    posiciones = [
        (f, c)
        for f in range(tablero['filas'])
        for c in range(tablero['columnas'])
        if not (f == fila_excluida and c == col_excluida)
    ]

    # random.sample elige posiciones unicas (sin repetir celdas).
    for f, c in random.sample(posiciones, tablero['minas']):
        tablero['matriz_minas'][f][c] = True
        tablero['matriz_numeros'][f][c] = -1

    calcular_numeros(tablero)


def calcular_numeros(tablero):
    # Desplazamientos de los 8 vecinos alrededor de una celda.
    vecinos = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    for f in range(tablero['filas']):
        for c in range(tablero['columnas']):
            if tablero['matriz_minas'][f][c]:
                continue

            total = 0
            for df, dc in vecinos:
                nf, nc = f + df, c + dc
                # Solo contamos vecinos dentro de los limites del tablero.
                if 0 <= nf < tablero['filas'] and 0 <= nc < tablero['columnas']:
                    if tablero['matriz_minas'][nf][nc]:
                        total += 1
            tablero['matriz_numeros'][f][c] = total


def expandir(tablero, fila, col):
    # FUNCION CLAVE 2: Ejecuta la apertura en cadena de celdas vacias (flood fill).
    # Caso base: si no esta tapada, no se procesa de nuevo.
    if tablero['matriz_estado'][fila][col] != 'tapada':
        return

    tablero['matriz_estado'][fila][col] = 'descubierta'
    tablero['celdas_descubiertas'] += 1

    if tablero['celdas_descubiertas'] >= tablero['celdas_sin_mina']:
        tablero['ganado'] = True
        tablero['juego_terminado'] = True

    if tablero['matriz_numeros'][fila][col] != 0:
        return

    vecinos = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    # Flood fill: solo cuando la celda es 0, se abre en cadena a vecinos.
    for df, dc in vecinos:
        nf, nc = fila + df, col + dc
        if 0 <= nf < tablero['filas'] and 0 <= nc < tablero['columnas']:
            if tablero['matriz_estado'][nf][nc] == 'tapada':
                expandir(tablero, nf, nc)


def descubrir(tablero, fila, col):
    # FUNCION CLAVE 3: Controla la jugada principal (primer click seguro, mina o expansion).
    # En la primera jugada se colocan minas despues del click seguro.
    if tablero['primera_jugada']:
        colocar_minas(tablero, fila, col)
        tablero['primera_jugada'] = False

    # Si la celda ya no esta tapada, ignoramos el evento.
    if tablero['matriz_estado'][fila][col] != 'tapada':
        return True

    # Si pisamos mina, termina la partida.
    if tablero['matriz_minas'][fila][col]:
        tablero['matriz_estado'][fila][col] = 'descubierta'
        tablero['juego_terminado'] = True
        return False

    expandir(tablero, fila, col)
    return True


def marcar_bandera(tablero, fila, col):
    estado = tablero['matriz_estado'][fila][col]
    if estado == 'tapada':
        tablero['matriz_estado'][fila][col] = 'bandera'
        tablero['minas_marcadas'] += 1
    elif estado == 'bandera':
        tablero['matriz_estado'][fila][col] = 'tapada'
        tablero['minas_marcadas'] -= 1


def revelar_minas(tablero):
    for f in range(tablero['filas']):
        for c in range(tablero['columnas']):
            if tablero['matriz_minas'][f][c]:
                tablero['matriz_estado'][f][c] = 'descubierta'


# ==========================
# BLOQUE 2: PUNTAJES
# ==========================
def asegurar_directorio_puntajes():
    if not os.path.exists(DIRECTORIO_PUNTAJES):
        os.makedirs(DIRECTORIO_PUNTAJES)


def ruta_puntajes(nivel):
    nombre_archivo = nivel.replace(' ', '_').lower()
    return os.path.join(DIRECTORIO_PUNTAJES, f'puntajes_{nombre_archivo}.json')


def leer_puntajes(nivel):
    ruta = ruta_puntajes(nivel)
    if not os.path.exists(ruta):
        return []

    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def guardar_puntaje(nivel, nombre, tiempo_segundos):
    puntajes = leer_puntajes(nivel)
    puntajes.append({
        'nombre': nombre,
        'tiempo': tiempo_segundos,
        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M'),
    })

    puntajes.sort(key=lambda x: x['tiempo'])
    puntajes = puntajes[:10]

    with open(ruta_puntajes(nivel), 'w', encoding='utf-8') as f:
        json.dump(puntajes, f, ensure_ascii=False, indent=2)


# ==========================
# BLOQUE 3: NAVEGACION Y PANTALLAS
# ==========================
def centrar_ventana():
    root.update_idletasks()
    ancho = root.winfo_width()
    alto = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (ancho // 2)
    y = (root.winfo_screenheight() // 2) - (alto // 2)
    root.geometry(f'+{x}+{y}')


def cambiar_pantalla(constructor):
    global frame_actual

    if frame_actual is not None:
        frame_actual.destroy()

    frame_actual = constructor()
    frame_actual.pack(fill='both', expand=True)
    root.after(10, centrar_ventana)


def pantalla_menu():
    frame = tk.Frame(root, bg='#2c3e50', padx=60, pady=40)

    tk.Label(
        frame,
        text='💣 BUSCAMINAS',
        font=('Arial', 36, 'bold'),
        fg='#ecf0f1',
        bg='#2c3e50',
    ).pack(pady=(0, 10))

    tk.Label(
        frame,
        text='Proyecto #2 - IS 2026',
        font=('Arial', 11),
        fg='#95a5a6',
        bg='#2c3e50',
    ).pack(pady=(0, 30))

    tk.Button(
        frame,
        text='🎮  Nueva Partida',
        font=('Arial', 13),
        width=22,
        command=lambda: cambiar_pantalla(pantalla_dificultad),
        bg='#3498db',
        fg='white',
        relief='flat',
        cursor='hand2',
        pady=9,
    ).pack(pady=6)

    tk.Button(
        frame,
        text='🏆  Puntajes Altos',
        font=('Arial', 13),
        width=22,
        command=lambda: cambiar_pantalla(pantalla_puntajes),
        bg='#3498db',
        fg='white',
        relief='flat',
        cursor='hand2',
        pady=9,
    ).pack(pady=6)

    tk.Button(
        frame,
        text='❌  Salir',
        font=('Arial', 13),
        width=22,
        command=root.quit,
        bg='#3498db',
        fg='white',
        relief='flat',
        cursor='hand2',
        pady=9,
    ).pack(pady=6)

    return frame


def pantalla_dificultad():
    frame = tk.Frame(root, bg='#2c3e50', padx=60, pady=30)

    tk.Label(
        frame,
        text='Seleccionar Dificultad',
        font=('Arial', 22, 'bold'),
        fg='#ecf0f1',
        bg='#2c3e50',
    ).pack(pady=(0, 20))

    colores = ['#27ae60', '#f39c12', '#e74c3c', '#8e44ad']
    for (nivel, (f, c, m)), color in zip(NIVELES.items(), colores):
        tk.Button(
            frame,
            text=f'{nivel}   ({f}x{c}, {m} minas)',
            font=('Arial', 12),
            width=28,
            command=lambda n=nivel: iniciar_partida(n),
            bg=color,
            fg='white',
            relief='flat',
            cursor='hand2',
            pady=7,
        ).pack(pady=5)

    tk.Frame(frame, bg='#7f8c8d', height=1).pack(fill='x', pady=15)

    tk.Button(
        frame,
        text='⚙️  Nivel Personalizado',
        font=('Arial', 12),
        width=28,
        command=pedir_personalizado,
        bg='#16a085',
        fg='white',
        relief='flat',
        cursor='hand2',
        pady=7,
    ).pack(pady=5)

    tk.Button(
        frame,
        text='← Menú Principal',
        font=('Arial', 10),
        command=lambda: cambiar_pantalla(pantalla_menu),
        bg='#7f8c8d',
        fg='white',
        relief='flat',
        cursor='hand2',
    ).pack(pady=(20, 0))

    return frame


def pedir_personalizado():
    ventana = tk.Toplevel(root)
    ventana.title('Nivel Personalizado')
    ventana.configure(bg='#2c3e50', padx=30, pady=20)
    ventana.resizable(False, False)
    ventana.grab_set()

    tk.Label(
        ventana,
        text='Configuración personalizada',
        font=('Arial', 14, 'bold'),
        fg='#ecf0f1',
        bg='#2c3e50',
    ).grid(row=0, column=0, columnspan=2, pady=(0, 15))

    tk.Label(ventana, text='Filas (4 - 30):', font=('Arial', 11), fg='#ecf0f1', bg='#2c3e50').grid(row=1, column=0, sticky='w', pady=5)
    tk.Label(ventana, text='Columnas (4 - 30):', font=('Arial', 11), fg='#ecf0f1', bg='#2c3e50').grid(row=2, column=0, sticky='w', pady=5)
    tk.Label(ventana, text='Minas:', font=('Arial', 11), fg='#ecf0f1', bg='#2c3e50').grid(row=3, column=0, sticky='w', pady=5)

    entrada_filas = tk.Entry(ventana, width=8, justify='center', font=('Arial', 11))
    entrada_columnas = tk.Entry(ventana, width=8, justify='center', font=('Arial', 11))
    entrada_minas = tk.Entry(ventana, width=8, justify='center', font=('Arial', 11))

    entrada_filas.grid(row=1, column=1, padx=(10, 0), pady=5)
    entrada_columnas.grid(row=2, column=1, padx=(10, 0), pady=5)
    entrada_minas.grid(row=3, column=1, padx=(10, 0), pady=5)

    def confirmar():
        try:
            f = int(entrada_filas.get())
            c = int(entrada_columnas.get())
            m = int(entrada_minas.get())
        except ValueError:
            messagebox.showerror('Error', 'Ingresa solo números enteros.', parent=ventana)
            return

        if not (4 <= f <= 30 and 4 <= c <= 30):
            messagebox.showerror('Error', 'Filas y columnas deben estar entre 4 y 30.', parent=ventana)
            return

        max_minas = f * c - 1
        if not (1 <= m <= max_minas):
            messagebox.showerror('Error', f'Las minas deben ser entre 1 y {max_minas}.', parent=ventana)
            return

        ventana.destroy()
        iniciar_partida('Personalizado', f, c, m)

    tk.Button(
        ventana,
        text='🎮 Iniciar Partida',
        command=confirmar,
        font=('Arial', 12),
        bg='#27ae60',
        fg='white',
        relief='flat',
        cursor='hand2',
        pady=6,
    ).grid(row=4, column=0, columnspan=2, pady=(20, 0))

    ventana.bind('<Return>', lambda _: confirmar())


def iniciar_partida(nivel, filas=None, columnas=None, minas=None):
    juego['nivel'] = nivel

    if nivel in NIVELES:
        filas, columnas, minas = NIVELES[nivel]

    juego['tablero'] = crear_tablero(filas, columnas, minas)
    juego['botones'] = {}
    juego['lbl_minas'] = None
    juego['lbl_timer'] = None
    juego['tiempo_inicio'] = 0
    juego['tiempo_transcurrido'] = 0
    juego['temporizador_activo'] = False
    juego['after_id'] = None

    cambiar_pantalla(pantalla_tablero)


def pantalla_tablero():
    frame = tk.Frame(root, bg='#2c3e50')
    tablero = juego['tablero']

    barra = tk.Frame(frame, bg='#34495e', pady=8)
    barra.pack(fill='x')

    tk.Button(
        barra,
        text='← Menú',
        font=('Arial', 10),
        command=volver_menu,
        bg='#7f8c8d',
        fg='white',
        relief='flat',
        cursor='hand2',
    ).pack(side='left', padx=10)

    juego['lbl_minas'] = tk.Label(
        barra,
        text=f"💣 {tablero['minas']}",
        font=('Arial', 14, 'bold'),
        fg='#e74c3c',
        bg='#34495e',
    )
    juego['lbl_minas'].pack(side='left', padx=15)

    tk.Label(
        barra,
        text=juego['nivel'],
        font=('Arial', 12, 'bold'),
        fg='#ecf0f1',
        bg='#34495e',
    ).pack(side='left', padx=10)

    tk.Button(
        barra,
        text='🔄 Reiniciar',
        font=('Arial', 10),
        command=reiniciar_partida,
        bg='#e67e22',
        fg='white',
        relief='flat',
        cursor='hand2',
    ).pack(side='right', padx=10)

    juego['lbl_timer'] = tk.Label(
        barra,
        text='⏱ 000',
        font=('Arial', 14, 'bold'),
        fg='#2ecc71',
        bg='#34495e',
    )
    juego['lbl_timer'].pack(side='right', padx=15)

    grilla = tk.Frame(frame, bg='#2c3e50', padx=8, pady=8)
    grilla.pack()

    max_dim = max(tablero['filas'], tablero['columnas'])
    ancho_btn = 2 if max_dim <= 20 else 1
    font_size = 10 if max_dim <= 20 else 8

    for f in range(tablero['filas']):
        for c in range(tablero['columnas']):
            btn = tk.Button(
                grilla,
                width=ancho_btn,
                height=1,
                font=('Arial', font_size, 'bold'),
                relief='raised',
                bg='#95a5a6',
                activebackground='#bdc3c7',
                cursor='hand2',
                bd=1,
            )
            btn.grid(row=f, column=c, padx=1, pady=1)
            btn.bind('<Button-1>', lambda _, fi=f, ci=c: click_izquierdo(fi, ci))
            btn.bind('<Button-3>', lambda _, fi=f, ci=c: click_derecho(fi, ci))
            juego['botones'][(f, c)] = btn

    return frame


# ==========================
# BLOQUE 4: EVENTOS DE LA PARTIDA
# ==========================
def click_izquierdo(fila, col):
    # FUNCION CLAVE 4: Conecta la UI con la logica del juego para cada jugada del usuario.
    tablero = juego['tablero']

    # Guardas de seguridad para evitar acciones invalidas.
    if tablero['juego_terminado']:
        return
    if tablero['matriz_estado'][fila][col] in ('descubierta', 'bandera'):
        return

    # El tiempo empieza cuando el usuario hace la primera accion real.
    if tablero['primera_jugada']:
        iniciar_temporizador()

    sigue = descubrir(tablero, fila, col)
    refrescar_grilla()

    if not sigue:
        revelar_minas(tablero)
        refrescar_grilla()
        detener_temporizador()
        messagebox.showwarning('💥 ¡Boom!', '¡Pisaste una mina!\nJuego terminado.')
        return

    if tablero['ganado']:
        detener_temporizador()
        registrar_victoria()


def click_derecho(fila, col):
    tablero = juego['tablero']

    if tablero['juego_terminado']:
        return
    if tablero['matriz_estado'][fila][col] == 'descubierta':
        return

    marcar_bandera(tablero, fila, col)
    refrescar_grilla()


def refrescar_grilla():
    # FUNCION CLAVE 5: Cdonvierte el estado interno del tablero en la vista visual de botones.
    tablero = juego['tablero']
    juego['lbl_minas'].config(text=f"💣 {tablero['minas'] - tablero['minas_marcadas']}")

    # Esta funcion traduce el estado logico a estado visual de botones.
    for f in range(tablero['filas']):
        for c in range(tablero['columnas']):
            estado = tablero['matriz_estado'][f][c]
            btn = juego['botones'][(f, c)]

            if estado == 'tapada':
                btn.config(text='', bg='#95a5a6', relief='raised', fg='black')
            elif estado == 'bandera':
                btn.config(text='🚩', bg='#95a5a6', relief='raised')
            else:
                if tablero['matriz_minas'][f][c]:
                    btn.config(text='💣', bg='#e74c3c', relief='sunken', fg='black')
                else:
                    n = tablero['matriz_numeros'][f][c]
                    # Si n=0 se deja vacio; si n>0 se pinta con color clasico.
                    btn.config(
                        text=str(n) if n > 0 else '',
                        bg='#d5dbdb',
                        relief='sunken',
                        fg=COLORES_NUMEROS.get(n, '#2c3e50'),
                    )


def iniciar_temporizador():
    juego['tiempo_inicio'] = time.time()
    juego['temporizador_activo'] = True
    actualizar_temporizador()


def actualizar_temporizador():
    if not juego['temporizador_activo']:
        return

    juego['tiempo_transcurrido'] = int(time.time() - juego['tiempo_inicio'])
    juego['lbl_timer'].config(text=f"⏱ {juego['tiempo_transcurrido']:03d}")
    juego['after_id'] = root.after(1000, actualizar_temporizador)


def detener_temporizador():
    juego['temporizador_activo'] = False
    if juego['after_id'] is not None:
        root.after_cancel(juego['after_id'])
        juego['after_id'] = None


def registrar_victoria():
    tiempo = juego['tiempo_transcurrido']
    nivel = juego['nivel']

    nombre = simpledialog.askstring(
        '🏆 ¡Ganaste!',
        f'¡Felicidades! Tiempo: {tiempo} segundos\n\nIngresa tu nombre para el ranking:',
        parent=root,
    )

    if nombre and nombre.strip():
        nombre = nombre.strip()
        guardar_puntaje(nivel, nombre, tiempo)
        messagebox.showinfo('¡Puntaje guardado!', f'Se guardó {nombre} - {tiempo}s en {nivel}.')
    else:
        messagebox.showinfo('¡Ganaste!', f'Tiempo: {tiempo} segundos\n(Puntaje no registrado)')


def reiniciar_partida():
    detener_temporizador()
    t = juego['tablero']
    iniciar_partida(juego['nivel'], t['filas'], t['columnas'], t['minas'])


def volver_menu():
    detener_temporizador()
    cambiar_pantalla(pantalla_menu)


# ==========================
# BLOQUE 5: PANTALLA DE PUNTAJES
# ==========================
def pantalla_puntajes():
    frame = tk.Frame(root, bg='#2c3e50', padx=20, pady=20)

    tk.Label(
        frame,
        text='🏆 Puntajes Altos',
        font=('Arial', 24, 'bold'),
        fg='#f1c40f',
        bg='#2c3e50',
    ).pack(pady=(0, 15))

    notebook = ttk.Notebook(frame)
    notebook.pack(fill='both', expand=True)

    for nivel in list(NIVELES.keys()) + ['Personalizado']:
        tab = tk.Frame(notebook, bg='#34495e', padx=10, pady=10)
        notebook.add(tab, text=f'  {nivel}  ')
        llenar_tabla_puntajes(tab, nivel)

    tk.Button(
        frame,
        text='← Menú Principal',
        font=('Arial', 11),
        command=lambda: cambiar_pantalla(pantalla_menu),
        bg='#7f8c8d',
        fg='white',
        relief='flat',
        cursor='hand2',
    ).pack(pady=(15, 0))

    return frame


def llenar_tabla_puntajes(parent, nivel):
    encabezados = ['#', 'Jugador', 'Tiempo (s)', 'Fecha']
    anchos = [4, 18, 12, 18]

    for col, (titulo, ancho) in enumerate(zip(encabezados, anchos)):
        tk.Label(
            parent,
            text=titulo,
            width=ancho,
            font=('Arial', 11, 'bold'),
            fg='#f1c40f',
            bg='#2d3436',
            anchor='center',
        ).grid(row=0, column=col, padx=2, pady=(0, 5), sticky='nsew')

    puntajes = leer_puntajes(nivel)
    if not puntajes:
        tk.Label(
            parent,
            text='Aún no hay puntajes en este nivel.',
            font=('Arial', 10),
            fg='#95a5a6',
            bg='#34495e',
        ).grid(row=1, column=0, columnspan=4, pady=20)
        return

    for i, p in enumerate(puntajes, start=1):
        color_fila = '#3d5166' if i % 2 == 0 else '#34495e'
        fila = [str(i), p['nombre'], str(p['tiempo']), p['fecha']]

        for col, (dato, ancho) in enumerate(zip(fila, anchos)):
            tk.Label(
                parent,
                text=dato,
                width=ancho,
                font=('Arial', 10),
                fg='#ecf0f1',
                bg=color_fila,
                anchor='center',
            ).grid(row=i, column=col, padx=2, pady=1, sticky='nsew')


# ==========================
# BLOQUE 6: MAIN (PUNTO DE ENTRADA)
# ==========================
def main():
    global root

    asegurar_directorio_puntajes()

    root = tk.Tk()
    root.title('💣 Buscaminas')
    root.resizable(False, False)
    root.configure(bg='#2c3e50')

    cambiar_pantalla(pantalla_menu)
    root.after(10, centrar_ventana)
    root.mainloop()


if __name__ == '__main__':
    main()
