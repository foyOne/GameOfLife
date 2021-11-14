from typing import Any
import numpy as np
from abc import ABC, abstractmethod

from Agent import Agent

# Команда связана с агентом и миром
class ICommand(ABC):
    number: int
    commandTape = None

    def __init__(self, number, commandTape):
        self.number = number
        self.commandTape = commandTape

    def GetNumber(self):
        return self.number
        
    @abstractmethod
    def Execute(self, sender: Agent = None, parameter=None):
        ...
    

class Nope(ICommand):

    def Execute(self, sender: Agent = None, parameter=None):
        self.commandTape.Move(self.number)


class Move(ICommand):

    def Execute(self, sender: Agent = None, parameter=None):
        return self.number

class Scan(ICommand):

    def Execute(self, sender: Agent = None, parameter=None):
        sender.WhatIsAround()
    
class GetPhysicalResource(ICommand):

    def Execute(self, sender: Agent = None, parameter=None):
        ...
        


class CommandTape:
    table: dict = ...
    tape = ...
    size = ...
    ptr = ...

    def __init__(self, size=64):
        self.tape = np.random.randint(0, 64, size)
        self.size = size
        self.ptr = 0
    
    def SetCommandTable(self, table):
        self.table = table
    
    def __getitem__(self, i):
        return self.tape[i % self.size]
    
    def GetNext(self, i=1):
        ptr = self.ptr + i
        return self[ptr]
    
    def Move(self, i):
        self.ptr = (self.ptr + i) % self.size
    
    def Execute(self, sender=None, parameter=None):
        commandNumber = self[self.ptr]
        command = self.table.get(commandNumber)
        command.Execute(sender, parameter)

a: ICommand = Nope(1, 1)
print(a.GetNumber())