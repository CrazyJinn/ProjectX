import csv
import numpy as np


def LoadCpuData(path):
    with open(path, 'r') as f:
        data = csv.reader(f)
        podDic = dict()
        tempValue = 0.0
        for row in data:
            if(row[3] == 'http'):
                if(podDic.__contains__(row[7])):
                    podDic[row[7]].append(round(float(row[2]) - tempValue, 2))
                else:
                    podDic[row[7]] = []
                tempValue = float(row[2])
        return podDic


def LoadRequestTotal(path):
    with open(path, 'r') as f:
        data = csv.reader(f)
        podDic = dict()
        tempValue = 0
        for row in data:
            if(podDic.__contains__(row[11])):
                if(row[4] == "200"):
                    key = row[5] + "_" + row[3] + "_" + row[4]
                    if(podDic[row[11]].__contains__(key)):
                        podDic[row[11]][key].append(round(float(row[2]) - tempValue, 2))
                    else:
                        podDic[row[11]][key] = []
                    tempValue = float(row[2])
            else:
                podDic[row[11]] = dict()
        return podDic


def fvk():
    cpuData = LoadCpuData('./last7days/process_cpu_seconds_total.csv')
    reqsData = LoadRequestTotal('./last7days/http_requests_received_total.csv')
    result = []
    for podName in reqsData.keys():
        if reqsData[podName].__contains__('__200'):
            del reqsData[podName]['__200']  # 去掉faq的请求
        maxLen = len(cpuData[podName])

        tempArr = np.zeros(maxLen)
        for key in reqsData[podName].keys():
            loss = maxLen - len(reqsData[podName][key])
            if loss > 0:
                for _ in range(loss):
                    reqsData[podName][key].append(0.0)
            tempArr = np.sum([tempArr, np.array(reqsData[podName][key])], axis=0)
        result.append(tempArr / np.array(cpuData[podName]))
    return result
