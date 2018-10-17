import numpy as np
import GA as ga
import Chromosome as ch

# population = [[[-10, -1, -1, -5, 6, -2]],0.0]
population = []
for i in range(30):
    population.append([ch.GenerateChromosome(), 0.0])

xSamplingList = []
ySamplingList = []
for i in range(120):
    xSamplingList.append(i / 10)
    ySamplingList.append(120 - (i * i / 100))


for i in range(5000):
    for temp in population:
        if(i % 50 == 0):
            temp[0] = ga.Append(temp[0])
        temp[1] = ga.FitnessForLine(temp[0], xSamplingList, ySamplingList)
    population = ga.Evolve(population)
    print(i)

bestChromosome = population[0]

print('+++++++++++++++++')
print(population[0][0])
print(ga.FitnessForLine(bestChromosome[0], xSamplingList, ySamplingList))
print('+++++++++++++++++')

import matplotlib.pyplot as plt
plt.figure()
plt.ion()
plt.axis([-2.0, 12.0, -2.0, 150.0])
plt.plot(xSamplingList, ySamplingList,  label='Original data', color='red')
plt.plot(xSamplingList, ch.GetChromosomeResult(
    bestChromosome[0], xSamplingList),  label='Fitted line', color='blue')
plt.pause(20)
