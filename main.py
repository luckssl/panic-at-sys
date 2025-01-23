from PPlay.window import *
from PPlay.keyboard import *
from PPlay.mouse import *
from PPlay.gameimage import *
from tela_menu import TelaMenu

class Jogo:
    def __init__(self):
        self.janela = Window(800, 600)
        self.teclado = Keyboard()
        self.mouse = Mouse()
        self.tela_atual = TelaMenu(self.janela, self.teclado, self.mouse)

    def run(self):
        while True:
            self.tela_atual = self.tela_atual.atualizar()
            self.janela.update()

if __name__ == "__main__":
    jogo = Jogo()
    jogo.run()


