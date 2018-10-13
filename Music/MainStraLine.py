import numpy as np
import GA as ga
import Chromosome as ch

# population = [[[-10, -1, -1, -5, 6, -2]],0.0]
population = []
for i in range(30):
    population.append([ch.GenerateChromosome(), 0.0])

samplingList = []
for i in range(10):
    samplingList.append(i)

for temp in population:
    temp[1] = ga.FitnessForStraLine(temp[0], samplingList)

population = [x for x in sorted(population, key=lambda o: o[1], reverse=False)]

for temp in population:
    print(temp[1])

bestChromosome = population[0]

# print('---------------------------------')

# for temp in population:
#     ga.Mutation(temp[0])

# for temp in population:
#     temp[1] = ga.FitnessForStraLine(temp[0], samplingList)

# population = [x for x in sorted(population, key=lambda o: o[1], reverse=False)]

# for temp in population:
#     print(temp[1])

import matplotlib.pyplot as plt
plt.figure()
plt.ion()
plt.axis([-5.0, 10.0, -5.0, 10.0])
plt.plot(samplingList, samplingList, 'ro', label='Original data')
plt.plot(samplingList, ch.GetChromosomeResult(bestChromosome[0], samplingList), label='Fitted line')
plt.pause(20)
