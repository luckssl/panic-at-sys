# Classe base para telas
class Tela:
    def __init__(self, janela, teclado, seta):
        self.janela = janela
        self.teclado = teclado
        self.mouse = seta

    def atualizar(self):
        """Método será implementado por outras classes (telas)"""
        pass

