from abc import ABC, abstractmethod
from Agent import Agent

class IBehaviour(ABC):

    def __init__(self, name, world):
        self.name = name
        self.world = world

    def GetName(self):
        return self.name
        
    @abstractmethod
    def Exist(self, sender: Agent, parameter = None):
        ...
    
    @abstractmethod
    def Move(self, sender: Agent):
        ...
    
    @abstractmethod
    def Action(self, sender: Agent):
        ...