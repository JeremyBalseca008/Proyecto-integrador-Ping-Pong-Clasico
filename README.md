# Ping Pong clásico

Proyecto integrador de Lógica de Programación de la Universidad Internacional del Ecuador (UIDE), paralelo C.

## Descripción

El proyecto consiste en un videojuego de Ping Pong para dos jugadores desarrollado en Python. Cada jugador controla una paleta y debe evitar que la pelota salga por su lado de la cancha. El jugador contrario obtiene un punto cuando esto sucede. La partida termina cuando uno de los jugadores alcanza cinco puntos.

El juego utiliza Pygame para la interfaz gráfica y sockets TCP para comunicar a los jugadores mediante un servidor que controla la lógica y envía su estado a ambos clientes.

## Integrantes

- Christopher Torres
- Gabriel Condor
- Jeremy Balseca

## Estructura

| Archivo | Función |
| --- | --- |
| juego.py | Menú principal, validación de IP y puerto, creación y conexión a partidas. |
| game_logic.py | Movimiento, límites, rebotes, marcador, resultado y conversión del estado a texto. |
| server.py | Acepta dos conexiones, recibe movimientos y sincroniza la partida. |
| client.py | Lee el teclado, recibe el estado y dibuja la cancha y el resultado en Pygame. |
| diseno/ | Diagramas de la Fase 2; arquitectura de red incluida, archivos RAPTOR pendientes de carga. |
| requirements.txt | Dependencia de Pygame. |
| LICENSE | Licencia MIT. |

## Instalación

Se necesita Python 3, pip, Pygame y un entorno gráfico. Desde la carpeta del repositorio:

```bash
python -m pip install -r requirements.txt
python juego.py
```

En Ubuntu se puede utilizar python3 en lugar de python. Si es necesario, crear un entorno virtual con python3 -m venv .venv y activarlo con source .venv/bin/activate antes de instalar.

## Cómo jugar

**Jugador 1:** ejecutar python juego.py, elegir la opción 1 (Crear partida) y presionar Enter para utilizar el puerto 5000, o introducir otro puerto válido.

**Jugador 2:** ejecutar python juego.py, elegir la opción 2 (Unirse), introducir la IPv4 del equipo servidor y utilizar el mismo puerto. Ambos equipos deben tener conectividad de red. Se puede consultar la IP con ipconfig en Windows o hostname -I en Ubuntu.

Para probar la conexión en un solo equipo, abrir dos terminales y usar 127.0.0.1 como IP del servidor. Cada ventana recibe el teclado cuando tiene el foco; no es un modo local de dos jugadores con teclado compartido.

| Tecla | Acción |
| --- | --- |
| W o flecha arriba | Subir la paleta |
| S o flecha abajo | Bajar la paleta |
| Sin teclas de movimiento | Mantener la posición |

## Funcionamiento

El servidor espera dos conexiones TCP, asigna el número de jugador según el orden de conexión y recibe U, D o N para interpretar el movimiento. La lógica mantiene las paletas dentro de la cancha, actualiza la pelota, controla las colisiones y suma puntos. Tras cada anotación, reinicia la pelota.

El servidor envía ocho valores separados por comas y terminados con un salto de línea: coordenadas de la pelota, posición de cada paleta, puntos de ambos jugadores, indicador de fin y número del ganador. Los clientes representan estos datos en una ventana de 800 × 500 píxeles.

## Relación con el diseño de la Fase 2

| Diagrama de la Fase 2 | Archivo y líneas | Qué cambió |
| --- | --- | --- |
| DF1_partida.rap | juego.py, 35–70; server.py, 49–62; game_logic.py, 55–95 | El menú Jugar/Salir pasó a Crear partida, Unirse y Salir. El ciclo de turnos se sustituyó por actualizaciones continuas. |
| DF2_validacion.rap | client.py, 54–64; server.py, 7–22; game_logic.py, 38–53 | Las letras I, C y D se sustituyeron por controles de teclado. Se limitan las paletas y se interpretan los mensajes de movimiento. |
| DF3_fin.rap | game_logic.py, 10 y 97–104; client.py, 76–86 | Se corrigió la puntuación de victoria de dos a cinco. La partida continúa si ninguno llega a cinco. |

**Alcance:** esta versión incluye avances de Fase 4 (interfaz gráfica, partida completa y sockets). No es una traducción literal del prototipo de consola de la Fase 3. No incorpora la validación independiente que repite la lectura por formato y reglas ni una rama de empate. Ejecutar game_logic.py directamente no muestra demostraciones. Para la entrega de Fase 3 se recomienda conservar también la versión de consola exigida y consultar al docente.

## Casos de prueba propuestos

| Caso | Resultado esperado |
| --- | --- |
| Opción 9 en el menú | Mensaje de error y repetición del menú. |
| Puerto fuera del intervalo 1024–65535 | Se vuelve a solicitar. |
| Paleta en el borde | Permanece dentro de la cancha. |
| Marcador 5–3 | Gana J1. |
| Marcador 3–5 | Gana J2. |
| Marcador 4–4 | Continúa. |
| Marcador artificial 5–5 | El código actual asigna la victoria a J2; no hay rama de empate. |
| Dos clientes en LAN | Se espera sincronización de ambos jugadores. |

Estos casos son resultados esperados. Las pruebas gráficas y de conexión quedan pendientes de verificar por el equipo.

## Video explicativo

Pendiente: incorporar el enlace del video del equipo (máximo cinco minutos para Fase 3).

## Autoría y créditos

El proyecto corresponde a Christopher Torres, Gabriel Condor y Jeremy Balseca. Los códigos de partida y los diagramas fueron proporcionados por el equipo para revisión.

- Python y sus módulos estándar socket, threading y time.
- [Pygame](https://www.pygame.org/docs/): biblioteca para la interfaz gráfica.
- RAPTOR y draw.io: herramientas de diseño utilizadas en la Fase 2.
- Los elementos gráficos se dibujan mediante código; no se identificaron imágenes externas en los cuatro archivos Python.
- ChatGPT (OpenAI): apoyo en el borrador de la Fase 3, revisión de comentarios, organización del repositorio y documentación.
- Gemini/asistente de IA: revisión del diseño, según la declaración de la Fase 2.
- Revisión del equipo: pendiente de detallar las modificaciones propias, confirmar el origen de los fragmentos utilizados y registrar las pruebas efectuadas.

## Licencia

El código propio está publicado bajo la licencia de código abierto MIT incluida en [LICENSE](LICENSE). Las bibliotecas y herramientas externas mantienen sus respectivas licencias.
