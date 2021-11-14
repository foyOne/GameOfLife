import numpy as np
import collections
from enum import Enum, auto
from abc import ABC
import Utils

class State(Enum):
    alive = auto()
    dead = auto()

class Agent:
    
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.state = State.alive
    
    def SetResources(self, resources):
        self.resources = list(resources)
    
    def SetWorld(self, world):
        self.world = world
    
    def GetPosition(self):
        return self.position
    
    def SetBehavior(self, behavior):
        self.behavior = behavior
    
    def Exist(self):
        self.behavior.Exist()
    
    def CreateChild(self):
        percent = 0.8
        if self.resources[0] > int(self.world.GetMPR() * percent):
            self.resources[0] *= (1 - percent)
            self.world.CreateAgent(self)

    def GetIndex(self, position):
        return np.array([[[i - 1, j - 1] for j in range(3)] for i in range(3)]).reshape(9, 2) + position

    def WhatIsAround(self):
        positionList = self.GetIndex(self.position)
        values = []
        for pos in positionList:
            values.append(self.TryValue(pos))
        return np.array(values).reshape(3, 3)
    
    def TryValue(self, position):
        i, j = position

        if i < 0 or j < 0:
            return 0
        
        if i > self.world.size[0] - 1 or j > self.world.size[1] - 1:
            return 0

        return self.world.resources[i, j]
    
    def __str__(self) -> str:
        return '\r\nagent {}... with pos = {}'.format(self.name[:8], self.position)
    
    def __repr__(self) -> str:
        return '\r\nagent {}... with pos = {}'.format(self.name[:8], self.position)


