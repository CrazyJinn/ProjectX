import tensorflow as tf
import codecs
import os
import numpy as np


vocab = codecs.open('C:\\Users\\jj84\\Desktop\\李白五言.txt',
                    encoding='utf-8').read().replace('\n', '').replace('\r', '')
int_to_vocab = dict(enumerate(vocab))
vocab_to_int = {c: i for i, c in enumerate(vocab)}

lstm_inputs = vocab
nSeqs = 100
nSteps = 12
lstmSize = 128
numLayers = 2
learningRate = 0.01
keepProb = 0.5
numClass = len(vocab)


def WordToInt(word):
    return vocab_to_int[word]


def VocabToIntArr(vocab):
    result = []
    for word in vocab:
        result.append(WordToInt(word))
    return np.array(result)


def GetBatch(arr, nSeqs, nSteps):
    batchSize = nSeqs * nSteps
    nBatch = int(len(arr) / batchSize)

    arr = arr[:batchSize * nBatch]
    arr = arr.reshape((nSeqs, -1))
    for i in range(0, arr.shape[1], nSteps):
        x = arr[:, i:i + nSteps]
        y = np.zeros_like(x)
        # y[:, :-1], y[:, -1] = x[:, 1:], x[:, 0] #??
        yield x, y


def BuildLSTM(lstmSize, numLayers, batchSize, keepProb):
    lsmt = tf.nn.rnn_cell.BasicLSTMCell(lstmSize)
    drop = tf.nn.rnn_cell.DropoutWrapper(lsmt, keepProb)
    cell = tf.nn.rnn_cell.MultiRNNCell([drop for _ in range(numLayers)])
    initCell = cell.zero_state(batchSize, tf.float32)
    return cell, initCell


def BuildOutput(lstmOutput, inputSize, outputSize):
    seqOutput = tf.concat(lstmOutput, 1)
    x = tf.reshape(seqOutput, [-1, inputSize])
    logits = tf.matmul(x, softmaxW) + softmaxB
    out = tf.nn.softmax(logits)
    return out, logits


def BuildLoss(logits, targets, lstmSize):
    yOneHot = tf.one_hot(targets, numClass)
    yReshape = tf.reshape(yOneHot, logits)

    loss = tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=yReshape)
    loss = tf.reduce_mean(loss)

    return loss


def BuildOptimizer(loss, learningRate, gradClip):
    tvars = tf.trainable_variables()
    grads = tf.clip_by_global_norm(tf.gradients(loss, tvars), gradClip)
    trainOp = tf.train.AdamOptimizer(learning_rate=learningRate)
    optimizer = trainOp.apply_gradients(zip(grads, tvars))
    return optimizer


asd = VocabToIntArr(vocab)

inputs = tf.placeholder(tf.int32, shape=(nSeqs, nSteps), name='input')
targets = tf.placeholder(tf.int32, shape=(nSeqs, nSteps), name='target')
keep_prob = tf.placeholder(tf.float32, name='keep_prod')

softmaxW = tf.Variable(tf.truncated_normal([lstmSize, numClass], stddev=0.1))
softmaxB = tf.Variable(tf.zeros(numClass))


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for (x, y) in GetBatch(asd, nSeqs, nSteps):
        cell, initState = BuildLSTM(lstmSize, numLayers, nSeqs, keepProb)
        xOneHot = tf.one_hot(inputs, numClass)
        output, state = tf.nn.dynamic_rnn(cell, xOneHot, initial_state=initState)

        _, logits = BuildOutput(output, lstmSize, numClass)
        loss = BuildLoss(logits, targets, lstmSize)
        optimizer = BuildOptimizer(loss, learningRate, 5)
        sess.run([loss, state, optimizer], feed_dict={inputs: x, targets: y, keep_prob: keepProb})
