
import random
import numpy as np

import Chromosome


class GA():

    def Crossover(self, chromosomeA, chromosomeB):
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

    def Mutation(self, chromosome):
        '''
        变异，现在是整个基因变异，也可以只改变基因中的某个值
        '''
        index = np.random.randint(0, len(chromosome))
        chromosome[index] = Chromosome.Chromosome().GenerateGene()
        return chromosome
