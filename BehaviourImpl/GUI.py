import pygame
import numpy as np
from World import World
from itertools import product


class PyGameGUI():

    def __init__(self, resolution, tile):
        self.resolution = resolution # (WIDTH, HEIGHT)
        self.tile = tile
        self.row = resolution[1] // tile
        self.col = resolution[0] // tile
    
    def Init(self):
        pygame.init()
        self.Surface = pygame.display.set_mode(self.resolution)
        self.Clock = pygame.time.Clock()

        self.game = World((self.row, self.col))
        self.game.InitWorld()
        self.game.InitLife(2)
    
    def Tune(self, settings: dict):
        self.FPS = settings['FPS']
    
    def Paint(self, position, color, agent=False):
        i, j = position
        if agent:
            a, b = j * self.tile + self.tile // 4, i * self.tile + self.tile // 4
            c, d = self.tile // 2, self.tile // 2
        else:
            a, b = j * self.tile, i * self.tile
            c, d = self.tile, self.tile
        pygame.draw.rect(self.Surface, pygame.Color(color), (a, b, c, d))

    def GameProcess(self):
        print(self.game.generation)

        res, agents = self.game.GetCurrentState() 
        for i, j in product(range(self.row), range(self.col)):
            color = (0, 255 * res[i, j] // self.game.MaxPhysical, 0)
            self.Paint((i, j), color)
        
        for a in agents:
            i, j = a.GetPosition()
            color = a.GetRGBColor()
            self.Paint((i, j), color, True)
        
        self.game.MakeIteration()
        
    
    def CreateGrid(self):
        [pygame.draw.line(self.Surface, pygame.Color('white'), (x, 0), (x, self.resolution[1])) for x in range(0, self.resolution[0], self.tile)]
        [pygame.draw.line(self.Surface, pygame.Color('white'), (0, y), (self.resolution[0], y)) for y in range(0, self.resolution[1], self.tile)]
    
    def Run(self):
        while True:
            self.Surface.fill(pygame.Color('black'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            self.CreateGrid()
            self.GameProcess()

            pygame.display.flip()
            self.Clock.tick(self.FPS)


gui = PyGameGUI((800, 800), 32)
gui.Init()
gui.Tune({ 'FPS': 30 })
gui.Run()