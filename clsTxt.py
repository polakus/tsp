# import sys
import os
# import csv
# import re
import ntpath
class clsTxt:
    def __init__(self, nombreTxt):
        self.__direccion = ""
        directorios = nombreTxt.split(os.sep)
        self.__nombre = directorios.pop(len(directorios)-1)
        for dir in directorios:
            if(not os.path.isdir(self.__direccion+dir)):
                os.mkdir(self.__direccion+dir)
                self.__direccion = self.__direccion + dir + "/"
            else:
                self.__direccion = self.__direccion + dir + "/"
        i = 1
        if(os.path.exists(self.__direccion+self.__nombre)):
            while(os.path.exists(self.__direccion+self.__nombre+ "("+str(i)+")")):
                i += 1
            self.__nombre = self.__nombre+ "("+str(i)+")"

        self.__nombre = self.__nombre
        self.__txt = open(str(self.__direccion + self.__nombre), "w")
        self.__st = ""
        self.__txt.close()

    
    def setTxtName(self, newname):
        os.rename(self.__nombre, newname)
        self.__nombre = newname

    def getTxtName(self):
        return self.__nombre

    def escribir(self, st):
        self.__st = self.__st + st+"\n"

    def imprimir(self):
        try:
            self.__txt = open(str(self.__direccion + self.__nombre), "w")
            self.__txt.write(self.__st)
            self.__txt.close()
        except IOError:
            print ("No se pudo abrir el txt para imprimir")
    
    # def nombreArchivo(self, path):
    #     head, tail = ntpath.split(path)
    #     print (ntpath.split(path))
    #     return tail or ntpath.basename(head)