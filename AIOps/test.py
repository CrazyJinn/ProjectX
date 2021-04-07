from typing import ValuesView
import matplotlib.pyplot as plt
from numpy.lib.financial import fv
import GetData as gd
import numpy as np
import pandas as pd

trainPath = 'D:/GitHub/project/AIOps/train/http_request_duration_seconds_bucket.csv'


def get_http_request_duration_seconds_bucket(path):
    df = pd.read_csv(path, low_memory=False)
    df = df.loc[(df['endpoint'] == 'http') & (df['code'] == 200)]  # 先只算http200
    table = pd.pivot_table(df, values='value',
                           index=['controller', 'action', 'pod', 'le'],
                           aggfunc=np.sum)
    return table


def format_P90(path, magicNumber):
    serieList = get_http_request_duration_seconds_bucket(path)
    result = dict()
    for controller in serieList.index.levels[0]:
        for action in serieList.index.levels[1]:
            for pod in serieList.index.levels[2]:
                df = serieList.query(
                    'controller == [@controller] and action == [@action] and pod == [@pod]')
                if(df.empty):   #因为分层级遍历index levels的时候，会拼凑出不存在的index，所以这里要排除掉
                    continue
                P90 = df.apply(Quantile, axis=0, **{'n': 90})
                for row in range(int(P90.shape[0]/magicNumber)):
                    rowStart = magicNumber*row
                    rowEnd = magicNumber*(row+1)
                    temp = P90.iloc[rowStart:rowEnd]
                    if (temp.shape[0] == magicNumber):
                        key = str(controller+"__"+action+"__"+pod) +\
                            "---row#:" + str(rowStart) + "~" + str(rowEnd)
                        result[key] = np.array(temp.values).reshape(magicNumber)
    return result


def Quantile(x, n):
    buckets = [0.001, 0.002, 0.004, 0.008, 0.016, 0.032, 0.064, 0.128,
               0.256, 0.512, 1.024, 2.048, 4.096, 8.192, 16.384, 32.768, 99.99]

    dataList = list()
    # for value in x.values:
    #     nparr = np.zeros(len(value[0]))
    #     for temp in value:
    #         nparr += np.array(eval(temp))
    #     dataList.append(nparr)
    # http200和其他错误请求不分开的时候用上面，如果只计算http200就用下面
    for value in x.values:
        dataList.append(eval(value))

    dataList = np.array(dataList)
    observations = dataList[len(buckets)-1]
    rankList = n * observations / 100
    result = []
    for (data, rank) in zip(dataList.T, rankList):
        if(rank < 3.0):
            result.append(0.0)  # 切流量的情况下会没数据或者间歇性的一两个请求，3种策略：1#补零 2#按照上一个值填充 3#直接抠掉
            continue
        b = 0
        for i in range(len(data)-1):
            if(data[i] >= rank):
                b = i
                break
        bucketEnd = buckets[b]
        bucketStart = buckets[b-1]
        count = data[b] - data[b-1]
        rank -= data[b-1]
        result.append(bucketStart + (bucketEnd-bucketStart)*(rank/count))
    return result


serieList = format_P90(trainPath, 120)
print(serieList)
