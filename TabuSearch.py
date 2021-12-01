from Vertice import Vertice
from Grafo import Grafo
from clsTxt import clsTxt
from Tabu import Tabu
import copy
from time import time
import random

class TabuSearch(object):
    def __init__(self, M: list, nombreArchivo, solInicial, nroIntercambios, opt, tenureADD, tenureDROP, tiempoEjec, optimo):
        self._G = Grafo (M)
        self.__soluciones = []
        self.__nroIntercambios=nroIntercambios*2    #corresponde al nro de vertices los intercambios. 1intercambio => 2 vertices
        self.__opt = opt
        self.__optimo = optimo
        self.__tenureADD =  tenureADD
        self.__tenureMaxADD = int(tenureADD*1.7)
        self.__tenureDROP =  tenureDROP
        self.__tenureMaxDROP = int(tenureDROP*1.7)
        self.__tiempoMaxEjec = float(tiempoEjec)
        # self.__solInicial 
        self.ts()

    def solucionVecinosCercanos(self):
        inicio = self._G.getV()[0] #SE PUEDE MEJORAR (que el inicio no sea siempre el primero)
        matrizDist = self._G.getMatriz()

        recorrido = []
        visitados = []
        
        recorrido.append(inicio)    #Agrego el vertice inicial
        visitados.append(0)     #Agrego el vertice inicial
        masCercano=0
        for i in range(0,len(matrizDist)-1):
             
                masCercano = self.vecinoMasCercano(matrizDist, masCercano, visitados) #obtiene la posicion dela matriz del vecino mas cercano
                recorrido.append(Vertice(masCercano+1))
                visitados.append(masCercano)
        return recorrido

    def ts(self):
        l_permit = []