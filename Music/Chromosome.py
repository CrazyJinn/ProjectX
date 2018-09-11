import random
import numpy as np
np.random.seed(0)

import Domain
domain = Domain.Domain


class Chromosome():

    def __init__(self):
        self.__initChromosomeLen = 4
        self.__chromosome = self.GenerateChromosome()

    def GenerateGene(self):
        '''
        返回随机基因
        现在只返回型如 a*cos(b*10^c*π+d)^e-f 的基因
        '''
        result = []
        for index in domain.domain:
            result.append(np.random.randint(index[0], index[1]))
        return result

    def GenerateChromosome(self):
        '''
        返回随机染色体
        '''
        chromosome = []
        for i in range(self.__initChromosomeLen):
            chromosome.append(self.GenerateGene())
        return chromosome

    def GetChromosome(self):
        return self.__chromosome
