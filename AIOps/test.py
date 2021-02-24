import matplotlib.pyplot as plt
import GetData as gd
import numpy as np
from sklearn.cluster import DBSCAN

trainPath = 'D:/GitHub/project/AIOps/train/process_cpu_seconds_total.csv'
testPath = 'D:/GitHub/project/AIOps/test/process_cpu_seconds_total.csv'

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
    result = result[np.where(result[:, 0] >= 0)]  # 排除未分类的点(-1为分类失败)
    result = result[np.argsort(result[:, 0])]  # 按照聚类排序
    result = np.split(result[:, 1], np.unique(result[:, 0], return_index=True)[1][1:])
    fvk = []
    for temp in result:
        fvk.append(np.mean(temp, axis=0))
    return fvk


train_cpuSeries = gd.GetCpuData(trainPath)
train_podNameList = gd.GetPodName(trainPath)
train_data = FormatSeriesData(train_cpuSeries, train_podNameList)

sbdValue = np.array([])
# line = []
for i in train_data:
    for j in i:
        sbdValue = np.append(sbdValue, SBD(j))
        # line.append(j)

clustering = DBSCAN(eps=0.010, min_samples=2).fit(sbdValue.reshape(-1, 1))


centroid = FindCentroid(clustering.labels_, sbdValue)
print(centroid)


test_cpuSeries = gd.GetCpuData(testPath)
test_podNameList = gd.GetPodName(testPath)
test_data = FormatSeriesData(test_cpuSeries, test_podNameList)
error_dataArr = []
for i in test_data:
    for j in i:
        print(SBD(j))
        if SBD(j) - centroid > 0.10:
            error_dataArr.append(j)

# print(error_dataArr)


plt.figure()


plt.plot(range(len(error_dataArr[0])), error_dataArr[0], "blue")

plt.plot(range(144), train_data[0][0], c="red")
plt.plot(range(144), test_data[0][0], c="green")

plt.show()
