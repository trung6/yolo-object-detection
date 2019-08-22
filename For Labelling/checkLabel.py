import os

d = dict.fromkeys(range(0, 36), 0)
# print(d)
inputFolder = r'F:\LpCrop'
for fileName in os.listdir(inputFolder):
    if '.txt' not in fileName:
        continue
    txtPath = os.path.join(inputFolder, fileName)
    f = open(txtPath, 'r')
    for line in f:
        line = line.split(' ')
        try:
            # if (int(line[0]) > 35):
            #     print(fileName)
            d[int(line[0])]+=1
        except:
            continue
    f.close()
print(d.items())
print(i for i,v in d.items() if v == 0)