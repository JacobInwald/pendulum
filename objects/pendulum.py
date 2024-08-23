import numpy as np
from random import random
from .object import *
from .utils import *
import pygame

   
class Pendulum(Object):
    
    def __init__(self, pos, size, id, root):
        super().__init__(pos, size, id)
        self.is_gravity = True
        self.is_collision = False
        self.root = root
        self.length = 100
        self.mass = 1
        self.vel = np.array([.0, .0])
        self.pos = self.r_pos() + clip(np.array([((random() > 0.5) * 2 - 1) * 3, -self.length]), self.length)
    
    def r_pos(self):
        return self.root.pos + self.root.size / 2
    
    def update(self, keys, others):
        self.pos = self.r_pos() + self.length * normalize(self.pos - self.r_pos())
        
        tangential = self.pos - self.r_pos()
        tangential = normalize(np.array([tangential[1], -tangential[0]]))
        if self.r_pos()[0] < self.pos[0]:
            tangential = -tangential

        self.vel += np.array([0.0, 0.03])
        self.vel = np.dot(self.vel, tangential) * tangential
        self.vel = self.vel * 0.999
        self.pos += self.vel
    
    def sprite(self):
        sprite = pygame.Surface(self.size)
        sprite = sprite.convert()
        sprite.fill((0, 0, 0))
        sprite.set_alpha(25)
        return sprite
    
    def render(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), self.pos, 10)
        pygame.draw.line(screen, (0, 0, 0, 25), self.r_pos(), self.pos, 3)
        # screen.blit(self.sprite(), self.pos)
        return True