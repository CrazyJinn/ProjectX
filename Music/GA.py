import random
import numpy as np
import MusicChromosome as mc

np.random.seed(0)


class GA():
    def __init__(self):
        self.__initChromosomeLen = 1

    def GetRandomGene(self):
        '''
        返回随机基因
        现在只返回型如 a*cos(b*π+d)^e-f 的基因
        '''
        return (np.random.randint(-10, 10),
                # 这里10^N限定得比较小，我觉得应该把N限定得更倾向于0，N取值正负2的时候基本就算出来是一个常数了
                np.random.randint(-10, 10) * np.power(10.0, np.random.randint(-2, 2)),
                np.random.randint(-10, 10),
                # e是否需要只能为正数，若为负数，会导致cos的值过小或者等于0的时候，取值接近无穷
                np.random.randint(0, 10),
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
