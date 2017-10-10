#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Solution(object):
    def __init__(self, vectors, labels, alpha, theta):
        self.vectors = vectors
        self.labels = labels
        self.weights = [[0.0, 0.0], [0.0, 0.0]]
        self.bias = [0.0, 0.0]
        self.alpha = alpha
        self.threshold = theta
        self.max_steps = 500
        self.max_iterations = 1
        self.mistakes = 0

    def update(self):
        for i in range(self.max_steps):
            vector = self.vectors[i % len(self.vectors)]
            label = self.labels[i % len(self.labels)]
            predict = [None, None]
            for j in range(len(vector)):
                if vector[0] * self.weights[j][0] + vector[1] * self.weights[j][1] + self.bias[j] > self.threshold:
                    predict[j] = 1
                elif vector[0] * self.weights[j][0] + vector[1] * self.weights[j][1] + self.bias[j] < -self.threshold:
                    predict[j] = -1
                else:
                    predict[j] = 0
            if predict == label:
                print "the ", i, " iterations without change"
            else:
                # Update the weights and labels using Perceptron Method
                for r in range(len(self.weights)):
                    for c in range(len(self.weights[-1])):
                        self.weights[r][c] += self.alpha * label[r] * vector[c]
                    self.bias[r] += self.alpha * label[r]
                self.max_iterations = i + 1
                print "the ", i, " iterations with change: weights =", self.weights, "bias =", self.bias


# Initiate the vectors
vectors = [[1, 1], [1, 2], [2, -1], [2, 0], [-1, 2], [-2, 1], [-1, -1], [-2, -2]]
labels = [[-1, -1], [-1, -1], [-1, 1], [-1, 1], [1, -1], [1, -1], [1, 1], [1, 1]]
alpha = 0.8
theta = 1.5
t = Solution(vectors, labels, alpha, theta)
print "initial weights:", t.weights
print "initial bias:", t.bias
t.update()
print "modified weights:", t.weights
print "modified bias:", t.bias
print "last iterations without change", t.max_iterations + len(t.vectors)
