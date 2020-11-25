import csv
import collections
import math
import numpy as np
import tensorflow as tf
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


vocabularySize = 70000
dataIndex = 0
userViewMaxNum = 7
batchSize = 128
embeddingSize = 256
skipWindow = 2
numSkip = 4

validSize = 16
validWindow = 100
validExample = np.random.choice(validWindow, validSize, replace=False)
numSampled = 64

numStep = 5000001


def LoadData(fileName):
    """
    Parameter
    ----------
    fileName : string
    Return
    ----------
    userItemDic : dic, key: deviceId; value: [itemNumber1,itemNumber2,……]
    根据deviceId进行聚合后形成的词典

    itemCountDic : dic, key: itemNumber; value: count(itemNumber)
    词频
    """
    with open(fileName, 'r') as f:
        userItemDic = dict()
        itemCountDic = dict()
        data = csv.reader(f)
        for row in data:
            if(row[1] == "" or row[1] == "productmerch" or row[1] == "pl"):
                continue
            if(userItemDic.__contains__(row[0])):
                if(userItemDic[row[0]].__len__() >= userViewMaxNum):
                    continue
                else:
                    userItemDic[row[0]].append(row[1])
            else:
                userItemDic[row[0]] = [row[1]]
            if(itemCountDic.__contains__(row[1])):
                itemCountDic[row[1]] += 1
            else:
                itemCountDic[row[1]] = 1
        return (userItemDic, itemCountDic)


def BuildVocabularyDic(itemCountDic, vocabularySize):
    """
    Parameter
    ----------
    itemCountDic : dic, key: itemNumber; value: count(itemNumber)

    vocabularySize : int
    词汇量, 超过词汇量的低频item直接归类为UNK
    Return
    ----------
    vocabularyDic : dic, key: itemNumber; value: int
    词典

    """
    vocabularyCount = [['UNK', -1]]
    vocabularyCount.extend(collections.Counter(itemCountDic).most_common(vocabularySize - 1))

    vocabularyDic = dict()
    for item, _ in vocabularyCount:
        vocabularyDic[item] = len(vocabularyDic)

    unkCount = 0
    for word in itemCountDic:
        if word in vocabularyDic:
            index = vocabularyDic[word]
        else:
            index = 0  # ['UNK']
            unkCount += 1
        vocabularyCount[0][1] = unkCount
    return vocabularyDic


def FormateData(userItemDic, numSkips):
    """
    将数据长链处理成短链

    例如 itemNumber1,itemNumber2,itemNumber3,itemNumber4,itemNumber5,itemNumber6

    会处理成[[itemNumber1,itemNumber2,itemNumber3,itemNumber4,itemNumber5],
                        [itemNumber2,itemNumber3,itemNumber4,itemNumber5,itemNumber6]]

    Parameter
    ----------
    userItemDic : userItemDic : dic, key: deviceId; value: [itemNumber1,itemNumber2,……]

    numSkips : int

    Return
    ----------
    dataArr : array
    处理完毕的数据集

    """
    dataArr = []
    for key in userItemDic.keys():
        loopCount = userItemDic[key].__len__() - numSkips
        for i in range(loopCount):
            tempArr = []
            for j in range(numSkips + 1):
                tempArr.append(itemToIntDict.get(userItemDic[key][i + j], 0))
            dataArr.append(tempArr)
    return dataArr


