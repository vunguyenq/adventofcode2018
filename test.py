import numpy as np
a = np.zeros((4,5) , dtype=int )
print(a)
a[3,2] = 1
a[1,1] = 3
a[3,3] = 3
print(a)
print(np.count_nonzero(a == 3))