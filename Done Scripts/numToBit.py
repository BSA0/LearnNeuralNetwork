tests_count, sensors_count = map(int, input("Enter count of tests and sensors: ").split())

if os.path.exists('input.txt'):
	f = open("input.txt", 'a')
else:
	f = open("input.txt", 'w')

print("isTrue, nums")

for i in range(tests_count):
	test = ["0"] * (sensors_count + 1)
	line = list(map(int, input().split()))
	print(line)
	test[0] = str(line[0])
	for j in line[1:]:
		test[j] = "1"
	f.write(" ".join(test) + "\n")

f.close()
