import ftplib
import os
import re
import math
import tsplib95
from TSP import TSP
# from TabuSearch import TabuSearch

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

    return optimo

ip="192.168.100.244"
usuario="ale368"
pw="11ixjnph"
formato="utf-8"
dir_rem="/home/ale368/unsa/LAS/TCIII/EXAMEN FINAL/instancias/"
dir_local="/home/aledvs/unsa/LAS/TCIII/EXAMEN FINAL/tsp final/temp"
instancias = traeInstancias(ip,usuario,pw,formato,dir_rem,dir_local)
for instancia in instancias:
    optimo = extraeOpt(dir_local,instancia)
    problem = tsplib95.load(os.path.join(dir_local, instancia))
    tam = problem.dimension
    matriz = leeInstancia(problem)
    os.remove(os.path.join(dir_local,instancia))
    print(f"ya leyó la instancia: {instancia}\nSe ejecutará {tam**(1/3)} y la instancia es de {tam} vertices")
    TSP(matriz, f"resultados/{instancia}.rdos", "Vecino mas cercano", 3, "2-opt", 4,5, tam**(1/3), optimo)
# optimo = extraeOpt(dir_local,"att48.tsp")
# problem = tsplib95.load(os.path.join(dir_local, "att48.tsp"))
# tam = problem.dimension
# matriz = leeInstancia(problem)
# print(matriz)
# os.remove(os.path.join(dir_local,"att48.tsp"))
# print(f"ya leyó la instancia: att48.tsp\nSe ejecutará {tam**(1/3)} y la instancia es de {tam} vertices")
# TSP(matriz, f"resultados/att48.tsp.rdos", "Vecino mas cercano", 3, "2-opt", 4,5, tam**(1/3), optimo)



# problema = TabuSearch(matriz, "resultados/ch130_prueba", "Vecino mas cercano", 3, "2-opt", 4,5, 5.0, optimo)