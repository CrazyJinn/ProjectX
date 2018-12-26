'''
使用遗传算法生成图像
使用CNN来判别生成出来的图像质量。换言之，使用CNN来计算fit
非常依赖CNN本身的判别效果，若判别错，并没有更新CNN
'''


import numpy as np
import GA as ga
import Chromosome as ch
import tensorflow as tf

import matplotlib.pyplot as plt


def gen_image(arr):
    image = np.array(arr, dtype='float').reshape((28, 28))
    plt.imshow(image,  cmap='gray')
    return plt


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='VALID')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                          strides=[1, 2, 2, 1], padding='VALID')


x = tf.placeholder(tf.float32, [None, 784])
x_image = tf.reshape(x, [-1, 28, 28, 1])

W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

# 如果padding使用SAME，则这里要使用7*7*64作为输出
W_fc1 = weight_variable([4 * 4 * 64, 1024])
b_fc1 = bias_variable([1024])
h_pool2_flat = tf.reshape(h_pool2, [-1, 4 * 4 * 64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder("float")
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])

y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)


def FitnessForMNIST(population, samplingList):
    '''
    计算MNIST适应度
    '''
    ChromosomeResult = []
    fitList = []
    for chromosome in population:
        aaa = ch.GetChromosomeResult(chromosome[0], samplingList) / 10
        aaa[aaa > 1] = 1
        aaa[aaa < 0] = 0
        ChromosomeResult.append(aaa)

    with tf.Session() as sess:
        saver = tf.train.Saver()
        saver.restore(sess, "C:/Users/jj84/Desktop/result/MNIST.ckpt")
        aaa = y_conv.eval(feed_dict={x: ChromosomeResult, keep_prob: 1.0})
        for temp in aaa:
            fitList.append(temp[7])

    return fitList


population = []
populationCount = 300
for i in range(populationCount):
    population.append([ch.GenerateChromosome(), 0.0])

xSamplingList = []
for i in range(784):
    xSamplingList.append(i)


for i in range(300):
    for temp in population:
        if(i % 50 == 0):
            temp[0] = ga.Append(temp[0])

    fit = FitnessForMNIST(population, xSamplingList)
    for p in range(populationCount):
        population[p][1] = fit[p]

    population = ga.Evolve(population)
    print(i)


for chromosome in population[:3]:
    aaa = ch.GetChromosomeResult(chromosome[0], xSamplingList) / 10
    aaa[aaa > 1] = 1
    aaa[aaa < 0] = 0
    print("final:", aaa)
    gen_image(aaa).show()
