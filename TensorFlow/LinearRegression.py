import tensorflow as tf
import numpy
import matplotlib.pyplot as plt
rng = numpy.random

# Parameters
learning_rate = 0.05
training_epochs = 2000
display_step = 50
# Training Data
train_X = numpy.asarray([2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0])
train_Y = numpy.asarray([1.0, 2.3, 2.9, 4.0, 4.5, 6.5, 7.1, 8.2, 8.8, 10.0])
paint_X = numpy.asarray([-100.0, 100.0])

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

            plt.axis([0.0, 12.01, 0.0, 11.01])
            plt.plot(train_X, train_Y, 'ro', label='Original data')
            plt.plot(paint_X, sess.run(W) * paint_X + sess.run(b), label='Fitted line')
            plt.pause(0.001)
            plt.clf()

    print("Optimization Finished!")
    training_cost = sess.run(cost, feed_dict={X: train_X, Y: train_Y})
    print("Training cost=", training_cost, "W=", sess.run(W), "b=", sess.run(b), '\n')

    plt.axis([0.0, 12.01, 0.0, 11.01])
    plt.plot(train_X, train_Y, 'ro', label='Original data')
    plt.plot(paint_X, sess.run(W) * paint_X + sess.run(b), label='Fitted line')
    plt.pause(10)
