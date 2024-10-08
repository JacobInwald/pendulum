import numpy as np
from random import random
from .object import *
from .utils import *
from pygame.locals import *
from time import time

class Player(Object):
    
    def __init__(self, pos, size, id):
        super().__init__(pos, size, id)
        self.is_gravity = True
        self.is_collision = True
        self.speed = 200
        self.update_time = time()
    
    
    def update_movement(self, dir):
        dir = np.array([dir[0], 0])
        self.vel += self.speed * normalize(dir)
        self.vel = clip(self.vel, self.speed)
    
    
    def update_friction(self): self.vel = self.vel * 0.9
    
    
    def update(self, keys, others):
        deltaTime = time() - self.update_time
        self.update_time = time()
        dir = np.array([keys[K_RIGHT] - keys[K_LEFT], 0])
        self.update_movement(dir)
        

        self.pos = self.pos + self.vel * deltaTime
            
        self.update_friction()
        
        if self.is_collision:
            self.update_collision(others)
        
    