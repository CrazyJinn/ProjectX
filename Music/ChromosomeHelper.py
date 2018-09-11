import numpy as np


class ChromosomeHelper():

    def _GetGeneResult(self, gene, period):
        '''
        计算 a*cos(b*10^c*π+d)^e-f
        '''
        result = 0
        result = np.multiply(np.multiply(
            gene[1], period), np.power(10, gene[2]))  # b*10^c*π
        result = np.add(result, gene[3])  # b*10^c*π+d
        result = np.cos(result)  # cos(b*10^c*π+d)
        result = np.power(result, gene[4])  # cos(b*10^c*π+d)^e
        result = np.multiply(result, gene[0])  # a*cos(b*10^c*π+d)^e
        result = np.add(result, gene[5])  # a*cos(b*10^c*π+d)^e-f
        return result

    def GetChromosomeResult(self, chromosome, period):
        '''
        返回染色体所表达的方程的值
        x: 未知数
        '''
        result = 0
        for gene in chromosome:
            result += self._GetGeneResult(gene, period)
        return result
