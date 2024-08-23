import pygame
import numpy as np
from .utils import *

class Object:

    def __init__(self, pos, size, id):
        self.id = id
        self.pos = np.array(pos)
        self.size = np.array(size)
        self.vel = np.array([0.0, 0.0])
        self.is_gravity = False
        self.is_collision = True


    def sprite(self):
        sprite = pygame.Surface(self.size)
        sprite = sprite.convert()
        sprite.fill((0, 0, 0))
        return sprite


    def render(self, screen):
        screen.blit(self.sprite(), self.pos)
        return True
    
    def update(self, keys, others):
        pass
    
    def get_collision_rect(self, other):
        x1, y1 = self.pos
        x2, y2 = self.pos + self.size
        x3, y3 = other.pos
        x4, y4 = other.pos + other.size
        x5 = max(x1, x3)
        y5 = max(y1, y3)
        x6 = min(x2, x4)
        y6 = min(y2, y4)
        return (x5, y5, x6, y6)
    
    
    def is_colliding(self, other):
        return self is not other and \
            self.is_collision and other.is_collision and \
            not is_degenerate_rect(self.get_collision_rect(other))
