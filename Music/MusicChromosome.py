import numpy as np
import MyEnum


class MusicChromosome():
    def __init__(self, chromosome):
        self.__chromosome = chromosome

    def GetChromosomeLen(self):
        return len(self.__chromosome)

    def GetChromosomeResult(self, x):
        '''
        返回染色体所表达的的值
        x: 未知数
        '''
        result = 0
        for gene in self.__chromosome:
            result += self.GetGeneResult(x, gene)
        return result

    def GetGeneResult(self, x, gene):
        '''
        返回基因所表达的方程的值
        x: 未知数
        gene: 基因,如[(2, 0), (1, 10), (0, -3)],返回10sin(x)-10
        '''
        result = x
        for parameter in gene:
            if isinstance(parameter[0], MyEnum.FunctionEnum):
                result = self.GetFunctionByEuem(result, parameter[0], parameter[1])
            elif isinstance(parameter[0], int):
                result = self.GetFunctionByInt(result, parameter[0], parameter[1])
            else:
                raise Exception("Invalid parameter", 1)
        return result

    def GetFunctionByEuem(self, x, function, coefficient):
        '''

        '''
        if function == MyEnum.FunctionEnum.add:
            return np.add(x, coefficient)
        elif function == MyEnum.FunctionEnum.multiply:
            return np.multiply(x, coefficient)
        elif function == MyEnum.FunctionEnum.sin:
            return np.sin(x)
        elif function == MyEnum.FunctionEnum.cos:
            return np.cos(x)
        else:
            pass

    def GetFunctionByInt(self, x, function, coefficient):
        '''

        '''
        if function == MyEnum.FunctionEnum.add.value:
            return np.add(x, coefficient)
        elif function == MyEnum.FunctionEnum.multiply.value:
            return np.multiply(x, coefficient)
        elif function == MyEnum.FunctionEnum.sin.value:
            return np.sin(x)
        elif function == MyEnum.FunctionEnum.cos.value:
            return np.cos(x)
        else:
            pass
