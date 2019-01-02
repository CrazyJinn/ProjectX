import numpy as np
import GA as ga
import Chromosome as ch

# population = []
# for i in range(300):
#     population.append([ch.GenerateChromosome(), 0.0])

# samplingList = [1]

noteList = [5,5,6,8,
            8,6,5,3,
            1,1,3,5,
            5,3,3]

melody = [2,2,2,2,
          2,2,2,2,
          2,2,2,2,
          3,1,4]

# noteList = [5,5,6,8,
#             8,6,5,3,
#             1,1,3,5,
#             5,3,3,
#             5,5,6,8,
#             8,6,5,3,
#             1,1,3,5,
#             3,1,1]
# for i in range(280):
#     noteList.append((i / 10) - 1)


def noteFilter(noteList):
    result = np.ceil(noteList)
    result[result < 0] = 0
    return result


noteList = noteFilter(noteList)


def getInterval(firstNote, secondNote): 
    return secondNote - firstNote + 1

def getIntervalList(noteList):
    result = []
    for i in range(len(noteList) -1):
        result.append(getInterval(noteList[i],noteList[i+1]))
    return result

def getFit(noteList,melody):
    fit = 0
    for i in range(len(noteList) -1):
        interval = getInterval(noteList[i],noteList[i+1])
        if(interval)
    return result

print(getIntervalList(noteList))

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
