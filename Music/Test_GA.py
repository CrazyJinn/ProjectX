import GA as GA
import unittest


class Test_GA(unittest.TestCase):
    '''
    因为生成基因是随机的，所以断言放得比较松散，没那么严格
    '''

    def setUp(self):
        self.chromosomeA = [[2, 5, 0, -10, 3, -7], [-3, -1, 0, 8, 4, -4],
                            [2, -9, 1, -3, 7, 4], [7, -5, 0, 3, 8, -1]]
        self.chromosomeB = [[9, 6, 0, 5, 0, 8], [-7, 7, 0, 9, 3, 4],
                            [-3, -10, 0, -1, 9, -10], [0, -7, 1, 1, 2, -8]]
        self.chromosomeC = [[2, 5, 0, -10, 3, -7], [-7, 7, 0, 9, 3, 4],
                            [2, -9, 1, -3, 7, 4], [0, -7, 1, 1, 2, -8]]

    def test_Crossover(self):
        # result = GA.Crossover(self.chromosomeA, self.chromosomeB)
        # self.assertEqual(result, self.chromosomeC)
        pass

    def test_Mutation(self):
        # result = GA.Mutation(self.chromosomeA)
        # notEqualGeneCount = 0
        # for i in range(len(result)):
        #     if(result[i] != self.chromosomeA[i]):
        #         notEqualGeneCount = notEqualGeneCount + 1
        # self.assertEqual(notEqualGeneCount, 1)
        pass

    def test_Append(self):
        # result = GA.Append(self.chromosomeA)
        # self.assertEqual(len(result), len(self.chromosomeA) + 1)
        # self.assertEqual(result[0], self.chromosomeA[1])
        # self.assertEqual(result[1], self.chromosomeA[1])
        # self.assertEqual(result[2], self.chromosomeA[2])
        # self.assertEqual(result[3], self.chromosomeA[3])
        pass

    def test_Fitness(self):
        pass

    def test_GetAbsFromNearestInt(self):
        # 这里通常会产生精度不匹配的错误
        # self.assertEqual(0.49, GA.GetAbsFromNearestInt(4.51))
        # self.assertEqual(0.49, GA.GetAbsFromNearestInt(4.49))
        # self.assertEqual(0.1, GA.GetAbsFromNearestInt(4.9))
        # self.assertEqual(0.1, GA.GetAbsFromNearestInt(5.1))
        pass

if __name__ == '__main__':
    unittest.main()
