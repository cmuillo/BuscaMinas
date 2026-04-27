# 💣 Buscaminas — Proyecto #2

> **Curso:** Ingeniería de Sistemas 2026  
> **Proyecto:** #2 — Valor 25%  
> **Lenguaje:** Python 3  
> **Interfaz:** Tkinter  
> **Entrega:** 22 de mayo de 2026

---

## Descripción

Implementación completa del clásico juego **Buscaminas** en Python con interfaz gráfica Tkinter. El jugador descubre celdas en un tablero ocultando minas, guiándose por los números que indican cuántas minas rodean cada celda. El objetivo es revelar todas las celdas sin minas sin detonar ninguna.

---

## Capturas de pantalla

> Las capturas se agregarán tras la primera ejecución del programa.

---

## Requisitos del sistema

- Python 3.8 o superior
- Módulo `tkinter` (incluido por defecto en la mayoría de instalaciones de Python)
- No requiere dependencias externas adicionales

---

## Instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/cmuillo/BuscaMinas.git
cd BuscaMinas

# 2. Ejecutar el juego directamente
py buscaminas.py
```

---

## Estructura del proyecto

```
BuscaMinas/
├── buscaminas.py        # Código fuente principal del juego
├── README.md            # Este archivo
└── puntajes/            # Directorio creado automáticamente al ganar
    ├── puntajes_fácil.json
    ├── puntajes_medio.json
    ├── puntajes_difícil.json
    ├── puntajes_experto.json
    └── puntajes_personalizado.json
```

---

## Niveles de dificultad

| Nivel       | Filas | Columnas | Minas |
|-------------|------:|:--------:|------:|
| Fácil       |   8   |    8     |   10  |
| Medio       |  10   |   10     |   15  |
| Difícil     |  12   |   12     |   25  |
| Experto     |  15   |   15     |   40  |
| Personalizado | 4–30 | 4–30   | 1–(f×c−1) |

---

## Funcionalidades implementadas

| # | Funcionalidad | Estado |
|---|---------------|--------|
| 1 | Menú principal con 3 opciones | ✅ |
| 2 | Selección de 4 niveles predefinidos | ✅ |
| 3 | Nivel personalizado con validación | ✅ |
| 4 | Generación aleatoria del tablero (matrices) | ✅ |
| 5 | Interfaz gráfica con Tkinter | ✅ |
| 6 | Temporizador en tiempo real | ✅ |
| 7 | Descubrir celdas y expansión automática (flood fill) | ✅ |
| 8 | Colocar/quitar banderas (click derecho) | ✅ |
| 9 | Detección de victoria y derrota | ✅ |
| 10 | Reiniciar partida / volver al menú | ✅ |
| 11 | Registro de top 10 puntajes por nivel (JSON) | ✅ |
| 12 | Consultar puntajes altos desde la interfaz | ✅ |

---

## Arquitectura del código

### Clases principales

```
App (tk.Tk)                   ← Ventana raíz / controlador de navegación
│
├── MenuPrincipal (Frame)     ← Pantalla de inicio
├── SeleccionDificultad (Frame) ← Elegir nivel o personalizar
├── TableroJuego (Frame)      ← Tablero activo con timer y controles
└── PuntajesAltos (Frame)     ← Rankings por nivel (ttk.Notebook)

Tablero                       ← Lógica pura del juego (sin GUI)
│   matriz_minas  bool[][]    ← True si hay mina
│   matriz_numeros int[][]    ← Número de minas vecinas (−1 = mina)
│   matriz_estado str[][]     ← 'tapada' | 'descubierta' | 'bandera'
│
├── colocar_minas()           ← random.sample para distribución aleatoria
├── calcular_numeros()        ← cuenta minas en 8 vecinos por celda
├── descubrir_celda()         ← punto de entrada de cada click
├── _expandir()               ← flood fill recursivo en celdas vacías
├── marcar_bandera()          ← toggle bandera en celda tapada
└── revelar_todo()            ← muestra minas al perder

GestorPuntajes                ← Lectura y escritura de archivos JSON
├── leer_puntajes(nivel)      ← retorna lista del archivo JSON
└── guardar_puntaje(nivel, nombre, tiempo) ← mantiene top 10
```

### Estructuras de datos usadas

| Estructura | Uso en el juego |
|------------|-----------------|
| `list[list[bool]]` | `matriz_minas` — posición de cada mina |
| `list[list[int]]`  | `matriz_numeros` — pistas numéricas |
| `list[list[str]]`  | `matriz_estado` — estado visual de cada celda |
| `dict[(int,int) → Button]` | Acceso O(1) a cada botón Tkinter |
| `dict[str → tuple]` | `NIVELES` — configuración por nivel |
| `list[dict]` | Puntajes leídos/escritos en JSON |

---

## Cómo jugar

1. **Click izquierdo** → Descubre una celda
2. **Click derecho** → Coloca o quita una 🚩 bandera
3. **Los números** indican cuántas minas hay en las 8 celdas alrededor
4. **Expansión automática** → Si una celda tiene 0 minas vecinas, se expanden todas las adyacentes automáticamente
5. **Ganar** → Revelar todas las celdas sin minas
6. **Perder** → Hacer click en una mina 💥

---

## Manejo de archivos

Los puntajes se almacenan en archivos **JSON** dentro de la carpeta `puntajes/`, uno por nivel de dificultad. El formato es:

```json
[
  {
    "nombre": "Ana García",
    "tiempo": 45,
    "fecha": "2026-04-27 14:30"
  },
  {
    "nombre": "Luis Rojas",
    "tiempo": 78,
    "fecha": "2026-04-27 15:00"
  }
]
```

- Ordenados de menor a mayor tiempo (menor tiempo = mejor resultado)
- Se conservan únicamente los **10 mejores** registros por nivel
- El archivo se crea automáticamente al ganar la primera partida

---

## Rúbrica de evaluación

| Criterio | Puntos |
|----------|-------:|
| Uso correcto de matrices | 10 pts |
| Generación aleatoria del tablero | 20 pts |
| Funcionamiento general (ganar/perder, descubrir, timer) | 25 pts |
| Nivel personalizado | 10 pts |
| Registro y consulta de puntajes + archivos | 15 pts |
| Navegación, orden y usabilidad | 10 pts |
| Documentación interna y externa | 10 pts |
| **TOTAL** | **100 pts** |

---

## Registro de cambios

| Fecha | Descripción |
|-------|-------------|
| 2026-04-27 | Creación inicial del proyecto |
| 2026-04-27 | Implementación completa: tablero, GUI, timer, puntajes, archivos |

---

## Autor

- **Desarrollador:** cmuillo  
- **Repositorio:** [github.com/cmuillo/BuscaMinas](https://github.com/cmuillo/BuscaMinas)
