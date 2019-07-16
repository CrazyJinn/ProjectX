import random
import numpy as np
import Const as const
import tensorflow as tf

np.random.seed(const.randomSeed)


def GenerateGene():
    '''
    返回随机基因
    现在只返回型如 a*cos(b*10^c*π+d)^e-f 的基因
    '''
    result = []
    for index in const.domain:
        result.append(np.random.randint(index[0], index[1]))
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
    result = tf.multiply(gene[1], samplingList)  # b*π
    result = tf.multiply(result, tf.cast(tf.pow(10, gene[2]), "float32"))  # b*10^c*π
    result = tf.add(result, gene[3])  # b*10^c*π+d
    result = tf.cos(result)  # cos(b*10^c*π+d)
    result = tf.cast(tf.pow(result, gene[4]), "float32")  # cos(b*10^c*π+d)^e
    result = tf.multiply(result, gene[0])  # a*cos(b*10^c*π+d)^e
    result = tf.add(result, gene[5])  # a*cos(b*10^c*π+d)^e-f
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
    for gene in chromosome:
        result += GetGeneResult(gene, samplingList)

    result = filter(result)
    return result
