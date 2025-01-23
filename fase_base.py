from PPlay.gameimage import *
from tela_base import Tela
from PPlay.sound import *

class Fase(Tela):
    def __init__(self, janela, teclado, mouse, proxima_fase=None):
        super().__init__(janela, teclado, mouse)
        self.proxima_fase = proxima_fase
        self.som_colisao = Sound("acertou.ogg")
        self.som_colisao.set_volume(20)
        self.overlay = GameImage("overlay.png")
        self.overlay_surface = pygame.image.load("overlay.png")
        self.morreu = GameImage("tela_morte.png")
    def atualizar(self):
        """Método que será chamado para atualizar a lógica da fase."""
        raise NotImplementedError("Esse método deve ser implementado na fase específica.")

    def transicao_fase(self):
        if self.proxima_fase:
            print("passou de fase")
            print(self.proxima_fase)
            return self.proxima_fase(self.janela, self.teclado, self.mouse)
        else:
            # Se não houver próxima fase, pode retornar None ou outra tela, como a TelaMenu
            return None 
        
    def set_opacity(self, surface, alpha):
        surface.set_alpha(alpha)  # Define a opacidade
        return surface

    # Função para aplicar fade
    def fade(self, fade_in=True, duration=10.0):
        if fade_in:
            alpha = 0 
        else: 
            alpha = 255
        alpha_step = 255 / (duration * 60)

        while (fade_in and alpha < 255) or (not fade_in and alpha > 0):
            self.janela.update()
            self.background.draw()
            self.overlay.image = self.set_opacity(self.overlay_surface, alpha)
            self.overlay.draw()
            self.janela.update()
            
            if fade_in:
                alpha += alpha_step
            else:
                alpha -= alpha_step
            
            # Garante que alpha esteja no intervalo correto
            alpha = min(255, max(0, alpha))  

