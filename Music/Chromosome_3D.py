import random
import numpy as np
import Const_3D as const

np.random.seed(const.randomSeed)


def GenerateGene():
    '''
    返回随机基因
    现在只返回型如 a*cos(b*10^c*π+d)^e-f 的基因
    '''
    result = []
    for index in range(len(const.domain)):
        if(index == 1):
            value = np.random.randint(const.domain[index][0], const.domain[index][1])
            result.append(np.random.random() * value)
        else:
            result.append(np.random.randint(const.domain[index][0], const.domain[index][1]))
    return result


def GenerateChromosome():
    '''
    返回随机染色体
    '''
    chromosome = []
    for i in range(const.initChromosomeLen):
        chromosome.append(GenerateGene())
    return chromosome


def GetGeneResult(gene, samplingList):
    '''
    计算基因在采样上表达的值
    方程为 ： a*cos(b*10^c*π+d)^e-f
    '''
    result = 0
    result = np.multiply(gene[1], samplingList)  # b*π
    # if gene[2] >= 0:
    #     result = np.multiply(result, np.power(10, gene[2]))  # b*10^c*π
    # else:
    #     result = np.multiply(result, 1 / np.power(10, np.abs(gene[2])))  # b*10^c*π
    result = np.add(result, gene[3])  # b*10^c*π+d
    result = np.cos(result)  # cos(b*10^c*π+d)
    if(gene[4] == 0):
        result = np.abs(result)
    # result = np.power(result, gene[4])  # cos(b*10^c*π+d)^e
    result = np.multiply(result, gene[0])  # a*cos(b*10^c*π+d)^e
    result = np.add(result, gene[5])  # a*cos(b*10^c*π+d)^e-f
    return result


def GetChromosomeResult(chromosome, samplingList):
    '''
    返回染色体在采样上表达的值
    '''
    result = 0
    for gene in chromosome:
        result += GetGeneResult(gene, samplingList)
    return result


def GetChromosomeResultWithFilter(chromosome, samplingList, filter):
    '''
    返回染色体在采样上表达的值
    filter : 滤波方法；以下是一个简单的滤波方法：
        def filter(result):
            result[result >= 0.5] = 1
            result[result < 0.5] = 0
            return result
    '''
    result = 0
    count = 0

    for gene in chromosome:
        tempSample = []
        if(count % 6 == 0):
            for x in samplingList[0]:
                for y in samplingList[1]:
                    tempSample.append(x + y)
        elif(count % 6 == 1):
            for x in samplingList[0]:
                for y in samplingList[1]:
                    tempSample.append(x - y)
        elif(count % 6 == 2):
            for x in samplingList[0]:
                for y in samplingList[1]:
                    tempSample.append(2 * x + y)
        elif(count % 6 == 3):
            for x in samplingList[0]:
                for y in samplingList[1]:
                    tempSample.append(x + 2 * y)
        elif(count % 6 == 4):
            for x in samplingList[0]:
                for y in samplingList[1]:
                    tempSample.append(x)
        elif(count % 6 == 5):
            for x in samplingList[0]:
                for y in samplingList[1]:
                    tempSample.append(y)
        result += GetGeneResult(gene, tempSample)
        count += 1

    result = filter(result)
    return result
