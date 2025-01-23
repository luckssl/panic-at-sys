from PPlay.window import *
from PPlay.sprite import *
from tela_base import Tela
from fase1 import Fase1

class TelaJogo(Tela):
    def __init__(self, janela, teclado, seta):
        super().__init__(janela, teclado, seta)
        self.fase_atual = Fase1(self.janela, self.teclado, self.mouse)

    def atualizar(self):
        # Atualiza a fase atual
        nova_fase = self.fase_atual.atualizar()
        if nova_fase:
            self.fase_atual = nova_fase

        
        return self



        