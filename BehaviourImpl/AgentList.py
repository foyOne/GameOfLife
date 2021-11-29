import random
from IAgent import IAgent
from dataclasses import dataclass


class Herbivorous(IAgent):

    proportion = 0.9
    MaxPhysical = 30
    MaxMental = 10
    MaxFood = 2

    def GetRGBColor(self):
        return (255, 0, 0)

    def Exist(self):

        if self.state == self.State.dead:
            return

        if self.physical == 0:
            self.Die()
            return

        if self.physical > int(self.MaxPhysical * self.proportion):
            self.CreateChild()
        else:
            res = self.world.GetResourceFromPosition(self.position)
            if res > 0:
                self.Action()
            else:
                self.Move()
        
        self.physical -= 1
    
    def Action(self):
        res = self.world.GetResourceFromPosition(self.position)
        res = min(res, Herbivorous.MaxFood)
        self.physical = min(self.physical + res, self.MaxPhysical)
        self.world.AddResourceAction((self.position, res))
    
    def Move(self):
        if self.mental > 0:
            res, _ = self.world.WhatIsAround(self.position)

            pos = max(res, key=res.get)
            if res[pos] == 0:
                res.pop(self.position, None)
                pos = random.choice(list(res))
            
            if pos == self.position:
                return
            
            irange = pos[0] - self.position[0]
            jrange = pos[1] - self.position[1]

            if abs(irange) + abs(jrange) == 1:
                self.position = pos
            else:
                near1 = (pos[0] - irange, pos[1])
                near2 = (pos[0], pos[1] - jrange)
                self.position = near1 if res.get(near1) > res.get(near2) else near2
            
            self.mental -= 1

    # def Move(self):
    #     if self.mental > 0:
    #         res, _ = self.world.WhatIsAround(self.position)

    #         for p in list(res):
    #             if self.world.IsPositionTaken(p):
    #                 res.pop(p)
            
    #         if len(res) == 0:
    #             return
            
    #         pos = max(res, key=res.get)
    #         if res[pos] == 0:
    #             pos = random.choice(list(res))
    #             self.position = pos
    #             self.mental -= 1
    #             return
            
    #         irange = pos[0] - self.position[0]
    #         jrange = pos[1] - self.position[1]

    #         if abs(irange) + abs(jrange) == 1:
    #             self.position = pos
    #         else:
    #             near1 = (pos[0] - irange, pos[1])
    #             near2 = (pos[0], pos[1] - jrange)
    #             taken1 = self.world.IsPositionTaken(near1)
    #             taken2 = self.world.IsPositionTaken(near2)
    #             if taken1 and taken2:
    #                 pos = random.choice(list(res))
    #                 self.position = pos
    #             if not taken1 and not taken2:
    #                 self.position = near1 if res.get(near1) > res.get(near2) else near2
    #             else:
    #                 self.position = near1 if res.get(near1) else near2
            
    #         self.mental -= 1

    def CreateChild(self):
        self.physical = int(self.physical * (1 - self.proportion))
        self.world.CreateAgent(self)



class Predator(IAgent):

    proportion = 0.8
    MaxPhysical = 30
    MaxMental = 20

    def Action(self):
        res, agents = self.world.WhatIsAround(self.position)
        agents = list(filter(lambda x: bool(x[1]), agents))

    def CreateChild(self):
        self.physical = int(self.physical * (1 - self.proportion))
        self.world.CreateAgent(self)