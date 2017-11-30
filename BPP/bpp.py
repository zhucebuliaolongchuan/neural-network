# -*- coding: utf-8 -*-
from numpy import *
import numpy as np
#import random
import math

class BPNN:
    def __init__(self, train_data, train_label, hidden_num):
        self.train_data = train_data
        self.train_label = train_label
        self.hidden_num = hidden_num
        # Initialize the hidden layer data
        self.hidden_data_n = np.zeros((1, self.hidden_num))
        self.hidden_data_a = np.zeros((1, self.hidden_num))
        # Initialize the output layer data
        self.output_data_n = 0.0
        self.output_data_a = 0.0
        # Initialize the weights from input layer to hidden layer
        # self.i_h_weight=[[ random.uniform(-1.0, 1.0) for j in range(hidden_num)] for i in range(len(train_data[0]))]
        self.i_h_weight = [[0.1970, 0.3191, -0.1448, 0.3594], [0.3099, 0.1904, -0.0347, -0.4861]]
        # Initialize the weights from hidden layer to output layer
        # self.h_o_weight=[[ random.uniform(-1.0, 1.0) for i in range(output_num)] for j in range(hidden_num)]
        self.h_o_weight = [0.4919, -0.2913, -0.3979, 0.3581]
        # Initialize the bias of the hidden layer
        # self.hidden_b=[0 for i in range(hidden_num)]
        self.hidden_b = [-0.3378, 0.2771, 0.2859, -0.3329]
        # Initialize the bias of the output layer
        # self.output_b= 0.0
        self.output_b = -0.1401

    # Sigmoid activation function
    def sigmoid(self, x):
        return (1.0 - math.exp(-x)) / (1.0 + math.exp(-x))

    # The derivative of sigmoid activation function
    def sigmoid_derivative(self, x):
        return 0.5 * (1.0 + self.sigmoid(x)) * (1.0 - self.sigmoid(x))

    # Forward active function
    def activate(self, data_index):
        # Only train one list of training data at one time instead of one epoch
        # Calculate the hidden layer data
        self.hidden_data_n = np.dot(array([self.train_data[data_index]]), self.i_h_weight) + self.hidden_b
        for i in range(self.hidden_num):
            self.hidden_data_a[0, i] = self.sigmoid(self.hidden_data_n[0, i])
        # Calculate the output layer data
        self.output_data_n = np.dot(self.hidden_data_a, self.h_o_weight) + self.output_b
        self.output_data_a = self.sigmoid(self.output_data_n)

    # Back propagation update
    def update(self, alpha, data_index):
        # back propagation
        # Calculate the sensivity from the last layer
        s2 = (self.output_data_a - self.train_label[data_index]) * self.sigmoid_derivative(self.output_data_n)

        s1 = np.zeros((1, self.hidden_num))
        for j in range(self.hidden_num):
            s1[0, j] = self.sigmoid_derivative(self.hidden_data_n[0, j]) * self.h_o_weight[j] * s2

        # Update the weights
        x = array([self.train_data[data_index]])
        for m in range(self.hidden_num):
            for n in range(len(self.train_data[data_index])):
                self.i_h_weight[n][m] -= alpha * x[0, n] * s1[0, m]
            self.h_o_weight[m] -= alpha * self.hidden_data_a[0, m] * s2

        # Update the biases
        self.hidden_b -= alpha * s1
        self.output_b -= alpha * s2

    # train
    def train(self, train_num, alpha):
        for i in range(train_num):
            data_index = i % 4
            self.activate(data_index)
            self.update(alpha, data_index)
        

if __name__ == '__main__':
    data = [[1.0, 1.0], 
            [1.0, -1.0], 
            [-1.0, 1.0], 
            [-1.0, -1.0]]
    label = [-1.0, 1.0, 1.0, -1.0]
    epoch = 1
    hidden_num = 4
    learning_rate = 0.2
    bpnn = BPNN(data, label, hidden_num)
    bpnn.train(epoch * 4, learning_rate)
    print "Weights of Input Layer To Hidden Layer:\n %s \n" % bpnn.i_h_weight
    print "Biases of Hidden Layer:\n %s \n" % bpnn.hidden_b
    print "Weights of Hidden Layer To Output Layer:\n %s \n" % bpnn.h_o_weight
    print "Biases of Output Layer:\n %s " % bpnn.output_b
