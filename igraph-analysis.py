from igraph import *
import numpy as np
import pandas as pd
g = Graph.Read_GraphML('tracetofrom-stage123-onelevel-tx.graphml')
print(g.node)
# 点的入度
# list = g.degree(mode=IN)
# test = pd.DataFrame(data=list)#数据有三列，列名分别为one,two,three
# test.to_csv('testcsvin.csv',encoding='gbk')

# 点的出度
# list = g.degree(mode=OUT)
# test = pd.DataFrame(data=list)#数据有三列，列名分别为one,two,three
# test.to_csv('testcsvout.csv',encoding='gbk')

# 计算中介中心性
# betweenness = g.betweenness()
# betweenness1 = pd.DataFrame(data=betweenness)#数据有三列，列名分别为one,two,three
# betweenness1.to_csv('testcsv1.csv',encoding='gbk')

# 计算中介中心性
# closeness = g.closeness()
# closeness1 = pd.DataFrame(data=closeness)#数据有三列，列名分别为one,two,three
# closeness1.to_csv('testcsv2.csv',encoding='gbk')