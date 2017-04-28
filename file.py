import json
f = open('save','w')
ar = {
	'ip_address' : 'localhost',
	'port' : '13336',
	'cpu_load' : []	
}
json.dump(ar,f)
f = open('save','r')
array = json.load(f)
for key,ob in array.items():
	print(key,ob)