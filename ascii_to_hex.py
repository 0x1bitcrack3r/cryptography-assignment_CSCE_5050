files_list=['m1.txt','m2.txt','m3.txt']

for i in files_list:
    with open(i, 'r') as f:
        hexdata = f.read().encode('utf-8').hex()
        print(hexdata)