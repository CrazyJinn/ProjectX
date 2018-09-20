import Chromosome as ch
import unittest

class Test_Chromosome(unittest.TestCase):
    def setUp(self):
        self.chromosomeA = [[2, 5, 0, -10, 3, -7], [-3, -1, 0, 8, 4, -4],
                            [2, -9, 1, -3, 7, 4], [7, -5, 0, 3, 8, -1]]
        self.chromosomeB = [[9, 6, 0, 5, 0, 8], [-7, 7, 0, 9, 3, 4],
                            [-3, -10, 0, -1, 9, -10], [0, -7, 1, 1, 2, -8]]
        self.chromosomeC = [[2, 5, 0, -10, 3, -7], [-7, 7, 0, 9, 3, 4],
                            [2, -9, 1, -3, 7, 4], [0, -7, 1, 1, 2, -8]]

    def test_GetGeneResult(self):
        pass

    def test_GetChromosomeResult(self):
        pass