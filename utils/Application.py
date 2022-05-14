import pygame

class Application:
    def init(title):
        if not pygame.get_init():
            pygame.init()
        pygame.display.set_caption(title)
