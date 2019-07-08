import os
import cupy as cp
import numpy as np
import random as rnd
from time import perf_counter as pc


mempool = cp.get_default_memory_pool()


@cp.fuse(kernel_name='teach_analyzers')
def teach_analyzers(rates, sensors, numTrue, activate_level):
    values = np.sum(rates * sensors, axis=1) >= activate_level

    for i, v in enumerate(values):
        if numTrue == i and not v:  # не узнал своего
            rates[i] += sensors
        elif numTrue != i and v:  # признал чужого
            rates[i] -= sensors

    return values * 1, rates


neurons_count = 10
centres_count = 10
sensors_count = 15
learn_count = 100000
activate_level = 33
sensors = np.zeros(sensors_count)

rates = []
if os.path.exists('rates.txt'):
    f = open('rates.txt')
    s = f.readline()
    while s:
        rates.append(list(map(float, s.split())))
        s = f.readline()
    f.close()

if not (len(rates) == neurons_count and len(rates[0]) == sensors_count):
    rates = list()
    for i in range(neurons_count):
        ent = np.zeros(sensors_count)
        rates.append(ent)

rates = np.array(rates)

center_decision = []
if os.path.exists('center_decision.txt'):
    f = open('center_decision.txt')
    s = f.readline()
    while s:
        center_decision.append(list(map(float, s.split())))
        s = f.readline()
    f.close()

if not (len(center_decision) == centres_count and len(center_decision[0]) == neurons_count):
    center_decision = list()
    for i in range(centres_count):
        ent = np.zeros(neurons_count)
        center_decision.append(ent)

center_decision = np.array(center_decision)

print(*rates, sep='\n')
print("--")
print(*center_decision, sep='\n')


# mx elem 109647424 * 2 + 2

f = open("input.txt")  # Считываем тесты
s = f.readline()
tests = []

while s:
    line = list(s.split())
    isTrue = int(line[0])
    test = list(map(int, line[1:]))
    tests.append([isTrue, test])
    s = f.readline()
f.close()

test_count = len(tests)

t = pc()

for learn_pos in range(learn_count):  # Обучение
    test_num = rnd.randint(0, test_count - 1)
    sensors = np.array(tests[test_num][1])
    numTrue = tests[test_num][0]

    output, rates = teach_analyzers(rates, sensors, numTrue, activate_level)
    result, center_decision = teach_analyzers(center_decision, output, numTrue, activate_level)

print(pc() - t)

mempool.free_all_blocks()

f = open('rates.txt', 'w')
print(*rates, sep='\n')
for rate in rates:
    f.write(' '.join(map(str, rate)) + '\n')
f.close()

print("--")

f = open('center_decision.txt', 'w')
print(*center_decision, sep='\n')
for rate in center_decision:
    f.write(' '.join(map(str, rate)) + '\n')
f.close()

