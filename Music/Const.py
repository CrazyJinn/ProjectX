
domain = [(-9, 10),
          (-9, 10),
          (-2, 3),  # 这里10^c限定得比较小，我觉得应该把N限定得更倾向于0，N取值正负2的时候基本就算出来是一个常数了
          (-9, 10),
          (0, 10),  # e是否需要只能为正数，若为负数，会导致cos的值过小或者等于0的时候，取值接近无穷
          (-9, 10)]

initChromosomeLen = 20

randomSeed = 0
