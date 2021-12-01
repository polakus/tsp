from clsTxt import clsTxt
import ftplib
import re
import math
import os
import tsplib95

def distEuclidea(x, y):
    return round(math.sqrt((x[0]-x[1])**2 + (y[0]-y[1]**2)),2)

ftp = ftplib.FTP("192.168.100.244", "ale368", "11ixjnph")
ftp.encoding = "utf-8"
# filename = "a280.tsp"
ftp.cwd("/home/ale368/unsa/LAS/TCIII/EXAMEN FINAL/instancias/")
dir = "/home/aledvs/unsa/LAS/TCIII/EXAMEN FINAL/tsp final/temp"
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))
for filename in ftp.nlst():
    try:
        with open(os.path.join(dir,filename), "wb") as file:
            ftp.retrbinary(f"RETR {filename}", file.write)
    except:
        print(f"{filename} no es una instancia")
        os.remove(os.path.join(dir,filename))
    # ftp.quit()
    # with open(filename, "r") as input:
    #     with open("temp", "w") as output:
    #         for line in input:
    #             if "OPTIMO" not in line.strip("\n"):
    #                 output.write(line)
    #             else:
    #                 print("Encontro optimo")
    #                 optimo = float(re.findall(r"[0-9]+", line)[0])

    # os.replace('temp', filename)

    # file.close()



# problem = tsplib95.load('/home/aledvs/unsa/LAS/TCIII/EXAMEN FINAL/tsp final/'+filename, special = distEuclidea)
# print(problem.get_weight(1,2))
# print(problem.get_display(1))
# print(math.sqrt((problem.get_display(1)[0]-problem.get_display(2)[0])**2
#     +(problem.get_display(1)[1]-problem.get_display(2)[1])**2))
# print(problem.get_display(2))

# matriz = []
# for i in range(problem.dimension):
#     columna = []
#     for j in range(problem.dimension):
#         if(problem.get_weight(i,j)==0):
#             columna.append(999999999999)
#         else:
#             columna.append(problem.get_weight(i,j))
#     matriz.append(columna)


# for i in range(problem.dimension):
#     print(matriz[i])















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

