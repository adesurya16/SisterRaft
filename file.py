import json
f = open('save','w')
ar = {
	'ip_address' : 'localhost',
	'port' : '13336',
	'cpu_load' : []	
}
list1 = [ar]
# list1.append(ar)
# list1.append(ar)
json.dump(list1,f)
f.close()
f = open('save','r+')
array = json.load(f)
array.append(ar)
# if len(array) > 0:
# 	ar1 = {
# 		'ip_address' : 'localhost',
# 		'port' : '13337',
# 		'cpu_load' : []	
# 	}
# 	array1=[ar1]
# 	# array1.append(ar1)
json.dump(array,f)
for obj in array:
	print(obj)
f.close()
# for key,ob in array.items():
# 	print(key,ob)