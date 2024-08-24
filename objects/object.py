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
        self.is_render = True


    def render(self, screen):
        if self.is_render:
            pygame.draw.rect(screen, (10, 10, 10), pygame.Rect(*self.pos, *self.size))
        return True
    
    def update(self, keys, others):
        pass
    
    
    def update_collision(self, others):
        for other in others:
            if self.is_colliding(other):
                self.resolve_collision(other)
    
    def resolve_collision(self, other):
        if not self.is_colliding(other):
            return
        
        collision_right = self.pos[0] + self.size[0] - other.pos[0]
        collision_left = other.pos[0] + other.size[0] - self.pos[0]
    
        if collision_right < collision_left:
            self.pos[0] = other.pos[0] - self.size[0] - 1
            self.vel[0] = - np.abs(self.vel[0])
        elif collision_left < collision_right:
            self.pos[0] = other.pos[0] + other.size[0] + 1
            self.vel[0] = np.abs(self.vel[0])
        
        
    
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
            
    
