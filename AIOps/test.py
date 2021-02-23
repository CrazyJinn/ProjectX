import matplotlib.pyplot as plt
import FormatData
import numpy as np
from sklearn.cluster import DBSCAN
# import tensorflow as tf

cpuSeries = FormatData.FormatCpuData()

podNameList = FormatData.GetPodName()


x = []
for podName in podNameList.values:
    cpu = cpuSeries.loc[podName].diff().iloc[1:]
    xNp = np.array(cpu.values).reshape(len(cpu.values))
    xRange = np.max(xNp) - np.min(xNp)
    x.append((xNp - np.min(xNp))/xRange)


def np_move_avg(a, n=10, mode="same"):
    return(np.convolve(a, np.ones((n,))/n, mode=mode))


def SBD(a, v):
    correlate = np.correlate(a, v, mode='full')
    norm1 = np.linalg.norm(a)
    norm2 = np.linalg.norm(v)
    return 1 - np.max(correlate / (norm1 * norm2))


sbdValue = []
line = []
reshapeX = np.array(x).reshape(5, 10, 144)
baseLine = np.ones(144)
for i in reshapeX:
    for j in i:
        sbdValue.append(SBD(baseLine, j))
        line.append(j)

clustering = DBSCAN(eps=0.015, min_samples=2).fit(np.array(sbdValue).reshape(-1, 1))


def FindCentroid(labels, SBD):
    result = np.dstack((labels, SBD))[0]
    result = result[np.argsort(result[:, 0])]
    # print(np.unique(result[:, 0], return_index=True)[1][1:])
    result = np.split(result[:, 1], np.unique(result[:, 0], return_index=True)[1][1:])
    fvk = []
    for temp in result[1:]:
        fvk.append(np.mean(temp, axis=0))
    return fvk


result = FindCentroid(clustering.labels_, sbdValue)

print(result)


# plt.figure()


# plt.plot(range(144), line[30], c="red")
# plt.plot(range(144), line[41], c="red")

# plt.plot(range(144), line[45], c="blue")
# plt.plot(range(144), line[2], c="blue")

# plt.plot(range(144), line[43], c="green")
# plt.plot(range(144), line[3], c="green")

# # for i in range(50):
# #     if result[i][0] == -1:
# #         print(result[i][2])
# #         plt.plot(range(144), line[int(result[i][2])])

# plt.show()
