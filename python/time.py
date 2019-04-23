import random, timeit

def way1():
	with open('way1.txt', 'w') as f:
		f.write(str([random.randint(100000000000000000,999999999999999999) for i in range(1000)]))

def way2():
	faceid = []
	for i in range(1000):
		id = random.randint(100000000000000000,999999999999999999)
		faceid.append(id)
	with open('way2.txt', 'w') as f:
		f.write(str(faceid))
		
if __name__=='__main__':
	t1 = timeit.timeit('way1()', setup="from __main__ import way1", number=1)
	print(t1)
	t2 = timeit.timeit('way2()', setup="from __main__ import way2", number=1)
	print(t2)