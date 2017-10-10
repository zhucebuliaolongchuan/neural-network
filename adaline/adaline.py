#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Solution(object):
    def __init__(self, vectors, labels, alpha, theta):
        self.vectors = vectors
        self.labels = labels
        self.exact_weights = [[-91.0 / 153, -8.0 / 153], [1.0 / 6, -2.0 / 3]]
        self.weights = [[0.0, 0.0], [0.0, 0.0]]
        self.bias = [0.0, 0.0]
        self.exact_bias = [2.0 / 153, 1.0 / 6]
        self.max_iterations = 1
        self.alpha = alpha
        self.threshold = theta
        self.max_steps = 10000
        self.mistakes = 0

    def update(self):
        for i in range(self.max_steps):
            self.alpha = alpha / (i + 1.0)
            vector = self.vectors[i % len(self.vectors)]
            label = self.labels[i % len(self.labels)]
            predict = [None, None]
            for j in range(len(predict)):
                predict[j] = vector[0] * self.weights[j][0] + vector[1] * self.weights[j][1] + self.bias[j]
            # Update the weights and labels using Delta Method
            # w_new = w_old - 2 * alpha * x * (y - t)
            # b_new = b_new - 2 * aplha * (y - t)
            cur_weights = [[0.0, 0.0], [0.0, 0.0]]
            cur_bias = [0.0, 0.0]
            y_t = [predict[0] - label[0], predict[1] - label[1]]
            for j in range(len(vector)):
                cur_weights[j][0] = self.weights[j][0] - (vector[0] * y_t[j] * self.alpha * 2)
                cur_weights[j][1] = self.weights[j][1] - (vector[1] * y_t[j] * self.alpha * 2)
                cur_bias[j] = self.bias[j] - (y_t[j] * self.alpha * 2)
            if i > 0 and self.need_to_stop(cur_weights, cur_bias):
                print "the changes of the weights and the bias are under the tolerant error"
                self.check()
                self.compare_exact_error_rate()
                break
            else:
                for j in range(len(vector)):
                    self.weights[j][0] -= (vector[0] * y_t[j] * self.alpha * 2)
                    self.weights[j][1] -= (vector[1] * y_t[j] * self.alpha * 2)
                    self.bias[j] -= (y_t[j] * self.alpha * 2)
                self.max_iterations = i + 1
                print "the ", i, " iterations with change: weights =", self.weights, "bias =", self.bias
                self.check()

    def need_to_stop(self, cur_weights, cur_bias):
        weights_change_rate = [[0.0, 0.0], [0.0, 0.0]]
        bias_change_rate = [0.0, 0.0]
        for j in range(len(self.weights)):
            weights_change_rate[j][0] = abs((self.weights[j][0] - cur_weights[j][0]) / self.weights[j][0]) * 100
            weights_change_rate[j][1] = abs((self.weights[j][1] - cur_weights[j][1]) / self.weights[j][1]) * 100
            bias_change_rate[j] = abs((self.bias[j] - cur_bias[j]) / self.bias[j]) * 100
        res = 0
        for j in range(len(weights_change_rate)):
            res += sum(weights_change_rate[j])
        res += sum(bias_change_rate)
        print res
        if res < 5.0:
            return True
        else:
            return False

    # def cal_square_error(self):
    #     res = 0
    #     for i in range(len(self.vectors)):
    #         vector = self.vectors[i]
    #         label = self.labels[i]
    #         predict = [None, None]
    #         for j in range(len(predict)):
    #             predict[j] = vector[0] * self.weights[j][0] + vector[1] * self.weights[j][1] + self.bias[j]
    #         y_t = [predict[0] - label[0], predict[1] - label[1]]
    #         res += pow(y_t[0], 2) + pow(y_t[1], 2)
    #     return res / len(self.vectors)

    def check(self):
        predicts = []
        for i in range(len(self.vectors)):
            vector = self.vectors[i]
            predict = [None, None]
            for j in range(len(predict)):
                # predict[j] = vector[0] * self.weights[j][0] + vector[1] * self.weights[j][1] + self.bias[j]
                if vector[0] * self.weights[j][0] + vector[1] * self.weights[j][1] + self.bias[j] > self.threshold:
                    predict[j] = 1
                elif vector[0] * self.weights[j][0] + vector[1] * self.weights[j][1] + self.bias[j] < -self.threshold:
                    predict[j] = -1
                else:
                    predict[j] = 0
            predicts.append(predict)
        if predicts == self.labels:
            print "correctly classify all the vectors\n"
            return True
        else:
            print "incorrectly classify all the vectors\n"
            return False

    def compare_exact_error_rate(self):
        # Check the errors for weights
        weights_error_rate = [[0.0, 0.0], [0.0, 0.0]]
        bias_error = [0.0, 0.0]
        for j in range(len(self.weights)):
            weights_error_rate[j][0] = abs((self.exact_weights[j][0] - self.weights[j][0]) / self.exact_weights[j][0]) * 100
            weights_error_rate[j][1] = abs((self.exact_weights[j][1] - self.weights[j][1]) / self.exact_weights[j][1]) * 100
            bias_error[j] = abs((self.exact_bias[j] - self.bias[j]) / self.exact_bias[j]) * 100
        print "weights error rate compared with exact weights:", weights_error_rate
        print "bias error rate compared with exact bias:", bias_error


# Initiate the vectors
vectors = [[1, 1], [1, 2], [2, -1], [2, 0], [-1, 2], [-2, 1], [-1, -1], [-2, -2]]
labels = [[-1, -1], [-1, -1], [-1, 1], [-1, 1], [1, -1], [1, -1], [1, 1], [1, 1]]
alpha = 0.1
theta = 0.0
t = Solution(vectors, labels, alpha, theta)
print "initial weights:", t.weights
print "initial bias:", t.bias
t.update()
print "modified weights:", t.weights
print "modified bias:", t.bias
print "compare to exact weights and bias:\n", t.compare_exact_error_rate()
print "last iterations without change", t.max_iterations + len(t.vectors)
