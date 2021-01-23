import matplotlib.pyplot as plt
import FormatData
import tensorflow as tf
import numpy as np

cpuSeries = FormatData.FormatCpuData()

goodPodNameList = ["prod-ssl-cookie-v1-7b4d5fbbdb-jzlfd", "prod-ssl-cookie-v1-7b4d5fbbdb-rddgj", "prod-ssl-cookie-v1-7b4d5fbbdb-hphv9", "prod-ssl-cookie-v1-7b4d5fbbdb-qnrjb",
                   "prod-ssl-cookie-v1-7b4d5fbbdb-r2fcc"]

x = []
y = []
origin = []

for podName in goodPodNameList:
    cpu = np.asarray(cpuSeries.loc[podName].diff().iloc[1:])
    origin.append(cpu)
    x.append(cpu[0:864])
    y.append(cpu[864:])

x_train = np.asarray(x).reshape(len(goodPodNameList), 864, 1)
y_train = np.asarray(y).reshape(len(goodPodNameList), 144)

print(y_train)

# model = tf.keras.models.Sequential([
#     tf.keras.layers.SimpleRNN(20, return_sequences=True, input_shape=[None, 1]),
#     tf.keras.layers.SimpleRNN(20),
#     tf.keras.layers.Dense(8)
# ])

model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(20, return_sequences=True, input_shape=[None, 1]),
    tf.keras.layers.LSTM(20),
    tf.keras.layers.Dense(144)
])

model.compile(optimizer='adam', loss='mae')

EPOCHS = 1000

model.fit(x=x_train, y=y_train, epochs=EPOCHS, batch_size=144)

# print(model.predict(x_train))

cpuTest = np.asarray(cpuSeries.loc['prod-ssl-cookie-v1-7b4d5fbbdb-r84hb'].diff().iloc[1:])

x_test = cpuTest[-144:]
x_test = np.asarray(x_test).reshape(1, 144, 1)

plt.figure()

# for fvk in origin:
#     plt.plot(range(144), fvk[-144:], c='blue')
plt.plot(range(144), cpuTest[-144:], c='blue')
plt.plot(range(144), model.predict(x_test)[0], c='red', marker='x')
plt.show()
