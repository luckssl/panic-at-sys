from PPlay.window import *
from PPlay.gameimage import *
from tela_base import Tela
from fase1 import Fase1
from tela_menu import TelaMenu
from PPlay.gameobject import *
import json
from PPlay.sound import *

class TelaLoja(Tela):
    def __init__(self, janela, teclado, mouse):
        super().__init__(janela, teclado, mouse)
        self.janela = janela
        self.background = GameImage("background_loja.png")
        self.botao_vida = GameImage("botao_vida.png")
        self.botao_vida.set_position(40, 110)
        self.botao_velocidade = GameImage("botao_velocidade.png")
        self.botao_velocidade.set_position(440, 110)
        self.botao_velocidade_projetil = GameImage("botao_velocidade_projetil.png")
        self.botao_velocidade_projetil.set_position(40, 210)
        self.botao_cadencia = GameImage("botao_cadencia.png")
        self.botao_cadencia.set_position(440, 210)
        self.quadro_atributos = GameImage("quadro_atributos.png")
        self.quadro_atributos.set_position(40, 310)
        self.modificado = False
        self.som_hover = Sound("som_hover.ogg")
        self.hovering = {
            "vida": False,
            "velocidade": False,
            "cadencia": False,
            "disparo": False
        }
        self.som_clicar = Sound("som_clicar.ogg")


        with open('aprimoramentos.json', 'r') as f:
            self.dados = json.load(f)
    
    def atualizar(self):
        if self.mouse.is_over_object(self.botao_vida):
            if not self.hovering["vida"]:
                self.som_hover.play()
                self.hovering["vida"] = True
            if self.mouse.is_button_released(1) and self.dados["lives"] < 6 and self.dados["dinheiro"] - self.dados["valor_compra"] >= 0:
                self.som_clicar.play()
                self.dados["lives"] += 1
                self.modificado = True
                self.dados["dinheiro"] -= self.dados["valor_compra"]
        else:
            self.hovering["vida"] = False

        if self.mouse.is_over_object(self.botao_velocidade):
            if not self.hovering["velocidade"]:
                self.som_hover.play()
                self.hovering["velocidade"] = True
            if self.mouse.is_button_released(1) and self.dados["speed"] < 350 and self.dados["dinheiro"] - self.dados["valor_compra"] >= 0:
                self.som_clicar.play()
                self.dados["speed"] += 25
                self.modificado = True
                self.dados["dinheiro"] -= self.dados["valor_compra"]
        else:
            self.hovering["velocidade"] = False

        if self.mouse.is_over_object(self.botao_cadencia):
            if not self.hovering["cadencia"]:
                self.som_hover.play()
                self.hovering["cadencia"] = True
            if self.mouse.is_button_released(1) and self.dados["shoot_delay"] > 0.3 and self.dados["dinheiro"] - self.dados["valor_compra"] >= 0:
                self.som_clicar.play()
                self.dados["shoot_delay"] -= 0.1
                self.modificado = True
                self.dados["dinheiro"] -= self.dados["valor_compra"]
        else:
            self.hovering["cadencia"] = False

        if self.mouse.is_over_object(self.botao_velocidade_projetil):
            if not self.hovering["disparo"]:
                self.som_hover.play()
                self.hovering["disparo"] = True
            if self.mouse.is_button_released(1) and self.dados["shoot_speed"] < 480 and self.dados["dinheiro"] - self.dados["valor_compra"] >= 0:
                self.som_clicar.play()
                self.dados["shoot_speed"] += 50
                self.modificado = True
                self.dados["dinheiro"] -= self.dados["valor_compra"]
        else:
            self.hovering["disparo"] = False
        
        if self.modificado:
            self.dados["valor_compra"] += 50
            with open('aprimoramentos.json', 'w') as f:
                json.dump(self.dados, f, indent=4)
            


            self.modificado = False



        # Desenhando a tela de menu inicial
        self.background.draw()
        self.botao_vida.draw()
        self.botao_velocidade.draw()
        self.botao_cadencia.draw()
        self.botao_velocidade_projetil.draw()
        self.quadro_atributos.draw()


        if self.teclado.key_pressed("ENTER"):
            return Fase1(self.janela, self.teclado,self.mouse)
        
        if self.teclado.key_pressed("ESC"):
            return TelaMenu(self.janela, self.teclado,self.mouse)
        
        self.janela.draw_text(f"{self.dados['dinheiro']}", 290, 324, color=(255,255,255), font_name="Press Start 2P", bold=True, size=26)
        self.janela.draw_text(f"Nº DE VIDAS: {self.dados['lives']}", 50, 324, color=(255,255,255), font_name="Press Start 2P", bold=True, size=26)
        self.janela.draw_text(f"VELOCIDADE: {self.dados['speed']}", 50, 356, color=(255,255,255), font_name="Press Start 2P", bold=True, size=26)
        self.janela.draw_text(f"VELOCIDADE DO PROJÉTIL: {self.dados['shoot_speed']}", 50, 388, color=(255,255,255), font_name="Press Start 2P", bold=True, size=26)
        self.janela.draw_text(f"TEMPO ENTRE DISPAROS: {self.dados['shoot_delay']:.1f}", 50, 420, color=(255,255,255), font_name="Press Start 2P", bold=True, size=26)
        self.janela.draw_text(f"VALOR DE COMPRA: {self.dados['valor_compra']}", 50, 452, color=(255,255,255), font_name="Press Start 2P", bold=True, size=26)
        return self
    
