import typing
import numpy as np
from collections import Counter
from IAgent import IAgent
import Utils
from AgentList import Herbivorous
from enum import Enum, auto



class World:
    resources = ...
    size = (0, 0) # row, column
    generation = 0
    rumors = []
    agents = []
    resourceAction = []
    MaxPhysical = 10
    MaxMental = 10

    def __init__(self, size):
        self.size = size
        self.resources = np.zeros(self.size, dtype=np.uint8)
    
    def InitWorld(self, MPR = 10):
        self.MaxPhysical = abs(MPR)
        self.UpdateResources(self.MaxPhysical // 2, 0.8)
    
    def InitLife(self, count):
        maxLife = int(self.resources.size * 0.6)
        count = min(maxLife, abs(count))
        for _ in range(count):
            self.CreateAgent()
        
    def GetMPR(self):
        return self.MaxPhysical
    
    def GenerateUniquePosition(self):
        positionList = self.GetAgentPositions()
        if len(positionList) == self.resources.size:
            return None
        pos = Utils.GetRandomPair(self.size)
        while pos in positionList:
            pos = Utils.GetRandomPair(self.size)
        return pos
    
    def IsCorrectPosition(self, position):
        i, j = position
        _1 = 0 <= i < self.size[0]
        _2 = 0 <= j < self.size[1]
        return _1 and _2
    
    def GetAgentPositions(self):
        positionList = []
        for a in self.agents:
            positionList.append(a.GetPosition())
        return positionList
        
    def CreateAgent(self, sender: IAgent = None):
        name = Utils.GetRandomStringValue()
        position = self.GeneratePosition(sender)
        if position is None:
            return
        agent = None
        if sender:
            agent = type(sender)(name, position)
        else:
            agent = self.CreateRandomAgent(name, position)
        agent.SetResources((self.MaxPhysical // 2, self.MaxMental))
        agent.world = self
        self.AddAgent(agent)
    
    def CreateRandomAgent(self, name, position):
        return Herbivorous(name, position)
    
    def GeneratePosition(self, agent: IAgent = None):
        if agent:
            env = self.GetIndex(agent.GetPosition())
            for pos in env:
                pos = tuple(pos)
                if self.IsCorrectPosition(pos) and not self.IsPositionTaken(pos):
                    return tuple(pos)
        else:
            return self.GenerateUniquePosition()
        return None
    
    def IsPositionTaken(self, position):
        position = tuple(position)
        positionList = self.GetAgentPositions()
        return position in positionList

    def AddAgent(self, agent):
        if len(self.agents) == self.resources.size:
            agent.world = None
            return
        agent.world = self
        self.agents.append(agent)
    
    def DeleteAgent(self, agent):
        agent.world = None
        self.agents.remove(agent)
    
    def GetResourcesInPosition(self, position):
        if self.IsCorrectPosition(position):
            i, j = position
            return self.resources[i, j]

    def UpdateResources(self, value = 1, percent = 0.5):
        value = min(abs(value), self.MaxPhysical)

        newResources = np.random.randint(0, value + 1, self.size).ravel()
        indexList = np.random.randint(0, newResources.size, int(newResources.size * (1 - percent)))
        newResources[indexList] = 0
        self.resources += np.reshape(newResources.astype(dtype=np.uint8), self.size)

        self.resources = np.where(self.resources > self.MaxPhysical, self.MaxPhysical, self.resources)
    
    def GetCurrentState(self):
        return self.resources, self.agents
    
    def GetAgentsByPosition(self, position):
        agents = []
        position = tuple(position)
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
            pos = tuple(pos)
            if self.IsCorrectPosition(pos):
                resources[pos] = self.resources[pos]
                agents[pos] = self.GetAgentsByPosition(pos)
            
        return resources, agents
    
    def GetResourceFromPosition(self, position):
        if self.IsCorrectPosition(position):
            return self.resources[position]
    
    def AddResourceAction(self, action):
        self.resourceAction.append(action)
    
    def CheckWorld(self):
        return np.where(self.resources < 0)[0].size > 0
    
    def CheckPositionUniqueness(self):
        posotionList = self.GetAgentPositions()
        return len(posotionList) == len(set(posotionList))


    def MakeIteration(self):
        agentList = list(self.agents)
        for a in agentList:
            a.Exist()
        
        self.resourceAction = list(set(self.resourceAction))
        while self.resourceAction:
            resAction = self.resourceAction.pop()
            self.resources[resAction[0]] -= resAction[1]
        self.resourceAction = []
        
        if self.CheckWorld():
            raise

        self.UpdateResources(1, 0.1)

        dead = list(filter(lambda x: x.state == IAgent.State.dead, self.agents))

        for d in dead:
            self.DeleteAgent(d)
        
        self.generation += 1
        return bool(self.agents)
    

# w = World((25, 25))
# w.InitWorld()
# w.InitLife(2)
# while True:

#     print(w.generation, len(w.agents))
#     # print(w.CheckPositionUniqueness())
#     # print(w.agents)
#     # print(w.resources)
#     w.MakeIteration()