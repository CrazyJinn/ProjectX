import numpy as np
import GA as ga
import Chromosome as ch

chromosome = [-10, -1, -1, -5, 6, -2]
# population = []
# for i in range(300):
#     population.append([ch.GenerateChromosome(), 0.0])

samplingList = [1]


# for i in range(300):
#     for temp in population:
#         if(i % 50 == 0):
#             temp[0] = ga.Append(temp[0])
#         temp[1] = ga.FitnessForLine(temp[0], xSamplingList, ySamplingList)

#     population = ga.Evolve(population)
#     print(i)


def filter(asd):
    print(asd)

ch.GetChromosomeResultWithFilter(chromosome,samplingList,filter)

# 这里是计算music适应度的

def Fitness(chromosome, samplingList):
    '''
    计算适应度
    '''
    result = 0.0
    for sampling in samplingList:
        result = result + GetAbsFromNearestInt(ch.GetChromosomeResult(chromosome, sampling))
    return result


def GetAbsFromNearestInt(number):
    temp = round(number)
    return np.abs(number - temp)

# 这里是计算music适应度的 end