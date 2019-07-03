import os
import random as rnd
import pprint as pp
#import matplotlib.pyplot as plt


def sum_dis(x0, y0, xs, ys):
	s = 0
	
	for i in range(len(xs)):
		s += (x0 - xs[i]) ** 2 + (y0 - ys[i]) ** 2
	return s


def gen_children(anims, xs, ys):
	distances = [sum_dis(i[0], i[1], xs, ys) for i in anims]
	
	sum_d = sum(distances)
	
	
	chances = [sum_d / distances[i] for i in range(len(distances))]
	#for i in range(len(distances)):
	#	print(chances[i], distances[i], anims[i])
	
	def random_num(chances):
		rand = rnd.randint(0, int(10000*sum(chances))) / 10000
		i = -1
		while rand > 0:
			rand -= chances[i]
			i += 1
		return i
	
	def random_exp():
		return rnd.randint(-50000, 50000) / 10000
	
	children = [[0, 0] for i in range(len(anims)//2)]
	
	for i in range(len(children)):
		children[i][0] = anims[random_num(chances)][0] + random_exp()
		children[i][1] = anims[random_num(chances)][1] + random_exp()
		while children in anims:
			children[i][0] = anims[random_num(chances)][0] + random_exp()
			children[i][1] = anims[random_num(chances)][1] + random_exp()
	
	return children


fin = open("input.txt")
xs = list(map(float, fin.readline().split()))
ys = list(map(float, fin.readline().split()))
fin.close()

anims = []

if os.path.exists('anim.txt'):
	finAnim = open("anim.txt")
	animX = list(map(float, finAnim.readline().split()))
	animY = list(map(float, finAnim.readline().split()))
	for i in zip(animX, animY):
		anims.append(list(i))
	finAnim.close()
else:
	anims = [[rnd.random() * 10, rnd.random() * 10] for i in range(30)]

# print(anims)

# for i in range(len(xs)):
# 	plt.scatter(xs[i], ys[i])

# plt.show()

# for i in range(1000):

for i in range(100000):
	anims = sorted(anims, key=lambda anim: sum_dis(anim[0], anim[1], xs, ys))
	alive = anims[:len(anims)//2]
	children = gen_children(anims, xs, ys)
	anims = alive + children
print()

foutAnim = open("anim.txt", 'w')
animX = [str(i[0]) for i in anims]
animY = [str(i[1]) for i in anims]
foutAnim.write(" ".join(animX) + "\n")
foutAnim.write(" ".join(animY) + "\n")
foutAnim.close()

distance_mn = [[sum_dis(i[0], i[1], xs, ys), i] for i in anims]
print(*sorted(distance_mn), sep='\n')

