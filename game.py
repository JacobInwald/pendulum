import pygame
from pygame.locals import *
import numpy as np
from random import random
from objects import *
import time as time

class Game:

    def __init__(self, size):
        pygame.init()
        self._running = True
        self.size = self.width, self.height = size
        
        self.screen = pygame.display.set_mode(self.size)
        
        # player variables
        self.player = Player([320.0, 300.0], [50.0, 10.0], '_player')
        self.pendulum = Pendulum([320.0, 100.0], [10, 10], '_pendulum', self.player)
        
        l_wall = Object([-10, 0], [10, self.height], '_l_wall')
        r_wall = Object([self.width, 0], [10, self.height], '_r_wall')
        self.objects = [self.player, self.pendulum, l_wall, r_wall]


    def background(self):
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        colour = (240, 240, 240)
        if self.pendulum.pos[1] > self.player.pos[1] + 20:
            colour = (255, 0, 0)
        background.fill(colour)
        return background
    
    
    def render(self):
        self.screen.blit(self.background(), (0, 0))
        for obj in self.objects:
            obj.render(self.screen)
        pygame.display.flip()
        
        
    def update(self):
        keys = pygame.key.get_pressed()
        for obj in self.objects:
            obj.update(keys, self.objects)
        
        
    def check_quit(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
                    
    def run_step(self):
        fail_timer = 2
        then = 0
        
        self.check_quit()
        
        self.update()
                
        self.render()
        
        if self.pendulum.pos[1] > self.player.pos[1] + 20:
            if then == 0:
                then = time.time()
                
            fail_timer -= time.time() - then
            then = time.time()
            if fail_timer <= 0:
                self._running = False
        else:
            fail_timer = 2
            then = 0
    
    def run(self):
        while self._running:
            self.run_step()
            pygame.display.flip()
        pygame.quit()
            
g = Game((640, 480))
g.run()
