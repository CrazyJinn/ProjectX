# import random
# import numpy as np
# np.random.seed(0)

# import Domain
# domain = Domain.Domain


# class ChromosomeHelper():

#     def __init__(self):
#         self.__initChromosomeLen = 4

#     def GenerateGene(self):
#         '''
#         返回随机基因
#         现在只返回型如 a*cos(b*10^c*π+d)^e-f 的基因
#         '''
#         result = []
#         for index in domain.domain:
#             result.append(np.random.randint(index[0], index[1]))
#         return result

#     def GenerateChromosome(self):
#         '''
#         返回随机染色体
#         '''
#         chromosome = []
#         for i in range(self.__initChromosomeLen):
#             chromosome.append(self.GenerateGene())
#         return chromosome

#     def _GetGeneResult(self, gene, period):
#         '''
#         计算 a*cos(b*10^c*π+d)^e-f
#         '''
#         result = 0
#         result = np.multiply(np.multiply(
#             gene[1], period), np.power(10, gene[2]))  # b*10^c*π
#         result = np.add(result, gene[3])  # b*10^c*π+d
#         result = np.cos(result)  # cos(b*10^c*π+d)
#         result = np.power(result, gene[4])  # cos(b*10^c*π+d)^e
#         result = np.multiply(result, gene[0])  # a*cos(b*10^c*π+d)^e
#         result = np.add(result, gene[5])  # a*cos(b*10^c*π+d)^e-f
#         return result

#     def GetChromosomeResult(self, chromosome, period):
#         '''
#         返回染色体所表达的方程的值
#         x: 未知数
#         '''
#         result = 0
#         for gene in chromosome:
#             result += self._GetGeneResult(gene, period)
#         return result
