import random as random
import numpy as np
import pygame
from pygame.locals import *
from training_game import Game
from time import time
import sys


def convert_to_rgb(val, minval=-1, maxval=+1, colors=[(0, 0, 255), (0, 255, 0), (255, 0, 0)]):
    i_f = float(val-minval) / float(maxval-minval) * (len(colors)-1)
    i, f = int(i_f // 1), i_f % 1
    
    if f < sys.float_info.epsilon:
        return colors[i]
    else:
        (r1, g1, b1), (r2, g2, b2) = colors[i], colors[i+1]
        return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))

def new_network():
    w1 = (np.random.rand(3, 3) - 0.5) * 1e-3
    w2 = (np.random.rand(2, 3) - 0.5) * 1e-3
    return w1, w2

def feed_forward(inp, w1, w2, display=False):
    hid = np.dot(w1, inp)
    o_hid = np.tanh(hid)
    out = np.dot(w2, o_hid)
    o_out = np.tanh(out)
    o_out[0] = 0 if o_out[0] < 0 else 1
    o_out[1] = 0 if o_out[1] < 0 else 1
    o_out = {K_LEFT: int(o_out[0]), K_RIGHT: int(o_out[1])}
    
    if display:
        
        cap = 5e-1
        
        surf = pygame.Surface((200, 100))
        surf.fill((240, 240, 240))
        
        if (np.abs(w1) > cap).any():
            cap = int(np.max(np.abs(w1))) + 1
        if (np.abs(w2) > cap).any():
            cap = int(np.max(np.abs(w2))) + 1
            
        # First layer Weights
        pygame.draw.line(surf, convert_to_rgb(w1[0][0], maxval=cap+0.1, minval=-cap-0.1), (20, 20), (80, 20), width=2)
        pygame.draw.line(surf, convert_to_rgb(w1[0][1], maxval=cap+0.1, minval=-cap-0.1), (20, 20), (80, 50), width=2)
        pygame.draw.line(surf, convert_to_rgb(w1[0][2], maxval=cap+0.1, minval=-cap-0.1), (20, 20), (80, 80), width=2)
        
        pygame.draw.line(surf, convert_to_rgb(w1[1][0], maxval=cap+0.1, minval=-cap-0.1), (20, 50), (80, 20), width=2)
        pygame.draw.line(surf, convert_to_rgb(w1[1][1], maxval=cap+0.1, minval=-cap-0.1), (20, 50), (80, 50), width=2)
        pygame.draw.line(surf, convert_to_rgb(w1[1][2], maxval=cap+0.1, minval=-cap-0.1), (20, 50), (80, 80), width=2)
        
        pygame.draw.line(surf, convert_to_rgb(w1[2][0], maxval=cap+0.1, minval=-cap-0.1), (20, 80), (80, 20), width=2)
        pygame.draw.line(surf, convert_to_rgb(w1[2][1], maxval=cap+0.1, minval=-cap-0.1), (20, 80), (80, 50), width=2)
        pygame.draw.line(surf, convert_to_rgb(w1[2][2], maxval=cap+0.1, minval=-cap-0.1), (20, 80), (80, 80), width=2)
        
        # Second layer Weights
        pygame.draw.line(surf, convert_to_rgb(w2[0][0], maxval=cap+0.1, minval=-cap-0.1), (140, 35), (80, 20), width=2)
        pygame.draw.line(surf, convert_to_rgb(w2[0][1], maxval=cap+0.1, minval=-cap-0.1), (140, 35), (80, 50), width=2)
        pygame.draw.line(surf, convert_to_rgb(w2[0][2], maxval=cap+0.1, minval=-cap-0.1), (140, 35), (80, 80), width=2)
        
        pygame.draw.line(surf, convert_to_rgb(w2[1][0], maxval=cap+0.1, minval=-cap-0.1), (140, 65), (80, 20), width=2)
        pygame.draw.line(surf, convert_to_rgb(w2[1][1], maxval=cap+0.1, minval=-cap-0.1), (140, 65), (80, 50), width=2)
        pygame.draw.line(surf, convert_to_rgb(w2[1][2], maxval=cap+0.1, minval=-cap-0.1), (140, 65), (80, 80), width=2)
        
        
        # Layer 1 Circles
        pygame.draw.circle(surf, (10, 10, 10), (20, 20), 12, width=0)
        pygame.draw.circle(surf, (10, 10, 10), (20, 50), 12, width=0)
        pygame.draw.circle(surf, (10, 10, 10), (20, 80), 12, width=0)
        # Layer 2 Circles
        pygame.draw.circle(surf, (10, 10, 10), (80, 20), 12, width=0)
        pygame.draw.circle(surf, (10, 10, 10), (80, 50), 12, width=0)
        pygame.draw.circle(surf, (10, 10, 10), (80, 80), 12, width=0)
        
        # Layer 3 Circles
        pygame.draw.circle(surf, (10, 10, 10), (140, 35), 12, width=0)
        pygame.draw.circle(surf, (10, 10, 10), (140, 65), 12, width=0)
        
        
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
    
    return o_out

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
        self.size = self.width, self.height = 640, 350
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
        
        title_str = f"Generation Number {self.gen_num} | Size: {len(self.gen)} | Prev Best: {self.best_fitness:.2f}"
        frame_st = time()
        while any_running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                
            self.fitness = [frame_count / 60 if game._running else self.fitness[i] for i, game in enumerate(games)]
            
            self.screen.blit(background, (0, 0))
            
            for i, game in enumerate(games):
                if game._running:
                    game.run_step(feed_forward(game.inputs(), *self.gen[i]))
            
                    
            any_running = any(game._running for game in games)
            
            self.screen.blit(*self.title(title_str + f" | Current Best: {(frame_count / 60):.2f} | Frame: {frame_count} | FPS: {(1 / (time() - frame_st)):.2f}"))
            frame_st = time()

            # Show the best ones network
            best = self.gen[np.argmax(self.fitness)]
            surf = feed_forward(games[np.argmax(self.fitness)].inputs(), *best, display=True)
            self.screen.blit(surf, (420, 40))
            
            
            pygame.display.flip()
            frame_count += 1
            
        self.gen_num += 1
    
    
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