import matplotlib.pyplot as plt
from numpy.lib.financial import fv
import GetData as gd
import numpy as np
from sklearn.cluster import DBSCAN

trainPath = 'D:/GitHub/project/AIOps/train/process_cpu_seconds_total.csv'

test_NERealtime_Path = 'D:/GitHub/project/AIOps/test_NERealtime/process_cpu_seconds_total.csv'

magicNumber = 144


def FormatSeriesData(cpuSeries, podNameList):
    result = np.array([])
    valid_count = 0
    for podName in podNameList:
        cpu = cpuSeries.loc[podName].diff().iloc[1:]
        npArr = np.array(cpu.values).reshape(len(cpu.values))
        for i in range(int(len(npArr) / magicNumber)):
            result = np.append(result, npArr[magicNumber*i: magicNumber*(i+1)])
            valid_count = valid_count+1
    return result.reshape(valid_count, -1, magicNumber)


def SBD(v):
    a = np.ones(magicNumber)  # 暂时全和1比较
    correlate = np.correlate(a, v, mode='full')
    norm1 = np.linalg.norm(a)
    norm2 = np.linalg.norm(v)
    return 1 - np.max(correlate / (norm1 * norm2))


def FindCentroid(labels, sbdValue):
    result = np.dstack((labels, sbdValue))[0]
    print("============ train data =============")
    print(result)
    print("============ ========== =============")
    result = result[np.where(result[:, 0] >= 0)]  # 排除未分类的点(-1为分类失败)
    result = result[np.argsort(result[:, 0])]  # 按照聚类排序
    result = np.split(result[:, 1], np.unique(result[:, 0], return_index=True)[1][1:])
    fvk = []
    for temp in result:
        fvk.append(np.mean(temp, axis=0))
    return fvk


train_series = gd.GetCpuData(trainPath)
train_podNameList = gd.GetPodName(trainPath)
train_data = FormatSeriesData(train_series, train_podNameList)

sbdValue = np.array([])
# line = []
for i in train_data:
    for j in i:
        sbdValue = np.append(sbdValue, SBD(j))

clustering = DBSCAN(eps=0.010, min_samples=2).fit(sbdValue.reshape(-1, 1))


centroidList = FindCentroid(clustering.labels_, sbdValue)
print(centroidList)


test_NERealtime_series = gd.GetCpuData(test_NERealtime_Path)
test_NERealtime_podNameList = gd.GetPodName(test_NERealtime_Path)
test_NERealtime_data = FormatSeriesData(test_NERealtime_series, test_NERealtime_podNameList)
error_NERealtime_dataArr = []
right_NERealtime_dataArr = []

print("============ test Error data =============")
for i in test_NERealtime_data:
    for j in i:
        sbd = SBD(j)
        fvk = abs(centroidList - sbd)
        for aaa in fvk:
            if aaa > 0.2:
                print(sbd)
                error_NERealtime_dataArr.append(j)
            else:
                right_NERealtime_dataArr.append(j)
print("============ ============ =============")


print(error_NERealtime_dataArr[0][:42])
print(SBD(error_NERealtime_dataArr[0][:42]))

# fake_series = [12.63, 11.84,  9.85, 10.15, 10.13,
#                10.5,  8.02,  8.39,  8.77,  8.6199999,
#                10.1000001, 10.85, 11.26, 11.78,  9.5,
#                8.86,  8.92,  8.68,  8.13,  7.6699999,
#                8.2700001,  8.45,  9.41, 10.,  8.53,
#                8.24,  9.04,  5., 0.,  0., ]

# print(SBD(fake_series))


plt.figure()

# plt.plot(range(len(fake_series)), fake_series, "orange")
plt.plot(range(144), train_data[0][0], c="red")

for i in error_NERealtime_dataArr[0:2]:
    plt.plot(range(144), i, "orange")

for i in right_NERealtime_dataArr[0:2]:
    plt.plot(range(144), i, "blue")

plt.show()
