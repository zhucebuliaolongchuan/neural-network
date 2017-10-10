#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Solution(object):
    def __init__(self):
        self.attributes = []
        self.labels = []
        self.weights = [0.0, 0.0, 0.0, 0.0]
        self.bias = 0
        self.mistakes = 0

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
            length = len(self.attributes)
            for p in range(length):
                for i in range(len(self.weights)):
                    self.weights[i] += self.attributes[p][i] * self.labels[p]
                self.bias += self.labels[p]

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
                if result >= 0 and self.labels[p] == 1 or result < 0 and self.labels[p] == -1:
                    continue
                else:
                    self.mistakes += 1


t = Solution()
file_name = "PerceptronDataF17.txt"
t.readfile(file_name)
print "initial weights:", t.weights
print "initial bias:", t.bias
# First Update
print "----------First Update----------"
t.update()
print "modified weights:", t.weights
print "modified bias:", t.bias
t.check()
print "total number of vectors:", len(t.attributes)
print "number of incorrectly classified vectors:", t.mistakes
# Second Update
print "----------Second Update----------"
t.update()
print "modified weights:", t.weights
print "modified bias:", t.bias
t.check()
print "total number of vectors:", len(t.attributes)
print "number of incorrectly classified vectors:", t.mistakes
