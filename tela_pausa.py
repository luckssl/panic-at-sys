from PPlay.window import *
from PPlay.gameimage import *
from tela_base import Tela
from PPlay.sound import *

class TelaPausa(Tela):
    def __init__(self, janela, teclado, mouse, tela_jogo):
        super().__init__(janela, teclado, mouse)
        self.tela_jogo = tela_jogo
        
        self.botao_voltar_jogo = GameImage("botao_voltar_jogo.png")
        self.botao_voltar_jogo.set_position(self.janela.width/2 - self.botao_voltar_jogo.width/2, self.janela.height/2 - self.botao_voltar_jogo.height*2)
        self.botao_voltar_menu = GameImage("botao_voltar_menu.png")
        self.botao_voltar_menu.set_position(self.janela.width/2 - self.botao_voltar_jogo.width/2, self.janela.height/2 - self.botao_voltar_jogo.height/2)
        self.background = GameImage("background_pausa.png")
        self.tela_jogo = tela_jogo
        tela_jogo.soundtrack.pause()
        self.som_hover = Sound("som_hover.ogg")
        self.hovering = {
            "menu": False,
            "continuar": False
        }

    def atualizar(self):
        
        # Desenhando a tela de menu inicial
        self.background.draw()
        self.botao_voltar_jogo.draw()
        self.botao_voltar_menu.draw()
        self.janela.draw_text(f"DINHEIRO: {self.tela_jogo.player.dinheiro}", 20, 20, color=(255,255,255), font_name="Press Start 2P", bold=True, size=26)

        if self.mouse.is_over_object(self.botao_voltar_jogo):
            if not self.hovering["continuar"]:
                self.som_hover.play()
                self.hovering["continuar"] = True
            if self.mouse.is_button_released(1):
                self.tela_jogo.soundtrack.unpause()
                return self.tela_jogo
        else:
            self.hovering["continuar"] = False

        if self.mouse.is_over_object(self.botao_voltar_menu):
            if not self.hovering["menu"]:
                self.som_hover.play()
                self.hovering["menu"] = True
            if self.mouse.is_button_released(1):
                self.tela_jogo.soundtrack.stop()
                from tela_menu import TelaMenu
                return TelaMenu(self.janela, self.teclado,self.mouse)
        else:
            self.hovering["menu"] = False

        return self