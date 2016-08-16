#!/usr/bin/env python

import numpy as np


class MultiLayerPerceptron():
    def softmax(self, x):
        """softmax normalization"""
        np.exp(x, x)
        x /= np.sum(x, axis=1)[:, np.newaxis]

    def predict_proba(self, x):
        x = np.atleast_2d(x)
        x_hidden = np.empty((x.shape[0], self.n_hidden))
        x_output = np.empty((x.shape[0], self.n_outs))
        self._forward(x, x_hidden, x_output)
        return x_output

    def predict(self, x):
        x = np.atleast_2d(x)
        x_output = self.predict_proba(x)
        max_out = np.argmax(x_output, axis=1)
        return [self.classes_[max] for max in max_out]

    def _forward(self, x, x_hidden, x_output):
        """Forward pass through the network"""
        x_hidden[:] = np.dot(x, self.w1)
        x_hidden += self.b1
        x_hidden = np.maximum(x_hidden, 0)
        x_output[:] = np.dot(x_hidden, self.w2)
        x_output += self.b2
        self.softmax(x_output)
