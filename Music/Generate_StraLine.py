import numpy as np
import GA as ga
import Chromosome as ch
import time

start = time.clock()


def FitnessForLine(chromosome, xSamplingList, ySamplingList):
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
for i in range(120):
    xSamplingList.append(i / 10)
    # ySamplingList.append(10 * np.log(i / 10 + 1))
    # ySamplingList.append(i / 10)
    # ySamplingList.append(i * i / 100)
    ySamplingList.append(i / 10 + 10 * np.sin(0.5 * i) + 7 * np.cos(0.4 * i))
    # if(i % 50 == 0):
    #     ySamplingList.append(1)
    # elif(i % 30 == 0):
    #     ySamplingList.append(1)
    # else:
    #     ySamplingList.append(0)

for i in range(300):
    fitList = []
    for chromosome in population:
        if(i % 50 == 0):
            chromosome = ga.Append(chromosome)
        fitList.append(FitnessForLine(chromosome, xSamplingList, ySamplingList))

    population = ga.WeedOut(population, fitList, 100)
    population = ga.Evolve(population, populationQuantity)
    print(i)
    # input('------------------')

chromosome1 = population[0]

print('+++++++++++++++++')
print(population[0])
print(FitnessForLine(chromosome1, xSamplingList, ySamplingList))
print("time span:",time.clock() - start)
print('+++++++++++++++++')

import matplotlib.pyplot as plt
plt.figure()
plt.ion()
plt.axis([-2.0, 13.0, -20.0, 30.0])
plt.plot(xSamplingList, ySamplingList,  label='Original data', color='red')
plt.plot(xSamplingList, ch.GetChromosomeResult(
    chromosome1, xSamplingList),  label='Fitted line', color='blue')
plt.pause(20)
