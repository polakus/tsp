import ftplib
import os
import sys
import random
import re
import math
import tsplib95
# from TSP import TSP
from TabuSearch import TabuSearch

def leeInstancia(problem): # -> list : matriz
    matriz = []
    if problem.edge_weight_type == "EXPLICIT":
        for i in range(problem.dimension):
            columna = []
            for j in range(problem.dimension):
                if(problem.get_weight(i,j)==0):
                    columna.append(float(999999999999))
                else:
                    columna.append(float(problem.get_weight(i,j)))
            matriz.append(columna)
    elif problem.edge_weight_type == "EUC_2D":
        print("ENTRO EN EUC_2D")
        for i in range(problem.dimension):
            columna = []
            for j in range(problem.dimension):
                if(problem.get_weight(i+1,j+1)==0):
                    columna.append(999999999999.0)
                else:
                    columna.append(problem.get_weight(i+1,j+1))
            matriz.append(columna)
    else:
        print("SE DESCONOCE EL TIPO DE PESO DE ARISTA")
    # print(matriz)
    return matriz

def traeInstancias(ip, usuario, pw, formato, dir_rem, dir_local): # -> list: nomb instancias
    ftp = ftplib.FTP(ip, usuario, pw, formato)
    ftp.cwd(dir_rem)
    for f in os.listdir(dir_local): #limpia dirección local
        os.remove(os.path.join(dir_local,f))
    for filename in ftp.nlst():
        try:
            with open(os.path.join(dir_local,filename), "wb") as file:
                ftp.retrbinary(f"RETR {filename}", file.write)
            file.close()
        except:
            print(f"{filename} no es una instancia")
            os.remove(os.path.join(dir_local,filename))
    ftp.quit()
    return os.listdir(dir_local)

def extraeOpt(dir_local, filename): # -> int : optimo de instancia
    with open(os.path.join(dir_local,filename), "r") as input:
        with open(os.path.join(dir_local,"temp"), "w") as output:
            for line in input:
                if "OPTIMO" not in line.strip("\n"):
                    output.write(line)
                else:
                    optimo = float(re.findall(r"[0-9]+", line)[0])

    os.replace(os.path.join(dir_local,'temp'), os.path.join(dir_local,filename))
    try:
        return optimo
    except:
        return float(2085)

ip="192.168.100.244"
usuario="ale368"
pw="11ixjnph"
formato="utf-8"
dir_rem="/home/ale368/unsa/LAS/TCIII/EXAMEN FINAL/instancias/"
dir_local="/home/aledvs/unsa/LAS/TCIII/EXAMEN FINAL/tsp final/temp"
# instancias = traeInstancias(ip,usuario,pw,formato,dir_rem,dir_local)
# for instancia in instancias:
#     optimo = extraeOpt(dir_local,instancia)
#     problem = tsplib95.load(os.path.join(dir_local, instancia))
#     tam = problem.dimension
#     matriz = leeInstancia(problem)
#     os.remove(os.path.join(dir_local,instancia))
#     print(f"ya leyó la instancia: {instancia}\nSe ejecutará {tam**(1/3)} y la instancia es de {tam} vertices")
#     TSP(matriz, f"resultados/{instancia}.rdos", "Vecino mas cercano", 3, "2-opt", 4,5, tam**(1/3), optimo)
optimo = extraeOpt(dir_rem,"gr17.tsp")
problem = tsplib95.load(os.path.join(dir_rem, "gr17.tsp"))
tam = problem.dimension
matriz = leeInstancia(problem)
# os.remove(os.path.join(dir_rem,"gr17.tsp"))
# print(f"ya leyó la instancia: gr17.tsp\nSe ejecutará {tam**(1/3)} y la instancia es de {tam} vertices")
# TSP(matriz, f"resultados/gr17.tsp.rdos", "Vecino mas cercano", 3, "2-opt", 4,5, tam**(1/3), optimo)

# problema = TabuSearch(matriz, f"resultados/gr17.tsp.rdos", "Vecino mas cercano", 3, "2-opt", 4,5, tam**(1/3), optimo)


# # # # matriz = []
# # # # for i in range(8):
# # # #     col = []
# # # #     for j in range(8):
# # # #         if i==j:
# # # #             col.append(999999999999)
# # # #         else:
# # # #             col.append(round(random.uniform(5.0,20.0),2))
# # # #     matriz.append(col)
# # # # for j in range(len(matriz)):
# # # #     for i in range(j):
# # # #         matriz[i][j]=matriz[j][i]

# # # # for i in matriz:
# # # #     print(i)
matriz = [  [999999999999, 19.5, 8.94, 11.31, 9.02, 10.53, 5.35, 19.51],
            [19.5, 999999999999, 9.26, 7.82, 10.02, 13.85, 9.36, 5.33],
            [8.94, 9.26, 999999999999, 9.3, 19.95, 12.9, 9.94, 17.59],
            [11.31, 7.82, 9.3, 999999999999, 13.85, 19.18, 12.62, 10.08],
            [9.02, 10.02, 19.95, 13.85, 999999999999, 19.96, 15.07, 18.88],
            [10.53, 13.85, 12.9, 19.18, 19.96, 999999999999, 5.95, 9.1],
            [5.35, 9.36, 9.94, 12.62, 15.07, 5.95, 999999999999, 7.6],
            [19.51, 5.33, 17.59, 10.08, 18.88, 9.1, 7.6, 999999999999]]

optimo=0
problema = TabuSearch(matriz, f"resultados/gr17.tsp.rdos", "Vecino mas cercano", 3, "2-opt", 4,5, 1.0, optimo)

