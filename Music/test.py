

import Equation
import random


a = Equation.Equation()


parameter = (random.randint(0, 9), random.randint(0, 9), random.randint(-9, 9),
             random.randint(-9, 9), random.randint(0, 1))
# parameter = (10, 2, 0, -3, 1)

print(a.GetResult(0, parameter))
