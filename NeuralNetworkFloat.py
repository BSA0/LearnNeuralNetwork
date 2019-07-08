import os
from math import e
import numpy as np
import random as rnd
from time import perf_counter as pc


def expon(x):
    return 1 / (1 + e ** (-1 * x))


def teach_analyzers(rates, sensors, numTrue, activate_level):
    values = expon(np.sum(rates * sensors, axis=1))


def reverse_way():
    pass


layer_count = [784, 100, 25, 10]
layers = []
learn_count = 100000

for i in range(1, len(layer_count)):
    if os.path.exists('{}rates.txt'.format(i)):
        layers.append(np.loadtxt('{}rates.txt'.format(i), delimiter=" ", dtype=np.uint8))
    else:
        layers.append(np.zeros((layer_count[i], layer_count[i - 1]), dtype=np.uint8))

# print(*layers, sep='\n')


train_data = np.loadtxt("input.txt", delimiter=" ", dtype=np.uint8)
print(*expon(train_data), sep='\n')
    
