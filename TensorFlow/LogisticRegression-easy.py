import tensorflow as tf

train_X = [0.0, 1.0]
train_Y = [1.0, 0.0]

n_samples = len(train_X) 
learning_rate = 0.1
training_epoch = 30000
display_step = 100

X = tf.placeholder("float")
Y = tf.placeholder("float")

W = tf.Variable(0.0)
b = tf.Variable(0.0)

pred = tf.sigmoid(tf.multiply(W, X) + b)

cost_1 = tf.add(Y * tf.log(pred), (1 - Y) * tf.log(1 - pred)) 
cost = tf.negative(tf.reduce_sum(cost_1))/ (2 * n_samples)
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)

    for epoch in range(training_epoch):
        for (x, y) in zip(train_X, train_Y):
            sess.run(optimizer, feed_dict={X: x, Y: y})
        if epoch % display_step == 0:
            print("W:", sess.run(W), ";b:", sess.run(b))