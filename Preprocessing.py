File = open('C:\\Users\\lenovo\\Desktop\\网络科学导论cpp代码\\时序网络数据集\\email-Eu-core-temporal.txt', 'r')
lineList = File.readlines()
print(len(lineList))
#该数据文件共有332334条记录
lasttime = -1
num = 0
for line in lineList:
    #首先要对line进行split处理
    curlineList = line.split(' ')
    #print(curlineList)
    #print(type(curlineList))
    curtime = int(curlineList[2][:len(curlineList[2]) - 1])
    #print(curtime)
    if (lasttime == curlineList[2]):
        continue
    lasttime = curlineList[2]
    num += 1

print('时间戳共有:' + str(num) + '条')
