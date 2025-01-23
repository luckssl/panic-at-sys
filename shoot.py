from PPlay.sprite import Sprite
from PPlay.window import *
import math

class Shoot(Sprite):
    def __init__(self, player, y, dir, janela, imagem, velocidade=300):
        super().__init__(imagem)
        if dir == -1:
            self.set_position(player.x, y - self.height/2)
        else:
            self.set_position(player.x + player.width - self.width, y - self.height/2)
        self.direction = dir
        self.janela = janela
        self.velocidade = velocidade

    def atualiza_posicao(self, projectile):
        self.move_x(self.velocidade*self.direction*self.janela.delta_time()) # movimento do projetil pelo eixo x
        # se o projetil passar dos limites da tela ele é eliminado
        if projectile.x < -projectile.width or projectile.x > self.janela.width + projectile.width:
            return True
        else:
            return False

class ShootLaser(Sprite):
    def __init__(self, boss):
        super().__init__("laser.png")
        self.boss = boss

        self.set_position(boss.x, boss.y + boss.height/2 - self.height/2)
    
    def atualizar_posicao(self):
        self.x = self.boss.x - self.width  # Atualize a posição x do laser
        self.y = self.boss.y + self.boss.height/2 - self.height/2 

class Projetil(Sprite):
    def __init__(self, boss, velocidade_x, velocidade_y, imagem):
        super().__init__(imagem)
        self.x = boss.x
        self.y = boss.y
        self.velocidade_x = velocidade_x
        self.velocidade_y = velocidade_y
        self.janela = boss.janela
        self.set_position(boss.x, boss.y + boss.height)

    def atualiza_posicao(self, projectile):
        self.x += self.velocidade_x * self.janela.delta_time()
        self.y += self.velocidade_y * self.janela.delta_time()

        if projectile.x < -projectile.width or projectile.x > self.janela.width + projectile.width:
            return True
        else:
            return False
    
