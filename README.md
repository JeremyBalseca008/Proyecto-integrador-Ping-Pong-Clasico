# Ping Pong clásico

Proyecto integrador de primer nivel · Lógica de Programación · UIDE · Paralelo C

Videojuego de Ping Pong para dos jugadores desarrollado en Python. Cada jugador controla una paleta y debe evitar que la pelota salga por su lado de la cancha. Gana quien alcanza cinco puntos. El diseño inicial por turnos evolucionó hacia una partida gráfica en tiempo real mediante Pygame y una arquitectura cliente-servidor TCP en red LAN.

## Integrantes

- Christopher Torres
- Gabriel Condor
- Jeremy Balseca

## Cómo ejecutarlo

Requiere Python 3, pip y un entorno gráfico. Desde la carpeta del repositorio, instalar Pygame y ejecutar el menú:

```bash
python -m pip install -r requirements.txt
python juego.py
```

Para ejecutar por separado el archivo de lógica:

```bash
python game_logic.py
```

En la versión actual, este segundo comando carga las definiciones de la clase Juego y las funciones auxiliares, pero no inicia una demostración interactiva de DF2 y DF3. La lógica se utiliza al ejecutar una partida desde el menú.

En Ubuntu se puede utilizar `python3` en lugar de `python`. Si el sistema requiere un entorno virtual, crearlo con `python3 -m venv .venv`, activarlo con `source .venv/bin/activate` e instalar las dependencias.

### Cómo jugar

1. Jugador 1: ejecutar `python juego.py`, seleccionar **Crear partida** y elegir el puerto (5000 por defecto).
2. Jugador 2: ejecutar `python juego.py`, seleccionar **Unirse a una partida** e introducir la dirección IPv4 del servidor y el mismo puerto.
3. Ambos jugadores pueden utilizar W o flecha arriba para subir la paleta, y S o flecha abajo para bajarla.

Los equipos deben tener conectividad entre sí. La IP del servidor se puede consultar con `ipconfig` en Windows o `hostname -I` en Ubuntu. Para una prueba en un mismo equipo, abrir dos terminales y utilizar la IP `127.0.0.1`. Cada ventana recibe las entradas del teclado cuando tiene el foco; no es un modo local con teclado compartido.

## Estructura del repositorio

| Archivo | Qué hace | Estado |
|---|---|---|
| [`juego.py`](juego.py) | Menú que se repite hasta Salir, valida la IP y el puerto, permite crear o unirse a una partida. | Implementado |
| [`game_logic.py`](game_logic.py) | Movimiento, límites de las paletas, rebotes, marcador y fin de la partida (DF2 y DF3 adaptados). | Implementado para el juego gráfico; demostración independiente de Fase 3 no incluida |
| [`server.py`](server.py) | Servidor TCP: acepta dos conexiones, recibe movimientos y sincroniza la partida. | Implementado (avance de Fase 4) |
| [`client.py`](client.py) | Cliente TCP: lee el teclado, recibe el estado y dibuja la partida mediante Pygame. | Implementado (avance de Fase 4) |
| [`diseno/`](diseno/) | Diagramas RAPTOR y arquitectura de la Fase 2. | Subido |
| [`requirements.txt`](requirements.txt) | Dependencia de Pygame. | Incluido |
| [`LICENSE`](LICENSE) | Licencia MIT. | Incluido |
| `.gitignore` | Excluye archivos temporales y otros archivos generados durante el desarrollo. | Incluido |
| `README.md` | Documentación y créditos del proyecto. | Incluido |

### Diagramas de la Fase 2

- [DF1_partida.rap](diseno/DF1_partida.rap)
- [DF2_validacion.rap](diseno/DF2_validacion.rap)
- [DF3_fin.rap](diseno/DF3_fin.rap)
- [arquitectura.drawio](diseno/arquitectura.drawio)

## Del diseño al código

