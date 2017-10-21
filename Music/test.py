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


gene1 = [(2, 0), (1, 10), (0, -3)]
gene2 = [(3, 0), (1, 3), (0, -1)]
Chromosome = GA.GA().GetRandomChromosome()

a = mc.MusicChromosome(Chromosome)

resultList = []
for i in range(10):
    period = i * np.pi / 2
    resultList.append(a.GetChromosomeResult(period) / a.GetChromosomeLen())

print(resultList)

for i in Judge(resultList):
    if(i == 1):
        print('↑', end='')
    elif (i == -1):
        print('↓', end='')
    else:
        print('->', end='')
