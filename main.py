import ftplib
import os
import re
import tsplib95
from TSP import TSP

ftp = ftplib.FTP("192.168.100.244", "ale368", "11ixjnph")
ftp.encoding = "utf-8"
filename = "gr17.tsp"
ftp.cwd("/home/ale368/unsa/LAS/TCIII/EXAMEN FINAL/instancias/no euc")
with open(filename, "wb") as file:
    ftp.retrbinary(f"RETR {filename}", file.write)

with open(filename, "r") as input:
    with open("temp", "w") as output:
        for line in input:
            if "OPTIMO" not in line.strip("\n"):
                output.write(line)
            else:
                optimo = float(re.findall(r"[0-9]+", line)[0])

os.replace('temp', filename)

file.close()

problem = tsplib95.load('/home/aledvs/unsa/LAS/TCIII/EXAMEN FINAL/tsp final/' + filename)

def lee(problem, filename):
    matriz = []
    for i in range(problem.dimension):
        columna = []
        for j in range(problem.dimension):
            if(problem.get_weight(i,j)==0):
                # print(problem.get_weight(i,j))
                columna.append(float(999999999999))
            else:
                # print(problem.get_weight(i,j))
                columna.append(float(problem.get_weight(i,j)))
        matriz.append(columna)
    os.remove(filename)
    return matriz

matriz = lee(problem, filename)

# problema = TSP(matriz, "resultados/ch130_prueba", "Vecino mas cercano", 3, "2-opt", 4,5, 5.0, optimo)