from PPlay.sprite import *
from PPlay.keyboard import *
from PPlay.window import *
from shoot import Shoot
import json
from PPlay.sound import *

class Player(Sprite):
    def __init__(self, x, y, janela):
        super().__init__("player.png")
        self.set_position(x - self.width, y - self.height)
        self.janela = janela

        with open('aprimoramentos.json', 'r') as f:
            dados = json.load(f)

        self.speed = dados["speed"]
        self.dinheiro = dados["dinheiro"]
        self.lives = dados["lives"]
        self.shoot_delay = dados["shoot_delay"]
        self.shoot_speed = dados["shoot_speed"]

        self.projectiles = []
        self.shoot_tick = self.shoot_delay
        self.direction = 1
        self.invencible = False
        self.invencible_time = 2
        self.visivel = True
        self.paralisado = False
        self.tempo_paralisado = 2
        self.som_laser = Sound("som_laser.ogg")
        self.som_laser.set_volume(40)
    
    def atualiza_jogador(self):
        if not self.paralisado:
            self.get_input()
        
        else:
            self.atualiza_paralisia()

        if self.invencible:
            self.atualiza_invencibilidade()

    def get_input(self):
        teclado = Keyboard()

        if teclado.key_pressed("UP") and self.y > 0:
            self.y -= self.janela.delta_time()*self.speed
        if teclado.key_pressed("DOWN") and self.y < self.janela.height - self.height:
            self.y += self.janela.delta_time()*self.speed
        if teclado.key_pressed("LEFT") and self.x > 0:
            self.x -= self.janela.delta_time()*self.speed
            if self.direction == 1:
                self.direction = -1
                self.flip(True, False)
        if teclado.key_pressed("RIGHT") and self.x < self.janela.width - self.width:
            self.x += self.janela.delta_time()*self.speed
            if self.direction == -1:
                self.direction = 1
                self.flip(True, False)
        if teclado.key_pressed("SPACE"):
            if self.shoot_tick > self.shoot_delay:
                self.som_laser.play()
                self.shoot()
    
    def shoot(self): # insere os projeteis na lista
        self.shoot_tick = 0
        self.projectiles.append(Shoot(self, self.y + self.height/2, self.direction, self.janela, "shoot.png", self.shoot_speed))

    def atingido(self, dano=1):
        if not self.invencible:
            self.lives -= dano
            self.invencible = True
            self.invencible_time = 2
            print(self.lives)

    def atualiza_invencibilidade(self):
        self.piscar()
        self.invencible_time -= self.janela.delta_time()
        
        if self.invencible_time <= 0:
            self.invencible = False
            self.visivel = True

    def atualiza_paralisia(self):
        self.tempo_paralisado -= self.janela.delta_time()

        if self.tempo_paralisado <= 0:
            self.paralisado = False
            self.tempo_paralisado = 2

    def piscar(self):
        self.visivel = not self.visivel
            
        

