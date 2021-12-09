from Vertice import Vertice
from Grafo import Grafo
from Arista import Arista
from clsTxt import clsTxt
from Tabu import Tabu
import copy
from time import time
from random import sample, randint, shuffle

class TabuSearch(object):
  def __init__(self, M: list, nombreArchivo, tenureADD, tenureDROP, tiempoEjec, optimo):
    self._G = Grafo (M)
    self.__soluciones = []
    self.__aristas = [] # lista de toda sla saristaas
    self.__optimo = optimo
    self.__add = []
    self.__drop = []
    self.__permitidos_add = []
    self.__permitidos_drop = []
    self.__tenureADD =  tenureADD
    self.__tenureDROP =  tenureDROP
    self.__tiempoMaxEjec = float(tiempoEjec*60) # pasamos a segundos
    self.__tiempoIni = time()
    # self.__txt = clsTxt(nombreArchivo)
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
    g1 = self._G.copyVacio()
    print(f"self.__tenureADD: {self.__tenureADD}")
    print(f"self.__tenureDROP: {self.__tenureDROP}")
    # self.__txt.escribir(str(g1))
    # self.__txt.escribir("------------------   DATOS INICIALES ----------------")
    # self.__txt.escribir(f"Mejor encontrado (peso): {self.__optimo}")
    # self.__txt.escribir(f"TenureADD: {self.__tenureADD}, TenureDROP: {self.__tenureDROP}")
    # self.__txt.escribir(f"Tiempo de Ejecución asignado: {self.__tiempoMaxEjec}")
    vecinosCercanos = self.solucionVecinosCercanos()
    
    g1.cargarDesdeSecuenciaDeVertices(vecinosCercanos) #Carga el recorrido a la solución
    print(f"Pero solución inicial: {g1.getCostoAsociado()}")
    self.__soluciones.append(copy.deepcopy(g1)) #Agregar solución inicial
    self.__permitidos_add = g1.cargaAristas() # cargamos una lista de todas las aristas
    self.__permitidos_drop = copy.deepcopy(self.__permitidos_add)
    # aux = g1.cargaAristas()
    # print(f"len(aux): {len(aux)}")
    # shuffle(aux)
    # self.__permitidos_add = aux[0:int(len(aux)/2)]
    # self.__permitidos_drop = aux[int(len(aux)/2):int(len(aux))]
    # self.__txt.escribir("------------------   SOL INICIAL ----------------")
    # self.__txt.escribir(f"Secuencia de vertices: {g1.getV()}")
    # self.__txt.escribir(f"Costo asociado: {g1.getCostoAsociado()}")
    # self.__txt.escribir(f"Desviación: {round((g1.getCostoAsociado()*100)/self.__optimo,3)-100}%")

    iterac = 0
    tiempoEjec = time() - self.__tiempoIni
    tiempoAviso_max = float(10)
    tiempoAviso_ini = time()
    tiempoAviso = 0

    while tiempoEjec < self.__tiempoMaxEjec:
      add = []
      drop = []
      
      costo, seq, add, drop= g1.swap_3opt(self.__permitidos_add, self.__permitidos_drop)
      self.decrementaTenure(self.__add, True)
      self.decrementaTenure(self.__drop, False)
      self.agregaAListaTabu(add,drop)
      # print(f"len(self.__permitidos_add): {len(self.__permitidos_add)}")
      # print(f"len(self.__permitidos_drop): {len(self.__permitidos_drop)}")
      # print(f"self.__add: {self.__add}")
      # print(f"self.__drop: {self.__drop}")
      if costo < self.__soluciones[-1].getCostoAsociado():
        g1.cargarDesdeSecuenciaDeVertices(seq)
        # self.__txt.escribir(f"------------------   NUEVA SOLUCIÓN ENCONTRADA ----------------")
        # self.__txt.escribir(str(g1.getV()))
        # self.__txt.escribir(f"Costo Asociado: {g1.getCostoAsociado()}")
        # self.__txt.escribir(f"Desviación: {round((g1.getCostoAsociado()*100)/self.__optimo,3)-100}%")
        # self.__txt.escribir(f"Tiempo: {int(tiempoEjec/60)} min {int(tiempoEjec%60)} seg")
        print(f"Costo asociado de nueva solución: {g1.getCostoAsociado()}")
        self.__soluciones.append(copy.deepcopy(g1))

      iterac += 1
      tiempoEjec = time() - self.__tiempoIni
      tiempoAviso = time() - tiempoAviso_ini
      if tiempoAviso > tiempoAviso_max:
        tiempoAviso = 0
        tiempoAviso_ini = time()
        print(f"Número de iteraciones: {iterac}. len(add): {len(self.__add)}, len(drop): {len(self.__drop)}  <---------------------")
        print(f"len(permitidos_add): {len(self.__permitidos_add)} len(permitidos_drop): {len(self.__permitidos_drop)}")
    print(f"optimo mejor solución: {self.__soluciones[-1].getCostoAsociado()}")
    print(f"len(self.__soluciones): {len(self.__soluciones)}")
    print(f"Número de iteraciones: {iterac}")
    # self.__txt.escribir(f"Número de iteraciones: {iterac}")
    # self.__txt.escribir(f"Tiempo total de ejecución: {int(tiempoEjec/60)} min {int(tiempoEjec%60)} seg")
    # self.__txt.imprimir()
    

  def aristasConVertice(self, v):
    aristas = []
    for a in self.__aristas:
      if a.getOrigen() == v or a.getDestino() == v:
        aristas.append(a)
    return aristas

  def decrementaTenure(self, lista_tabu: list, add):
    i=0
    while i < len(lista_tabu):
      lista_tabu[i].decrementaT()
      if(lista_tabu[i].getTenure()==0):
        if add:
          self.__permitidos_add.append(lista_tabu.pop(i).getElemento())
        else:
          self.__permitidos_drop.append(lista_tabu.pop(i).getElemento())
      else:
        i+=1

  def agregaAListaTabu(self, add, drop):
    for d in drop:
      self.__permitidos_drop.remove(d)
      self.__drop.append(Tabu(d, self.__tenureDROP))
    for a in add:
      self.__permitidos_add.remove(a)
      self.__add.append(Tabu(a, self.__tenureADD))