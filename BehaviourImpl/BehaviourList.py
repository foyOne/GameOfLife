from Behaviour import IBehaviour
from Agent import Agent
import operator


class Herbivorous(IBehaviour):
    
    DeadThreshold = 1e-3

    def Exist(self, sender: Agent, parameter = None):
        self.agent = sender
        if sender.state is sender.State.dead:
            return
        
        if sender.GetResourcesFromCurrentPosition() == 0:
            if sender.CanMove():
                self.Move()
            else:
                self.Action()
        else:
            self.Action()
    
    def Move(self, sender: Agent):
        resources, _ = sender.WhatIsAround()
        maxResource = max(resources.items(), key=operator.itemgetter(1))
        pos, _ = maxResource
        sender.Move(pos)

    
    def Action(self, sender: Agent):
        resources, _ = sender.WhatIsAround()
        

