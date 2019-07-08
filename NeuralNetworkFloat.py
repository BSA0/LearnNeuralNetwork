import os
from math import e
import numpy as np
import random as rnd
from time import perf_counter as pc


def exponent(x):
    return 1 / (1 + e ** (-1 * x))


def test_analyzers(rates, sensors):
    return exponent(np.sum(rates * sensors, axis=1))


def count_errors(errors, rates): # В ОБРАТНОМ ПОРЯДКЕ!!
    pass


layer_count = [784, 100, 25, 10]
layers = []
learn_count = 1  # 00000

for i in range(1, len(layer_count)):
    if os.path.exists('{}rates.txt'.format(i)):
        layers.append(np.loadtxt('{}rates.txt'.format(i), delimiter=" ", dtype=np.uint8))
    else:
        layers.append(np.random.random((layer_count[i], layer_count[i - 1])))

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
    in_ = train_data[test_num][1:]
    # Ведём логи
    values_ = np.empty(len(layer_count))
    values_[0] = in_

    # Прямой проход (-> Заполнение нейронов данными)
    for i in range(len(layers)):
        in_ = test_analyzers(layers[i], in_)
        values_[1] = in_

    # Смотрим результаты и выбираем провинившихся (или нет)

    activated_neuron = np.argmax(in_)
    if activated_neuron != correct_ans:
        errors_ = np.empty(len(layer_count))
        # Обратный проход (<- Высчитывание ошибок *ЫЫЫ рекурсия*)