def GenerateBatch(batchSize, numSkips, skipWindow, dataArr):
    """
    构造训练集

    Parameter
    ----------
    batchSize : int
    训练集大小

    numSkips : int

    skipWindow : int

    dataArr : array
    Return
    ----------
    batch : array
    训练集

    labels : array
    标签

    """
    global dataIndex
    assert batchSize % numSkips == 0
    assert numSkips <= 2 * skipWindow
    batch = np.ndarray(shape=(batchSize), dtype=np.int32)
    labels = np.ndarray(shape=(batchSize, 1), dtype=np.int32)
    for i in range(batchSize // numSkips):
        for j in range(numSkips):
            batch[i * numSkips + j] = dataArr[dataIndex][skipWindow]
            if(j >= skipWindow):
                labels[i * numSkips + j, 0] = dataArr[dataIndex][j + 1]
            else:
                labels[i * numSkips + j, 0] = dataArr[dataIndex][j]
        dataIndex = (dataIndex + 1) % len(dataArr)
    return batch, labels


def Draw(sampleLowEmbedding, filename='tsne.png'):
    """
    绘制降维后的embedding示例图
    Parameter
    ----------
    sampleEmbedding : array
    """
    plt.figure(figsize=(20, 20))
    plt.xticks([])
    plt.yticks([])
    for i in range(len(sampleLowEmbedding)):
        x, y = sampleLowEmbedding[i, :]
        plt.scatter(x, y, c='gray', marker='o', alpha=0.5, s=200 * 1.5)
    plt.savefig(filename)


# Step 1: Prepare data
userItemDic, itemCountDic = LoadData('./TestData/all-distinct-367W.csv')

vocabularyDic = BuildVocabularyDic(itemCountDic, vocabularySize)

intToItemDict = dict(zip(vocabularyDic.values(), vocabularyDic.keys()))
itemToIntDict = dict(zip(vocabularyDic.keys(), vocabularyDic.values()))

dataArr = FormateData(userItemDic, numSkip)

batch, labels = GenerateBatch(16, 4, 2, dataArr)
for i in range(16):
    print(batch[i], intToItemDict[batch[i]],
          '->', labels[i, 0], intToItemDict[labels[i, 0]])

# Step 2: Build tensor
graph = tf.Graph()
with graph.as_default():
    trainInput = tf.placeholder(tf.int32, shape=[batchSize])
    trainLabel = tf.placeholder(tf.int32, shape=[batchSize, 1])
    validDataset = tf.constant(validExample, dtype=tf.int32)
    with tf.device('/cpu:0'):
        embedding = tf.Variable(
            tf.random_uniform([vocabularySize, embeddingSize], -1.0, 1.0))
        embed = tf.nn.embedding_lookup(embedding, trainInput)
        nceWeight = tf.Variable(tf.truncated_normal(
            [vocabularySize, embeddingSize], stddev=1.0 / math.sqrt(embeddingSize)))
        nceBias = tf.Variable(tf.zeros([vocabularySize]))
    loss = tf.reduce_mean(tf.nn.nce_loss(nceWeight, nceBias, trainLabel,
                                         embed, numSampled, vocabularySize))
    optimizer = tf.train.GradientDescentOptimizer(1.0).minimize(loss)
    norm = tf.sqrt(tf.reduce_sum(tf.square(embedding), 1, keep_dims=True))
    normalizeEmbedding = embedding / norm
    validEmbedding = tf.nn.embedding_lookup(normalizeEmbedding, validDataset)
    similarity = tf.matmul(validEmbedding, normalizeEmbedding, transpose_b=True)
    init = tf.global_variables_initializer()

# Step 3: Begin training
with tf.Session(graph=graph) as session:
    init.run()
    print("Initialized")

    avgLoss = 0
    for step in range(numStep):
        batchInput, batchLabel = GenerateBatch(batchSize, numSkip, skipWindow, dataArr)
        feedDict = {trainInput: batchInput, trainLabel: batchLabel}
        _, lossVal = session.run([optimizer, loss], feed_dict=feedDict)
        avgLoss += lossVal

        if step % 2000 == 0:
            if step > 0:
                avgLoss /= 2000
            print("Average loss at step ", step, ": ", avgLoss)
            avgLoss = 0
        if step % 10000 == 0:
            sim = similarity.eval()
            for i in range(validSize):
                validWord = intToItemDict[validExample[i]]
                topK = 8  # number of nearest neighbors
                nearest = (-sim[i, :]).argsort()[1:topK + 1]
                logStr = "Nearest to %s:" % validWord
                for k in range(topK):
                    closeWord = intToItemDict[nearest[k]]
                    logStr = "%s %s," % (logStr, closeWord)
                print(logStr)
        if (step + 1) % 100000 == 0:
            tf.train.Saver().save(session, './CheckPoint/item2vec.ckpt', global_step=step)

    finalEmbedding = normalizeEmbedding.eval()

# Step 4: Visualize
try:
    tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000)
    sampleCount = 1500
    sampleLowEmbedding = tsne.fit_transform(finalEmbedding[:sampleCount, :])
    Draw(sampleLowEmbedding)

except ImportError:
    print("Please install sklearn, matplotlib, and scipy to visualize.")
