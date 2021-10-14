x = 1

def p1():
    print(x + x)

def p2():
    print(x*x)

mydict = {'p1': p1, 'p2': p2}

def myMain(key):
    mydict[key]()

#myMain('p1')
list_key = ['p1', 'p2']

for key in list_key:
    myMain(key)
