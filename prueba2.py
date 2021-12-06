# import time

# d = dict()
# # print(type(d))
# for i in range(100000):
#     d[(i,i+1)]=i*i
# acud = 0
# for key in d:
#     acud += d[key]
# # print(f"rdo: {6001,6002},{d[(6001,6002)]}")
# ini = time.time()
# print(acud)
# print(f"tiempo diccionario: {time.time()-ini}. len: {len(d)}")
# #######################################################################
# l = list()
# # print(type(l))
# for i in range(100000):
#     l.append((i,i+1,i*i))
# acul = 0
# for i in range(100000):
#     acul += l[i][2]
# pos = -1
# for i in range(100000):
#     if l[i][0]==6001 and l[i][1]==6002:
#         pos = i
# # print(f"rdo: {l[pos]}")
# ini = time.time()
# print(acul)
# print(f"tiempo lista: {time.time()-ini}. len: {len(l)}")
from Arista import Arista
from Vertice import Vertice
from Tabu import Tabu

a = Arista(Vertice(1),Vertice(2),float(3))
b = Arista(Vertice(2),Vertice(1),float(3))
c = [a,b]
print(c)
# c.remove(Arista(Vertice(1),Vertice(3),float(3)))
print(c)

for i in [1,2,3]+[8,9]:
    print(i)