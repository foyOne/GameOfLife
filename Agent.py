import numpy as np
import collections
from enum import Enum, auto
from abc import ABC


class State(Enum):
    alive = auto()
    dead = auto()



class Agent:
    
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.resource = (0, 0)
        self.state = State.alive
    
    def SetResource(self, resource):
        ...
    
    def SetWorld(self, world):
        self.world = world
    
    def GetPosition(self):
        return self.position
    
    def SetBehavior(self, behavior):
        self.behavior = behavior
    
    def GetInfoAbout(self, position):
        ...
    
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

        return self.world.world[i, j]
    
    def GetOtherAgents(self):
        agentPositions = self.world.GetAgentPositions()
        agentPositions.remove(self.position)
        return agentPositions
    
    def live(self):
        info = self.world.WhatIsAround(self.position)
        print(info)
    
    def __str__(self) -> str:
        return '\r\nagent {}... with pos = {}'.format(self.name[:8], self.position)
    
    def __repr__(self) -> str:
        return '\r\nagent {}... with pos = {}'.format(self.name[:8], self.position)