| Diagrama de la Fase 2 | Archivo y líneas | Qué cambió al traducirlo |
|---|---|---|
| DF1 Partida completa (solo el menú) | [`juego.py`, líneas 35–70](juego.py#L35-L70) | El Loop de RAPTOR pasó a un while y las decisiones a if, elif y else. El menú Jugar/Salir se amplió a Crear partida, Unirse y Salir. |
| DF2 Validación de la jugada | [`game_logic.py`, líneas 38–53](game_logic.py#L38-L53); [`server.py`, líneas 7–22](server.py#L7-L22); [`client.py`, líneas 54–64](client.py#L54-L64) | Las entradas I, C y D del prototipo se sustituyeron por movimientos del teclado. Las condiciones if mantienen las paletas dentro de la cancha y el servidor interpreta los mensajes U, D y N. No se conserva el ciclo independiente de validación por formato y reglas del DF2 original. |
| DF3 Fin de la partida | [`game_logic.py`, línea 10](game_logic.py#L10) y [líneas 97–104](game_logic.py#L97-L104); [`client.py`, líneas 76–86](client.py#L76-L86) | Las decisiones del diagrama se traducen a condiciones if sobre el marcador. Se cambió el límite de dos a cinco puntos. El juego termina con la victoria de un jugador y continúa si ninguno alcanza cinco; no existe una condición explícita de empate en la implementación actual. |

### Evolución del diseño

Los diagramas originales se conservan como evidencia de la Fase 2. El diseño utilizaba turnos, entradas I, C y D y el puerto 5555. La versión actual utiliza movimiento continuo, mensajes U (subir), D (bajar) y N (sin movimiento), y el puerto 5000 por defecto, que se puede configurar.

El ciclo completo de la partida se encuentra en [`server.py`, líneas 49–62](server.py#L49-L62), y el movimiento, rebote y puntuación en [`game_logic.py`, líneas 55–95](game_logic.py#L55-L95). El servidor actualiza el estado y los clientes representan la cancha y el marcador en una ventana de 800 × 500 píxeles.

**Alcance de Fase 3:** el repositorio contiene avances de Fase 4, como la partida completa, la interfaz gráfica y los sockets. Para cumplir literalmente con la consigna de Fase 3, falta la demostración independiente de DF2 que repite una jugada inválida y la de DF3 que distingue los cuatro resultados, incluido el empate. El juego gráfico actual se conserva sin modificaciones.

### Casos de verificación

| Caso | Comportamiento esperado según el código |
|---|---|
| Opción 9 en el menú | Mensaje de error y repetición del menú. |
| Puerto fuera de 1024–65535 | Se vuelve a solicitar. |
| Paleta en el borde | Permanece dentro de la cancha. |
| Marcador 5–3 | Gana el Jugador 1. |
| Marcador 3–5 | Gana el Jugador 2. |
| Marcador 4–4 | La partida continúa. |
| Marcador artificial 5–5 | El código actual asigna la victoria a J2; no hay rama de empate. |
| Dos clientes conectados | Reciben el estado enviado por el servidor. |

La revisión anterior registró comprobaciones de lógica y conexión TCP local sin interfaz gráfica. Estos casos documentan el comportamiento esperado y no acreditan por sí solos una prueba gráfica de Pygame ni una prueba entre dos equipos físicos de la LAN.

## Video explicativo

[Ver video explicativo del equipo](https://mailinternacionaledu-my.sharepoint.com/:v:/g/personal/jebalsecaba_uide_edu_ec/IQDjuqG1WgX_T4zvCW53mOB4AZ_jf8wegpp35otjB2dxw2U?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=AeDoNX)

La consigna establece un máximo de cinco minutos y solicita explicar la traducción de los diagramas, ejecutar el menú, mostrar una jugada inválida y demostrar el fin de la partida. La duración, el contenido y los permisos de acceso del video deben comprobarse con el archivo original.

## Licencia

Este proyecto se distribuye bajo la licencia de código abierto MIT. El texto completo se encuentra en el archivo [`LICENSE`](LICENSE). Los recursos externos conservan sus respectivas licencias.

## Declaración de autoría

El proyecto corresponde a Christopher Torres, Gabriel Condor y Jeremy Balseca. Los integrantes aportaron el diseño de la Fase 2, los archivos de código fuente para revisión, los diagramas y el video explicativo. El repositorio incorpora apoyo de herramientas de inteligencia artificial, según se detalla en los créditos. Los recursos de terceros se identifican en la sección siguiente.

La declaración distingue las aportaciones documentadas del equipo de la asistencia recibida; no atribuye contribuciones individuales ni cambios que no estén confirmados.

## Créditos

| Recurso (código, librería, imagen…) | Autor o fuente | Dónde se usa | Licencia |
|---|---|---|---|
| Python y módulos estándar (socket, threading y time) | [Python Software Foundation](https://www.python.org/) | `juego.py`, `server.py`, `client.py` y lógica general | PSF License |
| Pygame | [Comunidad de Pygame](https://www.pygame.org/docs/) | `client.py`, interfaz gráfica y lectura del teclado | LGPL 2.1 |
| Diagramas RAPTOR | Elaboración del equipo con RAPTOR | `diseno/DF1_partida.rap`, `DF2_validacion.rap` y `DF3_fin.rap` | MIT para los aportes propios; la herramienta no se distribuye |
| Diagrama de arquitectura | Elaboración del equipo con [draw.io](https://www.diagrams.net/) | `diseno/arquitectura.drawio` | MIT para los aportes propios; la herramienta no se distribuye |
| Elementos gráficos del juego | Figuras dibujadas mediante el código de Pygame | `client.py`, líneas 66–83 | MIT para el código propio; no se identificaron imágenes externas |

### Uso de IA

| Herramienta | Para qué la usamos | Qué revisamos o cambiamos nosotros |
|---|---|---|
| ChatGPT (OpenAI) | Apoyo en el borrador de Fase 3, revisión y simplificación de comentarios, organización de archivos y redacción del README. | El equipo proporcionó los archivos de código y diseño, subió los diagramas originales y agregó el enlace del video. No se han detallado otros cambios manuales del código. |
| Gemini / asistente de IA | Revisión del diseño y observaciones de la Fase 1, según la declaración del informe de Fase 2. | Según el informe, el equipo revisó la condición de victoria de cinco puntos, el alcance del modo local y las inconsistencias de los escenarios. |
