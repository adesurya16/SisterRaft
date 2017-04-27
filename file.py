import json
f = open('save','w')
ar = [1,3,4]
json.dump(ar,f)
f = open('save','r')
x = json.load(f)
print(x)