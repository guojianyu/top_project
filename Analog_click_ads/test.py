import random
a = {'a':123,'b':2234,'c':334,'d':222,'r':['a','b','c']}
b = random.sample(a['r'],1)
print (b[0])