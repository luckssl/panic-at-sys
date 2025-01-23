from PPlay.sprite import Sprite
from PPlay.window import *
from shoot import Shoot, ShootLaser, Projetil

class Boss1(Sprite):
    def __init__(self, janela, imagem):
        super().__init__(imagem)

        self.janela = janela
        self.speed = 50
        self.projectiles = []
        self.shoot_delay = 2
        self.shoot_tick = 0
        self.espacamento = 0.01*self.janela.height
        self.lim_max = self.janela.height - self.height
        self.lim_min = 0
        self.lim_x = self.janela.width - self.width
        self.carregando = False
        self.tempo = 10
        self.tempo_inicial = 0
        self.i = 1
        self.tempo_carregamento = 1.5
        self.duracao_laser = 3
        self.vida = 5
        self.laser = ShootLaser(self)
        self.posx = False
        self.posy = False
        self.laser_desenha = False

        self.set_position(self.janela.width+self.width, self.janela.height+self.height)

    def atualizar_movimento(self):
        self.movimento()
        self.laser.atualizar_posicao()
    
    def atirar(self): # insere os projeteis na lista
        self.shoot_tick = 0
        self.projectiles.append(Shoot(self, self.y + self.height/2, -1, self.janela, "shoot_boss1.png"))
    
    def movimento(self):
        if self.x >= self.lim_x:
            self.x -= self.speed * self.janela.delta_time()*2
        else:
            self.posx = True
        
        if self.y >= self.lim_max:
            self.y -= self.speed * self.janela.delta_time()*2
        else:
            self.posy = True
        
        if self.posy and self.posx:
            if not self.carregando:
                self.y += self.speed * self.janela.delta_time() * self.i
                if self.y >= self.lim_max or self.y <= self.lim_min:
                    self.i *= -1  # Inverta a direção vertical
                self.shoot_tick += self.janela.delta_time()
                if self.shoot_tick >= self.shoot_delay:
                    self.atirar()
                
                # Controle de carregamento
                self.tempo_inicial += self.janela.delta_time()
                if self.tempo_inicial >= self.tempo:
                    self.carregando = True
                    self.tempo_inicial = 0
            else:
                if self.tempo_inicial < self.tempo_carregamento:
                    self.tempo_inicial += self.janela.delta_time()
                # Movimento durante carregamento
                else:
                    self.laser_desenha = True
                    self.tempo_inicial += self.janela.delta_time()
                    if self.tempo_inicial >= self.duracao_laser:
                        self.tempo_inicial = 0
                        self.carregando = False
                        self.laser_desenha = False
    
    def atingido(self):
        self.vida -= 1

class Boss2(Sprite):
    def __init__(self, janela, imagem):
        super().__init__(imagem)
        self.janela = janela
        self.speed = 50
        self.projectiles = []
        self.shoot_delay = 2
        self.shoot_tick = 0
        self.espacamento = 0.01*self.janela.height
        self.lim_max = self.janela.height - (self.height)
        self.lim_min = self.janela.height - (self.height*1.5)
        self.lim_x = self.janela.width - self.width
        self.i = 1
        self.vida = 5
        self.posy = False

        self.set_position(self.lim_x, -self.height)

    def atualizar_movimento(self):
        self.movimento()
    
    def atirar(self): # insere os projeteis na lista
        self.shoot_tick = 0
        self.projectiles.append(Shoot(self, self.y + self.height, -1, self.janela, "shoot_boss2.png"))
        self.projectiles.append(Projetil(self, -150, -150, "shoot_boss2_2.png"))
        self.projectiles.append(Projetil(self, -150, 150, "shoot_boss2_3.png"))

    def movimento(self):
        if self.y <= self.lim_min:
            self.y += self.speed * self.janela.delta_time()*2
        else:
            self.posy = True
        
        if self.posy:
            self.y += self.speed * self.janela.delta_time() * self.i
            if self.y > self.lim_max or self.y < self.lim_min:
                self.i *= -1  # Inverta a direção vertical
            self.shoot_tick += self.janela.delta_time()
            if self.shoot_tick >= self.shoot_delay:
                self.atirar()

    
    def atingido(self):
        self.vida -= 1