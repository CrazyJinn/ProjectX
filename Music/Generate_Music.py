import numpy as np
import GA as ga
import Chromosome as ch

# population = []
# for i in range(300):
#     population.append([ch.GenerateChromosome(), 0.0])

# samplingList = [1]

noteList = []
for i in range(280):
    noteList.append((i / 10) - 1)


def noteFilter(noteList):
    result = np.ceil(noteList)
    result[result < 0] = 0
    return result


noteList = noteFilter(noteList)


def interval(aNote, bNote):
    
    return aNote - bNote + 1



    # ch.GetChromosomeResultWithFilter(chromosome,samplingList,filter)

    # # 这里是计算music适应度的

    # def Fitness(chromosome, samplingList):
    #     '''
    #     计算适应度
    #     '''
    #     result = 0.0
    #     for sampling in samplingList:
    #         result = result + GetAbsFromNearestInt(ch.GetChromosomeResult(chromosome, sampling))
    #     return result

    # def GetAbsFromNearestInt(number):
    #     temp = round(number)
    #     return np.abs(number - temp)

    # 这里是计算music适应度的 end
