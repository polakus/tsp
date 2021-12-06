from Vertice import Vertice
from Arista import Arista
from random import randint, sample
from Tabu import Tabu
import copy

class Grafo:
    def __init__(self, M: list):
      self._V = []
      self._A = []
      self._mDist = M
      self.__costoAsociado = 0
      self.cargarDesdeMatriz(M)

    def setA(self, A):
      self._A = A

    def setV(self, V):
      self._V = V

    def getCostoAsociado(self):
      return self.__costoAsociado

    def getA(self):
      return self._A

    def getV(self):
      return self._V

    def __lt__(self, otro):
      return (self.__costoAsociado < otro.__costoAsociado)

    def __le__(self, otro):
      return (self.__costoAsociado <= otro.__costoAsociado)    
    
    def __gt__(self, otro):
      return (self.__costoAsociado > otro.__costoAsociado)

    def __ge__(self, otro):
      return (self.__costoAsociado >= otro.__costoAsociado)    
    
    def __eq__(self, other):
      return (self.__class__ == other.__class__ and self.__costoAsociado == other.__costoAsociado)

    #Compara entre 2. Se fija si hay aristas de A contenidas en si misma. Si hay aristas, se detiene
    def contieneA(self,A):
      sigue = True
      i = 0
      n = len(self.getA())
      while((sigue == True) and i < n):
        if(self.getA()[i].tieneOrigen(A.getOrigen()) and self.getA()[i].tieneDestino(A.getDestino())):
          sigue = False
          i=n
        i+=1
      return not(sigue)

    def getCostoArista(self, A):
      sigue = True
      i = 0
      n = len(self.getA())
      while((sigue == True) and i < n):
        if(self.getA()[i].tieneOrigen(A.getOrigen()) and self.getA()[i].tieneDestino(A.getDestino())):
          sigue = False
        i+=1
      return i-1

    def getAristaMinima(self,listaAristas):
      minimo = listaAristas[0]
      for i in listaAristas:
        if(i.getPeso() < minimo.getPeso()):
          minimo = i

      return minimo

    def cargaAristas(self):
      A=[]
      cantV = len(self._V)
      for row in range(1,cantV):
        for col in range(row):
          arista_aux = Arista(Vertice(row+1),Vertice(col+1),self._mDist[row][col])
          A.append(arista_aux)
      return A
    
    def rellenarAristas(self):
      A = self._A
      V = self._V
      for i in V:
        for j in V:
          arista_aux = Arista(i,j,0)
          if(not(self.contieneA(arista_aux))):
            A.append(arista_aux)

    def __str__(self):
      salida = ""
      V = self.getV()
      #Muestra la primera fila con los vertices
      if(len(self._mDist) == len(self.getV())):
        for i in range(0,len(V)):
          salida += "     " +  str(V[i]) 

        salida = salida + "\n"
        for i in range(0,len(V)):
          salida += str(V[i]) + "    "
          for j in range(0,len(V)):
            salida += str(self._mDist[i][j]) + "    "
          salida = salida + "\n"
      else:
        for i in range(0,len(V)):
          salida += str(V[i]) + "    "

        salida = salida + "\n"
        for i in V:
          salida += str(i) + "    "
          for j in V:
            indice = self.getCostoArista(Arista(i,j,0))
            salida += str(self.getA()[indice].getPeso()) + "    "
          salida = salida + "\n"
      return salida
    
    def __repr__(self):
      return str(self.getV)
    
    #Cargar los vérticees y las aristas
    def cargarDesdeMatriz(self, Matriz):
      for fila in range(0,len(Matriz)): #carga vértices
        self._V.append(Vertice(fila+1))    #V = [1,2,3,4,5]; V=[1,3,4] A=[(1,3)(3,4)] => sol 1->3->4->5->2
      for fila in range(0,len(Matriz)): #carga aristas
        for columna in range(0, len(Matriz[fila])):
          aux = Arista(self._V[fila],self._V[columna],(Matriz[fila][columna]))
          self._A.append(aux)

    def getVerticeInicio(self):
      return self._A[0].getOrigen()

    def getMatriz(self):
      return self._mDist
    
    def setMatriz(self, M):
      self._mDist = M

    #Para que cargue desde una secuencia de vertices por ej. s1= [1,3,4,5,8,9,6,7] -> s2=[1,3,9,5,8,4,6,7]
    def cargarDesdeSecuenciaDeVertices(self,seq:list):
      self._V = seq
      rV = [] #Vértices de la matriz ordenados, para obtener la referencia en la matriz de distnacias
      costo = 0
      for j in range(0,len(self._mDist)):
        rV.append(Vertice(j+1))
      self._A = []
      for i in range(0,len(seq)-1):
        dist = self._mDist[rV.index(seq[i])][rV.index(seq[i+1])] #Referencias en la matriz
        self._A.append(Arista(seq[i], seq[i+1], dist))
        costo += dist
      self._A.append(Arista(seq[-1],seq[0], self._mDist[rV.index(seq[-1])][rV.index(seq[0])]))
      self.__costoAsociado = costo + self._mDist[rV.index(seq[len(seq)-1])][rV.index(seq[0])]

    def incrementaFrecuencia(self):
      for x in range(0,len(self.getA())):
        self.getA()[x].incFrecuencia()

    def copyVacio(self):
      ret = Grafo([])
      ret.setMatriz(self._mDist)
      return ret

    def copy(self):
      G = Grafo(self._mDist)
      G.setA(copy.deepcopy(self.getA()))
      G.setV(copy.deepcopy(self.getV()))
      return G

    def swap_2opt(self, add, drop, tenureADD, tenureDROP, aristas):
      permitidos_add = []
      permitidos_drop = []
      # print("############ empieza aca ############")
      # if add
      for a in aristas:
        i = 0
        # print(add[0].getElemento()==a)
        while i < len(add) and add[i].getElemento() != a:
          # print("al menos una vez")
          i+=1
        if i>=len(add):
          permitidos_add.append(a)
        i = 0
        while i<len(drop) and drop[i].getElemento() != a:
          i+=1
        if i>=len(drop):
          permitidos_drop.append(a)
      vertices = self._V
      # print(f"vertices: {vertices}")
      # print(f"aristas: {self._A+[Arista(vertices[-1], vertices[0], self._mDist[vertices[-1].getValue()-1][vertices[0].getValue()-1])]}")
      # print(f"costo asociado: {self.__costoAsociado}")
      grado = len(vertices)
      cond = True # cond para saber si hay que elegir otras aaristas
      lista_aristas=[x for x in self._A if x in permitidos_drop]
      print(" ####################################### aca empieza ###########################")
      print(f"add: {add}")
      print(f"drop: {drop}")
      print(f"lista_aristas: {lista_aristas}")
      while cond:
        candidatos = sample(lista_aristas, 2)
        print(f"candidatos: {candidatos}")
        if not candidatos[0].mismoVertice(candidatos[1]) :
          # print(f"candidatos: {candidatos}")
          cond = False
          secuencia = []
          indices = []
          indices.append(vertices.index(candidatos[0].getOrigen()))
          indices.append(vertices.index(candidatos[0].getDestino()))
          indices.append(vertices.index(candidatos[1].getOrigen()))
          indices.append(vertices.index(candidatos[1].getDestino()))
          indices.sort()
          cond_0 = True
          EnPermitidosAdd = True
          ind = 0
          i = 0
          print(f"vertices: {vertices}")
          print(f"indices: {indices}")
          while i < grado and EnPermitidosAdd:
            print(f"ind: {ind}")
            if cond_0:
              secuencia.append(vertices[ind])
              if vertices[ind] == vertices[indices[0]]:
                nueva_a = Arista(vertices[ind],vertices[indices[2]],self._mDist[vertices[ind].getValue()-1][vertices[indices[2]].getValue()-1])
                try:
                  permitidos_add.remove(nueva_a)
                  add.append(Tabu(nueva_a, tenureADD))
                  cond_0 = False
                  ind = indices[2]
                except:
                  print(f"EnPermitidosAdd: {False} cond_0: {cond_0}")
                  EnPermitidosAdd = False
              else:
                ind += 1
            else:
              secuencia.append(vertices[ind])
              if vertices[ind] == vertices[indices[1]]:
                nueva_a = Arista(vertices[ind],vertices[indices[3]],self._mDist[vertices[ind].getValue()-1][vertices[indices[3]].getValue()-1])
                try:
                  permitidos_add.remove(nueva_a)
                  add.append(Tabu(nueva_a, tenureADD))
                  cond_0 = True
                  ind = indices[3]
                except:
                  print(f"EnPermitidosAdd: {False} cond_0: {cond_0}")
                  EnPermitidosAdd = False
              else:
                ind -= 1
            i += 1
          if not EnPermitidosAdd:
            cond = True
        # else:
          # if not (candidatos[0] in permitidos_add and candidatos[1] not in permitidos_add):
          #   if candidatos[0] in permitidos_add: # entonces candidatos[1] not in permitidos_add
          #     candidatos[1] = lista_aristas[randint(0,len(lista_aristas)-1)]
          #   else:
          #     candidatos[0] = lista_aristas[randint(0,len(lista_aristas)-1)]
          # else:
          #   candidatos[randint(0,1)] = lista_aristas[randint(0,len(lista_aristas)-1)]
      # print(f"secuencia: {secuencia}")
      self.cargarDesdeSecuenciaDeVertices(copy.deepcopy(secuencia))
      drop.append(Tabu(candidatos[0],tenureDROP))
      drop.append(Tabu(candidatos[1],tenureDROP))
      permitidos_drop.remove(candidatos[0])
      permitidos_drop.remove(candidatos[1])
      return self.__costoAsociado

    def mejoresIndices(self, solucion, lista_permit):
      mayorVerticeOrigen = 0
      iMin = 0
      for i in range(0,len(solucion)):
        origen = solucion[i].getValue()-1
        destino = solucion[i+1].getValue()-1
        dist = self._mDist[origen][destino]
        
        #Busca la peor arista
        if(dist > mayorVerticeOrigen and (origen in lista_permit) and (destino in lista_permit)): 
          minimo = self._mDist[origen][0]
          filaVertice = self._mDist[origen]
          jMin = 0
          #Busca el mejor destino para la arista encontrada, asegurándose de que no esté en la lista Tabú
          for j in range(0,len(filaVertice)):
            if(filaVertice[j]<minimo and Vertice(j+1) in lista_permit):
              minimo = dist
              jMin = j
          iMin = i
          
          iMin
          jMin

      return i,j