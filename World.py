import numpy as np
from collections import Counter

from numpy.random.mtrand import f
from Agent import SimpleAgent
import Utils

class World:
    world = ...
    size = (0, 0) # row, column
    generation = 0
    mentalDamage = 0
    rumors = []
    agents = []

    def __init__(self, size):
        self.size = size
        self.world = np.zeros(self.size, dtype=np.uint8)
    
    def InitWorld(self):
        self.UpdatePhysicalResource()
    
    def initLife(self, count):
        if count > self.world.size:
            raise
        for _ in range(count):
            self.CreateAgent()
    
    def GenerateUniquePosition(self):
        positionList = []
        for a in self.agents:
            positionList.append(a.GetPosition())
        
        pos = Utils.GetRandomPair(self.size)
        while pos in positionList:
            pos = Utils.GetRandomPair(self.size)
        return pos
    
    def GetAgentPositions(self):
        positionList = []
        for a in self.agents:
            positionList.append(a.GetPosition())
        return positionList
        
    def CreateAgent(self):
        name = Utils.GetRandomStringValue()
        position = self.GenerateUniquePosition()
        agent = SimpleAgent(name, position)
        agent.world = self
        self.agents.append(agent)
        
    def AddAgent(self, agent):
        if self.world.size >= len(self.agents):
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
    
    def GetPhysicalResource(self, position):
        return self.world[position]
    

    def UpdatePhysicalResource(self):
        self.world = np.random.random_integers(0, 20, self.size)
    
    def GetCurrentState(self):
        return self.world