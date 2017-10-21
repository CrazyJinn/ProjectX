import random
import numpy as np
import MusicChromosome as mc

np.random.seed(0)


class GA():
    def __init__(self):
        self.__initChromosomeLen = 3

    def GetRandomGene(self):
        '''
        返回随机基因
        现在只返回型如 Asin(Bx+C)-D or Acos(Bx+C)-D 的基因
        '''
        return [(1, np.random.randint(0, 10)),  # Bx
                (0, np.random.randint(-7, 8)),  # Bx+c,在正负2pi之间取值
                (np.random.randint(8, 10), 0),  # sin or cos
                (1, np.random.randint(0, 10)),
                (0, np.random.randint(-9, 10))]

    def GetRandomChromosome(self):
        '''
        返回随机染色体
        '''
        chromosome = []
        for i in range(self.__initChromosomeLen):
            chromosome.append(self.GetRandomGene())
        return chromosome

    def Crossover(self):
        '''
        '''
        pass
