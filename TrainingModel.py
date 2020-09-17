import pandas as pd
from pgmpy.models import BayesianModel

#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)

File = open('C:\\Users\\lenovo\\Desktop\\网络科学导论cpp代码\\时序网络数据集\\Data_Laptop1.txt', 'r')
Data = File.readlines()
AllData = []
for i in range(len(Data)):
    line = Data[i]
    lineList = line.split('|')
    lineList = lineList[1:72]
    print(len(lineList))
    #print(lineList)
    for j in range(71):
        lineList[j] = int(lineList[j])
    AllData.append(lineList)

File.close()

column = []
dropCols = []
for i in range(1, 72):
    column.append(str(i))
    if i >= 50:
        dropCols.append(str(i))

values = pd.DataFrame(AllData, columns=column)
TrainData = values[:1000]
TestData = values[1000:]

File = open('C:\\Users\\lenovo\\Desktop\\网络科学导论cpp代码\\时序网络数据集\\network_Laptop.txt', 'r')
Edges = []
EdgeList = File.readlines()
for e in EdgeList:
    e = e[:-1]
    eTuple = tuple(e.split('|'))
    #print(eTuple)
    Edges.append(eTuple)

File.close()
model = BayesianModel(Edges)
model.fit(TrainData)
print('model.fit完毕')

predict_data = TestData.copy()
predict_data.drop(dropCols, axis=1, inplace=True)
print(predict_data)
y_prob = model.predict_probability(predict_data)
print(y_prob)
#下面考虑将预测数据与实际数据进行比对（我们认为后验概率大于0.5就表示预测发生）
P = 0.5
y_prob = y_prob.sort_index(axis=1, ascending=True)
print(y_prob)
y_prob.to_csv("C:\\Users\\lenovo\\Desktop\\网络科学导论cpp代码\\时序网络数据集\\PredictResult_Laptop2.csv", index=False, sep=',')