from factor import fact
import math
import random

File = open('C:\\Users\\lenovo\Desktop\\网络科学导论cpp代码\\时序网络数据集\\email-Eu-core-temporal-Dept3.txt', 'r')
lineList = File.readlines()
print(len(lineList))
#该数据文件共有12216条记录
lasttime = -1
num = 0
NodeSet = set()
for line in lineList:
    #首先要对line进行split处理
    curlineList = line.split(' ')
    #print(curlineList)
    #print(type(curlineList))
    ProNode = int(curlineList[0])
    PostNode = int(curlineList[1])
    if ProNode < 20:
        ProNode += 1
    if PostNode < 20:
        PostNode += 1
    NodeSet.add(ProNode)
    NodeSet.add(PostNode)
    curtime = int(curlineList[2][:len(curlineList[2]) - 1])
    if (lasttime == curtime):
        continue
    lasttime = curtime
    num += 1

File.close()
print(lasttime)
#print('时间戳共有:' + str(num) + '条')
#时间戳共有8911条

#现在考虑将89*89个变量一维化
NodeList = list(NodeSet)
print(len(NodeList))
NodeList.sort()
print(NodeList)
N = NodeList[len(NodeList)-1]
print('N:'+str(N))

#现在考虑如何给边变量建立索引
Index = []
Index.append(0)
EdgeToIndex = dict()
for i in range(1, N+1):
    for j in range(i + 1, N+1):
        curelem = tuple([i, j])
        Index.append(curelem)
        EdgeToIndex[curelem] = len(Index) - 1

print(len(Index))
print(Index)
#print('EdgeToIndex'+str('1,89:')+str(EdgeToIndex[tuple([1, 89])]))
#这样共有3916个无向边变量

#下一步，我们对时间序列进行切片处理（以半天为一个测试点）
Data = [[] for i in range(803)]

#print(len(Data))
#print(Data)
for i in range(803):
    for j in range(3917):
        Data[i].append(0)


#print(len(Data[1]))
#print(Data[1])

#切片
T = int(lasttime / 803)
print(T)

#故以56426为时间间隔
File = open('C:\\Users\\lenovo\Desktop\\网络科学导论cpp代码\\时序网络数据集\\email-Eu-core-temporal-Dept3.txt', 'r')
lineList = File.readlines()
print(len(lineList))
#该数据文件共有12216条记录
num = 0
NodeSet = set()
possibleDateNumber = 0
for line in lineList:
    curlineList = line.split(' ')
    ProNode = int(curlineList[0])
    PostNode = int(curlineList[1])
    if ProNode < 20:
        ProNode += 1
    if PostNode < 20:
        PostNode += 1
    if PostNode > ProNode:
        temp = ProNode
        ProNode = PostNode
        PostNode = temp
    curtime = int(curlineList[2][:len(curlineList[2]) - 1])
    for t in range(possibleDateNumber, 803):
        if t*T < curtime < (t+1)*T:
            Data[t][EdgeToIndex[tuple([PostNode, ProNode])]] = 1
            possibleDateNumber = t
            break

    num += 1

print(Data[0])
File.close()

NewFile = open('C:\\Users\\lenovo\\Desktop\\网络科学导论cpp代码\\时序网络数据集\\Data.txt', 'w')

for i in range(0, 803):
    ranList = random.sample(range(3916), 500)
    for j in ranList:
        Data[i][j] = 1

for i in range(0, 803):
    for j in range(0, 3917):
        NewFile.write(str(Data[i][j])+'|')
    NewFile.write('\n')
NewFile.close()
'''
for i in range(3917):
    if (Data[0][i]==1):
        #print(i)
        print(Index[i])
'''

#至此，数据集Data构造完毕

#下面我们考虑给这3916个连边变量构建贝叶斯置信网络——K2算法实现
u = 10
ParentSet = [[] for i in range(3917)]


#这里定义关键的Maximize函数
def maximize(ii, Parents):
    #print('ii:'+str(ii))
    #这个函数需要遍历点ii的所有前驱节点，然后选择使g最大的z和g值作为返回值
    G = -1000000000000000000000
    returnZ = -1
    for zz in range(1, ii):
        if zz in Parents:
            continue
        #如果不在的话就要考虑计算它的g值，首先求其父节点的取值情况
        num = len(Parents) + 1
        proding = 0
        for j in range(2**num):
            v = bin(j)
            w = dict()
            for k in range(1, num - len(v) + 3):
                w[k] = 0
            cur = 2
            for k in range(num - len(v) + 3, num + 1):
                w[k] = int(v[cur])
                cur += 1
            #print('w:')
            #print(w)
            #先计算N_ijk
            temp = 1
            N_ij0 = 0
            N_ij1 = 0
            for kkk in range(len(Data)-200):
                line = Data[kkk]
                #print(line)
                flag = 1
                s = 1
                for k in Parents:
                    if line[k] != w[s]:
                        flag = 0
                    s += 1
                if line[zz] != w[s]:
                    flag = 0
                if flag == 0:
                    continue
                if line[ii] == 0:
                    N_ij0 += 1
                if line[ii] == 1:
                    N_ij1 += 1
            #print('N_ij1: '+str(N_ij1))
            proding += math.log(fact(N_ij0)) + math.log(fact(N_ij1))
            proding -= math.log(fact(N_ij0 + N_ij1 + 1))
            #proding = format(proding, '.4f')
            #print(proding)

        '''
        print('************')
        print('G:' + str(G))
        print('proding:' + str(proding))
        '''

        if G < proding:
            G = proding
            #print('ii: '+str(ii))
            #print('G:'+str(G))
            #print('proding:'+str(proding))
            returnZ = zz
    return returnZ, G


NewFile = open('C:\\Users\\lenovo\\Desktop\\网络科学导论cpp代码\\时序网络数据集\\network.txt', 'w')

for i in range(1, 500):
    P_old = -1000000000000000000
    OKToProceed = True
    while OKToProceed and (len(ParentSet[i]) < u):
        z, P_new = maximize(i, ParentSet[i])
        if P_new > P_old:
            P_old = P_new
            ParentSet[i].append(z)
        else:
            OKToProceed = False
    print("Node"+str(i)+":  Parents of this node:")
    print(ParentSet[i])
    for k in range(len(ParentSet[i])):
        NewFile.write(str(ParentSet[i][k])+'|'+str(i)+'\n')

NewFile.close()