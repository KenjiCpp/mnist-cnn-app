import pygame

def load_font(name, size, bold, italic):
    if not pygame.get_init():
        pygame.init()
    return pygame.font.SysFont(name, size, bold=bold, italic=italic)

btn_text_font     = load_font('Segoe UI', 24, True, False)
btn_text_color    = (236, 240, 241)
btn_color_idle    = ( 24,  94, 140)
btn_color_hover   = ( 41, 128, 185)
btn_color_pressed = ( 52, 152, 219)

class Button:
    def __init__(self, parent, text, offset, size, func):
        self.parent    = parent
        self.hover     = False
        self.pressed   = False
        self.btn_rect  = pygame.Rect(offset, size)
        self.text      = text
        self.text_surf = btn_text_font.render(self.text, True, btn_text_color)
        self.text_rect = self.text_surf.get_rect(center=self.btn_rect.center)
        self.func      = func
        parent.children.append(self)

    def render(self):
        btn_color = btn_color_idle
        if self.hover:
            btn_color = btn_color_hover
        if self.pressed:
            btn_color = btn_color_pressed
        pygame.draw.rect(self.parent.surface, btn_color, self.btn_rect, border_radius=10)
        self.parent.surface.blit(self.text_surf, self.text_rect)

    def update(self):
        mouse_pos = self.parent.global_to_local(pygame.mouse.get_pos())
        if self.btn_rect.collidepoint(mouse_pos):
            self.hover = True
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    self.func()
                    self.pressed = False
        else:
            self.hover   = False
            self.pressed = False
