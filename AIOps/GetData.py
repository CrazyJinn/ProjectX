import pandas as pd
import numpy as np


# 直接根据index循环遍历：
# for index in serieList.index:
#     df = serieList.query('index == [@index]').dropna(axis=1)

def get_http_requests_received_total_error(df):
    df = df.loc[(df['endpoint'] == 'http') & (df['code'] != 200)]
    table = pd.pivot_table(df, values='value',
                           index=['controller', 'action'],
                           aggfunc=lambda x: list(x.sum()))
    return table


def get_request_error(df, magicNumber):
    serieList = get_http_requests_received_total_error(df)
    result = dict()
    for data in serieList.itertuples():
        index = data[0]
        value = data[1]
        for row in range(int(len(value)/magicNumber)):
            rowStart = magicNumber*row
            rowEnd = magicNumber*(row+1)
            temp = value[rowStart:rowEnd]
            if (len(temp) == magicNumber):
                key = str(index[0]+"/"+index[1]) +\
                    "---row#:" + str(rowStart) + "~" + str(rowEnd)
                result[key] = np.array(temp).reshape(magicNumber)


    # for index in serieList.index:
    #     df = serieList.query('index == [@index]').dropna(axis=1)
    #     print(df.index.values)
    #     print(df.to_numpy())
        # for value in df.values:
        #     for row in range(len(value)/magicNumber):
        #         rowStart = magicNumber*row
        #         rowEnd = magicNumber*(row+1)
        #         temp = df.iloc[rowStart:rowEnd]
        #         if (temp.shape[0] == magicNumber):
        #             key = str(index) +\
        #                 "---row#:" + str(rowStart) + "~" + str(rowEnd)
        #             result[key] = np.array(temp.values).reshape(magicNumber)
    return result


def get_http_request_duration_seconds_bucket(df):
    df = df.loc[(df['endpoint'] == 'http') & (df['code'] == 200)]  # 先只算http200
    table = pd.pivot_table(df, values='value',
                           index=['controller', 'action', 'le'],
                           aggfunc=lambda x: list(x.sum()))   # https://github.com/pandas-dev/pandas/issues/24016#issuecomment-443232529
    return table


def get_P90(df, magicNumber):
    serieList = get_http_request_duration_seconds_bucket(df)
    result = dict()
    for controller in serieList.index.levels[0]:
        for action in serieList.index.levels[1]:
            df = serieList.query(
                'controller == [@controller] and action == [@action]')
            if(df.empty):  # 因为分层级遍历index levels的时候，会拼凑出不存在的index，所以这里要排除掉
                continue
            P90 = df.apply(Quantile, axis=0, **{'n': 90})
            P90 = P90.fillna(method='ffill')  # 锚点1 切流量造成的数据缺失 2#按照上一个值填充
            P90 = P90.fillna(P90.mean())  # 在进行2#补充之后，首值还是可能会是nan，此时用均值填充
            for row in range(int(P90.shape[0]/magicNumber)):
                rowStart = magicNumber*row
                rowEnd = magicNumber*(row+1)
                temp = P90.iloc[rowStart:rowEnd]
                if (temp.shape[0] == magicNumber):
                    key = str(controller+"/"+action) +\
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
        dataList.append(value)

    dataList = np.array(dataList)
    observations = dataList[len(buckets)-1]
    rankList = n * observations / 100
    result = []
    for (data, rank) in zip(dataList.T, rankList):
        if(data[-1] < 2.0):
            result.append(np.nan)  # 锚点1 切流量的情况下会没数据或者间歇性的一两个请求，这里直接置为nan，方便之后统一填充
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
