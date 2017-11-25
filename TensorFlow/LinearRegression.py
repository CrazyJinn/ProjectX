import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# Parameters
learning_rate = 0.05
training_epochs = 2000
display_step = 50
# Training Data
train_X = np.asarray([5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0])
train_Y = train_X - 4
paint_X = np.asarray([-100.0, 100.0])

n_samples = train_X.shape[0]
# tf Graph Input
X = tf.placeholder("float")
Y = tf.placeholder("float")

# Set model weights
W = tf.Variable(-10., name="weight")
b = tf.Variable(10., name="bias")
# Construct a linear model
pred = tf.add(tf.multiply(X, W), b)
# Mean squared error
cost = tf.reduce_sum(tf.pow(pred - Y, 2)) / (2 * n_samples)
# Gradient descent
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)
# Initializing the variables
init = tf.global_variables_initializer()
# Launch the graph

plt.figure()
plt.ion()

with tf.Session() as sess:
    sess.run(init)

    # Fit all training data
    for epoch in range(training_epochs):
        for (x, y) in zip(train_X, train_Y):
            sess.run(optimizer, feed_dict={X: x, Y: y})

        # Display logs per epoch step
        if (epoch + 1) % display_step == 0:
            c = sess.run(cost, feed_dict={X: train_X, Y: train_Y})
            print("Epoch:", '%04d' % (epoch + 1), "cost=", "{:.9f}".format(c),
                  "W=", sess.run(W), "b=", sess.run(b))

            plt.axis([0.0, np.max(train_X) + 1, 0.0, np.max(train_Y) + 1])
            plt.plot(train_X, train_Y, 'ro', label='Original data')
            plt.plot(paint_X, sess.run(W) * paint_X + sess.run(b), label='Fitted line')
            plt.pause(0.001)
            plt.clf()

    print("Optimization Finished!")
    training_cost = sess.run(cost, feed_dict={X: train_X, Y: train_Y})
    print("Training cost=", training_cost, "W=", sess.run(W), "b=", sess.run(b), '\n')

    plt.axis([0.0, np.max(train_X) + 1, 0.0, np.max(train_Y) + 1])
    plt.plot(train_X, train_Y, 'ro', label='Original data')
    plt.plot(paint_X, sess.run(W) * paint_X + sess.run(b), label='Fitted line')
    plt.pause(10)
