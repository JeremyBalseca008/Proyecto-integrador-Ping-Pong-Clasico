# Configuracion del juego
ANCHO = 800
ALTO = 500

ANCHO_PALETA = 15
ALTO_PALETA = 90
TAMANO_PELOTA = 15
VELOCIDAD_PALETA = 7

PUNTOS_PARA_GANAR = 5

X_PALETA1 = 20
X_PALETA2 = ANCHO - 20 - ANCHO_PALETA


# Logica de la partida
class Juego:
    def __init__(self):
        self.paleta1_y = ALTO // 2 - ALTO_PALETA // 2
        self.paleta2_y = ALTO // 2 - ALTO_PALETA // 2
        self.puntos1 = 0
        self.puntos2 = 0
        self.terminado = False
        self.ganador = 0
        self.pelota_x = 0
        self.pelota_y = 0
        self.vel_x = 0
        self.vel_y = 0
        self.reiniciar_pelota(1)

    # Saque de la pelota (RF-06)
    def reiniciar_pelota(self, direccion):
        self.pelota_x = ANCHO // 2 - TAMANO_PELOTA // 2
        self.pelota_y = ALTO // 2 - TAMANO_PELOTA // 2
        self.vel_x = 5 * direccion
        self.vel_y = 4

    # Movimiento y limites de las paletas (RF-02 y RF-03)
    def mover_paleta(self, jugador, direccion):
        cambio = direccion * VELOCIDAD_PALETA
        if jugador == 1:
            self.paleta1_y = self.paleta1_y + cambio
            self.paleta1_y = self.limitar(self.paleta1_y)
        else:
            self.paleta2_y = self.paleta2_y + cambio
            self.paleta2_y = self.limitar(self.paleta2_y)

    def limitar(self, y):
        if y < 0:
            y = 0
        if y > ALTO - ALTO_PALETA:
            y = ALTO - ALTO_PALETA
        return y

    # Movimiento y rebotes de la pelota (RF-04)
    def actualizar(self):
        if self.terminado:
            return

        self.pelota_x = self.pelota_x + self.vel_x
        self.pelota_y = self.pelota_y + self.vel_y

        if self.pelota_y <= 0:
            self.pelota_y = 0
            self.vel_y = -self.vel_y
        if self.pelota_y >= ALTO - TAMANO_PELOTA:
            self.pelota_y = ALTO - TAMANO_PELOTA
            self.vel_y = -self.vel_y

        if self.vel_x < 0:
            if (self.pelota_x <= X_PALETA1 + ANCHO_PALETA
                    and self.pelota_x + TAMANO_PELOTA >= X_PALETA1
                    and self.pelota_y + TAMANO_PELOTA >= self.paleta1_y
                    and self.pelota_y <= self.paleta1_y + ALTO_PALETA):
                self.vel_x = -self.vel_x
                self.pelota_x = X_PALETA1 + ANCHO_PALETA

        if self.vel_x > 0:
            if (self.pelota_x + TAMANO_PELOTA >= X_PALETA2
                    and self.pelota_x <= X_PALETA2 + ANCHO_PALETA
                    and self.pelota_y + TAMANO_PELOTA >= self.paleta2_y
                    and self.pelota_y <= self.paleta2_y + ALTO_PALETA):
                self.vel_x = -self.vel_x
                self.pelota_x = X_PALETA2 - TAMANO_PELOTA

        # Marcador (RF-05)
        if self.pelota_x < 0:
            self.puntos2 = self.puntos2 + 1
            self.reiniciar_pelota(1)

        if self.pelota_x > ANCHO:
            self.puntos1 = self.puntos1 + 1
            self.reiniciar_pelota(-1)

        self.revisar_fin()

    # Fin de la partida (RF-07 y RF-08)
    def revisar_fin(self):
        if self.puntos1 >= PUNTOS_PARA_GANAR:
            self.terminado = True
            self.ganador = 1
        if self.puntos2 >= PUNTOS_PARA_GANAR:
            self.terminado = True
            self.ganador = 2


# Datos de la partida para la red
def estado_a_texto(juego):
    datos = [juego.pelota_x, juego.pelota_y, juego.paleta1_y, juego.paleta2_y,
             juego.puntos1, juego.puntos2, int(juego.terminado), juego.ganador]
    texto = ""
    for d in datos:
        texto = texto + str(int(d)) + ","
    return texto[:-1]


def texto_a_estado(texto):
    partes = texto.split(",")
    numeros = []
    for p in partes:
        numeros.append(int(p))
    return numeros
