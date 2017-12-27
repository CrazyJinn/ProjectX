import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
# Import MINST data
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

batch_xs, batch_ys = mnist.test.next_batch(1)
two_d = (np.reshape(batch_xs[0], (28, 28)) * 255).astype(np.uint8)
plt.imshow(two_d, interpolation='nearest')
plt.show()