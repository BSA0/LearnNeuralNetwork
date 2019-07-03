neurons_count = 1
sensors_count = 15
sensors = [0] * sensors_count
rates = [[0] * sensors_count] * neurons_count

f = open("input.txt")

s = f.readline()
while s:
    line = list(s.split())
    isTrue = line[0]
    sensors = list(map(int, line[1:]))
    output = []
    for i in range(neurons_count):  # i - номер анализатора
        v = 0  # значение на нейроне
        for j in range(len(sensors)):  # j - номер сенсора и его коэф к анализатору
            v += sensors[j] * rates[i][j]
        print(v)
    s = f.readline()
