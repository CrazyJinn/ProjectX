import matplotlib.pyplot as plt
import FormatData
import tensorflow as tf
import numpy as np
import time

cpuSeries = FormatData.FormatCpuData()

podNameList = FormatData.GetPodName()

x = []
y = []
for podName in podNameList.values:
    cpu = cpuSeries.loc[podName].diff().iloc[1:]
    hourSeries = []
    for i in cpu.index:
        hourSeries.append(time.localtime(i).tm_hour)
    x.append(cpu.values)
    y.append(hourSeries)

a = np.array(x).reshape(5, 1440)
b = np.array(y).reshape(5, 1440)

npArr = np.dstack((a, b))


def GetBatch(step):
    index1 = 144 * step
    index2 = 144 * (step+1)
    x = npArr[:, index1:index2-6]
    y = a[:, index2-6: index2]
    return x, y


xx, yy = GetBatch(0)
print(xx.shape)
print(yy)

# model = tf.keras.models.Sequential([
#     tf.keras.layers.SimpleRNN(20, return_sequences=True, input_shape=[None, 1]),
#     tf.keras.layers.SimpleRNN(20),
#     tf.keras.layers.Dense(144)
# ])
model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(138, return_sequences=True, input_shape=[None, 2]),
    tf.keras.layers.LSTM(138),
    tf.keras.layers.Dense(6)
])

# optimizer = tf.keras.optimizers.Adam(lr=0.02)
model.compile(optimizer='adam', loss='mae')

for step in range(5000):
    print("Step:-----------  :", step)
    x_train, y_train = GetBatch(step % 8)
    model.fit(x=x_train, y=y_train, epochs=1, batch_size=138)


model.save("model")


cpuTest = np.asarray(cpuSeries.loc['prod-ssl-cart-v3-58676fbc6-7qjl9'].diff().iloc[1:])
x_test = cpuTest[-144:-6]
x_test = np.asarray(x_test).reshape(1, 138, 1)

plt.figure()
for fvk in origin:
    plt.plot(range(144), fvk[-144:], c='blue')
plt.plot(range(138, 144), model.predict(x_test)[0], c='red', marker='x')
plt.show()
