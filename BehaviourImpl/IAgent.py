from typing import NamedTuple
import numpy as np
import collections
from enum import Enum, auto
from abc import ABC, abstractmethod
import Utils


class IAgent(ABC):
    class State(Enum):
        alive = auto()
        dead = auto()
    
    MaxPhysical = 30

    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.state = self.State.alive

    def SetResources(self, resources):
        self.physical = resources[0]
        self.mental = resources[1]

    def SetWorld(self, world):
        self.world = world

    def GetPosition(self):
        return self.position
    
    def Die(self):
        self.state = IAgent.State.dead
    

    def __str__(self) -> str:
        return f'<{self.name[:4]}, ({self.physical}, {self.mental}), {self.position}>'
    
    def __repr__(self) -> str:
        return f'<{self.name[:4]}, ({self.physical}, {self.mental}), {self.position}>'
    
    @abstractmethod
    def GetRGBColor(self):
        ...

    @abstractmethod
    def Exist(self):
        ...
    
    @abstractmethod
    def Action(self):
        ...

    @abstractmethod
    def Move(self):
        ...
    
    @abstractmethod
    def CreateChild(self):
        ...