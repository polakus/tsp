from clsTxt import clsTxt
import ftplib
import re
import tsplib95

ftp = ftplib.FTP("192.168.100.244", "ale368", "11ixjnph")
ftp.encoding = "utf-8"
filename = "gr17.tsp"
ftp.cwd("/home/ale368/unsa/LAS/TCIII/EXAMEN FINAL/instancias/no euc")
with open(filename, "wb") as file:
    ftp.retrbinary(f"RETR {filename}", file.write)
archivo = open(filename, "r")
lineas = archivo.readlines()

# pathArchivo = "/home/aledvs/unsa/LAS/TCIII/EXAMEN FINAL/codigo reutilizado/tabusearch/TSP-Tabu-Search/Instances/dj38.tsp"
# archivo = open(pathArchivo,"r")
# print(type(archivo))
# lineas = archivo.readlines()

problem = tsplib95.load('/home/aledvs/unsa/LAS/TCIII/EXAMEN FINAL/tsp final/gr17.tsp')

matriz = []
for i in range(problem.dimension):
    columna = []
    for j in range(problem.dimension):
        if(problem.get_weight(i,j)!=999999999999):
            columna.append(999999999999)
        else:
            columna.append(problem.get_weight(i,j))
    matriz.append(columna)


for i in range(problem.dimension):
    print(matriz[i])















# try:
#     indWeightSection = lineas.index("EDGE_WEIGHT_SECTION\n")
#     lineaEOF = lineas.index("EOF\n")
# except:
#     print('No se encontró la línea "NODE_COORD_SECTION\\n" ó "EOF\\n"')
# lineaOptimo = [x for x in lineas[0:indWeightSection] if re.findall(r"OPTIMO:[\S 0-9]+",x)][0]
# optimo = float(re.findall(r"[0-9]+", lineaOptimo)[0])
# coordenadas = []
# print (indWeightSection)
# print (lineaEOF)
# print (lineaOptimo)
# print (optimo)
# matriz = []
# fila = []
# for i in range(indWeightSection + 1, lineaEOF):
#     lineas[i] = re.sub("\n", "", lineas[i])
#     linea = lineas[i].split(" ")
#     linea = [x for x in linea if x!='']
#     # print(linea)
#     for i in linea:
#         # print (type(i))
#         if(i=='0'):
#             fila.append(999999999999)
#             matriz.append(fila)
#             fila = []
#         else:
#             fila.append(float(i))
# # for i in range(4):    
# #     print(i)
# for i in range(len(matriz)-1,-1,-1):
#     for j in range(i):
#         print(str(len(matriz)-i-1) + " " + str(j) + " - " + str(len(matriz[i])))
#         if(not matriz[j+1][len(matriz)-i-1]==999999999999):
#             matriz[len(matriz)-i-1].append(matriz[j+1][len(matriz)-i-1])
#         print(matriz[len(matriz)-i-1])
# for i in matriz:
#     print(i)
    
