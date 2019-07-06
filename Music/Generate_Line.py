import numpy as np
import GA as ga
import Chromosome as ch
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

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


def function(i):
    # return 10 * np.log(i + 10)
    # return i
    # return i + 10 * np.sin(5 * i) + 7 * np.cos(4 * i)
    # return i + 5 * np.sin(5 * i) + 7 * np.cos(7 * i)
    return i - 5 * np.sin(5 * i) + 7 * np.cos(7 * i) + 9 * np.cos(9 * np.log(i + 1))

for i in range(720):
    xSamplingList.append(i / 10)
    ySamplingList.append(function(i / 10))

def plot(chromosomeList):
    fig = plt.figure(figsize=(16, 16))
    gs = gridspec.GridSpec(2, 2)
    gs.update(wspace=0.01, hspace=0.01)

    for i, chromosome in enumerate(chromosomeList):
        ax = plt.subplot(gs[i])
        plt.axis([-2.0, 72.0, -20.0, 100.0])
        plt.xticks([])
        plt.yticks([])
        plt.plot(xSamplingList, ySamplingList,  label='Original data', color='red')
        plt.plot(xSamplingList, ch.GetChromosomeResult(
            chromosome, xSamplingList),  label='Fitted line', color='blue')
    return fig

for i in range(500):
    fitList = []
    for chromosome in population:
        if(i % 50 == 0):
            chromosome = ga.Append(chromosome)
        fitList.append(FitnessForLine(chromosome, xSamplingList, ySamplingList))

    population = ga.WeedOut(population, fitList, 100)
    population = ga.Evolve(population, populationQuantity)
    # print(fitList[0:3])
    print(i)
    # input('------------------')

chromosome1 = population[0]

print('+++++++++++++++++')
print(population[0])
print(FitnessForLine(chromosome1, xSamplingList, ySamplingList))
print('+++++++++++++++++')

bestChromosomeResult = population[0:20:5]
fig = plot(bestChromosomeResult)
plt.savefig('out/{}.png'.format(str(0).zfill(3)), bbox_inches='tight')
plt.close(fig)
