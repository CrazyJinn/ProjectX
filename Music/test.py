import Chromosome_tf as ch_tf
import tensorflow as tf
import numpy as np


xSamplingList = np.asarray([5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0])


gene = [1, 2, 1, 1, 1, 1]
a = tf.placeholder("float32")
b = tf.placeholder("float32")
c = tf.placeholder("int32")
d = tf.placeholder("float32")
e = tf.placeholder("float32")
f = tf.placeholder("float32")


asd = [a, b, c, d, e, f]

result = ch_tf.GetGeneResult(asd, xSamplingList)


def SessionRun(tensor, gene):
    return sess.run(tensor, feed_dict={a: gene[0], b: gene[1], c: gene[2], d: gene[3], e: gene[4], f: gene[5]})


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    aaa = SessionRun(result, gene)
    print(aaa)
