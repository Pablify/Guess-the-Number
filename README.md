# 🎮 Guess the Number

El script **`guessnumber.py`** genera un número entero secreto y el jugador debe descubrirlo en un número limitado de intentos. Después de cada intento, el programa ofrece pistas indicando si el número secreto es mayor o menor que el elegido. Opcionalmente, pueden activarse pistas de **proximidad** (“caliente/frío”), así como un sistema de **puntuación** que guarda récords locales.

---

## 🚀 Características principales

- 🎲 Tres niveles de dificultad (`easy`, `normal`, `hard`).
- 🔢 Definición personalizada de rango y número de intentos.
- 🔥 Pistas opcionales de proximidad (“caliente/frío”).
- 🏆 Sistema de puntuación con guardado automático del récord en un archivo local.
- 🌍 Interfaz multilenguaje: ruso (`ru`) e inglés (`en`).
- 🎨 Soporte para salida en color ANSI (con opción de desactivar).
- ⚙️ Semilla opcional para reproducir partidas (`--seed`).
- 🖥️ 100% en un único archivo `.py`, sin dependencias externas.

---

## 📂 Estructura del proyecto

```

Guess-the-Number/
│
├── guessnumber.py    # Script principal del juego
├── LICENSE           # Licencia MIT
└── README.md         # Este archivo

````

---

## 🛠️ Requisitos

- Python **3.9** o superior.
- Sistema operativo: Windows, macOS o Linux.
- Terminal/Consola estándar.

---

## ▶️ Uso

Ejecuta el script directamente con Python:

```bash
python guessnumber.py
````

### Argumentos disponibles

| Opción                            | Descripción                                           |
| --------------------------------- | ----------------------------------------------------- |
| `--difficulty {easy,normal,hard}` | Define la dificultad (por defecto: `normal`).         |
| `--min INT --max INT`             | Establece el rango de números.                        |
| `--attempts INT`                  | Número de intentos fijo (sobrescribe la dificultad).  |
| `--proximity`                     | Activa pistas de proximidad.                          |
| `--seed INT`                      | Fija la semilla para generar siempre el mismo número. |
| `--no-score`                      | Desactiva el sistema de puntuación.                   |
| `--lang {ru,en}`                  | Idioma de la interfaz (por defecto: `ru`).            |
| `--no-color`                      | Desactiva los colores en la salida.                   |
| `--quiet`                         | Modo silencioso: solo pistas y resultado final.       |
| `--version`                       | Muestra la versión y termina.                         |

### Ejemplos de ejecución

```bash
# Juego en dificultad fácil
python guessnumber.py --difficulty easy

# Rango personalizado y 7 intentos
python guessnumber.py --min 1 --max 200 --attempts 7

# Con pistas de proximidad y en inglés
python guessnumber.py --proximity --lang en
```

---

## 📖 Reglas del juego

1. El programa genera un número secreto dentro del rango especificado.
2. El jugador debe introducir un número en cada intento.
3. Tras cada intento válido:

   * Se indica si el número secreto es **mayor** o **menor**.
   * Si está activada la opción `--proximity`, se añade una pista de proximidad.
4. El juego finaliza cuando:

   * El jugador acierta el número secreto.
   * Se agotan los intentos disponibles.
5. Al terminar, se ofrece la posibilidad de jugar otra ronda.

---

## 📜 Licencia

Este proyecto está bajo la licencia [MIT](./LICENSE). Eres libre de usar, modificar y distribuir este software, siempre que conserves la nota de copyright.
