# 📊 ESTRUCTURAS DE DATOS - Referencia Rápida

## Constantes Globales

```python
NIVELES = {'Fácil': (8,8,10), 'Medio': (10,10,15), 'Difícil': (12,12,25), 'Experto': (15,15,40)}
COLORES_NUMEROS = {1:'#0000FF', 2:'#008000', 3:'#FF0000', ..., 8:'#808080'}
DIRECTORIO_PUNTAJES = 'puntajes'
```

---

## Variable Global de Estado: `juego`

```python
juego = {
    'nivel': str,                   # Ej: 'Fácil', 'Personalizado'
    'tablero': dict,                # Ver estructura tablero (abajo)
    'botones': dict,                # {(fila, col): tk.Button}
    'lbl_minas': tk.Label,          # Label contador de minas
    'lbl_timer': tk.Label,          # Label del tiempo
    'tiempo_inicio': float,         # time.time() cuando empezó
    'tiempo_transcurrido': int,     # Segundos jugados
    'temporizador_activo': bool,    # True si cronómetro corre
    'after_id': int,                # ID para cancelar callback
}
```

---

## Estructura Principal: `tablero`

Creada por `crear_tablero(filas, columnas, minas)`:

```python
tablero = {
    # Dimensiones
    'filas': int,                   # Ej: 8
    'columnas': int,                # Ej: 8
    'minas': int,                   # Ej: 10
    
    # MATRICES PRINCIPALES (3D: filas × columnas)
    'matriz_minas': [[bool]],       # True si hay mina en (f,c)
    'matriz_numeros': [[int]],      # 0-8 minas adyacentes, -1 si es mina
    'matriz_estado': [[str]],       # 'tapada'/'descubierta'/'bandera'
    
    # CONTROL DE FLUJO
    'primera_jugada': bool,         # True hasta el primer click
    'juego_terminado': bool,        # True si ganó o perdió
    'ganado': bool,                 # True si descubrió todo
    
    # CONTADORES
    'minas_marcadas': int,          # Banderas colocadas
    'celdas_descubiertas': int,     # Celdas reveladas
    'celdas_sin_mina': int,         # Meta para ganar
}
```

### Relación entre Matrices

Para cada celda (f, c):
- Si `matriz_minas[f][c] == True` → es una mina
- Entonces `matriz_numeros[f][c] == -1` (marca especial)
- Si `matriz_minas[f][c] == False` → es segura
- Entonces `matriz_numeros[f][c]` = cantidad de minas adyacentes (0-8)

Estados visuales en `matriz_estado[f][c]`:
- `'tapada'` → botón gris sin descubrir
- `'descubierta'` → botón beige con número/vacío o 💣
- `'bandera'` → botón gris con 🚩

---

## Estructura de Puntajess

Leída desde `puntajes/{nivel}.json`:

```python
puntajes = [
    {
        'nombre': 'Ana',                    # str: nombre jugador
        'tiempo': 45,                       # int: segundos
        'fecha': '2026-01-15 10:30'        # str: YYYY-MM-DD HH:MM
    },
    {...},
    # Máximo 10 elementos, ordenados por tiempo ascendente
]
```

---

## Diccionarios de Configuraciones

### NIVELES (Tuplas de configuración)
```python
('filas', 'columnas', 'minas')
# Ejemplos:
(8, 8, 10)      # Fácil
(10, 10, 15)    # Medio
(12, 12, 25)    # Difícil
(15, 15, 40)    # Experto
```

### COLORES_NUMEROS (Mapeo número → color hex)
```python
{
    1: '#0000FF',   # Azul
    2: '#008000',   # Verde
    3: '#FF0000',   # Rojo
    4: '#000080',   # Azul oscuro
    5: '#800000',   # Marrón
    6: '#008080',   # Cian
    7: '#000000',   # Negro
    8: '#808080',   # Gris
}
```

---

## Diccionarios Locales Temporales

### En `pedir_personalizado()`: Entradas de usuario
```python
entrada_filas = tk.Entry(...)
entrada_columnas = tk.Entry(...)
entrada_minas = tk.Entry(...)

# Acceso: entrada_filas.get() → str, convierte a int
```

### En `llenar_tabla_puntajes()`: Visualización de tabla
```python
encabezados = ['#', 'Jugador', 'Tiempo (s)', 'Fecha']
anchos = [4, 18, 12, 18]
fila = [str(i), p['nombre'], str(p['tiempo']), p['fecha']]
```

---

## Tipos de Datos Utilizados

| Tipo | Uso | Ejemplo |
|------|-----|---------|
| `dict` | Estado de juego, tablero, puntaje | `{'nivel': 'Fácil', ...}` |
| `list` | Matrices, puntajes, botones | `[[False, True], [True, False]]` |
| `str` | Estados, nombres, rutas | `'tapada'`, `'Ana'` |
| `bool` | Flags, minas | `True` si hay mina |
| `int` | Dimensiones, tiempos, contadores | `8`, `45`, `10` |
| `float` | Timestamp | `1703001234.567` |
| `tk.Button` | Botones de celda | `btn.config(...)` |
| `tk.Label` | Etiquetas (contador, timer) | `lbl_minas.config(text=...)` |

---

## Patrones de Acceso

### Acceder a una mina
```python
tablero['matriz_minas'][fila][columna]  # bool
```

### Acceder al número de minas adyacentes
```python
tablero['matriz_numeros'][fila][columna]  # 0-8 o -1 si es mina
```

### Acceder al estado visual
```python
tablero['matriz_estado'][fila][columna]  # 'tapada'/'descubierta'/'bandera'
```

### Acceder a un botón específico
```python
juego['botones'][(fila, columna)]  # tk.Button
```

### Leer puntajes de archivo
```python
puntajes = leer_puntajes('Fácil')  # list[dict]
```

### Guardar nuevo puntaje
```python
guardar_puntaje('Fácil', 'Ana', 45)  # Escribe JSON
```

---

## Flujo de Transformación de Datos

```
crear_tablero()
  ↓
juego['tablero'] = tablero_dict
  ↓
click_izquierdo(f, c)
  ↓
descubrir(tablero, f, c)
  ↓
expandir(tablero, f, c)  [modifica matriz_estado]
  ↓
refrescar_grilla()  [lee matriz_estado, actualiza tk.Button]
  ↓
botón visual actualizado en pantalla
```

---

## Manejo de Archivos

### JSON de puntajes
- **Lectura:** `leer_puntajes(nivel)` → list[dict]
- **Escritura:** `guardar_puntaje(nivel, nombre, tiempo)` → JSON file
- **Ruta:** `puntajes/puntajes_{nivel}.json`
- **Formato:** UTF-8, indentado 2 espacios

### Directorio
- **Creación:** `asegurar_directorio_puntajes()` al inicio
- **Ubicación:** `BuscaMinas/puntajes/`

---

## Tamaños Típicos

| Campo | Min | Max | Típico |
|-------|-----|-----|--------|
| Filas | 4 | 30 | 8-15 |
| Columnas | 4 | 30 | 8-15 |
| Minas | 1 | filas×columnas-1 | 10-40 |
| Puntajes guardados | 0 | 10 | Variable |
| Nombre jugador | 1 | sin límite | 3-20 |
| Tiempo partida | 5 | 3600+ | 30-300 |
