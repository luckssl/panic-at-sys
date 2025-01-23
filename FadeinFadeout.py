from PPlay.window import Window
import pygame
from PPlay.gameimage import GameImage

# Configuração inicial
janela = Window(800, 600)
janela.set_title("Fade In e Fade Out com PPlay")
background = GameImage("background_fase1.jpg")
overlay = GameImage("overlay.png")  # fundo preto de transição

overlay_surface = pygame.image.load("overlay.png")


def set_opacity(surface, alpha):
    surface.set_alpha(alpha)  # Define a opacidade
    return surface

# Função para aplicar fade
def fade(janela, overlay, fade_in=True, duration=1.0):
    if fade_in:
        alpha = 0 
    else: 
        alpha = 255
    alpha_step = 255 / (duration * 60)

    while (fade_in and alpha < 255) or (not fade_in and alpha > 0):
        janela.update()
        background.draw()
        overlay.image = set_opacity(overlay_surface, alpha)
        overlay.draw()
        janela.update()
        
        if fade_in:
            alpha += alpha_step
        else:
            alpha -= alpha_step
        
        # Garante que alpha esteja no intervalo correto
        alpha = min(255, max(0, alpha))  

while True: 
    # if condicao de mudar de fase
    #     fade(janela, overlay, fade_in=True, duration=2.0)
    
    if janela.get_keyboard().key_pressed("ESC"):
        fade(janela, overlay, fade_in=True, duration=10.0)
        # volta pro menu

    janela.update()