import numpy as np
import MyEnum


class Equation():
    def __init__(self, equationList):
        self.__equationList = equationList

    def GetResult(self, x):
        '''
        将方程组逐个相加并除以方程个数
        x:未知数
        equationList:方程组
        '''
        result = 0
        for equation in self.__equationList:
            result += self.GetEquation(x, equation)
        return result / len(self.__equationList)

    def GetEquation(self, x, equation):
        '''
        根据equation返回一个方程
        x:未知数
        equation:方程,如[(2, 0), (1, 10), (0, -3)],返回10sin(x)-10
        '''
        result = x
        for parameter in equation:
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

