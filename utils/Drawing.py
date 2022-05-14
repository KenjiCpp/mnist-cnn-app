import pygame
import math

def line(surface, color, width, start, end):
    # Draw end points
    pygame.draw.circle(surface, color, start, width / 2)
    pygame.draw.circle(surface, color, end, width / 2)

    # Calculate and draw middle polygon
    if start != end:
        v = (end[0] - start[0], end[1] - start[1])
        l = math.sqrt(v[0] * v[0] + v[1] * v[1])
        u = (-v[1] / l * width / 2, v[0] / l * width / 2)

        p0 = (start[0] + u[0], start[1] + u[1])
        p1 = (start[0] - u[0], start[1] - u[1])
        p2 = (end[0]   - u[0], end[1]   - u[1])
        p3 = (end[0]   + u[0], end[1]   + u[1])
        ps = [p0, p1, p2, p3]
        pygame.draw.polygon(surface, color, ps)
