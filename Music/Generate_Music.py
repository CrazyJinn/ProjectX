import numpy as np
import GA as ga
import Chromosome as ch

chromosome = [-10, -1, -1, -5, 6, -2]
# population = []
# for i in range(300):
#     population.append([ch.GenerateChromosome(), 0.0])

samplingList = [1]


# for i in range(300):
#     for temp in population:
#         if(i % 50 == 0):
#             temp[0] = ga.Append(temp[0])
#         temp[1] = ga.FitnessForLine(temp[0], xSamplingList, ySamplingList)

#     population = ga.Evolve(population)
#     print(i)


def filter(asd):
    print(asd)

ch.GetChromosomeResultWithFilter(chromosome,samplingList,filter)
