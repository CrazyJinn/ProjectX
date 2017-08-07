L = [{'name':'john', 'state':'A', 'age':15},
{'name':'jane', 'state':'B', 'age':12},
{'name':'dave', 'state':'C', 'age':10},]

print(type(L))
sortL = sorted(L,key = lambda o: o['age'])
for i in sortL[0:6]:
    print(i)
