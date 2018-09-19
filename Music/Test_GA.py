

import GA as GA

import unittest


class Test_GA(unittest.TestCase):

    def test_Crossover(self):
        chromosomeA = [[2, 5, 0, -10, 3, -7], [-3, -1, 0, 8, 4, -4],
                       [2, -9, 1, -3, 7, 4], [7, -5, 0, 3, 8, -1]]
        chromosomeB = [[9, 6, 0, 5, 0, 8], [-7, 7, 0, 9, 3, 4],
                       [-3, -10, 0, -1, 9, -10], [0, -7, 1, 1, 2, -8]]
        chromosomeC = [[2, 5, 0, -10, 3, -7], [-7, 7, 0, 9, 3, 4],
                       [2, -9, 1, -3, 7, 4], [0, -7, 1, 1, 2, -8]]
        result = GA.Crossover(chromosomeA, chromosomeB)
        self.assertEqual(result, chromosomeC)


if __name__ == '__main__':
    unittest.main()