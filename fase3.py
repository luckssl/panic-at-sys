from fase_base import Fase
from tela_menu import TelaMenu
from player import Player
from enemywave import EnemyWave
from PPlay.gameimage import *
import json
from PPlay.sound import *

class Fase3(Fase):
    def __init__(self, janela, teclado, mouse, proxima_fase=None):
        super().__init__(janela, teclado, mouse, proxima_fase)
        self.background = GameImage("background_fase3.jpg")
        self.layer2 = GameImage("layer2_3.png")
        self.layer2_copia = GameImage("layer2_3.png")
        self.layer2_copia.set_position(self.janela.width, 0)
        self.vel_layer2 = 10
        self.fim = GameImage("tela_fim.png")

        self.total_ondas = 10
        self.contador_ondas = 1
        
        self.inimigos = EnemyWave(self.janela)
        self.player = Player(self.janela.width/2, self.janela.height/2, self.janela)  # O jogador será instanciado na fase
        self.boss = None  # Boss (caso haja)
        self.acabou_jogo = False
        self.soundtrack = Sound("soundtrack3.ogg")
        self.soundtrack.loop = True
        self.soundtrack.play()
        self.fade(fade_in=False)

        self.inimigos.spawn_inimigos()

    def atualizar(self):
        # atualiza contador de projeteis do player
        self.player.shoot_tick += self.janela.delta_time()
        
        # atualizar posição do jogador
        self.player.atualiza_jogador()
        
        # Atualizar o movimento dos inimigos
        self.inimigos.atualizar_movimento()

        # Verifica as colisoes dos objetos desenhados na tela
        self.verificar_colisoes()

        self.layer2.x -= self.vel_layer2*self.janela.delta_time()
        self.layer2_copia.x -= self.vel_layer2*self.janela.delta_time()

        if self.acabou_vida():
            self.fade()
            self.morreu.draw()
            prox_tela = False
            while not prox_tela:
                if self.teclado.key_pressed("ENTER"):
                    prox_tela = True
                    self.fade()
                    from tela_loja import TelaLoja
                    return TelaLoja(self.janela, self.teclado, self.mouse)
                self.janela.update()
        
        if self.teclado.key_pressed("ESC"):
            from tela_pausa import TelaPausa
            return TelaPausa(self.janela, self.teclado, self.mouse, self)

        # atualizar movimento dos projeteis atirado pelo jogador LEMBRAR DE PASSAR ISSO PARA A CLASSE PLAYER!!!!!
        for projectile in self.player.projectiles[:]:
            limite = projectile.atualiza_posicao(projectile)
            if limite:
                self.player.projectiles.remove(projectile) # se passar dos limites da tela, o projetil é removido

        for inimigo in self.inimigos.inimigos:
            for projectile in inimigo.projectiles:
                limite = projectile.atualiza_posicao(projectile)
                if limite:
                    inimigo.projectiles.remove(projectile)
            
        if len(self.inimigos.inimigos) == 0:
                if self.contador_ondas < self.total_ondas:
                    self.contador_ondas += 1
                    self.inimigos.spawn_inimigos()
                else:
                    self.soundtrack.stop()
                    self.zerou_jogo()
                    self.fade()
                    self.fim.draw()
                    prox_tela = False
                    while not prox_tela:
                        if self.teclado.key_pressed("ENTER"):
                            prox_tela = True
                        self.janela.update()
                    return TelaMenu(self.janela, self.teclado,self.mouse)

        self.desenhar()
        return self
    


    def verificar_colisoes(self):
        if not self.player.invencible:
            inimigos_para_remover = []
            projeteis_para_remover = []
            
            # Verificação de colisões entre o jogador e os inimigos/projéteis
            for inimigo in self.inimigos.inimigos:
                if self.player.collided(inimigo):
                    inimigos_para_remover.append(inimigo)
                    self.player.atingido()
                    self.som_colisao.play()
                    self.player.dinheiro += 5

                for projectile in inimigo.projectiles:
                    if self.player.collided(projectile):
                        projeteis_para_remover.append(projectile)
                        self.player.atingido()
                        self.som_colisao.play()

            # Remover projéteis dos inimigos antes de remover os inimigos
            for projectile in projeteis_para_remover:
                for inimigo in self.inimigos.inimigos:
                    if projectile in inimigo.projectiles:
                        inimigo.projectiles.remove(projectile)

            # Remover inimigos depois de seus projéteis
            for inimigo in inimigos_para_remover:
                self.inimigos.inimigos.remove(inimigo)

        # Colisões dos projéteis do jogador
        projeteis_para_remover_jogador = []
        inimigos_para_remover_jogador = []
        projeteis_inimigos_para_remover_jogador = []

        for projectile in self.player.projectiles:
            for inimigo in self.inimigos.inimigos:
                if projectile.collided(inimigo):
                    self.som_colisao.play()
                    projeteis_para_remover_jogador.append(projectile)
                    inimigos_para_remover_jogador.append(inimigo)
                    self.player.dinheiro += 5

                for projectile_inimigo in inimigo.projectiles:
                    if projectile.collided(projectile_inimigo):
                        projeteis_para_remover_jogador.append(projectile)
                        projeteis_inimigos_para_remover_jogador.append(projectile_inimigo)

        # Remover projetéis e inimigos após a verificação
        for p in projeteis_para_remover_jogador:
            if p in self.player.projectiles:  # Verificar se o projétil ainda está na lista
                self.player.projectiles.remove(p)

        # Remover projéteis dos inimigos
        for projectile in projeteis_inimigos_para_remover_jogador:
            for inimigo in self.inimigos.inimigos:
                if projectile in inimigo.projectiles:
                    inimigo.projectiles.remove(projectile)

        # Remover inimigos
        for inimigo in inimigos_para_remover_jogador:
            if inimigo in self.inimigos.inimigos:  # Verificar se o inimigo ainda está na lista
                self.inimigos.inimigos.remove(inimigo)

    def desenhar(self):
        # Desenhar elementos na tela
        self.background.draw()
        self.layer2.draw()
        self.layer2_copia.draw()

        if self.player.visivel or not self.player.invencible:
            self.player.draw()
        for projectile in self.player.projectiles:
            projectile.draw()
        for inimigo in self.inimigos.inimigos:
            inimigo.draw()
            
            for projectile in inimigo.projectiles:
                projectile.draw()
        
        self.janela.draw_text(f"VIDAS: {self.player.lives}", 20, 20, color=(255,255,255), font_name="Press Start 2P", bold=True, size=26)
        self.janela.draw_text(f"{self.player.dinheiro}", 20, 46, color=(255,255,255), font_name="Press Start 2P", bold=True, size=26)
    
    def acabou_vida(self):
        if self.player.lives == 0:
            self.soundtrack.stop()
            self.atualiza_dinheiro()
            return True
        
        return False
    
    def atualiza_dinheiro(self):
        with open('aprimoramentos.json', 'r') as dados:
            atributo_jogador = json.load(dados)

        atributo_jogador["dinheiro"] += self.player.dinheiro
        self.player.dinheiro = 0

        with open('aprimoramentos.json', 'w') as modificado:
            json.dump(atributo_jogador, modificado, indent=4)
        
    def zerou_jogo(self):
        with open('aprimoramentos.json', 'r') as f:
            dados = json.load(f)
        
        dados["shoot_delay"] = 0.7
        dados["speed"] = 200
        dados["lives"] = 1
        dados["dinheiro"] = 0
        dados["shoot_speed"] = 280
        dados["valor_compra"] = 50

        with open('aprimoramentos.json', 'w') as f:
            json.dump(dados, f, indent=4)