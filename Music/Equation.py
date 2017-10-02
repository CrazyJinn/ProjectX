import numpy as np

class Equation():
    def GetResult(self, period, parameter):
        """
        period:周期，一般为π的2的n次方倍
        parameter:方程的参数，tuple，(A,B,C,D,tFunction)
        tFunction:trigonometric function，会根据值选择一个三角函数
        
        return: A*tFunction(Bx+C)+D
        """
        result = np.add(np.multiply(parameter[1], period), parameter[2])  # Bx+C
        result = self.GetTFunction(result, parameter[4])
        result = np.add(np.multiply(parameter[0], result), parameter[3])  # A*sin(Bx+C)+D
        return result

    def GetTFunction(self, x, tFunction):
        """根据tFunction的值选择一个三角函数"""
        if tFunction == 0:
            return np.sin(x)
        elif tFunction == 1:
            return np.cos(x)
        elif tFunction == 2:
            pass
            # return np.tan(x) #这里有个问题，就是选择了tan之后出来的数值有可能太大，而且tan90°和会出现严重的问题，暂时不弄这玩意好了
        else:
            return np.sin(x)
