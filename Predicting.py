import csv


def summing(mylist):
    mysum = 0
    for i in range(len(mylist)):
        mysum += mylist[i]
    return mysum


File = csv.reader(open('C:\\Users\\lenovo\\Desktop\\网络科学导论cpp代码\\时序网络数据集\\PredictResult_Laptop2.csv', 'r'))
predictList = []
num = 0
for line in File:
    if num == 0:
        num += 1
        continue
    lineList = []
    for j in range(1, len(line), 2):   #表示只遍历表示边存在的可能性大小
        line[j] = float(line[j])
        lineList.append((line[j], int((j-1)/2)))
    predictList.append(lineList)
    num += 1

print('[0]length:'+str(len(predictList[0])))
print(predictList)
print('predictlistsLength'+str(len(predictList)))

File = open('C:\\Users\\lenovo\\Desktop\\网络科学导论cpp代码\\时序网络数据集\\Data_Laptop1.txt', 'r')
Data = File.readlines()
AllData = []
for i in range(len(Data)):
    line = Data[i]
    lineList = line.split('|')
    lineList = lineList[1:72]
    for j in range(71):
        lineList[j] = int(lineList[j])
    AllData.append(lineList)

#print(AllData[0])
#print(len(AllData[0]))
#下面比较AllData的第703-802行和predictList的匹配度
print(len(AllData))
lineNum = 0
accuracy = []
correctNum = 0
n = 0
for i in range(1000, 1776):
    RealLine = AllData[i]
    #print('RealLine:')
    print(RealLine[49:])
    tem = summing(RealLine[49:])
    n += tem
    PredictLine = predictList[lineNum]
    lineNum += 1
    #print(len(PredictLine))
    #PP = []
    PredictLine.sort(reverse=True)
    for k in range(tem):
        if RealLine[PredictLine[0][1]+49] == 1:
            correctNum += 1

print(correctNum/n)