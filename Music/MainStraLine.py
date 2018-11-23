import numpy as np
import GA as ga
import Chromosome as ch

# population = [[[-10, -1, -1, -5, 6, -2]],0.0]
population = []
for i in range(300):
    population.append([ch.GenerateChromosome(), 0.0])

xSamplingList = []
ySamplingList = []
for i in range(800):
    xSamplingList.append(i / 10)
    # ySamplingList.append(10 * np.log(i / 10 + 1))
    # ySamplingList.append(i / 10)
    # ySamplingList.append(i * i / 100)
    # ySamplingList.append(i / 10 + 10 * np.sin(0.5 * i) + 7 * np.cos(0.4 * i))
    if(i % 50 == 0):
        ySamplingList.append(1)
    else:
        ySamplingList.append(0)

for i in range(300):
    for temp in population:
        if(i % 50 == 0):
            temp[0] = ga.Append(temp[0])
        temp[1] = ga.FitnessWithFilter(temp[0], xSamplingList, ySamplingList)

    population = ga.Evolve(population)
    print(i)
    # input('------------------')

chromosome1 = population[0][0]

print('+++++++++++++++++')
print(population[0][0])
print(ga.FitnessWithFilter(chromosome1, xSamplingList, ySamplingList))
print('+++++++++++++++++')

import matplotlib.pyplot as plt
plt.figure()
plt.ion()
plt.axis([-2.0, 82.0, -2.0, 2.0])
plt.plot(xSamplingList, ySamplingList,  label='Original data', color='red')
plt.plot(xSamplingList, ch.GetChromosomeResultWithFilter(
    chromosome1, xSamplingList),  label='Fitted line', color='blue')
plt.pause(20)
