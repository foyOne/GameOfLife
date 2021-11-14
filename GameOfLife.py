import operator
import numpy as np

a = np.array([
    [1, 2],
    [3, 4]
])

print(a[0, 0])
print(a[(0, 0)])
print(a[[0, 0]])

