import pandas as pd
import numpy as np
import time

# def GetPodName(path):
#     df = pd.read_csv(path)
#     df = df.loc[:, ['pod']].drop_duplicates()
#     return df.pod.values


# def GetCpuData(path):
#     df = pd.read_csv(path)
#     df = df.loc[df['endpoint'] == 'http']
#     table = pd.pivot_table(df, values='value', index=['pod', 'timestamp'])
#     return table


# def GetRequestTotal(path):
#     df = pd.read_csv(path)
#     df = df.loc[df['endpoint'] == 'http']
#     table = pd.pivot_table(df, values='value', index=['pod', 'timestamp', 'code'], aggfunc=np.sum)
#     return table


def get_http_request_duration_seconds_sum(path):
    df = pd.read_csv(path, low_memory=False)
    df = df.loc[df['endpoint'] == 'http']
    table = pd.pivot_table(df, values='value',
                           index=['pod', 'controller', 'action'],
                           columns='timestamp')
    return table


def format_http_request_duration_seconds_sum(path, magicNumber):
    serieList = get_http_request_duration_seconds_sum()
    result = dict()
    serieList = serieList.diff(axis=1)
    for index in serieList.index:
        df = serieList.query('index == [@index]').dropna(axis=1)
        for row in range(int(df.shape[1]/magicNumber)):
            temp = df.iloc[:, magicNumber*row:magicNumber*(row+1)]
            if (temp.shape[1] == magicNumber):
                key = str(index) + ":" + str(magicNumber*row) + "-" + str(magicNumber*(row+1))
                result[key] = np.array(temp.values).reshape(magicNumber)
    return result


def get_http_request_duration_seconds_bucket(path):
    df = pd.read_csv(path, low_memory=False)
    df = df.loc[df['endpoint'] == 'http']
    table = pd.pivot_table(df, values='value',
                           index=['controller', 'action', 'le'],  # 先不根据pod聚合
                           columns='timestamp',
                           aggfunc=np.sum)
    return table


def format_P90(path, magicNumber):
    serieList = get_http_request_duration_seconds_bucket(path)
    result = dict()
    for controller in serieList.index.levels[0]:
        for action in serieList.index.levels[1]:
            # if(action != "SplitOrder"):
            #     continue
            df = serieList.query(
                'controller == [@controller] and action == [@action]').diff(axis=1).dropna(axis=1)
            #在pod重新部署的时候，会清空request的计数，导致部署完成前计数和前面的累计计数相减得到负数；现在统一置为0
            #当然也可以置为Nan之后截取掉，后面看看效果
            df[df < 0] = 0 
            P90 = df.apply(Quantile, axis=0, **{'n': 90}).fillna(value=0)

            for row in range(int(P90.shape[0]/magicNumber)):
                rowStart = magicNumber*row
                rowEnd = magicNumber*(row+1)
                temp = P90.iloc[rowStart:rowEnd]
                if (temp.shape[0] == magicNumber):
                    key = str(controller+"_"+action) + "---row#:" + str(rowStart) + "~" + \
                        str(rowEnd)+"---time:" + \
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(temp.index[0])) + "~" + \
                        time.strftime("%Y-%m-%d %H:%M:%S",
                                      time.localtime(temp.index[magicNumber-1]))
                    result[key] = np.array(temp.values).reshape(magicNumber)
    return result


def Quantile(x, n):
    buckets = [0.001, 0.002, 0.004, 0.008, 0.016, 0.032, 0.064, 0.128,
               0.256, 0.512, 1.024, 2.048, 4.096, 8.192, 16.384, 32.768]
    observations = x[len(buckets)]
    rank = n * observations / 100

    b = 0
    for i in range(len(x)-1):
        if(x[i] >= rank):
            b = i
            break

    # b = sort.Search(len(buckets)-1, func(i int) bool { return buckets[i].count >= rank })
    bucketEnd = buckets[b]
    bucketStart = buckets[b-1]
    count = x[b] - x[b-1]
    rank -= x[b-1]

    return bucketStart + (bucketEnd-bucketStart)*(rank/count)

# def GetRequest_200Total(path):
#     return GetRequestTotal(path).query('code == [200]')


# def GetRequest_ErrorTotal(path):
#     return GetRequestTotal(path).query('code != [200]')
