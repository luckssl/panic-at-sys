from PPlay.sprite import Sprite
from PPlay.window import *
import random
from shoot import Shoot

class Enemy(Sprite):
    def __init__(self, lim_min, lim_max, janela, imagem, lado):
        super().__init__(imagem)

        self.janela = janela
        self.speed = random.randint(20, 150)
        self.projectiles = []
        self.shoot_delay = random.uniform(1.5,4)
        self.shoot_tick = 0
        self.direction = lado
        self.lim_min = lim_min
        self.lim_max = lim_max
        self.espacamento = 0.1*self.janela.height
        self.medio = random.uniform(lim_min + self.espacamento, lim_max - self.espacamento*1.5)
        self.lim_max_x = random.uniform(self.janela.width*0.83, self.janela.width*0.92)
        self.lim_min_x = random.uniform(self.janela.width*0.08, self.janela.width*0.17)

        # Setando a posicao do inimigo
        if self.direction == 1: # Lado direito
            self.set_position(self.janela.width + 2 * self.width, self.medio)
        else: # Lado esquerdo
            self.set_position(-2 * self.width, self.medio)
            self.flip(True, False)
    
    def movimento(self):
        if self.direction == 1:
            if self.x > self.lim_max_x:
                self.x -= self.speed*self.janela.delta_time()
        else:
            if self.x < self.lim_min_x:
                self.x += self.speed*self.janela.delta_time()

    def atirar(self): # insere os projeteis na lista
        self.shoot_tick = 0
        self.projectiles.append(Shoot(self, self.y + self.height/2, -self.direction, self.janela, "enemy_shoot.png"))

class InimigoInvestidor(Sprite):
    def __init__(self, lim_min, lim_max, janela, imagem, lado):
        super().__init__(imagem)
        self.janela = janela
        self.speed = 100
        self.projectiles = []
        self.direction = lado
        self.lim_min = lim_min
        self.lim_max = lim_max
        self.espacamento = 0.1*self.janela.height
        self.medio = random.uniform(lim_min + self.espacamento, lim_max - self.espacamento*1.5)
        self.lim_min = lim_min + self.espacamento
        self.lim_max = lim_max - self.espacamento
        self.lim_max_x = random.uniform(self.janela.width*0.83, self.janela.width*0.92)
        self.lim_min_x = random.uniform(self.janela.width*0.12, self.janela.width*0.17)
        self.carregando = False
        self.tempo = 3
        self.tempo_inicial = 0
        self.i = 1
        self.tempo_carregamento = 1.5
        self.vida = 2
        # Setando a posicao do inimigo
        if self.direction == 1: # Lado direito
            self.set_position(self.janela.width + 2 * self.width, self.medio)
        else: # Lado esquerdo
            self.set_position(-2 * self.width, self.medio)
            self.flip(True, False)
    
    def movimento(self):
        if not self.carregando:
            # Movimento padrão
            if self.direction == 1 and self.x > self.lim_max_x:
                self.x -= self.speed * self.janela.delta_time()
            elif self.direction == -1 and self.x < self.lim_min_x:
                self.x += self.speed * self.janela.delta_time()
            
            self.y += self.speed * self.janela.delta_time() * self.i
            if self.y >= self.lim_max or self.y <= self.lim_min:
                self.i *= -1  # Inverta a direção vertical
            
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
                self.x += (self.speed * 14 * -self.direction) * self.janela.delta_time()
                if self.x < -self.width or self.x > self.janela.width + self.width:
                    # Reiniciar estado
                    self.carregando = False
                    self.direction *= -1
                    self.flip(True, False)
                    self.tempo_inicial = 0

        
                


class EnemyWave:
    def __init__(self, janela):
        self.total_inimigos_direita = 0
        self.total_inimigos_esquerda = 0
        self.janela = janela
        self.inimigos = [] # posicoes

    def atualizar(self):
        pass

    def spawn_inimigos(self):
        # Computar a posicao de cada inimigo
        self.total_inimigos_direita = random.randint(2, 5)
        self.total_inimigos_esquerda = random.randint(2, 5)
        self.inimigos_permitidos = [Enemy, InimigoInvestidor, Enemy, Enemy]
        
        tam = self.janela.height
        n = self.total_inimigos_direita
        n_esq = self.total_inimigos_esquerda

        for i in range(n):
            tipoInimigo = random.choice(self.inimigos_permitidos)
            if tipoInimigo == Enemy:
                inimigo = tipoInimigo(tam*i/n, tam*(i+1)/n,self.janela, "inimigo.png", 1)
            elif tipoInimigo == InimigoInvestidor:
                inimigo = tipoInimigo(tam*i/n, tam*(i+1)/n,self.janela, "investidor.png", 1)
            self.inimigos.append(inimigo)

        for i in range(n_esq):
            tipoInimigo = random.choice(self.inimigos_permitidos)
            if tipoInimigo == Enemy:
                inimigo = tipoInimigo(tam*i/n_esq, tam*(i+1)/n_esq,self.janela, "inimigo.png", -1)
            elif tipoInimigo == InimigoInvestidor:
                inimigo = tipoInimigo(tam*i/n_esq, tam*(i+1)/n_esq,self.janela, "investidor.png", -1)
            self.inimigos.append(inimigo)
    
    def atualizar_movimento(self):
        # Atualizar movimento de todos os inimigos
        for inimigo in self.inimigos:
            inimigo.movimento()
            if hasattr(inimigo, "shoot_tick"):
                inimigo.shoot_tick += self.janela.delta_time()
                if inimigo.shoot_tick >= inimigo.shoot_delay:
                    inimigo.atirar()

        
        
        

        



