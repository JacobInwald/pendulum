import random as random
import numpy as np
import pygame
from pygame.locals import *
from training_game import Game
from time import time
import sys


def convert_to_rgb(val, minval=-1, maxval=+1, colors=[(0, 255, 0), (255, 0, 0)]):
    i_f = float(val-minval) / float(maxval-minval) * (len(colors)-1)
    i, f = int(i_f // 1), i_f % 1
    
    if f < sys.float_info.epsilon:
        return colors[i]
    else:
        (r1, g1, b1), (r2, g2, b2) = colors[i], colors[i+1]
        return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))

def new_network(struct):
    w1 = (np.random.rand(struct[1], struct[0]) - 0.5) * 1e-3
    w2 = (np.random.rand(struct[2], struct[1]) - 0.5) * 1e-3
    return w1, w2


def feed_forward(inp, w1, w2, display=False):
    hid = np.dot(w1, inp)
    o_hid = np.tanh(hid)
    out = np.dot(w2, o_hid)
    o_out = np.tanh(out)
    o_out[0] = 0 if o_out[0] < 0 else 1
    o_out[1] = 0 if o_out[1] < 0 else 1
    o_out = {K_LEFT: int(o_out[0]), K_RIGHT: int(o_out[1])}
    return o_out


def display(w1, w2):
    cap = 1e-3
    
    surf = pygame.Surface((200, 40+20*len(w1[0])+10))
    surf.fill((240, 240, 240))
    
    if (np.abs(w1) > cap).any():
        cap = (int(np.max(np.abs(w1))*100) + 1) / 100
    if (np.abs(w2) > cap).any():
        cap = (int(np.max(np.abs(w2))*100) + 1) / 100
        

    # Weights
    for i in range(len(w1)):
        for j in range(len(w1[i])):
            pygame.draw.line(surf, convert_to_rgb(w1[i][j], -cap, cap), (20, 20 + 20 * i), (80, 20 + 20 * j), width=2)
    
    for i in range(len(w2)):
        for j in range(len(w2[i])):
            pygame.draw.line(surf, convert_to_rgb(w1[i][j], -cap, cap), (80, 20 + 20 * j), (140, 30 + 20 * (i + len(w1[0]) // 2 - 1)), width=2)
    

    # Layer 1 Circles
    for i in range(len(w1[0])):
        pygame.draw.circle(surf, (10, 10, 10), (20, 20 + 20 * i), 8, width=0)
    
    # Layer 2 Circles
    for i in range(len(w1[1])):
        pygame.draw.circle(surf, (10, 10, 10), (80, 20 + 20 * i), 8, width=0)
        
    # Layer 3 Circles
    for i in range(2):
        pygame.draw.circle(surf, (10, 10, 10), (140, 30 + 20 * (i + len(w1[0]) // 2 - 1)), 8, width=0)
    
    
    
    
    # Heatmap Key
    font = pygame.font.Font(None, 20)
    textSurface = font.render(f"-{cap}", 1, (0, 0, 255))
    textSurface1 = font.render("0", 1, (0, 255, 0))
    textSurface2 = font.render(f"{cap}", 1, (255, 0, 0))
    textRect = textSurface.get_rect()
    textRect1 = textSurface1.get_rect()
    textRect2 = textSurface2.get_rect()
    textRect.center = (180, 80)
    textRect1.center = (180, 50)
    textRect2.center = (180, 20)
    surf.blit(textSurface, textRect)
    surf.blit(textSurface1, textRect1)
    surf.blit(textSurface2, textRect2)
    
    
    return surf


def merge(w_1,  w_2, lr=1e-6, cap=1):
    w1_1, w2_1 = w_1
    w1_2, w2_2 = w_2
    
    w1 = w1_1 - w1_2 * lr
    w2 = w2_1 - w2_2 * lr
    
    if np.max(np.abs(w1)) > cap:
        w1 = w1 / np.max(np.abs(w1)) * cap
    if np.max(np.abs(w2)) > cap:
        w2 = w2 / np.max(np.abs(w2)) * cap
    
    return w1, w2




class GeneticTraining:
    
    def __init__(self, gen_size, mutation_rate, mutation_size, num_pendulums=1):
        # Genetic Algorithm Parameters
        self.gen_size = gen_size
        self.mutation_rate = mutation_rate
        self.mutation_size = mutation_size
        self._running = True
        self.size = self.width, self.height = 640, 350
        self.screen = pygame.display.set_mode(self.size)

        # Game Parameters
        self.num_pends = num_pendulums
        self.struct = [self.num_pends * 2 + 1,
                       self.num_pends * 2 + 1,
                       2]
        
        # Neural Network Parameters
        self.gen = [new_network(self.struct) for _ in range(gen_size)]
        self.fitness = [0 for _ in range(gen_size)]
        self.best = None
        self.best_fitness = 0
        self.generation = 0
        
        pygame.init()
        
    
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
        games = [Game(self.screen, self.size, num_pends=self.num_pends) for _ in self.gen]
        any_running = True
        frame_count = 0
        
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((240, 240, 240))
        
        title_str = f"Generation Number {self.generation} | Size: {len(self.gen)} | Prev Best: {self.best_fitness:.2f}"
        frame_st = time()
        while any_running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                
            self.fitness = [frame_count / 60 if game._running else self.fitness[i] for i, game in enumerate(games)]
            
            self.screen.blit(background, (0, 0))
            best = self.gen[np.argmax(self.fitness)]
            surf = display(*best)
            self.screen.blit(surf, (420, 40))
            
            for i, game in enumerate(games):
                if game._running:
                    game.run_step(feed_forward(game.inputs(), *self.gen[i]))
            
                    
            any_running = any(game._running for game in games)
            
            self.screen.blit(*self.title(title_str + f" | Current Best: {(frame_count / 60):.2f} | Frame: {frame_count} | FPS: {(1 / (time() - frame_st)):.2f}"))
            frame_st = time()

            # Show the best ones network
            best = self.gen[np.argmax(self.fitness)]
            surf = display(*best)
            self.screen.blit(surf, (420, 40))
            
            
            pygame.display.flip()
            frame_count += 1
            
        self.generation += 1
    
    
    def mutate(self, w1, w2):
        n_w1, n_w2 = new_network(self.struct)
        return w1 + n_w1, w2 + n_w2
    
    
    def evolve(self):
        self.best = self.gen[np.argmax(self.fitness)]
        self.best_fitness = max(self.fitness)
        self.gen = [self.best]
        self.gen += [merge(self.best, random.choice(self.gen)) for _ in range(self.gen_size - 1)]
        self.gen = [self.mutate(w1, w2) for w1, w2 in self.gen]
    
    
    def run(self, epochs):
        for _ in range(epochs):
            self.run_generation()
            self.evolve()
            print(f"Generation {self.generation} best fitness: {self.best_fitness}")
        

        

g = GeneticTraining(250, 0.1, 1e-2, 2)
g.run(100)