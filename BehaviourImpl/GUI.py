import pygame
import numpy as np
import World



class PyGameGUI():

    def __init__(self, resolution, tile):
        self.resolution = resolution # (WIDTH, HEIGHT)
        self.tile = tile
        self.row = resolution[0] // tile
        self.col = resolution[1] // tile
    
    def Init(self):
        pygame.init()
        self.Surface = pygame.display.set_mode(self.resolution)
        self.Clock = pygame.time.Clock()

        self.game = SimpleLife.SimpleLife((self.row, self.col))
        self.game.Init()
    
    def Tune(self, settings: dict):
        self.FPS = settings['FPS']
    
    def Paint(self, position, color):
        i, j = position
        a, b = i * self.tile + self.tile // 4, j * self.tile + self.tile // 4
        c, d = self.tile // 2, self.tile // 2
        pygame.draw.rect(self.Surface, pygame.Color(color), (a, b, c, d))

    def GameProcess(self):
        current = self.game.GetCurrent()
        nz = np.nonzero(current)
        for i, j in zip(nz[0], nz[1]):
            self.Paint((i, j), 'green')
        
        self.game.Update()
    
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

            # print(self.Clock.get_fps())
            pygame.display.flip()
            self.Clock.tick(self.FPS)


gui = PyGameGUI((1200, 600), 50)
gui.Init()
gui.Tune({ 'FPS': 10 })
gui.Run()