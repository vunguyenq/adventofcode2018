from itertools import product
a = list(product([-1,0,1], repeat = 2))
a.remove((0,0))
print(a)