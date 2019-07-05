import random as rnd
import os


def test_analyzers(rates, sensors, neurons_count, activate_level):
	output = []
	for i in range(neurons_count):  # i - номер анализатора
		v = 0  # значение на нейроне
		neurons_triggered = []
		for j in range(len(sensors)):  # j - номер сенсора и его коэф к анализатору
			v += sensors[j] * rates[i][j]
		output.append(1 if v >= activate_level else 0)
	return output


neurons_count = 10
centres_count = 10
sensors_count = 15
learn_count = 100000
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
	rates = list()
	for i in range(neurons_count):
		ent = list()
		for j in range(sensors_count):
			ent.append(0)
		rates.append(ent)


center_decision = []
if os.path.exists('center_decision.txt'):
	f = open('center_decision.txt')
	s = f.readline()
	while s:
		center_decision.append(list(map(int, s.split())))
		s = f.readline()
	f.close()

if not (len(center_decision) == centres_count and len(center_decision[0]) == neurons_count):
	center_decision = list()
	for i in range(centres_count):
		ent = list()
		for j in range(neurons_count):
			ent.append(0)
		center_decision.append(ent)


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
	
for learn_pos in range(learn_count):  # Обучение
	test_num = rnd.randint(0, test_count - 1)
	sensors = tests[test_num][1]
	numTrue = tests[test_num][0]
	
	output= test_analyzers(rates, sensors, neurons_count, activate_level)
	result = test_analyzers(center_decision, output, centres_count, activate_level)
	
	if learn_pos % 10000 == 0:
		print(learn_pos)

