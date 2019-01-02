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

def WeedOut(population, fitList, quantity, reverse=False):
    '''
    淘汰
    quantity , 期望淘汰后的种群数量
    reverse = false，种群根据fit从小到大排列
    reverse = true，种群根据fit从大到小排列
    '''
    data = [(chromosome, fit) for chromosome, fit in zip(population, fitList)]
    data = [x for x in sorted(data, key=lambda o: o[1], reverse=reverse)]
    return [chromosome for chromosome, fit in data][:quantity]


def Evolve(population, quantity):
    '''
    进化
    种群中幸存的所有染色体交配机会均等
    '''
    parentCount = len(population)
    childCount = quantity - parentCount

    for i in range(childCount):
        choiceA, choiceB = np.random.choice(parentCount, 2, replace=False)
        population.append(Crossover(population[choiceA], population[choiceB]))

    for chromosome in population:
        if random.random() < 0.05:
            chromosome = Mutation(chromosome)

    return population