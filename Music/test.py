import GA
import numpy as np
import MusicChromosome as mc
import MyEnum


def Judge(haha):
    result = []
    for i in haha:
        if(round(i) > 0):
            result.append(1)
        elif (round(i) < 0):
            result.append(-1)
        else:
            result.append(0)
    return result


# gene1 = [(2,0,10,7), (10,10,-8,-7), (2,-3,2,3)]
gene1 = [(1, 1, 0, 1, 0),(-1, 1, 0, 1, 0),(2, 1, 0, 1, 0)]

# Chromosome = GA.GA().GetRandomChromosome()

a = mc.MusicChromosome()

resultList = []
for i in range(10):
    period = i * np.pi / 2
    resultList.append(a.GetGeneListResult(gene1, period))

print(resultList)

for i in Judge(resultList):
    if(i == 1):
        print('↑', end='')
    elif (i == -1):
        print('↓', end='')
    else:
        print('->', end='')
