import threading
import time
from server import iniciar_servidor
from client import iniciar_cliente


# Configuracion de la conexion
def pedir_puerto():
    while True:
        texto = input("Puerto (por defecto 5000): ")
        if texto == "":
            return 5000
        if texto.isdigit():
            puerto = int(texto)
            if puerto >= 1024 and puerto <= 65535:
                return puerto
        print("Puerto invalido. Escribe un numero entre 1024 y 65535.")


def pedir_ip():
    while True:
        ip = input("IP del servidor (por defecto 127.0.0.1): ")
        if ip == "":
            return "127.0.0.1"
        partes = ip.split(".")
        valida = len(partes) == 4
        for p in partes:
            if not p.isdigit() or int(p) > 255:
                valida = False
        if valida:
            return ip
        print("IP invalida. Ejemplo: 192.168.1.10")


# Menu principal (RF-01)
def mostrar_menu():
    print()
    print("===== PING PONG =====")
    print("1. Crear partida (servidor)")
    print("2. Unirse a una partida")
    print("3. Salir")


def main():
    opcion = ""
    while opcion != "3":
        mostrar_menu()
        opcion = input("Elige una opcion: ")

        if opcion == "1":
            puerto = pedir_puerto()
            hilo = threading.Thread(target=iniciar_servidor, args=(puerto,), daemon=True)
            hilo.start()
            time.sleep(1)
            print("Controles: W/S o flechas. Gana quien llegue a 5 puntos.")
            iniciar_cliente("127.0.0.1", puerto)
        elif opcion == "2":
            ip = pedir_ip()
            puerto = pedir_puerto()
            print("Controles: W/S o flechas. Gana quien llegue a 5 puntos.")
            iniciar_cliente(ip, puerto)
        elif opcion == "3":
            print("Hasta luego!")
        else:
            print("Opcion invalida. Elige 1, 2 o 3.")


# Inicio del programa
if __name__ == "__main__":
    main()
