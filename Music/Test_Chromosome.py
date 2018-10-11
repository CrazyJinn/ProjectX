import Chromosome as ch
import unittest


class Test_Chromosome(unittest.TestCase):
    def setUp(self):
        self.gene1 = [0, 0, 0, 0, 0, 0]
        self.gene2 = [2, 5, 0, -10, 3, -7]
        self.chromosomeA = [[2, 5, 0, -10, 3, -7], [-7, 7, 0, 9, 3, 4],
                            [2, -9, 1, -3, 7, 4], [0, -7, 1, 1, 2, -8]]

    def test_GetGeneResult1(self):
        result = ch.GetGeneResult(self.gene1, 0)
        self.assertEqual(result, 0)

    def test_GetGeneResult2(self):
        result = ch.GetGeneResult(self.gene2, 0)
        self.assertEqual(result, 0)

    def test_GetChromosomeResult(self):
        pass

if __name__ == '__main__':
    unittest.main()