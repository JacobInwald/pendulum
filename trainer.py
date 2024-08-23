import random as random
import numpy as np
import pygame
from pygame.locals import *
from training_game import Game
from time import time
import sys

def new_network():
    w1 = (np.random.rand(3, 3) - 0.5) * 1e-3
    w2 = (np.random.rand(2, 3) - 0.5) * 1e-3
    return w1, w2

def feed_forward(inp, w1, w2):
    hid = np.dot(w1, inp)
    hid = np.tanh(hid)
    out = np.dot(w2, hid)
    out = np.tanh(out)
    out[0] = 0 if out[0] < 0 else 1
    out[1] = 0 if out[1] < 0 else 1
    out = {K_LEFT: int(out[0]), K_RIGHT: int(out[1])}
    return out

def merge(w_1,  w_2):
    w1_1, w2_1 = w_1
    w1_2, w2_2 = w_2
    
    w1 = w1_1 + w1_2 / 2
    w2 = w2_1 + w2_2 / 2
    return w1, w2


class GeneticTraining:
    
    def __init__(self, gen_size, mutation_rate, mutation_size):
        self.gen_size = gen_size
        self.mutation_rate = mutation_rate
        self.mutation_size = mutation_size
        self.gen = [new_network() for _ in range(gen_size)]
        self.fitness = [0 for _ in range(gen_size)]
        self.best = None
        self.best_fitness = 0
        self.generation = 0
        self.gen_num = 1
        pygame.init()
        self._running = True
        self.size = self.width, self.height = 640, 480
        self.screen = pygame.display.set_mode(self.size)
    
    def check_quit(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
    
    
    def title(self, string):
        font = pygame.font.Font(None, 20)
        textSurface = font.render(string , 1, (10, 10, 10))
        textRect = textSurface.get_rect()
        textRect.center = (self.width // 2, 20)
        return textSurface, textRect
    
    def run_generation(self):
        games = [Game(self.screen, self.size) for _ in self.gen]
        any_running = True
        frame_count = 0
        
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((240, 240, 240))
        
        title_str = f"Generation Number {self.gen_num} | Size: {len(self.gen)} | Prev Best: {self.best_fitness}"
        frame_st = time()
        while any_running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                
            self.fitness = [frame_count / 60 if game._running else self.fitness[i] for i, game in enumerate(games)]
            
            self.screen.blit(background, (0, 0))
            
            self.screen.blit(*self.title(title_str + f" | Frame: {frame_count} | FPS: {(1 / (time() - frame_st)):.2f}"))
            frame_st = time()
            for i, game in enumerate(games):
                if game._running:
                    game.run_step(feed_forward(game.inputs(), *self.gen[i]))
            
                    
            any_running = any(game._running for game in games)
            
            pygame.display.flip()
            frame_count += 1
            
        self.gen_num += 1
        # pygame.quit()
    
    
    def mutate(self, w1, w2):
        w1 = w1 + (np.random.rand(3, 3) - 0.5) * self.mutation_size
        w2 = w2 + (np.random.rand(2, 3) - 0.5) * self.mutation_size
        return w1, w2
    
    
    def evolve(self):
        self.best = self.gen[np.argmax(self.fitness)]
        self.best_fitness = max(self.fitness)
        self.gen = [self.best]
        self.gen += [merge(self.best, random.choice(self.gen)) for _ in range(self.gen_size - 1)]
        self.gen = [self.mutate(w1, w2) for w1, w2 in self.gen]
        self.generation += 1
    
    
    def run(self, epochs):
        for _ in range(epochs):
            self.run_generation()
            self.evolve()
            print(f"Generation {self.generation} best fitness: {self.best_fitness}")
        

        

g = GeneticTraining(100, 0.1, 0.1)
g.run(100)