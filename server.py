import socket
import threading
import time
from game_logic import Juego, estado_a_texto


# Recepcion de movimientos
def recibir_movimientos(conexion, jugador, movimientos):
    while True:
        try:
            datos = conexion.recv(16).decode()
        except:
            break
        if datos == "":
            break
        letra = datos[-1]
        if letra == "U":
            movimientos[jugador] = -1
        elif letra == "D":
            movimientos[jugador] = 1
        else:
            movimientos[jugador] = 0


# Conexion de los jugadores
def iniciar_servidor(puerto):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("0.0.0.0", puerto))
    servidor.listen(2)
    print("Servidor listo en el puerto", puerto, "- esperando jugadores...")

    conexiones = {}
    for numero in (1, 2):
        conexion, direccion = servidor.accept()
        print("Jugador", numero, "conectado desde", direccion[0])
        conexion.sendall((str(numero) + "\n").encode())
        conexiones[numero] = conexion

    juego = Juego()
    movimientos = {1: 0, 2: 0}

    for numero in (1, 2):
        hilo = threading.Thread(target=recibir_movimientos,
                                args=(conexiones[numero], numero, movimientos),
                                daemon=True)
        hilo.start()

    # Ciclo de la partida
    while not juego.terminado:
        juego.mover_paleta(1, movimientos[1])
        juego.mover_paleta(2, movimientos[2])
        juego.actualizar()

        mensaje = (estado_a_texto(juego) + "\n").encode()
        try:
            conexiones[1].sendall(mensaje)
            conexiones[2].sendall(mensaje)
        except:
            print("Un jugador se desconecto. Fin de la partida.")
            break
        time.sleep(1 / 60)

    # Cierre de conexiones
    print("Partida terminada. Ganador: jugador", juego.ganador)
    time.sleep(1)
    for numero in (1, 2):
        conexiones[numero].close()
    servidor.close()


if __name__ == "__main__":
    iniciar_servidor(5000)
