'''
整体思路非常类似于dcGAN，只是生成器换成了遗传算法
'''

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
import GA as ga
import Chromosome as ch

# 该函数将给出权重初始化的方法


def variable_init(size):
    in_dim = size[0]

    # 计算随机生成变量所服从的正态分布标准差
    w_stddev = 1. / tf.sqrt(in_dim / 2.)
    return tf.random_normal(shape=size, stddev=w_stddev)


# 定义输入矩阵的占位符，输入层单元为784，None代表批量大小的占位，X代表输入的真实图片。占位符的数值类型为32位浮点型
X = tf.placeholder(tf.float32, shape=[None, 784])

# 定义判别器的权重矩阵和偏置项向量，由此可知判别网络为三层全连接网络
D_W1 = tf.Variable(variable_init([784, 128]))
D_b1 = tf.Variable(tf.zeros(shape=[128]))

D_W2 = tf.Variable(variable_init([128, 1]))
D_b2 = tf.Variable(tf.zeros(shape=[1]))

theta_D = [D_W1, D_W2, D_b1, D_b2]

samplingList = []
for i in range(28):
    samplingList.append(i)

X_ = tf.placeholder(tf.float32, shape=[None, 784])

# 定义生成器


def filter(result):
    result[result >= 0.5] = 1
    result[result < 0.5] = 0
    return result


def generator(chromosome):
    result = []
    xResult = ch.GetChromosomeResult(chromosome[0], samplingList)
    yResult = ch.GetChromosomeResult(chromosome[1], samplingList)
    for x in xResult:
        for y in yResult:
            result.append(x + y)
    return filter(np.array(result))


population = []
populationCount = 300
for i in range(populationCount):
    population.append([ch.GenerateChromosome(), ch.GenerateChromosome()])


# 定义判别器


def discriminator(x):

    # 计算D_h1=ReLU（x*D_W1+D_b1）,该层的输入为含784个元素的向量
    D_h1 = tf.nn.relu(tf.matmul(x, D_W1) + D_b1)

    # 计算第三层的输出结果。因为使用的是Sigmoid函数，则该输出结果是一个取值为[0,1]间的标量（见上述权重定义）
    # 即判别输入的图像到底是真（=1）还是假（=0）
    D_logit = tf.matmul(D_h1, D_W2) + D_b2
    D_prob = tf.nn.sigmoid(D_logit)

    # 返回判别为真的概率和第三层的输入值，输出D_logit是为了将其输入tf.nn.sigmoid_cross_entropy_with_logits()以构建损失函数
    return D_prob, D_logit

# 该函数用于输出生成图片


def plot(samples):
    fig = plt.figure(figsize=(4, 4))
    gs = gridspec.GridSpec(4, 4)
    gs.update(wspace=0.05, hspace=0.05)

    for i, sample in enumerate(samples):
        ax = plt.subplot(gs[i])
        plt.axis('off')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_aspect('equal')
        plt.imshow(sample.reshape(28, 28), cmap='Greys_r')

    return fig


# 分别输入真实图片和生成的图片，并投入判别器以判断真伪
D_real, D_logit_real = discriminator(X)
D_fake, D_logit_fake = discriminator(X_)

# 以下为原论文的判别器损失和生成器损失，但本实现并没有使用该损失函数
# D_loss = -tf.reduce_mean(tf.log(D_real) + tf.log(1. - D_fake))
# G_loss = -tf.reduce_mean(tf.log(D_fake))

# 我们使用交叉熵作为判别器和生成器的损失函数，因为sigmoid_cross_entropy_with_logits内部会对预测输入执行Sigmoid函数，
# 所以我们取判别器最后一层未投入激活函数的值，即D_h1*D_W2+D_b2。
# tf.ones_like(D_logit_real)创建维度和D_logit_real相等的全是1的标注，真实图片。
D_loss_real = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(
    logits=D_logit_real, labels=tf.ones_like(D_logit_real)))
D_loss_fake = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(
    logits=D_logit_fake, labels=tf.zeros_like(D_logit_fake)))

# 损失函数为两部分，即E[log(D(x))]+E[log(1-D(G(z)))]，将真的判别为假和将假的判别为真
D_loss = D_loss_real + D_loss_fake

# 同样使用交叉熵构建生成器损失函数
G_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(
    logits=D_logit_fake, labels=tf.ones_like(D_logit_fake)))

# 定义判别器和生成器的优化方法为Adam算法，关键字var_list表明最小化损失函数所更新的权重矩阵
D_solver = tf.train.AdamOptimizer().minimize(D_loss, var_list=theta_D)

# 选择训练的批量大小
mb_size = 200

# 读取数据集MNIST，并放在当前目录data文件夹下MNIST文件夹中，如果该地址没有数据，则下载数据至该文件夹
mnist = input_data.read_data_sets("MNIST_data/", one_hot=False)

# 打开一个会话运行计算图
sess = tf.Session()

# 初始化所有定义的变量
sess.run(tf.global_variables_initializer())

# 如果当前目录下不存在out文件夹，则创建该文件夹
if not os.path.exists('out/'):
    os.makedirs('out/')

# 初始化，并开始迭代训练，100W次
i = 0
for it in range(20000):

    # next_batch抽取下一个批量的图片，该方法返回一个矩阵，即shape=[mb_size，784]，每一行是一张图片，共批量大小行
    X_mb = []

    while(len(X_mb) < 50):
        batchX, batchY = mnist.train.next_batch(mb_size)
        for j in range(mb_size):
            if batchY[j] == 5:
                batchX[j][batchX[j] >= 0.5] = 1
                batchX[j][batchX[j] < 0.5] = 0
                X_mb.append(batchX[j])

    bestChromosomeResult = []

    gaRound = 0
    gaMutationRate = 0.05
    while(True):
        ChromosomeResult = []
        fitList = []

        for chromosome in population:
            imgPX = generator(chromosome)
            ChromosomeResult.append(imgPX)

        discriminatorResult = sess.run(
            D_fake, feed_dict={X_: ChromosomeResult})
        for temp in discriminatorResult:
            fitList.append(temp)

        fitListSort = [x for x in sorted(fitList, key=lambda o: o, reverse=True)]
        avgFit = np.mean(fitListSort[:20])
        if(avgFit > 0.50):
            bestChromosomeResult = ChromosomeResult[:16]
            break
        gaRound += 1
        gaMutationRate += 0.001
        if(gaRound > 100):
            for temp in population:
                temp = ga.Append(temp)
            gaRound = 0
            gaMutationRate = 0.05
        population = ga.WeedOut(population, fitList, 100, True)
        population = ga.Evolve(population, populationCount, gaMutationRate)
        print("ga round:", gaRound, ";avg fit:", avgFit, ";chromosome len:", len(population[0][0]))

    print("normal round:", it, ";avg fit:", avgFit)

    # 投入数据并根据优化方法迭代一次，计算损失后返回损失值
    _, D_loss_curr = sess.run([D_solver, D_loss], feed_dict={X: X_mb, X_: ChromosomeResult[:200]})

    # 每2000次输出一张生成器生成的图片
    if it % 50 == 0:
        fig = plot(bestChromosomeResult)
        plt.savefig('out/{}.png'.format(str(i).zfill(3)), bbox_inches='tight')
        i += 1
        plt.close(fig)

    # 每迭代2000次输出迭代数、生成器损失和判别器损失
    if it % 50 == 0:
        print('Iter: {}'.format(it))
        print('D loss: {:.4}'. format(D_loss_curr))
        print()
