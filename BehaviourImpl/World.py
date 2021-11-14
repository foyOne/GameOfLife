import numpy as np
from collections import Counter
import Utils
from Agent import Agent



class World:
    resources = ...
    size = (0, 0) # row, column
    generation = 0
    mentalDamage = 1
    rumors = []
    agents = []
    previousPosition = []
    MPR = 30
    MMR = 15

    def __init__(self, size):
        self.size = size
        self.resources = np.zeros(self.size)
    
    def InitWorld(self, MPR = 30):
        self.MPR = abs(MPR)
        self.UpdateResources(MPR, 0.8)
    
    def initLife(self, count):
        count = min(10, abs(count))
        for _ in range(count):
            self.CreateAgent()
        
    def GetMPR(self):
        return self.MPR
    
    def GenerateUniquePosition(self):
        positionList = []
        for a in self.agents:
            positionList.append(a.GetPosition())
        
        pos = Utils.GetRandomPair(self.size)
        while pos in positionList:
            pos = Utils.GetRandomPair(self.size)
        return pos
    
    def IsCorrectPosition(self, position):
        i, j = position
        _1 = 0 <= i < self.size[0]
        _2 = 0 <= j < self.size[1]
        return _1 or _2
    
    def GetAgentPositions(self):
        positionList = []
        for a in self.agents:
            positionList.append(a.GetPosition())
        return positionList
        
    def CreateAgent(self, sender: Agent = None):
        name = Utils.GetRandomStringValue()
        position = self.GeneratePosition(sender)
        agent = Agent(name, position)
        agent.SetResources((self.MPR // 2, self.MMR))
        agent.world = self
        self.agents.append(agent)
    
    def GeneratePosition(self, agent: Agent = None):
        if agent:
            env = agent.GetIndex(agent.GetPosition())
            for pos in env:
                pos = tuple(pos)
                if self.IsCorrectPosition(pos) and self.IsPositionTaken(pos):
                    return tuple(pos)
        else:
            return self.GenerateUniquePosition()
    
    def IsPositionTaken(self, position):
        position = tuple(position)
        positionList = []
        for a in self.agents:
            positionList.append(a.GetPosition())
        return position in positionList

    def AddAgent(self, agent):
        if self.resources.size >= len(self.agents):
            raise
        agent.world = self
        self.agents.append(agent)
    
    def DeleteAgent(self, agent):
        agent.world = None
        self.agents.remove(agent)
    
    def DeleteAgentByPosition(self, position):
        found = list(filter(lambda o: o.position == position, self.agents))
        if len(found) == 1:
            agent = found[0]
            self.DeleteAgent(agent)
            print('{} deleted'.format(agent))
        else:
            print('There are no agents in this position')
    
    def GetMentalDamage(self):
        return self.mentalDamage
    
    def GetResourcesInPosition(self, position):
        if self.IsCorrectPosition(position):
            return self.resources[position]

    def UpdateResources(self, value = 1, percent = 0.4):
        value = min(abs(value), self.MPR)

        newResources = np.random.randint(0, value + 1, self.size).ravel()
        indexList = np.random.randint(0, newResources.size, int(newResources.size * (1 - percent)))
        newResources[indexList] = 0
        self.resources += np.reshape(newResources, self.size)

        self.resources = np.where(self.resources > self.MPR, self.MPR, self.resources)
    
    def GetCurrentState(self):
        return self.resources
    
    def GetAgentByPosition(self, position):
        agents = []
        for a in self.agents:
            if position == a.GetPosition():
                agents.append(a)
        return agents
    
    def GetIndex(self, position):
        return np.array([[[i - 1, j - 1] for j in range(3)] for i in range(3)]).reshape(9, 2) + position
    

    def WhatIsAround(self, position):
        positionList = self.GetIndex(position)
        resources = dict()
        agents = dict()
        for pos in positionList:
            if self.IsCorrectPosition(pos):
                resources[pos] = self.resources[pos]
                agents[pos] = self.GetAgentByPosition(pos)
            
        return resources, agents


w = World((4, 4))
w.InitWorld()
w.initLife(2)
w.agents[0].resources[0] = 30