import pygame

class Region:
    def __init__(self):
        self.size       = (0, 0)
        self.resolution = self.size
        self.surface    = None
        self.offset     = (0, 0)
        self.parent     = None
        self.children   = []

    def screen(size):
        res = Region()
        res.size       = size
        res.resolution = size
        res.surface    = pygame.display.set_mode(size)
        res.offset     = (0, 0)
        res.parent     = None
        res.children   = []
        return res

    def subregion(parent, offset, size, resolution=None):
        res = Region()
        res.size       = size
        res.resolution = size
        if resolution is not None:
            res.resolution = resolution
        res.surface    = pygame.Surface(res.resolution)
        res.offset     = offset
        res.parent     = parent
        res.children   = []
        parent.children.append(res)
        return res

    def fill(self, color):
        self.surface.fill(color)

    def render(self):
        for child in self.children:
            child.render()
        if self.parent is not None:
            self.parent.surface.blit(pygame.transform.scale(self.surface, self.size), self.offset)

    def update(self):
        for child in self.children:
            child.update()

    def local_to_global(self, pos):
        if self.parent is None:
            return pos
        scales = (self.size[0] / self.resolution[0], self.size[1] / self.resolution[1])
        return self.parent.local_to_global((pos[0] * scales[0] + self.offset[0], pos[1] * scales[1] + self.offset[1]))

    def global_to_local(self, pos):
        if self.parent is None:
            return pos
        scales = (self.size[0] / self.resolution[0], self.size[1] / self.resolution[1])
        return self.parent.global_to_local(((pos[0] - self.offset[0]) / scales[0], (pos[1] - self.offset[1]) / scales[1]))