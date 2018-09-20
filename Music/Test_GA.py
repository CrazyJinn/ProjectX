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

        result = GA.Crossover(self.chromosomeA, self.chromosomeB)
        self.assertEqual(result, self.chromosomeC)

    def test_Mutation(self):
        result = GA.Mutation(self.chromosomeA)
        self.assertNotEqual(result[0], self.chromosomeA[0])
        self.assertEqual(result[1], self.chromosomeA[1])
        self.assertEqual(result[2], self.chromosomeA[2])
        self.assertEqual(result[3], self.chromosomeA[3])

    def test_Append(self):
        result = GA.Append(self.chromosomeA)
        self.assertEqual(len(result), len(self.chromosomeA) + 1)
        self.assertEqual(result[0], self.chromosomeA[1])
        self.assertEqual(result[1], self.chromosomeA[1])
        self.assertEqual(result[2], self.chromosomeA[2])
        self.assertEqual(result[3], self.chromosomeA[3])


if __name__ == '__main__':
    unittest.main()
