import random as rnd
import os
import json


neurons_count = 10
centres_count = 10
sensors_count = 15
learn_count = 100000
activate_level = 31
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

test_count = len(tests)
	
for learn_pos in range(learn_count):  # Обучение
	test_num = rnd.randint(0, test_count - 1)
	sensors = tests[test_num][1]
	numTrue = tests[test_num][0]
	output = []
	result = []
	for i in range(neurons_count):  # i - номер анализатора
		v = 0  # значение на нейроне
		neurons_triggered = []
		for j in range(len(sensors)):  # j - номер сенсора и его коэф к анализатору
			v += sensors[j] * rates[i][j]
			if sensors[j]:
				neurons_triggered.append(j)
		# ругаем за ошибки
		if numTrue == i and v < activate_level:  # не узнал своего
			for k in neurons_triggered:
				rates[i][k] += 1
		elif numTrue != i and v >= activate_level:  # признал чужого
			for k in neurons_triggered:
				rates[i][k] -= 1
		output.append(1 if v >= activate_level else 0)
	
	for i in range(centres_count):  # i - номер центра принятия решения
		v = 0  # значение на центре
		centres_triggered = []
		for j in range(len(output)):  # j - номер анализатора и его коэф к центру
			v += output[j] * center_decision[i][j]
			if output[j]:
				centres_triggered.append(j)
		# ругаем за ошибки
		if numTrue == i and v < activate_level:  # не узнал своего
			for k in centres_triggered:
				center_decision[i][k] += 1
		elif numTrue != i and v >= activate_level:  # признал чужого
			for k in centres_triggered:
				center_decision[i][k] -= 1
		result.append(1 if v >= activate_level else 0)
	print(numTrue, result)
	

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


