import matplotlib.pyplot as plt
import FormatData
import tensorflow as tf
import numpy as np

cpuSeries = FormatData.FormatCpuData()
requestTotle = FormatData.FormatRequest200Total()

# podNameList = FormatData.GetPodName()


goodPodNameList = ["prod-ssl-cookie-v1-7b4d5fbbdb-jzlfd", "prod-ssl-cookie-v1-7b4d5fbbdb-rddgj", "prod-ssl-cookie-v1-7b4d5fbbdb-hphv9", "prod-ssl-cookie-v1-7b4d5fbbdb-qnrjb",
                   "prod-ssl-cookie-v1-7b4d5fbbdb-r2fcc"]

x = []
y = []
origin = []

for podName in goodPodNameList:
    cpu = cpuSeries.loc[podName].diff().iloc[1:]
    request = requestTotle.loc[podName].diff().iloc[1:]
    reqPerCpu = request.values / cpu.values

    origin.append(reqPerCpu)
    x.append(reqPerCpu[0:1000])
    y.append(reqPerCpu[1000:])

x_train = np.asarray(x).reshape(len(goodPodNameList), 1000, 1)
y_train = np.asarray(y).reshape(len(goodPodNameList), 8)

print(y_train)

model = tf.keras.models.Sequential([
    tf.keras.layers.SimpleRNN(20, return_sequences=True, input_shape=[None, 1]),
    tf.keras.layers.SimpleRNN(20),
    tf.keras.layers.Dense(8)
])

# model = tf.keras.models.Sequential([
#     tf.keras.layers.LSTM(8, return_sequences=True, input_shape=[None, 1]),
#     tf.keras.layers.LSTM(8),
#     tf.keras.layers.Dense(8)
# ])

optimizer = tf.keras.optimizers.Adam(lr=0.02)
model.compile(optimizer=optimizer, loss='mae')

EPOCHS = 1000

model.fit(x=x_train, y=y_train, epochs=EPOCHS)

print(model.predict(x_train))

cpuTest = cpuSeries.loc['prod-ssl-cookie-v1-7b4d5fbbdb-jzlfd'].diff().iloc[1:]
requestTest = requestTotle.loc['prod-ssl-cookie-v1-7b4d5fbbdb-jzlfd'].diff().iloc[1:]
reqPerCpuTest = requestTest.values / cpuTest.values

x_test = reqPerCpuTest[:1000]
x_test = x_test.reshape(1, 1000, 1)

plt.figure()

for fvk in origin:
    plt.plot(range(108), fvk[-108:])

plt.plot(range(100, 108), model.predict(x_test)[0], c='red', marker='x')
plt.show()
