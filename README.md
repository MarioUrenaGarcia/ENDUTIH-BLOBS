# ENDUTIH 2024 — Visualización Interactiva

Visualización web interactiva de los datos del **ENDUTIH 2016–2024** (Encuesta Nacional sobre Disponibilidad y Uso de Tecnologías de la Información en los Hogares, INEGI México).

**Demo en vivo:** [GitHub Pages](https://mariourenagarcia.github.io/ENDUTIH-BLOBS/)

---

## Descripción

La aplicación presenta el uso de internet en México para la población de 6 años en adelante, segmentada por **Generación**, **Grupo de Edad** y **Sexo**, a lo largo de 9 años (2016–2024), con énfasis en la **Generación Alpha**.

Desarrollada como herramienta de exposición interactiva para kiosco o pantalla de presentación.

---

## Funcionalidades

### Escena 3D — Blobs

- 150 figuras 3D animadas (blobs con ojos) renderizadas con **Three.js r158**
- Cada figura representa un segmento de la población
- Teal = usa internet · Gris = no usa internet
- Agrupación por Generación / Grupo de Edad / Sexo / Sin agrupar
- Año seleccionable (2016–2024) con etiquetas flotantes de porcentaje por grupo
- Botón Auto para avanzar años automáticamente
- Tooltip al pasar el cursor (o tocar en móvil) sobre cualquier blob

### Panel de Gráficas (4 slides)

| Slide | Contenido |
| ----- | --------- |
| 1 | Líneas animadas: % uso de internet por generación 2016–2024 |
| 2 | Barras: ¿Para qué usa internet? · Gen Alpha 2024 |
| 3 | Barras: Equipo de cómputo más utilizado · Gen Alpha 2024 |
| 4 | Barras: ¿Cómo aprendió a usar computadora? · Gen Alpha 2024 |

Marcadores históricos en la gráfica de líneas: **COVID-19 (2020)**, **Regreso a la normalidad (2022)**, **ChatGPT (2023)**.

### Panel Alpha (3 slides)

Panel exclusivo para la Generación Alpha con figuras blob 2D en lugar de barras. Cada figura representa el **5%** de la Generación Alpha.

| Slide | Contenido |
| ----- | --------- |
| 1 | Para qué usa internet (6 categorías con íconos) |
| 2 | Equipo de cómputo más utilizado (3 categorías) |
| 3 | ¿Cómo aprendió a usar la computadora? (4 categorías) |

Las figuras se animan de izquierda a derecha al entrar al slide. Incluye Auto propio para avanzar slides automáticamente.

### Modo Explorar (kiosco automático)

Ciclo infinito sin intervención del usuario:

1. Blobs — Generación (2016 a 2024)
2. Blobs — Grupo de Edad (2016 a 2024)
3. Blobs — Sexo (2016 a 2024)
4. Gráficas — Slide 1 (líneas, 10.5 s) → Slides 2–4 (5.5 s c/u)
5. Alpha — Slides 1–3 (5.5 s c/u)
6. Regresa al inicio y repite

Iniciar el modo Explorar desde cualquier panel continúa el ciclo desde la posición actual. Detener el modo deja al usuario en el panel y slide donde se interrumpió. El botón de siguiente fase permite avanzar manualmente entre etapas.

---

## Datos

Valores obtenidos del ENDUTIH publicado por INEGI. Todos los datos están embebidos directamente en `index.html`; no se requiere servidor ni conexión a ninguna API.

**Uso de internet (%) por generación — años seleccionados:**

| Generación   | 2016 | 2018 | 2020 | 2022 | 2024 |
| ------------ | ---- | ---- | ---- | ---- | ---- |
| Silenciosa   | 10.8 | 10.0 | 13.2 | 18.3 | 27.8 |
| Baby Boomers | 28.7 | 34.9 | 41.7 | 48.5 | 54.6 |
| Gen X        | 54.7 | 63.1 | 69.7 | 77.7 | 81.6 |
| Millennials  | 76.8 | 81.4 | 84.6 | 90.9 | 93.6 |
| Gen Z        | 72.1 | 77.0 | 85.6 | 91.9 | 96.1 |
| Alpha        | —    | —    | 58.4 | 68.7 | 79.7 |

---

## Tecnologías

- **Three.js r158** (local, sin CDN) — escena 3D
- **SVG + requestAnimationFrame** — gráfica de líneas animada
- **HTML / CSS / JS** — sin frameworks ni bundlers
- Archivo único: `index.html` (~1,600 líneas)

---

## Compatibilidad

- Escritorio: Chrome, Firefox, Edge, Safari
- Tablet
- Móvil (responsive para pantallas de hasta 640 px): cámara 3D ajustada automáticamente en modo retrato, scroll horizontal en slides con múltiples categorías, soporte táctil para información de blobs

---

## Uso de inteligencia artificial

Este proyecto fue desarrollado con asistencia de **Claude (Anthropic)** como herramienta de apoyo durante el proceso de desarrollo. El uso de IA se limitó a las siguientes etapas:

- **Generación y refinamiento de código:** implementación de la escena Three.js, lógica de animación de blobs, sistema de slides, gráfica de líneas animada y paneles interactivos.
- **Depuración:** identificación y corrección de errores en el ciclo de exploración, posicionamiento de etiquetas 3D y sincronización de estados entre paneles.
- **Diseño responsive:** adaptación del layout para dispositivos móviles, incluyendo ajuste de cámara por orientación y soporte táctil.
- **Documentación:** redacción de este README.

La definición del alcance, la selección de datos, las decisiones de diseño y la revisión del producto final fueron realizadas por el equipo de desarrollo.

---

## Uso local

```bash
git clone https://github.com/MarioUrenaGarcia/ENDUTIH2024_WEB.git
cd ENDUTIH2024_WEB
open index.html
```

> `three.min.js` debe estar en el mismo directorio que `index.html`.

---

## Estructura

```
ENDUTIH2024_WEB/
├── index.html        # Aplicación completa (Three.js + gráficas + lógica)
├── three.min.js      # Three.js r158 (local)
└── README.md
```

---

## Fuente de datos

INEGI — Encuesta Nacional sobre Disponibilidad y Uso de Tecnologías de la Información en los Hogares (ENDUTIH) 2016–2024
https://www.inegi.org.mx/programas/dutih/
