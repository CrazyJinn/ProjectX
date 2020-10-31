import csv

dic = {}

with open('TestData\TestData.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if(dic.__contains__(row[0])):
            dic[row[0]].append(row[1])
        else:
            dic[row[0]] = [row[1]]

# qqq = ["10-840-001", "10-840-002", "10-840-003",
#        "10-840-004", "10-840-005", "10-840-006"]

tempArr = []

for key in dic.keys():
    asd = dic[key].__len__() - 4
    for i in range(asd):
        tempArr.append(dic[key][i:i+5])

for temp in tempArr:
    print(temp)
