
import ChromosomeHelper
chromosomeHelper = ChromosomeHelper.ChromosomeHelper()
import GA
import numpy as np


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


# chromosome = [(2, 5, 1, -10, 3, -7)]

chromosome1 = chromosomeHelper.GenerateChromosome()
chromosome2 = chromosomeHelper.GenerateChromosome()
ga = GA.GA()

print(chromosome1)
print(chromosome2)

for i in range(10):
    period = i * np.pi / 2
    print(chromosomeHelper.GetChromosomeResult(chromosome1, period))

print(ga.Crossover(chromosome1, chromosome2))
# print(ga.Mutation(chromosome1))


# for i in Judge(resultList):
#     if(i == 1):
#         print('↑', end='')
#     elif (i == -1):
#         print('↓', end='')
#     else:
#         print('->', end='')
