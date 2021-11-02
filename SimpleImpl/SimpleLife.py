import numpy as np
from collections import Counter

class SimpleLife:

    def __init__(self, world):
        self.world = world
        self.current = None
        self.next = None

    def Init(self):
        self.current = np.random.random_integers(0, 1, self.world)
        self.next = np.zeros(self.world)
    
    def GetIndex(self, position):
        return np.array([[[i - 1, j - 1] for j in range(3)] for i in range(3)]).reshape(9, 2) + position
    
    def TryValue(self, position):
        i, j = position

        if i < 0 or j < 0:
            return 0
        
        if i > self.world[0] - 1 or j > self.world[1] - 1:
            return 0

        return self.current[i, j]
    
    def Update(self):
        row, col  = self.world
        for i in range(row):
            for j in range(col):
                area = self.WhatIsAround((i, j))
                ones = Counter(area.ravel()).get(1)
                
                if self.current[i, j]:
                    ones = ones - 1
                    if ones in [2, 3]:
                        self.next[i, j] = 1
                    else:
                        self.next[i, j] = 0
                else:
                    if ones == 3:
                        self.next[i, j] = 1

        self.current = np.copy(self.next)
        self.next = np.zeros(self.world)
    
    def GetCurrent(self):
        return self.current

    
    def WhatIsAround(self, position):
        positionList = self.GetIndex(position)
        values = []
        for pos in positionList:
            values.append(self.TryValue(pos))
        return np.array(values).reshape(3, 3)