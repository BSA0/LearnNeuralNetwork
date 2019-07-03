import os
import random as rnd
import pprint as pp
#import matplotlib.pyplot as plt


def random_exp(d=5, ex=1):
		return rnd.randint(-1 * d, d) / ex


def sum_dis(x0, y0, xs, ys):
	s = 0
	
	for i in range(len(xs)):
		s += (x0 - xs[i]) ** 2 + (y0 - ys[i]) ** 2
	return s


def gen_children(anims, xs, ys, de):
	distances = [sum_dis(i[0], i[1], xs, ys) for i in anims]
	
	sum_d = sum(distances)
	
	
	chances = [sum_d / distances[i] for i in range(len(distances))]
	
	def random_num(chances):
		rand = rnd.randint(0, int(10000*sum(chances))) / 10000
		i = -1
		while rand > 0:
			rand -= chances[i]
			i += 1
		return i
	
	children = [[0, 0] for i in range(len(anims)//2)]
	
	for i in range(len(children)):
		children[i][0] = anims[random_num(chances)][0] + random_exp(ex=de)
		children[i][1] = anims[random_num(chances)][1] + random_exp(ex=de)
		while children in anims:
			children[i][0] = anims[random_num(chances)][0] + random_exp(ex=de)
			children[i][1] = anims[random_num(chances)][1] + random_exp(ex=de)
	
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

de = 1
it = 100000

for i in range(it):
	anims = sorted(anims, key=lambda anim: sum_dis(anim[0], anim[1], xs, ys))
	alive = anims[:len(anims)//2]
	if i % 10000 == 0 and i != 0:
		de *= 10
		print(anims[0])
	children = gen_children(anims, xs, ys, de)
	anims = alive + children
	

foutAnim = open("anim.txt", 'w')
animX = [str(i[0]) for i in anims]
animY = [str(i[1]) for i in anims]
foutAnim.write(" ".join(animX) + "\n")
foutAnim.write(" ".join(animY) + "\n")
foutAnim.close()

distance_mn = [[sum_dis(i[0], i[1], xs, ys), i] for i in anims]
print(*sorted(distance_mn), sep='\n')

