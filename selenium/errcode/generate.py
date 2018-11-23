import random,os
os.remove('userid.csv')
for i in range(1000):
	id = str(random.randint(123456789123456789,999999999999999999))+'\n'
	with open('userid.csv','a')as f:
		f.write(id)