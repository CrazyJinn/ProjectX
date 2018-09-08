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
        现在只返回型如 Acos(Bπ+C)^D-E 的基因
        '''
        return (np.random.randint(-10, 10),
                np.random.randint(-10, 10),
                np.random.randint(-10, 10),
                np.random.randint(-10, 10),
                np.random.randint(-10, 10))

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
