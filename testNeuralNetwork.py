import random as rnd
import os

neurons_count = 10
centres_count = 10
sensors_count = 15
learn_count = 10000
activate_level = 33
sensors = [0] * sensors_count

rates = []
if os.path.exists('rates.txt'):
    f = open('rates.txt')
    s = f.readline()
    while s:
        rates.append(list(map(int, s.split())))
        s = f.readline()
    f.close()

if not (len(rates) == neurons_count and len(rates[0]) == sensors_count):
    rates = [[0] * sensors_count] * neurons_count

center_decision = []
if os.path.exists('center_decision.txt'):
    f = open('center_decision.txt')
    s = f.readline()
    while s:
        center_decision.append(list(map(int, s.split())))
        s = f.readline()
    f.close()

if not (len(center_decision) == centres_count and len(center_decision[0]) == neurons_count):
    center_decision = [[0] * neurons_count] * centres_count

f = open("input.txt")  # Считываем тесты
s = f.readline()
tests = []

while s:
    line = list(s.split())
    isTrue = int(line[0])
    test = list(map(int, line[1:]))
    tests.append([isTrue, test])
    s = f.readline()
