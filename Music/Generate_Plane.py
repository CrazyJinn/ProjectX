import numpy as np
import GA as ga
import Chromosome as ch
import time

start = time.clock()


def FitnessForLine(chromosome, xSamplingList, ySamplingList,zSamplingList):
    '''
    计算直线适应度
    '''
    result = GetResultForLine(ySamplingList, ch.GetChromosomeResult(chromosome, xSamplingList))
    return result


def GetResultForLine(result1, result2):
    return np.sum(np.power(np.add(result1, - result2), 2))


population = []
populationQuantity = 300
for i in range(populationQuantity):
    population.append(ch.GenerateChromosome())

xSamplingList = []
ySamplingList = []
zSamplingList = []
for i in range(12):
    xSamplingList.append(i / 10)
    ySamplingList.append(i / 10)
    zSamplingList.append(i * 2 / 10)

for i in range(300):
    fitList = []
    for chromosome in population:
        if(i % 50 == 0):
            chromosome = ga.Append(chromosome)
        fitList.append(FitnessForLine(chromosome, xSamplingList, ySamplingList))

    population = ga.WeedOut(population, fitList, 100)
    population = ga.Evolve(population, populationQuantity)
    print(i)

chromosome1 = population[0]

print('+++++++++++++++++')
print(population[0])
print(FitnessForLine(chromosome1, xSamplingList, ySamplingList))
print("time span:", time.clock() - start)
print('+++++++++++++++++')

import matplotlib.pyplot as plt
plt.figure()
plt.ion()
plt.axis([-2.0, 13.0, -20.0, 30.0])
plt.plot(xSamplingList, ySamplingList,  label='Original data', color='red')
plt.plot(xSamplingList, ch.GetChromosomeResult(
    chromosome1, xSamplingList),  label='Fitted line', color='blue')
plt.pause(20)
