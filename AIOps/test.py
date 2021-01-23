import matplotlib.pyplot as plt
import FormatData
import numpy as np


cpuSeries = FormatData.FormatCpuData()
podNameList = FormatData.GetPodName()

aaa = cpuSeries.loc['prod-ssl-cookie-v1-7b4d5fbbdb-r2fcc']
x = aaa.index[1:]
y = aaa.value.diff().iloc[1:]

goodPodNameList = ["prod-ssl-cookie-v1-7b4d5fbbdb-jzlfd", "prod-ssl-cookie-v1-7b4d5fbbdb-rddgj", "prod-ssl-cookie-v1-7b4d5fbbdb-hphv9", "prod-ssl-cookie-v1-7b4d5fbbdb-qnrjb",
                   "prod-ssl-cookie-v1-7b4d5fbbdb-r2fcc"]

plt.figure()
for podName in goodPodNameList:
    cpu = cpuSeries.loc[podName].diff().iloc[1:]
    if podName == 'prod-ssl-cookie-v1-7b4d5fbbdb-r2fcc':
        plt.plot(x, cpu)
plt.plot(x, y, marker='x')
plt.show()
