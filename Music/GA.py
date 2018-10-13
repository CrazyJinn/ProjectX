
import random
import numpy as np

import Chromosome as ch


def Crossover(chromosomeA, chromosomeB):
    '''
    繁殖，要求染色体长度相等
    现在是均匀的交换基因，之后应该需要改成随机交换基因
    '''
    result = []
    length = len(chromosomeA)
    for i in range(length):
        if(i % 2 == 0):
            result.append(chromosomeA[i])
        else:
            result.append(chromosomeB[i])
    return result


def Mutation(chromosome):
    '''
    变异，现在是整个基因变异，也可以只改变基因中的某个值
    '''
    index = np.random.randint(0, len(chromosome))
    chromosome[index] = ch.GenerateGene()
    return chromosome


def Append(chromosome):
    '''
    染色体增加长度
    '''
    chromosome.append(ch.GenerateGene())
    return chromosome

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

# 这里是计算直线适应度的


def FitnessForStraLine(chromosome, samplingList):
    '''
    计算直线适应度
    '''
    result = 0.0
    for sampling in samplingList:
        result = result + GetResultForStraLine(sampling,
                                               ch.GetChromosomeResult(chromosome, sampling))
    return result


def GetResultForStraLine(result1, result2):
    return np.power(result1 - result2, 2)
# 这里是计算直线适应度的 end


def Evolve(population):
    # population = [x for x in sorted(population, key=lambda o: o[1], reverse=False)]
    # parents = population[:10]  # todo
    # result = []
    # Crossover()
    pass

