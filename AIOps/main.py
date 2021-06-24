import matplotlib.pyplot as plt
from numpy.lib.financial import fv
import GetData as gd
import numpy as np
from sklearn.cluster import DBSCAN
import pandas as pd

# trainPath = 'D:/GitHub/project/AIOps/train/http_request_duration_seconds_bucket.csv'

trainPath = 'D:/GitHub/project/AIOps/debugData/333.csv'
train_df = pd.read_csv(trainPath, low_memory=False)

magicNumber = 60


def SBD(v):
    a = np.ones(magicNumber)  # 暂时全和1比较
    correlate = np.correlate(a, v, mode='full')
    norm1 = np.linalg.norm(a)
    norm2 = np.linalg.norm(v)
    return 1 - np.max(correlate / (norm1 * norm2))


def FindCentroid(labels, sbdValue):
    result = np.dstack((labels, sbdValue))[0]
    # print("============ train data =============")
    # print(result)
    # print("============ ========== =============")
    result = result[np.where(result[:, 0] >= 0)]  # 排除未分类的点(-1为分类失败)
    result = result[np.argsort(result[:, 0])]  # 按照聚类排序
    result = np.split(result[:, 1], np.unique(result[:, 0], return_index=True)[1][1:])
    fvk = []
    for temp in result:
        fvk.append(np.mean(temp, axis=0))
    return fvk


train_data = gd.get_P90(train_df, magicNumber)

print(train_data)


sbdValue = np.array([])

for key, value in train_data.items():
    # print(key)
    # print(value)
    # print(SBD(value))
    sbdValue = np.append(sbdValue, SBD(value))

clustering = DBSCAN(eps=0.005, min_samples=5).fit(sbdValue.reshape(-1, 1))

print(clustering.labels_)

centroid = FindCentroid(clustering.labels_,sbdValue)

print(centroid)

# result = list(zip(clustering.labels_, sbdValue, train_data.keys(), train_data.values()))

# result = sorted(result, key=lambda x: (x[0]))  # 根据类型排序

# # print(result)

# plt.figure()
# flag0 = 0
# flag1 = 0
# flag2 = 0
# flag3 = 0
# for temp in result:
#     # if(temp[0] == -1 and temp[1] < 0.1 and flag0 < 4):
#     #     plt.plot(range(magicNumber), temp[3], c="black")
#     #     print(temp)
#     #     flag0 += 1
#     # if(temp[0] == 0 and flag1 < 10):
#     #     plt.plot(range(magicNumber), temp[3], c="red")
#     #     print(temp[2])
#     #     flag1 += 1
#     # if(temp[0] == 1 and flag2 < 10):
#     #     plt.plot(range(magicNumber), temp[3], c="blue")
#     #     print(temp[2])
#     #     flag2 += 1
#     # if(temp[0] == 2 and flag3 < 1):
#     #     plt.plot(range(magicNumber), temp[3], c="orange")
#     #     print(temp[2])
#     #     flag3 += 1

# plt.show()
