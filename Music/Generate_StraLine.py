import numpy as np
import GA as ga
import Chromosome as ch

def FitnessForLine(chromosome, xSamplingList, ySamplingList):
    '''
    计算直线适应度
    '''
    result = GetResultForLine(ySamplingList, ch.GetChromosomeResult(chromosome, xSamplingList))
    return result


def GetResultForLine(result1, result2):
    return np.sum(np.power(np.add(result1, - result2), 2))

# population = [[[-10, -1, -1, -5, 6, -2]],0.0]
population = []
for i in range(30):
    population.append([ch.GenerateChromosome(), 0.0])

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
    for temp in population:
        if(i % 50 == 0):
            temp[0] = ga.Append(temp[0])
        temp[1] = FitnessForLine(temp[0], xSamplingList, ySamplingList)

    population = ga.Evolve(population)
    print(i)
    # input('------------------')

chromosome1 = population[0][0]

print('+++++++++++++++++')
print(population[0][0])
print(FitnessForLine(chromosome1, xSamplingList, ySamplingList))
print('+++++++++++++++++')

import matplotlib.pyplot as plt
plt.figure()
plt.ion()
plt.axis([-2.0, 13.0, -20.0, 30.0])
plt.plot(xSamplingList, ySamplingList,  label='Original data', color='red')
plt.plot(xSamplingList, ch.GetChromosomeResult(
    chromosome1, xSamplingList),  label='Fitted line', color='blue')
plt.pause(20)



