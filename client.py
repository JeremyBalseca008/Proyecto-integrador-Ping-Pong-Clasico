
import socket
import threading
import pygame
from game_logic import (ANCHO, ALTO, ANCHO_PALETA, ALTO_PALETA, TAMANO_PELOTA,
                        X_PALETA1, X_PALETA2, texto_a_estado)

# Estado de la partida
estado = [ANCHO // 2, ALTO // 2, 200, 200, 0, 0, 0, 0]


# Recepcion de datos
def recibir_estado(archivo):
    global estado
    while True:
        linea = archivo.readline()
        if linea == "":
            break
        try:
            estado = texto_a_estado(linea.strip())
        except:
            pass


# Conexion al servidor
def iniciar_cliente(ip, puerto):
    conexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conexion.connect((ip, puerto))
    except:
        print("No se pudo conectar al servidor.")
        return

    archivo = conexion.makefile("r")
    mi_numero = int(archivo.readline().strip())
    print("Eres el jugador", mi_numero)

    hilo = threading.Thread(target=recibir_estado, args=(archivo,), daemon=True)
    hilo.start()

    # Ventana del juego
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Ping Pong - Jugador " + str(mi_numero))
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("Arial", 40)
    fuente_grande = pygame.font.SysFont("Arial", 60)

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        # Controles (RF-02)
        teclas = pygame.key.get_pressed()
        mensaje = "N"
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            mensaje = "U"
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            mensaje = "D"
        try:
            conexion.sendall(mensaje.encode())
        except:
            pass

        # Cancha y marcador
        pantalla.fill((0, 0, 0))
        pygame.draw.line(pantalla, (100, 100, 100), (ANCHO // 2, 0), (ANCHO // 2, ALTO), 2)
        pygame.draw.rect(pantalla, (255, 255, 255), (X_PALETA1, estado[2], ANCHO_PALETA, ALTO_PALETA))
        pygame.draw.rect(pantalla, (255, 255, 255), (X_PALETA2, estado[3], ANCHO_PALETA, ALTO_PALETA))
        pygame.draw.rect(pantalla, (255, 255, 0), (estado[0], estado[1], TAMANO_PELOTA, TAMANO_PELOTA))

        marcador = fuente.render(str(estado[4]) + "   " + str(estado[5]), True, (255, 255, 255))
        pantalla.blit(marcador, (ANCHO // 2 - marcador.get_width() // 2, 20))

        # Resultado de la partida
        if estado[6] == 1:
            if estado[7] == mi_numero:
                texto = "¡Ganaste!"
            else:
                texto = "Perdiste"
            mensaje_fin = fuente_grande.render(texto, True, (0, 255, 0))
            pantalla.blit(mensaje_fin, (ANCHO // 2 - mensaje_fin.get_width() // 2, ALTO // 2 - 30))
            pygame.display.flip()
            pygame.time.wait(3000)
            corriendo = False

        pygame.display.flip()
        reloj.tick(60)

    # Cierre del cliente
    pygame.quit()
    conexion.close()
