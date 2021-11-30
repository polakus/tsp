import re
import math
from TSP import TSP
import ftplib

# pathArchivo = "/home/aledvs/unsa/LAS/TCIII/EXAMEN FINAL/codigo reutilizado/tabusearch/TSP-Tabu-Search/Instances/dj38.tsp"
# archivo = open(pathArchivo,"r")
# lineas = archivo.readlines()

ftp = ftplib.FTP("192.168.100.244", "ale368", "11ixjnph")
ftp.encoding = "utf-8"
filename = "a280.tsp"
ftp.cwd("/home/ale368/unsa/LAS/TCIII/EXAMEN FINAL/instancias/")
with open(filename, "wb") as file:
    ftp.retrbinary(f"RETR {filename}", file.write)
archivo = open(filename, "r")
lineas = archivo.readlines()

try:
    indSeccionCoord = lineas.index("NODE_COORD_SECTION\n")
    lineaEOF = lineas.index("EOF\n")
except:
    print('No se encontró la línea "NODE_COORD_SECTION\\n" ó "EOF\\n"')
lineaOptimo = [x for x in lineas[0:indSeccionCoord] if re.findall(r"OPTIMO:[\S 0-9]+",x)][0]
optimo = float(re.findall(r"[0-9]+", lineaOptimo)[0])
coordenadas = []

for i in range(indSeccionCoord+1, lineaEOF):
    textoLinea = lineas[i]
    textoLinea = re.sub("\n", "", textoLinea)
    splitLinea = textoLinea.split(" ")
    splitLinea = [x for x in splitLinea if x!= '']
    coordenadas.append([splitLinea[0],splitLinea[1],splitLinea[2]]) #[[v1,x1,y1], [v2,x2,y2], ...]

matriz = []
#Arma la matriz de distancias. Calculo la distancia euclidea
for coordRow in coordenadas:
    fila = []            
    for coordCol in coordenadas:
        x1 = float(coordRow[1])
        y1 = float(coordRow[2])
        x2 = float(coordCol[1])
        y2 = float(coordCol[2])
        dist = round(math.sqrt((x1-x2)**2+(y1-y2)**2),3)
        
        #Para el primer caso. Calculando la distancia euclidea entre si mismo da 0
        if(dist == 0):
            dist = 999999999999 #El modelo no debería tener en cuenta a las diagonal, pero por las dudas
        fila.append(dist)

    #print("Fila: "+str(fila))    
    matriz.append(fila)

problema = TSP(matriz, "resultados/ch130_prueba", "Vecino mas cercano", 3, "2-opt", 4,5, 5.0, optimo)

# problema.printG()