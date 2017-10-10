#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Solution(object):
    def __init__(self, alpha, theta):
        self.attributes = []
        self.labels = []
        self.weights = [0.0, 0.0, 0.0, 0.0]
        self.bias = 0
        self.alpha = alpha
        self.threshold = theta
        self.mistakes = 0
        self.max_iterations = 500000
        self.last_iter_without_change = 1

    def readfile(self, file_name):
        f = open(file_name, "r")
        for line in f:
            line = line.strip().split()
            line = map(lambda x:float(x), line)
            if len(line) == 5:
                self.attributes.append(line[:4])
                self.labels.append(line[-1])
            else:
                print "error"
        f.close()

    def update(self):
        if len(self.attributes) != len(self.labels):
            print "error"
        else:
            for iteration in range(self.max_iterations):
                predict = 0
                x = self.attributes[iteration % len(self.attributes)]
                target = self.labels[iteration % len(self.labels)]
                for i in range(len(self.weights)):
                    predict += self.weights[i] * x[i]
                predict += self.bias
                # Compare the true label and the predict value, and to determine modify the weights and bias or not
                if predict > self.threshold and target == 1 or predict < -self.threshold and target == -1:
                    # print "the", iteration, "iteration without change"
                    continue
                else:
                    weights_change = [0.0, 0.0, 0.0, 0.0]
                    for i in range(len(self.weights)):
                        self.weights[i] += x[i] * target * self.alpha
                        weights_change[i] = x[i] * target * self.alpha
                    self.bias += target * self.alpha
                    bias_change = target * self.alpha
                    self.last_iter_without_change = iteration + 1
                    print "the", iteration, "iteration with change: weights ", weights_change, "bias ", bias_change

    def check(self):
        if len(self.attributes) != len(self.labels):
            print "error"
        else:
            self.mistakes = 0
            length = len(self.attributes)
            for p in range(length):
                result = 0
                for i in range(len(self.weights)):
                    result += self.weights[i] * self.attributes[p][i]
                result += self.bias
                if result >= self.threshold and self.labels[p] == 1 or result < self.threshold and self.labels[p] == -1:
                    continue
                else:
                    self.mistakes += 1


alpha = 1.0
theta = 1.0
t = Solution(alpha, theta)
file_name = "PerceptronDataF17.txt"
t.readfile(file_name)
print "initial weights:", t.weights
print "initial bias:", t.bias
# First Update
t.update()
print "modified weights:", t.weights
print "modified bias:", t.bias
t.check()
print "total number of vectors:", len(t.attributes)
print "number of incorrectly classified vectors:", t.mistakes
print "last iterations without change", t.last_iter_without_change + len(t.attributes)
