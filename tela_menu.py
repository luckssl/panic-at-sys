from PPlay.window import *
from PPlay.gameimage import *
from tela_base import Tela
import json
import os.path
from PPlay.sound import *

class TelaMenu(Tela):
    def __init__(self, janela, teclado, mouse):
        super().__init__(janela, teclado, mouse)
        
        self.botao_start = GameImage("botao_start.png")
        self.background = GameImage("background_menu.jpg")
        self.botao_start.set_position(janela.width/2-self.botao_start.width/2, janela.height/2 + self.botao_start.height*3)
        self.botao_exit = GameImage("botao_exit.png")
        self.botao_exit.set_position(janela.width/2-self.botao_start.width/2, janela.height/2 + self.botao_start.height*6)
        self.botao_novo = GameImage("botao_novo.png")
        self.botao_novo.set_position(janela.width/2-self.botao_start.width/2, janela.height/2 + self.botao_start.height*4.5)
        self.mouse = mouse
        self.som_hover = Sound("som_hover.ogg")
        self.hovering = {
            "novo": False,
            "continuar": False,
            "sair": False
        }
        self.som_errado = Sound("som_errado.ogg")
        self.som_errado.set_volume(20)
        self.historia = GameImage("historia.png")

    def atualizar(self):
        # Desenhando a tela de menu inicial
        self.background.draw()
        self.botao_start.draw()
        self.botao_novo.draw()
        self.botao_exit.draw()

        if self.mouse.is_over_object(self.botao_start):
            if not self.hovering["continuar"]:
                self.som_hover.play()
                self.hovering["continuar"] = True
            if self.mouse.is_button_pressed(1):
                if os.path.exists('aprimoramentos.json'):
                    from tela_loja import TelaLoja
                    return TelaLoja(self.janela, self.teclado,self.mouse)
                else:
                    self.som_errado.play()

        else:
            self.hovering["continuar"] = False
        
        if self.mouse.is_over_object(self.botao_novo):
            if not self.hovering["novo"]:
                self.som_hover.play()
                self.hovering["novo"] = True
            if self.mouse.is_button_pressed(1):
                self.novo_jogo()
                self.janela.clear()
                self.historia.draw()
                prox_tela = False
                while not prox_tela:
                    if self.teclado.key_pressed("ENTER"):
                        prox_tela = True
                    self.janela.update()


                from tela_loja import TelaLoja
                return TelaLoja(self.janela, self.teclado,self.mouse)
        else:
            self.hovering["novo"] = False


        if self.mouse.is_over_object(self.botao_exit):
            if not self.hovering["sair"]:
                self.som_hover.play()
                self.hovering["sair"] = True
            if self.mouse.is_button_pressed(1):
                self.janela.close()
        else:
            self.hovering["sair"] = False
    
        return self
    
    def novo_jogo(self):
        dados = {}
        
        dados["shoot_delay"] = 0.7
        dados["speed"] = 200
        dados["lives"] = 1
        dados["dinheiro"] = 0
        dados["shoot_speed"] = 230
        dados["valor_compra"] = 50

        with open('aprimoramentos.json', 'w') as f:
            json.dump(dados, f, indent=4)

