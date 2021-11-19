import sys
import os
import csv
import re
import ntpath
class clsTxt:
    def __init__(self, nombreTxt, Carpeta, paralelismo, Subcarpeta):
        if paralelismo != "paralelismo":
            nombreTxt = nombreArchivo(nombreTxt)
            Carpeta = Carpeta
            print (re.findall(r"[0-9A-Za-z-]+.",nombreTxt))
            nombreCarpeta = re.findall(r"[0-9A-Za-z-]+.",nombreTxt)[0]
            
            if(os.path.exists(Carpeta)):
                self.__carpeta = Carpeta
            else:
                os.mkdir(Carpeta)
                self.__carpeta = Carpeta
            
            nombreCarpeta = self.__carpeta +"/"+nombreCarpeta
            if(os.path.exists(nombreCarpeta)):
                self.__nombre = "%s/%s" %(nombreCarpeta,nombreTxt)
            else:
                os.mkdir(nombreCarpeta)
                self.__nombre = "%s/%s" %(nombreCarpeta,nombreTxt)    
            i = 0
            while os.path.exists("%s (%i).txt" %(self.__nombre ,i)):
                i += 1
            self.__nombre = "%s (%i)" %(self.__nombre,i)
            self.__txt = open(str(self.__nombre)+".txt", "w")
        else:
            if(os.path.exists(Carpeta)):
                self.__carpeta = Carpeta
            else:
                os.mkdir(Carpeta)
                self.__carpeta = Carpeta

            nombreCarpeta = self.__carpeta +"/"+nombreTxt.split('_')[0]
            if(os.path.exists(nombreCarpeta)):
                self.__nombre = nombreCarpeta
            else:
                os.mkdir(nombreCarpeta)
                self.__nombre = nombreCarpeta

            nombreCarpeta = nombreCarpeta+"/"+Subcarpeta
            if(os.path.exists(nombreCarpeta)):
                self.__nombre = nombreCarpeta+"/"+nombreTxt
            else:
                os.mkdir(nombreCarpeta)
                self.__nombre = nombreCarpeta+"/"+nombreTxt

            
            self.__txt = open(str(self.__nombre)+".txt", "w")
        self.__st = ""
    
    def setTxtName(self, newname):
        os.rename(self.__nombre+".txt", newname+".txt")
        self.__nombre = newname

    def getTxtName(self):
        return self.__nombre

    def escribir(self, st):
        self.__st = self.__st + st+"\n"

    def imprimir(self):
        try:
            self.__txt = open(self.__nombre+".txt", "w")
            self.__txt.write(self.__st)
            self.__txt.close()
        except IOError:
            print ("No se pudo abrir el txt para imprimir")
    
def nombreArchivo(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)