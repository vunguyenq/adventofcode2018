import numpy as np
a = np.array([0,1,2,3,4,5,6])
print(a)
print(a[3:6] == [3,3,5])
print((a[3:6] == [3,3,5]).all())
print(a[3:6] == [3,4,5])
print((a[3:6] == [3,4,5]).all())
a[2:5] = [9, 9, 9]
print(a)