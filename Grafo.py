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

    def swap_2opt(self, add: list, drop: list, tenureADD, tenureDROP, permitidos_add: list, permitidos_drop: list):
      vertices = self._V
      grado = len(vertices)
      cond = True # cond para saber si hay que elegir otras aristas
      lista_aristas=[x for x in self._A if x in permitidos_drop]
      # # print(" ####################################### aca empieza ###########################")
      # # print(f"add: {add}, permitidos_add: {permitidos_add}")
      # # print(f"drop: {drop}, permitidos_drop: {permitidos_drop}")
      # # print(f"lista_aristas: {lista_aristas}")
      if len(lista_aristas) >= 3:
        cand_d = sample(lista_aristas, 2)
        cond = True
        while cond:
          if not cand_d[0].mismoVertice(cand_d[1]):
            if cand_d[0] in permitidos_drop and cand_d[1] in permitidos_drop:
              indices = []
              indices.append(vertices.index(cand_d[0].getOrigen()))
              indices.append(vertices.index(cand_d[0].getDestino()))
              indices.append(vertices.index(cand_d[1].getOrigen()))
              indices.append(vertices.index(cand_d[1].getDestino()))
              indices.sort()
              cand_a = []
              aux1 = Arista(vertices[indices[0]],vertices[indices[2]],self._mDist[vertices[indices[0]].getValue()-1][vertices[indices[2]].getValue()-1])
              aux2 = Arista(vertices[indices[1]],vertices[indices[3]],self._mDist[vertices[indices[1]].getValue()-1][vertices[indices[3]].getValue()-1])
              if aux1 in permitidos_add and aux2 in permitidos_add:
                cond = False
                permitidos_drop.remove(cand_d[0])
                permitidos_drop.remove(cand_d[1])
                permitidos_add.remove(aux1)
                permitidos_add.remove(aux2)
                add.append(Tabu(aux1, tenureADD))
                add.append(Tabu(aux2, tenureADD))
                drop.append(Tabu(cand_d[0], tenureDROP))
                drop.append(Tabu(cand_d[1], tenureDROP))
                cand_a.append(aux1)
                cand_a.append(aux2)
              else:
                cand_d = sample(lista_aristas,2)
            else:
              cand_d = sample(lista_aristas,2)
          else:
            cand_d = sample(lista_aristas,2)
          
        # # print(f"cand_d: {cand_d}")
        # # print(f"cand_a: {cand_a}")
        secuencia = []
        ind = 0
        i = 0
        c1=vertices[0]==cand_d[0].getOrigen() and vertices[-1]==cand_d[0].getDestino()
        c2=vertices[0]==cand_d[0].getDestino() and vertices[-1]==cand_d[0].getOrigen()
        c3=vertices[0]==cand_d[1].getOrigen() and vertices[-1]==cand_d[1].getDestino()
        c4=vertices[0]==cand_d[1].getDestino() and vertices[-1]==cand_d[1].getOrigen()
        if not (c1 or c2 or c3 or c4):
          der = True
          while i < grado:
            secuencia.append(vertices[ind])
            if der:
              if vertices[ind] == vertices[indices[0]]:
                der = False
                ind = indices[2]
              else:
                ind += 1
            else:
              if vertices[ind] == vertices[indices[1]]:
                der = True
                ind = indices[3]
              else:
                ind -= 1
            # costo += self._mDist[secuencia[i].getValue()-1][vertices[ind%grado].getValue()-1]
            i += 1
        else:
          der = True
          while i < grado:
            secuencia.append(vertices[ind])
            if der:
              if vertices[ind] == vertices[indices[0]]:
                der = False
                ind = indices[2]
              else:
                ind -= 1
            else:
              if vertices[ind] == vertices[indices[3]]:
                der = True
                ind = indices[1]
              else:
                ind += 1
            # costo += self._mDist[secuencia[i].getValue()-1][vertices[ind%grado].getValue()-1]
            i += 1
        # # print(f"vertices: {vertices}")
        # # print(f"secuencia: {secuencia}")
        self.cargarDesdeSecuenciaDeVertices(copy.deepcopy(secuencia))
      else:
        print("CUIDADO!! TENURE MUY ALTO")
      return self.__costoAsociado
        # costo += self._mDist[secuencia[0].getValue()-1][secuencia[-1].getValue()-1]

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


      ##################### porcion de código ######################

      # cand_d = []
      # cand_d.append(lista_aristas[randint(0,len(lista_aristas)-1)])
      # cond1 = True
      # while cond1:
      #   try:
      #     permitidos_drop.remove(cand_d[0])
      #     rand_ind = randint(0,len(lista_aristas)-1)
      #     if cand_d[0].mismoVertice(lista_aristas[rand_ind]):
      #       rand_ind = randint(0,len(lista_aristas)-1)
      #     else:
      #       cond1 = False
      #       cond2 = True
      #       while cond2:
      #         try:
      #           permitidos_drop.remove(lista_aristas[rand_ind])
      #           if cand_d[0].mismoVertice(lista_aristas[rand_ind]):
      #             rand_ind = randint(0,len(lista_aristas)-1)
      #           else:
      #             cand_d.append(lista_aristas[rand_ind])
      #             indices = []
      #             indices.append(vertices.index(cand_d[0].getOrigen()))
      #             indices.append(vertices.index(cand_d[0].getDestino()))
      #             indices.append(vertices.index(cand_d[1].getOrigen()))
      #             indices.append(vertices.index(cand_d[1].getDestino()))
      #             indices.sort()
      #             aux1 = Arista(vertices[indices[0]],vertices[indices[2]],self._mDist[vertices[indices[0]].getValue()-1][vertices[indices[2]].getValue()-1])
      #             aux2 = Arista(vertices[indices[0]],vertices[indices[2]],self._mDist[vertices[indices[0]].getValue()-1][vertices[indices[2]].getValue()-1])
      #             if aux1 not in permitidos_add or aux2 not in permitidos_add:
      #               cond1 = True
                  
      #         except:
      #           rand_ind = randint(0,len(lista_aristas)-1)
      #   except:
      #     cand_d[0] = lista_aristas[randint(0,len(lista_aristas)-1)]