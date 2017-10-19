
import numpy as np
import Equation
import random
import MyEnum

def GetRandomTFunctionEquation():
    '''
    获取一个随机的三角函数方程
    '''
    pass


equation1 = [(2, 0), (1, 10), (0, -3)]
equation2 = [(3, 0), (1, 3), (0, -1)]
equationList = [equation1, equation2]

a = Equation.Equation(equationList)

for i in range(10):
    period = i * np.pi / 2

    result = a.GetResult(period)
    print(result)
