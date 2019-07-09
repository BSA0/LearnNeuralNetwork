import os
import csv
import numpy as np
import random as rnd
from time import perf_counter as pc


def exponent(x):
    return 1 / (1 + np.exp(-x))


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
        print(len(layers[-1]))
print("Loaded")
# print(*layers, sep='\n')  # debug


print("Started load trains")
t = pc()
trains_data = open('mnist_train.csv')
trains = csv.reader(trains_data)
print("Loaded in", pc() - t, "second(s)")
# print(*expon(train_data), sep='\n')

for learn_step in range(learn_count):
    # Подгружаем тест
    test = list(map(int, next(trains)))
    correct_ans = test[0]
    # Ведём логи
    values_ = [0] * len(layer_count)
    values_[0] = np.array(test[1:]) / 255

    # Прямой проход (-> Заполнение нейронов данными)
    for i in range(len(layers)):
        values_[i + 1] = exponent(test_analyzers(layers[i], values_[i]))

    # Смотрим результаты и считаем ошибки (<- Заполнение нейронов ошибками)
    errors_rates = [0] * len(layer_count)
    errors_rates[-1] = np.zeros(layer_count[-1]) - values_[-1]
    errors_rates[-1][correct_ans] += 1
    for i in range(-1, -1 * len(layer_count), -1):
        errors_rates[i - 1] = test_analyzers(np.transpose(layers[i]), errors_rates[i])
    
    # Меняем веса
    for i in range(len(layers)):
        print('i', i)
        d = [0] * layer_count[i + 1]
        for j in range(layer_count[i + 1]):
            print('j', j)
            print(values_[j])
            d[j] = values_[i] * errors_rates[j]
        layers[i] += d

for i, v in enumerate(layers):
    with open('{}rates.txt'.format(i), 'w') as f:
        for j in v:
            f.write(" ".join(j))
