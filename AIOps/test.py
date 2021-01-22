import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

x_train = []
y_train = []
for i in range(200):
    time = i * np.pi / 2
    x_train.append(np.cos(i * np.pi / 2))
    y_train.append(np.cos(i * np.pi / 2))

x = np.array(x_train[:100]).reshape(1, 100, 1)
y = np.array(y_train[100:108]).reshape(1, 8)

# print(x)
# print(y)

# x = np.array(x_train)
# y = np.array(y_train)


# model = tf.keras.models.Sequential([
#     tf.keras.layers.Flatten(input_shape=[1, 1]),
#     tf.keras.layers.Dense(8)
# ])

# model = tf.keras.models.Sequential([
#     tf.keras.layers.SimpleRNN(8, return_sequences=True, input_shape=[None, 1]),
#     tf.keras.layers.SimpleRNN(8),
#     tf.keras.layers.Dense(8)
# ])

model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(8, return_sequences=True, input_shape=[None, 1]),
    tf.keras.layers.LSTM(8),
    tf.keras.layers.Dense(8)
])

model.compile(optimizer='adam', loss='mae')


EPOCHS = 1000

model.fit(x=x, y=y, epochs=EPOCHS)

print(model.predict(x))

plt.figure()

plt.plot(range(100), x_train[:100])

for i in range(8):
    plt.scatter(100 + i, model.predict(x)[0][i], c='red', marker='x')

# plt.scatter(100, model.predict(x)[0], c='red', marker='x')

plt.show()
