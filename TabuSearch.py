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
    self.__add = []
    self.__drop = []
    self.__permitidos_add = []
    self.__permitidos_drop = []
    self.__tenureADD =  tenureADD
    self.__tenureMaxADD = int(tenureADD*1.7)
    self.__tenureDROP =  tenureDROP
    self.__tenureMaxDROP = int(tenureDROP*1.7)
    self.__tiempoMaxEjec = float(tiempoEjec*60)
    self.__tiempoIni = time()
    self.__txt = clsTxt(nombreArchivo)
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
    vecinosCercanos = self.solucionVecinosCercanos()
    
    g1.cargarDesdeSecuenciaDeVertices(vecinosCercanos) #Carga el recorrido a la solución
    self.__soluciones.append(copy.deepcopy(g1)) #Agregar solución inicial
    self.__permitidos_add = g1.cargaAristas() # cargamos una lista de todas las aristas
    self.__permitidos_drop = copy.deepcopy(self.__permitidos_add)
    # self.__txt.escribir(str(g1))
    self.__txt.escribir("------------------   DATOS INICIALES ----------------")
    self.__txt.escribir(f"Mejor encontrado (peso): {self.__optimo}")
    self.__txt.escribir(f"TenureADD: {self.__tenureADD}, TenureDROP: {self.__tenureDROP}")
    self.__txt.escribir(f"Tiempo de Ejecución asignado: {int(self.__tiempoMaxEjec/60)} min {int(self.__tiempoMaxEjec)%60} seg")
    self.__txt.escribir("------------------   SOL INICIAL ----------------")
    self.__txt.escribir(f"Secuencia de vertices: {g1.getV()}")
    self.__txt.escribir(f"Costo asociado: {g1.getCostoAsociado()}")
    self.__txt.escribir(f"Desviación: {round((g1.getCostoAsociado()*100)/self.__optimo,3)-100}%")

    iterac = 0
    tiempoEjec = time() - self.__tiempoIni
    tiempoAviso_max = float(10)
    tiempoAviso_ini = time()
    tiempoAviso = 0

    t_interc = self.__tiempoMaxEjec*0.03
    ini_t_interc = time()
    k_opt = 2

    while tiempoEjec < self.__tiempoMaxEjec:
      add = []
      drop = []
      if time() - ini_t_interc > t_interc and k_opt == 2:
        k_opt = 3
        ini_t_interc = time()
        print(f"{int((tiempoEjec*100)/self.__tiempoMaxEjec)}% - ATENCIÓN: cabio a {k_opt}")
      elif time() - ini_t_interc > t_interc and k_opt == 3:
        k_opt = 2
        ini_t_interc = time()
        print(f"{int((tiempoEjec*100)/self.__tiempoMaxEjec)}% - ATENCIÓN: cambió a {k_opt}")
      if k_opt == 2:
        costo, seq, add, drop = g1.swap_2optV2(self.__add, self.__drop)
      else:
        costo, seq, add, drop = g1.swap_3optV2(self.__add, self.__drop)
        
      self.decrementaTenure(self.__add)
      self.decrementaTenure(self.__drop)
      self.agregaAListaTabu(add,drop)
      if costo < self.__soluciones[-1].getCostoAsociado():
        g1.cargarDesdeSecuenciaDeVertices(seq)
        self.__soluciones.append(copy.deepcopy(g1))
        ini_t_interc = time()
        self.__txt.escribir(f"------------------   NUEVA SOLUCIÓN ENCONTRADA ----------------")
        self.__txt.escribir(str(g1.getV()))
        self.__txt.escribir(f"Costo Asociado: {g1.getCostoAsociado()}")
        self.__txt.escribir(f"Desviación: {round((g1.getCostoAsociado()*100)/self.__optimo,3)-100}%")
        self.__txt.escribir(f"Tiempo: {int(tiempoEjec/60)} min {int(tiempoEjec%60)} seg")
        print(f"{int((tiempoEjec*100)/self.__tiempoMaxEjec)}% - Costo asociado de nueva solución: {g1.getCostoAsociado()}")
        print(f"{int((tiempoEjec*100)/self.__tiempoMaxEjec)}% - Desviación: {round((g1.getCostoAsociado()*100)/self.__optimo,3)-100}% <---------------------------")
      iterac += 1
      tiempoEjec = time() - self.__tiempoIni
      tiempoAviso = time() - tiempoAviso_ini
      if tiempoAviso > tiempoAviso_max:
        tiempoAviso = 0
        tiempoAviso_ini = time()
        print(f"{int((tiempoEjec*100)/self.__tiempoMaxEjec)}% - Número de iteraciones: {iterac}. len(add): {len(self.__add)}, len(drop): {len(self.__drop)}")
        print(f"{int((tiempoEjec*100)/self.__tiempoMaxEjec)}% - len(permitidos_add): {len(self.__permitidos_add)} len(permitidos_drop): {len(self.__permitidos_drop)}")
    print(f"optimo mejor solución: {self.__soluciones[-1].getCostoAsociado()}")
    print(f"len(self.__soluciones): {len(self.__soluciones)}")
    print(f"Número de iteraciones: {iterac}")
    self.__txt.escribir(f"Número de iteraciones: {iterac}")
    self.__txt.escribir(f"Tiempo total de ejecución: {int(tiempoEjec/60)} min {int(tiempoEjec%60)} seg")
    self.__txt.imprimir()

  def decrementaTenure(self, lista_tabu: list):
    i=0
    while i < len(lista_tabu):
      lista_tabu[i].decrementaT()
      if(lista_tabu[i].getTenure()==0):
        lista_tabu.pop(i)
      else:
        i+=1

  def agregaAListaTabu(self, add, drop):
    for d in drop:
      d.setTenure( randint(1,self.__tenureDROP))
      self.__drop.append(d)
    for a in add:
      a.setTenure( randint(1,self.__tenureADD))
      self.__add.append(a)