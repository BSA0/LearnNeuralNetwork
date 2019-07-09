import os
from math import e
import numpy as np
import random as rnd
from time import perf_counter as pc


def exponent(x):
    return 1 / ( 1 + np.exp(-x))


def test_analyzers(rates, sensors):
    return np.sum(rates * sensors, axis=1)


layer_count = [784, 150, 75, 10]
layers = []
learn_count = 1  # 00000

print("Started load rates")
for i in range(1, len(layer_count)):
    if os.path.exists('{}rates.txt'.format(i)):
        layers.append(np.loadtxt('{}rates.txt'.format(i), delimiter=" "))
    else:
        layers.append(np.random.random((layer_count[i], layer_count[i - 1])))
print("Loaded")
# print(*layers, sep='\n')  # debug


print("Started load trains")
t = pc()
train_data = np.loadtxt("mnist_train.csv", delimiter=",", dtype=np.uint8)
train_count = len(train_data)
print("Loaded in", pc() - t, "second(s)")
# print(*expon(train_data), sep='\n')

for learn_step in range(learn_count):
    # Подгружаем тест
    test_num = rnd.randint(0, train_count)
    correct_ans = train_data[test_num][0]
    # Ведём логи
    values_ = np.empty(len(layer_count))
    values_[0] = train_data[test_num][1:] / 255

    # Прямой проход (-> Заполнение нейронов данными)
    for i in range(len(layers)):
        values_[i + 1] = exponent(test_analyzers(layers[i], values_[i]))

    # Смотрим результаты и считаем ошибки (<- Заполнение нейронов ошибками)
    errors_rates = np.empty(len(layers))
    errors_rates[-1] = np.zeros(layer_count[-1]) - values_[-1]
    errors_rates[-1][correct_ans] += 1
    for i in range(-1, -1 * len(layer_count), -1):
        errors_rates[i - 1] = test_analyzers(layers[i], errors_rates[i])
    
    # Меняем веса
    for i in range(len(layers)):
        d = np.empty((layer_count[i + 1], layer_count[i]))
        for j in range(layer_count[i + 1]):
            d[j] = values[j] * errors_rates[j]
        layers[i] += d

for i, v in enumerate(layers):
    with open('{}rates.txt'.format(i), 'w') as f:
        for j in v:
            f.write(" ".join(j))
