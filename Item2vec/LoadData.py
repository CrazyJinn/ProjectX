import csv
import collections
import numpy as np


vocabulary_size = 4


def LoadData(fileName):
    with open(fileName, 'r') as f:
        dic = dict()
        itemDic = dict()
        data = csv.reader(f)
        for row in data:
            if(dic.__contains__(row[0])):
                dic[row[0]].append(row[1])
            else:
                dic[row[0]] = [row[1]]
            if(itemDic.__contains__(row[1])):
                itemDic[row[1]] += 1
            else:
                itemDic[row[1]] = 1
        return (dic, itemDic)


(dic, itemDic) = LoadData('TestData\TestData.csv')


count = [['UNK', -1]]
count.extend(collections.Counter(itemDic).most_common(vocabulary_size - 1))
print(count)

dictionary = dict()
for item, _ in count:
    dictionary[item] = len(dictionary)
data = list()
unk_count = 0
for word in itemDic:
    if word in dictionary:
        index = dictionary[word]
    else:
        index = 0  # dictionary['UNK']
        unk_count += 1
    data.append(index)
    count[0][1] = unk_count
    reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))

print(reverse_dictionary)

# for key in dic.keys():
#     asd = dic[key].__len__() - 4
#     for i in range(asd):
#         tempArr.append(dic[key][i:i+5])
