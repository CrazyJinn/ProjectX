
import random
import numpy as np
import Const as const
import Chromosome as ch

np.random.seed(const.randomSeed)


# def Crossover(chromosomeA, chromosomeB):
#     '''
#     繁殖，要求染色体长度相等
#     现在是均匀的交换基因，之后应该需要改成随机交换基因
#     '''
#     result = []
#     length = len(chromosomeA)
#     for i in range(length):
#         if(i % 2 == 0):
#             result.append(chromosomeA[i])
#         else:
#             result.append(chromosomeB[i])
#     return result

# def Crossover(chromosomeA, chromosomeB):
#     '''
#     繁殖，要求染色体长度相等
#     此繁殖方法是随机选择一个交叉点，交叉点前使用A，交叉点后使用B
#     '''
#     result = []
#     length = len(chromosomeA)

#     crossPos = np.random.randint(0, length)
#     result.extend(chromosomeA[0:crossPos])
#     result.extend(chromosomeB[crossPos:length])
#     return result

def Crossover(chromosomeA, chromosomeB):
    '''
    繁殖，要求染色体长度相等
    '''
    result = []
    length = len(chromosomeA)

    chromosome = []
    chromosome.extend(chromosomeA)
    chromosome.extend(chromosomeB)

    randomNum = np.random.choice(length * 2, length, replace=False)

    for i in randomNum:
        result.append(chromosome[i])

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

# 这里是计算线适应度的


def FitnessForLine(chromosome, xSamplingList, ySamplingList):
    '''
    计算直线适应度
    '''
    result = GetResultForLine(ySamplingList, ch.GetChromosomeResult(chromosome, xSamplingList))
    return result


def GetResultForLine(result1, result2):
    return np.sum(np.power(np.add(result1, - result2), 2))
# 这里是计算线适应度的 end


def Evolve(population):
    population = [x for x in sorted(population, key=lambda o: o[1], reverse=False)]

    result = []

    parentCount = (int)(len(population) / 3)
    childCount = parentCount * 2

    for temp in population[:parentCount]:
        result.append([temp[0], 0.0])

    # for temp in population[:parentCount]:
    #     print(temp[0])
    #     print("fit:", temp[1])

    # result.append(population[np.random.randint(0, 3) + 7])
    # result.append(population[np.random.randint(0, 10) + 10])
    # result.append(population[np.random.randint(0, 10) + 20])

    for i in range(childCount):
        choiceA, choiceB = np.random.choice(parentCount, 2, replace=False)
        result.append([Crossover(result[choiceA][0], result[choiceB][0]), 0.0])

    for temp in result:
        if random.random() < 0.05:
            temp[0] = Mutation(temp[0])

    return result
