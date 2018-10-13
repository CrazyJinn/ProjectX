import numpy as np
import GA as ga
import Chromosome as ch


chromosomeList = [[-10, -1, -1, -5, 6, -2]]
# chromosomeList = []
# for i in range(10):
#     chromosomeList.append(ch.GenerateChromosome())

samplingList = []
for i in range(12):
    samplingList.append(i * np.pi/4)

for temp in chromosomeList:
    print(ga.Fitness(temp, samplingList))

print('---------------------------------')

for temp in chromosomeList:
    ga.Mutation(temp)

for temp in chromosomeList:
    print(ga.Fitness(temp, samplingList))

