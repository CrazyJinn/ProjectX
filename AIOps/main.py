import matplotlib.pyplot as plt
import FormatData as fd
import do
import numpy as np
import tensorflow as tf

data = np.array(fd.fvk())

print(data)

batch_size = 5         # Sequences per batch
num_steps = 72          # Number of sequence steps per batch
lstm_size = 512         # Size of hidden layers in LSTMs
num_layers = 2          # Number of LSTM layers
learning_rate = 0.002    # Learning rate
keep_prob = 0.5         # Dropout keep probability
epochs = 100
save_every_n = 200

max_length = 1008


model = do.CharRNN(max_length, batch_size=batch_size, num_steps=num_steps,
                   lstm_size=lstm_size, num_layers=num_layers,
                   learning_rate=learning_rate)
saver = tf.train.Saver(max_to_keep=100)
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    counter = 0
    for e in range(epochs):
        # Train network
        new_state = sess.run(model.initial_state)
        loss = 0
        for x, y in do.get_batches(data, batch_size, num_steps):
            counter += 1
            feed = {model.inputs: x,
                    model.targets: y,
                    model.keep_prob: keep_prob,
                    model.initial_state: new_state}
            batch_loss, new_state, _ = sess.run([model.loss,
                                                 model.final_state,
                                                 model.optimizer],
                                                feed_dict=feed)

            # control the print lines
            if counter % 10 == 0:
                print('轮数: {}/{}... '.format(e + 1, epochs),
                      '训练步数: {}... '.format(counter),
                      '训练误差: {:.4f}... '.format(batch_loss))

            if (counter % save_every_n == 0):
                saver.save(sess, "checkpoints/i{}_l{}.ckpt".format(counter, lstm_size))


def pick_top_n(preds, vocab_size, top_n=1):
    """
    从预测结果中选取前top_n个最可能的字符

    preds: 预测结果
    vocab_size
    top_n
    """
    p = np.squeeze(preds)
    # 将除了top_n个预测值的位置都置为0
    p[np.argsort(p)[:-top_n]] = 0
    # 归一化概率
    p = p / np.sum(p)
    # 随机选取一个字符
    c = np.random.choice(vocab_size, 1, p=p)[0]
    return c


def sample(checkpoint, n_samples, lstm_size, vocab_size, prime):
    """
    生成新文本

    checkpoint: 某一轮迭代的参数文件
    n_sample: 新闻本的字符长度
    lstm_size: 隐层结点数
    vocab_size
    prime: 起始文本
    """

    # sampling=True意味着batch的size=1 x 1
    model = do.CharRNN(max_length, lstm_size=lstm_size, sampling=True)
    saver = tf.train.Saver()
    with tf.Session() as sess:
        # 加载模型参数，恢复训练
        saver.restore(sess, checkpoint)
        new_state = sess.run(model.initial_state)
        samples = [c for c in prime]
        for c in prime:
            x = np.zeros((1, 1))
            # 输入单个字符
            x[0, 0] = c
            feed = {model.inputs: x,
                    model.keep_prob: 1.,
                    model.initial_state: new_state}
            preds, new_state = sess.run([model.prediction, model.final_state],
                                        feed_dict=feed)

        c = pick_top_n(preds, max_length)
        # 添加字符到samples中
        samples.append(c)

        # 不断生成字符，直到达到指定数目
        for i in range(n_samples):
            x[0, 0] = c
            feed = {model.inputs: x,
                    model.keep_prob: 1.,
                    model.initial_state: new_state}
            preds, new_state = sess.run([model.prediction, model.final_state],
                                        feed_dict=feed)

            c = pick_top_n(preds, max_length)
            samples.append(c)

    return samples


checkpoint = tf.train.latest_checkpoint('D://GitHub/project/AIOps/checkpoints/')

prime1 = [11710, 6370, 9986]
samp = sample(checkpoint, 1008 - 4, lstm_size, max_length, prime=prime1)

plt.figure(figsize=(100, 20))
x1 = []
for i in range(1008):
    x1.append(i)

# plt.plot(x1, data[0])

# x2 = []
# for i in range(1008):
#     x2.append(i)
# plt.plot(x1, samp)
plt.plot(x1, samp / data[0])

plt.show()
