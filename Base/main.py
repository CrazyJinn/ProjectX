import numpy as np
import matplotlib.pyplot as plt


train_X = np.asarray([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
train_Y = np.asarray([0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0])

plt.figure()
plt.ion()
plt.axis([0.0, 13.01, 0.0, 1.01])

# lista = []
# for i in range(150):
#     lista.append(i / 10)
# train_X = np.asarray(lista)

plt.xlabel("x")
plt.ylabel("y")
plt.plot(train_X, train_Y, 'ro', label='Original data')
# plt.plot(train_X, (train_X - 6) * (train_X - 6) + 1, label='Fitted line')
plt.pause(10)


# plt.figure()
# plt.ion()
# plt.axis([0.0, 13.01, 0.0, 11.01])

# train_X = numpy.asarray([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
# train_Y = numpy.asarray([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
# paint_X = numpy.asarray([-100.0, 100.0])
# plt.plot(train_X, train_Y, 'ro', label='Original data')
# plt.plot(paint_X, paint_X/2 , label='Fitted line')
# plt.pause(10)
