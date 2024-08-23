import pygame
from pygame.locals import *
import numpy as np
from random import random
from objects import *
import time as time

class Game:

    def __init__(self, screen, size):
        pygame.init()
        self._running = True
        self.size = self.width, self.height = size
        
        self.screen = screen
        
        # player variables
        self.player = Player([320.0, 300.0], [50.0, 10.0], '_player')
        self.pendulum = Pendulum([320.0, 100.0], [10, 10], '_pendulum', self.player)
        
        l_wall = Object([-10, 0], [10, self.height], '_l_wall')
        r_wall = Object([self.width, 0], [10, self.height], '_r_wall')
        self.objects = [self.player, self.pendulum, l_wall, r_wall]

    
    def inputs(self):
        return np.array([self.player.pos[0], self.pendulum.pos[0], self.pendulum.pos[1]])
    
    
    def render(self):
        for obj in self.objects:
            obj.render(self.screen)
        
        
    def update(self, inp):
        for obj in self.objects:
            obj.update(inp, self.objects)
        
                    
    def run_step(self, inp={K_LEFT: 0, K_RIGHT: 0}):
        self.update(inp)
                
        self.render()
        
        if self.pendulum.pos[1] > self.player.pos[1] + 40:
            self._running = False
            return False
        
        return True