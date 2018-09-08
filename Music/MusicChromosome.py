import numpy as np
import MyEnum


class MusicChromosome():
    # def __init__(self, chromosome):
    #     self.__chromosome = chromosome

    def GetGeneListResult(self, geneList, period):
        '''
        返回基因所表达的方程的值
        x: 未知数
        gene: 基因,如[(2,0,10,7), (10,10,-8,-7), (2,-3,2,3)]
        '''
        result = 0
        for gene in geneList:
            result += self.GetGeneResult(gene, period)
        return result

    def GetGeneResult(self, gene, period):
        result = 0
        result = np.multiply(gene[1], period)
        result = np.add(result, gene[2])
        result = np.cos(result)
        result = np.power(result, gene[3])
        result = np.multiply(result, gene[0])
        result = np.add(result, gene[4])
        return result

