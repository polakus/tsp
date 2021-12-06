from Vertice import Vertice
from Grafo import Grafo
from Arista import Arista
from clsTxt import clsTxt
from Tabu import Tabu
import copy
from time import time
from random import sample, randint

class TabuSearch(object):
  def __init__(self, M: list, nombreArchivo, solInicial, nroIntercambios, opt, tenureADD, tenureDROP, tiempoEjec, optimo):
    self._G = Grafo (M)
    self.__soluciones = []
    self.__aristas = [] # lista de toda sla saristaas
    self.__nroIntercambios=nroIntercambios*2    #corresponde al nro de vertices los intercambios. 1intercambio => 2 vertices
    self.__opt = opt
    self.__optimo = optimo
    self.__tenureADD =  tenureADD
    self.__tenureMaxADD = int(tenureADD*1.7)
    self.__tenureDROP =  tenureDROP
    self.__tenureMaxDROP = int(tenureDROP*1.7)
    self.__tiempoMaxEjec = float(tiempoEjec*60)
    self.__tiempoIni = time()
    # self.__txt = clsTxt("depurando")
    self.ts()

  def vecinoMasCercano(self, matrizDist: list, pos: int, visitados: list):
    masCercano = matrizDist[pos][pos]
    indMasCercano = 0
    for i in range(0, len(matrizDist)):
      costo = matrizDist[pos][i]
      if(costo < masCercano and i not in visitados):
        masCercano = costo
        indMasCercano = i
    return indMasCercano

  def solucionVecinosCercanos(self):
    recorrido = []
    visitados = []
    inicio = self._G.getV()[0] #SE PUEDE MEJORAR (que el inicio no sea siempre el primero)
    matrizDist = self._G.getMatriz()
    recorrido.append(inicio) #Agrego el vertice inicial
    visitados.append(0) #Agrego el indice del vertice inicial
    masCercano=0
    for _ in range(0,len(matrizDist)-1):
      masCercano = self.vecinoMasCercano(matrizDist, masCercano, visitados) #obtiene la posicion dela matriz del vecino mas cercano
      recorrido.append(Vertice(masCercano+1))
      visitados.append(masCercano)
    return recorrido

  def ts(self):
    add = [] # Tiene objetos de la clase Tabu
    drop = [] # Tiene objetos de la clase Tabu
    g1 = self._G.copyVacio()
    vecinosCercanos = self.solucionVecinosCercanos()
    
    g1.cargarDesdeSecuenciaDeVertices(vecinosCercanos) #Carga el recorrido a la solución
    self.__soluciones.append(copy.deepcopy(g1)) #Agregar solución inicial
    Sol_Actual = self._G.copyVacio()
    Sol_Actual = self.__soluciones[len(self.__soluciones)-1] #La actual es la Primera solución
    Sol_Optima = copy.deepcopy(Sol_Actual) #Ultima solucion optima obtenida, corresponde a la primera Solucion
    
    
    self.__aristas = g1.cargaAristas() # cargamos una lista de todas las aristas
    add = []
    drop = []
    iterac = 0
    tiempoEjec = time() - self.__tiempoIni
    tiempoAviso_max = float(10)
    tiempoAviso_ini = time()
    tiempoAviso = 0
    # self.__txt.escribir(str(g1.getMatriz()))
    # print(f"len(self.__aristas): {len(self.__aristas)}")
    # print(f"vertices: {g1.getV()}")
    # print(f"aristas: {g1.getA()}")
    
    # self.getArista2opt(add, drop, g1)

    while tiempoEjec < self.__tiempoMaxEjec:
      costo = g1.swap_2opt(add, drop, self.__tenureADD, self.__tenureDROP, self.__aristas)
      # print(g1.getA())
      self.decrementaTenure(add)
      self.decrementaTenure(drop)
      if costo < self.__soluciones[-1].getCostoAsociado():
        # print(f"costo: {costo} y self.__soluciones[-1].getCostoAsociado(): {self.__soluciones[-1].getCostoAsociado()}")
        # print(f"Costo asociado de nueva solució: {g1.getCostoAsociado()}")
        self.__soluciones.append(copy.deepcopy(g1))
      iterac += 1
      tiempoEjec = time() - self.__tiempoIni
      tiempoAviso = time() - tiempoAviso_ini
      if tiempoAviso > tiempoAviso_max:
        tiempoAviso = 0
        tiempoAviso_ini = time()
      # print(f"Número de iteraciones: {iterac}. len(add): {len(add)}, len(drop): {len(drop)}  <---------------------")
    # self.__txt.imprimir()
    # print(f"len(self.__soluciones): {len(self.__soluciones)}")
    # print(f"Número de iteraciones: {iterac}")
    

  def aristasConVertice(self, v):
    aristas = []
    for a in self.__aristas:
      if a.getOrigen() == v or a.getDestino() == v:
        aristas.append(a)
    return aristas

  def decrementaTenure(self, lista_tabu: list):
    i=0
    while i < len(lista_tabu):
      lista_tabu[i].decrementaT()
      if(lista_tabu[i].getTenure()==0):
        lista_tabu.pop(i)
      else:
        i+=1