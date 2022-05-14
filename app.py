import cv2
import pygame
import numpy as np

from keras.models import load_model

from utils.Application import Application
from utils.Region import Region
from utils.Button import Button
from utils.Drawing import line

Application.init('Handwritten Digit Recognition')

model = load_model('model.h5')

screen = Region.screen((886, 564))
canvas = Region.subregion(screen, (  2,   2), (560, 560), ( 28,  28))
inform = Region.subregion(screen, (564,   2), (320, 560))

clr_btn = Button(inform, 'Clear', ( 80,  90), (160,  48), lambda: canvas.fill((  0,   0,   0)))

brush_color = (255, 255, 255)
brush_width = 1.25

update = False
res    = None
prd    = None

running    = True
mouse_down = False
mouse_pos  = pygame.mouse.get_pos()

font_r = pygame.font.SysFont('Consolas', 20, bold=False)

while running:
    screen.fill((205, 255, 255))
    inform.fill(( 13,  41,  69))

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
            mouse_pos = pygame.mouse.get_pos()
            line(canvas.surface, brush_color, brush_width, canvas.global_to_local(mouse_pos), canvas.global_to_local(mouse_pos))
        elif ev.type == pygame.MOUSEBUTTONUP:
            mouse_down = False 
            update     = True
        elif ev.type == pygame.MOUSEMOTION:
            new_mouse_pos = pygame.mouse.get_pos()
            if mouse_down:
                line(canvas.surface, brush_color, brush_width, canvas.global_to_local(mouse_pos), canvas.global_to_local(new_mouse_pos))
                mouse_pos = new_mouse_pos

    if res is not None:
        for i in range(0, 10):
            if i == res:
                text_color = (0, 255, 0)
            else:
                text_color = (255, 255, 255)
            text_surf = font_r.render('{}: {:.3f}'.format(i, prd[i]), True, text_color)
            text_rect = text_surf.get_rect(center=pygame.Rect((0, 200 + 30 * i, 320, 30)).center)
            inform.surface.blit(text_surf, text_rect)


    screen.update()
    screen.render()
    pygame.display.update()

    if update:
        img = np.array(pygame.surfarray.array2d(canvas.surface)) / 16777215 * 255
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        img = cv2.flip(img, 1)
        img = img / 255
        img = np.array([img.reshape((28, 28, 1))])
        
        prd = model.predict(img)[0]
        res = np.argmax(prd, axis=0)

        update = False