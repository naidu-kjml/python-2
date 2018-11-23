import json
with open('test.txt','r') as f:
	cont = f.read()

cookies = {}
for line in cont.split('&'):
	key,value=line.split('=',1)
	cookies[key]=value

	
	
with open('data.txt','w') as f:
	f.write(json.dumps(cookies))