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


# gene1 = [(10, 10, 10, 10, 10)]

chromosome = GA.GA().GetRandomChromosome()

a = mc.MusicChromosome()



resultList = []
for i in range(10):
    period = i * np.pi / 2
    resultList.append(a.GetGeneListResult(chromosome, period))

print(chromosome)
print(resultList)

# for i in Judge(resultList):
#     if(i == 1):
#         print('↑', end='')
#     elif (i == -1):
#         print('↓', end='')
#     else:
#         print('->', end='')
