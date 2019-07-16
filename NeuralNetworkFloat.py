import os
import csv
import numpy as np
from math import e
import random as rnd
from time import perf_counter as pc

np.set_printoptions(linewidth=np.inf)


def sigmoid(x):
    return [1 / (1 + e ** (-i)) for i in x]


def normalize(x, n):
    s = 0
    for i in x:
        s += abs(i)
    if s == 0:
        s = max(x)
    if s == 0:
        s = 1
    return [(i / s) * n for i in x]


def test_analyzers(rates, sensors):
    z = [0] * len(rates)
    print(len(rates), len(rates[0]), len(sensors))
    for i in range(len(rates)):
        for j in range(len(rates[i])):
            z[i] += rates[i][j] * sensors[j]
    return z


def randomize(r=1, c=1):
    return [[rnd.random() for _ in range(c)] for __ in range(r)]


layer_count = [784, 150, 75, 10]
layers = []
test_count = 4000  # 60000
learn_count = 3
learn_norm = 1

print("Started load rates")
for i in range(1, len(layer_count)):
    print('Loading {}rates.txt'.format(i))
    if os.path.exists('{}rates.txt'.format(i)):
        f = open('{}rates.txt'.format(i)).read()
        layers.append([list(map(float, r.split())) for r in f.split('\n')])
    else:
        layers.append(randomize(layer_count[i], layer_count[i - 1]))
print("Loaded")


for learn_step in range(learn_count):
    trains_data = open('mnist_train.csv')
    trains = csv.reader(trains_data)

    errors_count = 0

    print("Start {} epoch".format(learn_step + 1))

    t = pc()
    for test_step in range(test_count):
        # Подгружаем тест
        test = list(map(int, next(trains)))
        correct_ans = test[0]

        # Ведём логи
        values_ = [[]] * len(layer_count)
        values_[0] = test[1:]

        for i in range(len(values_[0])):
            values_[0][i] /= 255

        # Прямой проход (-> Заполнение нейронов данными)
        for i in range(len(layers)):
            values_[i + 1] = sigmoid(test_analyzers(layers[i], values_[i]))

        if learn_step % 100 == 99:
            print('out', values_[-1])

        if correct_ans != np.argmax(values_[-1]):
            errors_count += 1

        # Смотрим результаты и считаем ошибки (<- Заполнение нейронов ошибками)
        errors_rates = [[]] * len(layer_count)
        errors_rates[-1] = [0] * layer_count[-1]
        errors_rates[-1][correct_ans] += 1

        for i in range(len(errors_rates)):
            errors_rates[-1][i] -= values_[-1][i]

        for i in range(-1, -1 * len(layer_count), -1):
            errors_rates[i - 1] = normalize(test_analyzers(layers[i], errors_rates[i]), learn_norm)
        # Меняем веса
        for i in range(len(layers)):
            d = np.empty((layer_count[i + 1], layer_count[i]))
            for j in range(layer_count[i + 1]):
                for r in range(len(values_[i])):
                    d[j] = normalize(values_[i] * errors_rates[i][j], learn_norm)

            layers[i] += d

        if test_step % 100 == 99:
            print('Done {} step(s) in {} seconds. Mistakes {}% ({}/{})'.format(test_step + 1, pc() - t,
                                                                               (errors_count / (test_step + 1)) * 100,
                                                                               errors_count, test_step + 1))

    for i, v in enumerate(layers, 1):
        with open('{}rates.txt'.format(i), 'w') as f:
            for j in v:
                f.write(" ".join(map(str, j)) + '\n')

    print('Done {} epoch(s) in {} seconds'.format(learn_step + 1, pc() - t))

    trains_data.close()
