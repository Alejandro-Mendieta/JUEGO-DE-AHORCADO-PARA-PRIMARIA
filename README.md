
# 🎮 **Juego del Ahorcado**

<img width="901" height="636" alt="image" src="https://github.com/Alejandro-Mendieta/JUEGO-DE-AHORCADO-PARA-PRIMARIA/blob/main/assets/FOTOS/foto1.jpg?raw=true" />
<img width="905" height="633" alt="image" src="https://github.com/Alejandro-Mendieta/JUEGO-DE-AHORCADO-PARA-PRIMARIA/blob/main/assets/FOTOS/foto2.jpg?raw=true" />

Un juego del ahorcado **interactivo** desarrollado en **Python con Pygame**, que incluye múltiples dificultades, sistema de puntuación, efectos visuales y sonoros.
Perfecto para aprender, jugar y mejorar tus habilidades de lógica y programación 🧠⚡

---

## ✨ **Características Principales**

### 🎯 **Niveles de Dificultad**

| Dificultad    | Intentos | Recompensa      | Desbloqueo                 |
| ------------- | -------- | --------------- | -------------------------- |
| 🟢 **EASY**   | 8        | Puntos normales | Disponible desde el inicio |
| 🔵 **DARK**   | 6        | +50% puntos     | Requiere 50 puntos         |
| 🔴 **EXTREM** | 4        | +100% puntos    | Requiere 50 puntos         |

---

### 🎨 **Interfaz y Jugabilidad**

* Interfaz visual **atractiva** con animaciones y efectos de partículas.
* **Sistema de puntuación progresivo** con recompensas por dificultad.
* Más de **300 palabras** clasificadas por categorías.
* **Pistas descriptivas** para cada palabra.
* Efectos visuales del ahorcado que evolucionan con los errores.
* **Teclado virtual interactivo** y soporte para teclado físico.
* Sistema de **desbloqueo de niveles** por puntaje.

---

### 🎵 **Sistema de Audio**

* Música de fondo ambiental inmersiva.
* Efectos de sonido para aciertos, errores y fin del juego.
* Gestión de audio inteligente: pausa automática durante efectos.

---

## 🚀 **Instalación y Ejecución**

### 🔧 **Requisitos Previos**

* Python **3.7 o superior**
* Librería **Pygame**

### 💻 **Instalación**

```bash
pip install pygame
```

### ▶️ **Ejecución**

```bash
python ahorcado.py
```

---

## 🗂️ **Estructura del Proyecto**

```text
juego_ahorcado/
├── ahorcado.py              # Archivo principal del juego
├── assets/
│   ├── FOTOS/
│   │   ├── fondo.png        # Imagen de fondo
│   │   └── logo.ico         # Ícono del juego
│   ├── MUSICA/
│   │   ├── Musica-De-Fondo.wav
│   │   ├── correcto.wav
│   │   ├── incorrecto.wav
│   │   ├── ganador.wav
│   │   └── perdedor.wav
│   └── STYLE/
│       ├── Montserrat-Regular.ttf
│       └── Montserrat-Bold.ttf
└── README.md
```

---

## 🕹️ **Cómo Jugar**

### 🎮 **Controles**

* 🖱️ **Ratón:** Haz clic en las letras del teclado virtual.
* ⌨️ **Teclado:** Presiona las teclas correspondientes.
* ⎋ **ESC:** Pausa / reanuda el juego.
* ↩️ **ENTER:** Reinicia al finalizar una partida.

### ⚙️ **Mecánica**

1. Elige una dificultad desde el menú principal.
2. Adivina la palabra letra por letra.
3. Usa las pistas si lo necesitas.
4. Gana puntos por cada palabra adivinada.
5. Desbloquea nuevos niveles al alcanzar 50 puntos.
6. ¡Evita que el ahorcado se complete para ganar! 🪢

---

## 💯 **Sistema de Puntuación**

| Dificultad | Victoria | Derrota |
| ---------- | -------- | ------- |
| EASY       | +10 pts  | -2 pts  |
| DARK       | +15 pts  | -1 pt   |
| EXTREM     | +20 pts  | 0 pts   |

---

## 🛠️ **Desarrollo y Personalización**

### 🔹 **Estructura del Código**

* **Inicialización:** Carga de Pygame y recursos.
* **Sistema de Sonido:** Música y efectos.
* **Dificultades:** Lógica y desbloqueos.
* **Partículas:** Efectos visuales animados.
* **Lógica del Juego:** Mecánica del ahorcado.
* **Interfaz:** Menús, botones, estados del juego.
* **Bucle Principal:** Control de eventos.

### 🎨 **Personaliza fácilmente:**

* **Palabras:** Edita el diccionario en el código.
* **Dificultades:** Ajusta `CONFIG_DIFICULTAD`.
* **Puntos de desbloqueo:** Modifica `PUNTOS_PARA_DESBLOQUEAR`.
* **Sonidos:** Cambia los archivos en `assets/MUSICA/`.

---

## 🧩 **Solución de Problemas**

| Error                                  | Causa                 | Solución                                  |
| -------------------------------------- | --------------------- | ----------------------------------------- |
| ❌ `No se pudo cargar [recurso]`        | Ruta incorrecta       | Verifica las carpetas y nombres           |
| ⚠️ `pygame.error: Unable to open file` | Archivo no encontrado | Ejecuta el juego desde el directorio raíz |
| 🐢 El juego va lento                   | Recursos limitados    | Cierra apps o baja la resolución          |

---

## 📝 **Licencia**

Este proyecto es de **uso educativo y libre**.
Puedes **modificarlo, mejorarlo y distribuirlo** libremente.

---

## 👨‍💻 **Autor**

**-Desarrollado como proyecto educativo en **Python + Pygame**.
**-Desarrollado por ALEJANDRO MENDIETA**
**-Hecho con 💙 para fomentar el aprendizaje y la creatividad.**

> 🎯 *“Cada error te acerca más a la palabra correcta.”*

