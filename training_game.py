import pygame
from pygame.locals import *
import numpy as np
from random import random
from objects import *
import time as time

class Game:

    def __init__(self, screen, size, num_pends=1, alpha=None):
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
        self.objects = [self.player]
        
        for i in range(num_pends):
            self.objects.append(Pendulum([320.0, 100.0], [10, 10], f'_pendulum_{i}', self.objects[i]))
        
        self.mouse_circle = Object([0, 0], [40, 40], '_mouse')
        self.mouse_circle.is_collision = False
        
        l_wall = Object([-10, 0], [10, self.height], '_l_wall')
        r_wall = Object([self.width, 0], [10, self.height], '_r_wall')
        
        self.objects.extend([self.mouse_circle, l_wall, r_wall])

    
    def inputs(self):
        inps = [self.player.pos[0]]
        for obj in self.objects[1:-3]:
            inps.extend([obj.pos[0], obj.pos[1]])
        return np.array(inps)
    
    
    def render(self):
        if self.alpha:
            self.alpha_screen.fill((240, 240, 240))
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
        for obj in self.objects[1:-3]:
            obj.is_collision = pygame.mouse.get_pressed()[0] 
        self.mouse_circle.is_render = pygame.mouse.get_pressed()[0]
        self.mouse_circle.is_collision = pygame.mouse.get_pressed()[0]
        self.mouse_circle.pos = np.array(pygame.mouse.get_pos()) - self.mouse_circle.size / 2

        self.update(inp)
        
        self.render()
        
        pends = self.objects[1:-3]
        for i in range(len(pends)):
            if self.objects[i+1].pos[1] > self.objects[i].pos[1] + 20:
                self._running = False
                return False
        
        return True