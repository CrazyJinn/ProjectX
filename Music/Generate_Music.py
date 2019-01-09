import numpy as np
import GA as ga
import Chromosome as ch
import time


def NoteFilter(noteList):
    result = np.ceil(noteList)
    result[result < 0] = 0

    # # todo 这里将音符归一化写得不好，要修改
    # minNote = 0
    # for note in sorted(list(set(result))):
    #     if(note != 0):
    #         minNote = note - 1
    #         break
    # result -= minNote
    # result[result < 0] = 0
    # # end todo
    return result


def GetInterval(firstNote, secondNote):
    if(firstNote == 0 or secondNote == 0):
        return 0
    else:
        return np.abs(secondNote - firstNote) + 1


def GetIntervalList(noteList):
    result = []
    for i in range(len(noteList) - 1):
        result.append(GetInterval(noteList[i], noteList[i + 1]))
    return result


def GetNoiseCount(noteList, melody):
    result = 0
    for i in range(len(noteList) - 1):
        interval = GetInterval(noteList[i], noteList[i + 1])
        if(interval > 8 and melody[i] <= 2):
            result += 1
    return result


def GetZeroCount(noteList, melody):
    result = 0
    for note in noteList:
        if(note == 0):
            result += 1
    return result


def GetSamplingList(melody):
    result = [0]
    sampling = 0
    for index in melody:
        sampling += index
        result.append(sampling)
    return result


def GetFit(chromosome, melody):
    samplingList = GetSamplingList(melody)
    noteList = ch.GetChromosomeResultWithFilter(
        chromosome, samplingList, NoteFilter)
    fit = GetZeroCount(noteList, melody)
    fit += GetNoiseCount(noteList, melody)
    return fit


start = time.clock()

population = []
populationQuantity = 300
for i in range(populationQuantity):
    population.append(ch.GenerateChromosome())

melody = [2, 2, 2, 2,
          2, 2, 2, 2,
          2, 2, 2, 2,
          3, 1, 4]

samplingList = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 27, 28, 32]


for i in range(300):
    fitList = []
    for chromosome in population:
        if(i % 50 == 0):
            chromosome = ga.Append(chromosome)

        fitList.append(GetFit(chromosome, melody))

    population = ga.WeedOut(population, fitList, 100)
    population = ga.Evolve(population, populationQuantity)
    print(i)
    # input('------------------')

print('+++++++++++++++++')
print(GetFit(population[0], melody))
print(ch.GetChromosomeResultWithFilter(
    population[0], samplingList, NoteFilter))
print("time span:", time.clock() - start)
print('+++++++++++++++++')
