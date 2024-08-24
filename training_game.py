import pygame
from pygame.locals import *
import numpy as np
from random import random
from objects import *
import time as time

class Game:

    def __init__(self, screen, size, alpha=None):
        self._running = True
        self.size = self.width, self.height = size
        
        self.screen = screen
        self.alpha = alpha
        self.alpha_screen = pygame.Surface(self.size)
        self.alpha_screen = self.alpha_screen.convert()
        self.alpha_screen.fill((0, 0, 0))
        self.alpha_screen.set_alpha(alpha)
        # player variables
        self.player = Player([320.0, 300.0], [50.0, 10.0], '_player')
        self.pendulum = Pendulum([320.0, 100.0], [10, 10], '_pendulum', self.player)
        
        self.mouse_circle = Object([0, 0], [40, 40], '_mouse')
        self.mouse_circle.is_collision = False
        
        l_wall = Object([-10, 0], [10, self.height], '_l_wall')
        r_wall = Object([self.width, 0], [10, self.height], '_r_wall')
        self.objects = [self.player, self.pendulum, self.mouse_circle, l_wall, r_wall]

    
    def inputs(self):
        return np.array([self.player.pos[0], self.pendulum.pos[0], self.pendulum.pos[1]])
    
    
    def render(self):
        # self.alpha = None
        if self.alpha:
            self.alpha_screen.fill((240, 240, 240))
            # self.alpha_screen.set_alpha(self.alpha)
            for obj in self.objects:
                obj.render(self.alpha_screen)
            self.screen.blit(self.alpha_screen, (0, 0))
        else:
            for obj in self.objects:
                obj.render(self.screen)
        
        
    def update(self, inp):
        for obj in self.objects:
            obj.update(inp, self.objects)
        
                    
    def run_step(self, inp={K_LEFT: 0, K_RIGHT: 0}):
        self.pendulum.is_collision = pygame.mouse.get_pressed()[0]
        self.mouse_circle.is_render = pygame.mouse.get_pressed()[0]
        self.mouse_circle.is_collision = pygame.mouse.get_pressed()[0]
        self.mouse_circle.pos = np.array(pygame.mouse.get_pos()) - self.mouse_circle.size / 2

        self.update(inp)
        
        self.render()
        
        
        if self.pendulum.pos[1] > self.player.pos[1] + 40:
            self._running = False
            return False
        
        return True