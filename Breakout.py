import sys    # para usar exit()
import pygame
import time

ANCHO = 640 # Ancho de la pantalla.
ALTO = 480  # Alto de la pantalla.
# Colores
azul = (0,0,64)
# Inicializar
pygame.init()
# Bolita

class Bolita(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('bolita.png')
        # Obtener rectángulo de la imagen
        self.rect = self.image.get_rect()
        # Posición inicial centrada en pantalla.
        self.rect.centerx = ANCHO / 2
        self.rect.centery = ALTO / 2
        # Velocidad
        self.speed = [7,7]

    def update(self):
        if self.rect.top <= 0:
            self.speed[1] =- self.speed[1]
        elif self.rect.right >= ANCHO or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]
        self.rect.move_ip(self.speed)

# Jugador
class Paleta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('paleta.png')
        # Obtener rectángulo de la imagen
        self.rect = self.image.get_rect()
        # Posición inicial centrada en x
        self.rect.midbottom = (ANCHO/2,ALTO-20)
        # Velocidad
        self.speed = [0,0]

    def update(self,evento):
        if evento.key == pygame.K_a and self.rect.left > 0:
            self.speed = [-13,0]
        elif evento.key == pygame.K_d and self.rect.right < ANCHO:
            self.speed = [13,0]
        else:
            self.speed = [0,0]
        self.rect.move_ip(self.speed)
# Ladrillo
class Ladrillo(pygame.sprite.Sprite):
    def __init__(self, posicion):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('ladrillo.png')
        # Obtener rectángulo de la imagen
        self.rect = self.image.get_rect()
        # Posicion inicial
        self.rect.topleft = posicion
# Muro
class Muro(pygame.sprite.Group):
    def __init__(self, cantidadLadrillos):
        pygame.sprite.Group.__init__(self)
        pos_x = 0
        pos_y = 0
        for i in range(cantidadLadrillos):
            ladrillo = Ladrillo((pos_x,pos_y))
            self.add(ladrillo)
            pos_x += ladrillo.rect.width
            if pos_x >= ANCHO:
                pos_x = 0
                pos_y += ladrillo.rect.height

# Funcion llamada tras dejar ir a la bolita
def juego_terminado():
    fuente = pygame.font.SysFont("Arial",50)
    texto = fuente.render("Juego terminado, perdiste", True,(100,0,0))
    texto_rect = texto.get_rect()
    texto_rect.center = [ANCHO / 2, ALTO / 2]
    pantalla.blit(texto,texto_rect)
    pygame.display.flip()
    # Pausar por tres segundos
    time.sleep(2)
    # Sys
    sys.exit()

# Mostrar puntuacion
def mostrar_puntuacion():
    fuente = pygame.font.SysFont("Consolas",40)
    texto = fuente.render(str(puntuacion).zfill(0), True,(255,255,255))
    texto_rect = texto.get_rect()
    texto_rect.center = [ANCHO / 2, ALTO / 2]
    pantalla.blit(texto,texto_rect)
# Mostrar vidas
def mostrar_vidas():
    fuente = pygame.font.SysFont("Consolas",15)
    cadena = "Vidas: " + str(vidas)
    texto = fuente.render(cadena, True,(255,255,255))
    texto_rect = texto.get_rect()
    texto_rect.bottomleft = [0,ALTO]
    pantalla.blit(texto,texto_rect)


# Inicializando pantalla.
pantalla = pygame.display.set_mode((ANCHO, ALTO))
# Configurar título de pantalla.
pygame.display.set_caption('Juego de ladrillos')
# FPS
reloj = pygame.time.Clock()
# Repeticion de eventos
pygame.key.set_repeat(30)
# Elementos
bolita = Bolita()
jugador = Paleta()
muro = Muro(64)
puntuacion = 0
vidas = 3
esperando_saque = True

while True:
    # Establecer FPS
    reloj.tick(60)
    # Revisar todos los eventos.
    for evento in pygame.event.get():
        # Si se presiona la tachita de la barra de título,
        if evento.type == pygame.QUIT:
            # cerrar el videojuego.
            sys.exit()
        # Buscar eventos del teclado
        elif evento.type == pygame.KEYDOWN:
            jugador.update(evento)
            if esperando_saque == True and evento.key == pygame.K_SPACE:
                esperando_saque = False
                if bolita.rect.centerx < ANCHO / 2:
                    bolita.speed = [5,5]
                else:
                    bolita.speed = [5,5]

    # Revisar si la bolita sale de la pantalla
    if bolita.rect.top > ALTO:
        vidas -= 1
        esperando_saque = True
    #Actualizar bolita
    if esperando_saque == False:
        bolita.update()
    else:
        bolita.rect.midbottom = jugador.rect.midtop

    # Colision entre bolita y jugador
    if pygame.sprite.collide_rect(bolita,jugador):
        bolita.speed[1] =-bolita.speed[1]

    # Colision entre bolita y muro
    colision_jugador_muro = pygame.sprite.spritecollide(bolita,muro,False)
    if colision_jugador_muro:
        ladrillo = colision_jugador_muro[0]
        cx = bolita.rect.centerx
        if cx < ladrillo.rect.left or cx > ladrillo.rect.right:
            bolita.speed[0] =- bolita.speed[0]
        else:
            bolita.speed[1] =- bolita.speed[1]
        muro.remove(ladrillo)
        puntuacion += 1

    #Rellanar pantalla
    pantalla.fill(azul)
    # Mostrar puntuacion en pantalla
    mostrar_puntuacion()
    # Mostrar vidas en pantalla
    mostrar_vidas()
    # Dibujar bolita en pantalla.
    pantalla.blit(bolita.image, bolita.rect)
    # Dibujar paleta en pantalla
    pantalla.blit(jugador.image,jugador.rect)
    # Dibujar los ladrillos
    muro.draw(pantalla)
    # Actualizar los elementos en pantalla.
    pygame.display.flip()
    # Manejo vidas
    if vidas <= 0:
        juego_terminado()