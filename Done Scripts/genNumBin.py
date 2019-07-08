import random


masks = []
output = []
f = open("input_backup.txt")  # Считываем тесты
s = f.readline()

while s:
    line = list(s.split())
    numTrue = int(line[0])
    mask = ''.join(line[1:])
    masks.append(int(mask, 2))
    s = f.readline()
f.close()

maxmax = 2 ** 15

for gen in range(maxmax):
    if random.random() > 0.05:
        continue
    dis = []
    mn = maxmax
    for i, mask in enumerate(masks):
        dista = bin(gen ^ mask).count("1")
        if dista < mn:
            mn = dista
            dis = [[i] + list(map(int, format(gen, '015b')))]
        elif dista == mn:
            dis.append([i] + list(map(int, format(gen, '015b'))))
    output += dis


f = open("input.txt", 'a')
for i in output:
    f.write(" ".join(map(str, i)) + "\n")
f.close()

