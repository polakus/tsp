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

    def compara(self, aristas, permitidos):
      AristasNuevas = []
      claves = [hash(a) for a in permitidos]
      dictA = dict(zip(claves,permitidos))
      for EP in aristas:
        h = hash(EP)
        hInverso = hash(EP.getAristaInvertida())
        try:
          arista = dictA[h]
        except KeyError:
          arista = None
        try:
          aristaInv = dictA[hInverso]
        except KeyError:
          aristaInv = None 
        if arista is not None or aristaInv is not None:
          AristasNuevas.append(EP)
      return AristasNuevas

    def swap_2opt(self, permitidos_add: list, permitidos_drop: list):
      vertices = self._V
      grado = len(vertices)
      cond = True # cond para saber si hay que elegir otras aristas
      # lista_aristas=[x for x in self._A if x in permitidos_drop]
      lista_aristas = self.compara(self._A, permitidos_drop)
      # # print(" ####################################### aca empieza ###########################")
      # # print(f"add: {add}, permitidos_add: {permitidos_add}")
      # # print(f"drop: {drop}, permitidos_drop: {permitidos_drop}")
      # # print(f"lista_aristas: {lista_aristas}")
      if len(lista_aristas) >= 2:
        cand_d = sample(lista_aristas, 2)
        cond = True
        cant_it = 0
        while cond:
          cant_it += 1
          if cant_it > 10:
            print("ESTÁ ESTANCADO 2opt")
            cant_it = 0
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
                # permitidos_drop.remove(cand_d[0])
                # permitidos_drop.remove(cand_d[1])
                # permitidos_add.remove(aux1)
                # permitidos_add.remove(aux2)
                # add.append(Tabu(aux1, tenureADD))
                # add.append(Tabu(aux2, tenureADD))
                # drop.append(Tabu(cand_d[0], tenureDROP))
                # drop.append(Tabu(cand_d[1], tenureDROP))
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
        costo = 0
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
            costo += self._mDist[secuencia[i].getValue()-1][vertices[ind%grado].getValue()-1]
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
            costo += self._mDist[secuencia[i].getValue()-1][vertices[ind%grado].getValue()-1]
            i += 1
        # # print(f"vertices: {vertices}")
        # # print(f"secuencia: {secuencia}")
        # self.cargarDesdeSecuenciaDeVertices(copy.deepcopy(secuencia))
        # if costo != self.__costoAsociado:
        #   print("ERROR DE COSTO")
        #   exit()
      else:
        costo = self.__costoAsociado
        secuencia = vertices
        print("CUIDADO!! TENURE MUY ALTO")
      return costo, secuencia, cand_a, cand_d
        # costo += self._mDist[secuencia[0].getValue()-1][secuencia[-1].getValue()-1]

    def swap_2optV2(self, addT: list, dropT: list):
      # ini = time()
      vertices = self._V
      grado = len(vertices)
      encontrada = True # encontrada para saber si hay que elegir otras aristas
      ar_drop = []
      for t in dropT:
        elem = t.getElemento()
        ar_drop.append(elem)
      lista_aristas = self.complemento(self._A, ar_drop)
      cand_a = []
      cand_d = []
      if len(lista_aristas) >= 2:
        for a in sample(lista_aristas, 2):
          cand_d.append(Tabu(a,0))
        encontrada = False
        cant_it = 0
        estancado = False
        while not encontrada and not estancado:
          cant_it += 1
          if cant_it > grado:
            print("ESTÁ ESTANCADO 2opt")
            estancado = True

          # print(f"cand_d: {cand_d}")
          if not cand_d[0].getElemento().mismoVertice(cand_d[1].getElemento()):
            if cand_d[0] not in dropT and cand_d[1] not in dropT:
              indices = []
              indices.append(vertices.index(cand_d[0].getElemento().getOrigen()))
              indices.append(vertices.index(cand_d[0].getElemento().getDestino()))
              indices.append(vertices.index(cand_d[1].getElemento().getOrigen()))
              indices.append(vertices.index(cand_d[1].getElemento().getDestino()))
              indices.sort()
              cand_a = []
              aux1 = Tabu(Arista(vertices[indices[0]],vertices[indices[2]],self._mDist[vertices[indices[0]].getValue()-1][vertices[indices[2]].getValue()-1]),0)
              aux2 = Tabu(Arista(vertices[indices[1]],vertices[indices[3]],self._mDist[vertices[indices[1]].getValue()-1][vertices[indices[3]].getValue()-1]),0)
              if aux1 not in addT and aux2 not in addT:
                encontrada = True
                cand_a.append(aux1)
                cand_a.append(aux2)
              else:
                cand_d=[]
                for a in sample(lista_aristas, 2):
                  cand_d.append(Tabu(a,0))
            else:

              cand_d = []
              for a in sample(lista_aristas, 2):
                cand_d.append(Tabu(a,0))
          else:
            cand_d = []
            for a in sample(lista_aristas, 2):
              cand_d.append(Tabu(a,0))

        # # print(f"cand_d: {cand_d}")
        # # print(f"cand_a: {cand_a}")
        if encontrada:
          secuencia = []
          ind = 0
          i = 0
          costo = 0
          c1=vertices[0]==cand_d[0].getElemento().getOrigen() and vertices[-1]==cand_d[0].getElemento().getDestino()
          c2=vertices[0]==cand_d[0].getElemento().getDestino() and vertices[-1]==cand_d[0].getElemento().getOrigen()
          c3=vertices[0]==cand_d[1].getElemento().getOrigen() and vertices[-1]==cand_d[1].getElemento().getDestino()
          c4=vertices[0]==cand_d[1].getElemento().getDestino() and vertices[-1]==cand_d[1].getElemento().getOrigen()
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
              costo += self._mDist[secuencia[i].getValue()-1][vertices[ind%grado].getValue()-1]
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
              costo += self._mDist[secuencia[i].getValue()-1][vertices[ind%grado].getValue()-1]
              i += 1
        else:
          cand_d = []
          cand_a = []
          costo = self.__costoAsociado
          secuencia = vertices  
      else:
        costo = self.__costoAsociado
        secuencia = vertices
        print("CUIDADO!! TENURE MUY ALTO 2opt")
      # fin = time() - ini
      # print(f"swap 2opt tarda: {fin}")
      return costo, secuencia, cand_a, cand_d

    def en(self, a: Arista, aristas: list):
      claves = [hash(a) for a in aristas]
      dictA = dict(zip(claves,aristas))
      h = hash(a)
      hInverso = hash(a.getAristaInvertida())
      try:
        arista = dictA[h]
      except KeyError:
        arista = None
      try:
        aristaInv = dictA[hInverso]
      except KeyError:
        aristaInv = None
      if arista is not None or aristaInv is not None:
        return True
      else:
        return False
    
    def swap_3opt(self, permitidos_add: list, permitidos_drop: list):
      # print("EMPIEZA ACA")
      drop = []
      add = []
      secuencia = self._V
      costo = self.__costoAsociado
      # print(f"vertices: {self._V}")
      lista_aristas = self.compara(self._A, permitidos_drop)
      # print(f"lista_aristas: {lista_aristas}")
      if len(lista_aristas) >= 3:
        # print("ESTAMOS EN 3 OPT")
        vertices = self._V
        # print(f"vertices: {vertices}")
        grado = len(vertices)
        # print(f"permitidos_add: {permitidos_add}")
        # print(f"permitidos_drop: {permitidos_drop}")
        # print(f"lista_aristas: {lista_aristas}")
        list_ind_v = list(range(grado))
        encontradas = False
        iter = 0
        while not encontradas and len(list_ind_v)>0:
          iter += 1
          if iter > 10:
            print("ESTANCADO 3opt")
            iter = 0
            # list_ind_v = []
          ind = randint(0,len(list_ind_v)-1)
          aux = [] # para ir guardando aristas de lista_aristas
          ant = vertices[(list_ind_v[ind]-1)%grado]
          med = vertices[list_ind_v[ind]]
          # print(f"med vertice: {med}")
          pos = vertices[(list_ind_v[ind]+1)%grado]
          d1 = Arista(ant, med, self._mDist[ant.getValue()-1][med.getValue()-1])
          d2 = Arista(pos, med, self._mDist[pos.getValue()-1][med.getValue()-1])
          a1 = Arista(ant, pos, self._mDist[pos.getValue()-1][ant.getValue()-1])
          if self.en(d1, permitidos_drop) and self.en(d2, permitidos_drop) and self.en(a1, permitidos_add):
            f1 = vertices[(list_ind_v[ind]-2)%grado]
            f2 = vertices[(list_ind_v[ind]+2)%grado]
            c1 = Arista(f1, ant, self._mDist[f1.getValue()-1][ant.getValue()-1])
            c2 = Arista(f2, pos, self._mDist[f2.getValue()-1][pos.getValue()-1])
            try:
              aux.append(lista_aristas.pop(lista_aristas.index(c1)))
            except:
              pass
              # print(f"{c1} no estaba en lista_aristas")
              
            try:
              aux.append(lista_aristas.pop(lista_aristas.index(c2)))
            except:
              pass
              # print(f"{c2} no estaba en lista_aristas")
            while len(lista_aristas)>0 and not encontradas:
              ind_a = randint(0,len(lista_aristas)-1)
              d3 = lista_aristas[ind_a]
              a2 = Arista(med, lista_aristas[ind_a].getOrigen(), self._mDist[med.getValue()-1][lista_aristas[ind_a].getOrigen().getValue()-1])
              a3 = Arista(med, lista_aristas[ind_a].getDestino(), self._mDist[med.getValue()-1][lista_aristas[ind_a].getDestino().getValue()-1])
              if self.en(d3, permitidos_drop) and self.en(a2 , permitidos_add) and self.en(a3, permitidos_add):
                encontradas = True
                drop.append(d1)
                drop.append(d2)
                drop.append(d3)
                add.append(a1)
                add.append(a2)
                add.append(a3)
                # print(f"list_ind_v[ind]: {list_ind_v[ind]}")
                # print(f"add: {add}")
                # print(f"drop: {drop}")    
              else:
                aux.append(lista_aristas.pop(ind_a))
                # print(f"lista_aristas dentro while: {lista_aristas}")
            if not encontradas:
              lista_aristas = lista_aristas + aux
              list_ind_v.pop(ind)
          else:
            # print("vertice no sirve, cambiando a otro")
            lista_aristas = lista_aristas + aux
            list_ind_v.pop(ind)
            # ind = randint(0,len(list_ind_v)-1)
        if encontradas:
          secuencia = vertices[:]
          v = secuencia.pop(list_ind_v[ind])
          insert1 = secuencia.index(d3.getOrigen())
          insert2 = secuencia.index(d3.getDestino())
          if list_ind_v[ind] != 0:
            if insert1 < insert2:
              secuencia.insert(insert2,v)
            else:
              secuencia.insert(insert1,v)
          else:
            aux_l = []
            aux_l.append(v)
            if insert1 < insert2:
              aux_l = aux_l + secuencia[insert2:]
              aux_l = aux_l + secuencia[0:insert2]
            else:
              aux_l = aux_l + secuencia[insert1:]
              aux_l = aux_l + secuencia[0:insert1]
            secuencia = aux_l

          # print(f"costo: {costo}")
          for a in drop:
            costo -= a.getPeso()
            # print(f"costo: {costo+a.getPeso()} - {a.getPeso()} = {costo}")
          for a in add:
            costo += a.getPeso()
        else:
          print("Se probaron todos los vértices sin éxito 3opt")
          secuencia = vertices
      else:
        print("CUIDADO!! TENURE MUY ALTO 3opt")
      
      
      # asd = self.calcCosto(secuencia)
      # if costo != asd:
      #   print(F"ERROR DE COSTO costo: {costo}, asd: {asd}")
        # print(f"costo: {costo-a.getPeso()} + {a.getPeso()} = {costo}")
      # print(f"costo final: {costo}")
      # print(f"swap 3opt tarda: {fin} seg")
      # print(f"secuencia: {secuencia}")
      # print("FIN EJECUCIÓN 3opt")
      return round(costo,2), secuencia, add, drop

    def complemento(self, aristas, permitidos):
      AristasNuevas = []
      claves = [hash(a) for a in permitidos]
      dictA = dict(zip(claves,permitidos))
      for EP in aristas:
        h = hash(EP)
        hInverso = hash(EP.getAristaInvertida())
        try:
          arista = dictA[h]
        except KeyError:
          arista = None
        try:
          aristaInv = dictA[hInverso]
        except KeyError:
          aristaInv = None
        if arista is None and aristaInv is None:
          AristasNuevas.append(EP)
      return AristasNuevas

    def swap_3optV2(self, addT: list, dropT: list):
      # print("EMPIEZA ACA")
      drop = []
      add = []

      costo = self.__costoAsociado
      # print(f"vertices: {self._V}")
      ar_drop = []
      # print(addT)
      # print(dropT)
      for x in dropT:
        elem = x.getElemento()
        ar_drop.append(elem)
      lista_aristas = self.complemento(self._A, ar_drop)

      # print(f"lista_aristas: {lista_aristas}")
      if len(lista_aristas) >= 3:

        vertices = self._V

        grado = len(vertices)
        list_ind_v = list(range(grado))
        encontradas = False
        iter = 0
        while not encontradas and len(list_ind_v)>0:
          iter += 1
          if iter > grado:
            print("ESTANCADO 3opt")
            iter = 0
            # list_ind_v = []
          ind = randint(0,len(list_ind_v)-1)
          aux = [] # para ir guardando aristas de lista_aristas
          ant = vertices[(list_ind_v[ind]-1)%grado]
          med = vertices[list_ind_v[ind]]
          # print(f"med vertice: {med}")
          pos = vertices[(list_ind_v[ind]+1)%grado]
          d1 = Tabu(Arista(ant, med, self._mDist[ant.getValue()-1][med.getValue()-1]),0)
          d2 = Tabu(Arista(pos, med, self._mDist[pos.getValue()-1][med.getValue()-1]),0)
          a1 = Tabu(Arista(ant, pos, self._mDist[pos.getValue()-1][ant.getValue()-1]),0)
          if d1 not in dropT and d2 not in dropT and a1 not in addT:
            f1 = vertices[(list_ind_v[ind]-2)%grado]
            f2 = vertices[(list_ind_v[ind]+2)%grado]
            c1 = Arista(f1, ant, self._mDist[f1.getValue()-1][ant.getValue()-1])
            c2 = Arista(f2, pos, self._mDist[f2.getValue()-1][pos.getValue()-1])
            try:
              aux.append(lista_aristas.pop(lista_aristas.index(c1)))
            except:
              pass
              # print(f"{c1} no estaba en lista_aristas")
            try:
              aux.append(lista_aristas.pop(lista_aristas.index(d1.getElemento())))
            except:
              pass
            try:
              aux.append(lista_aristas.pop(lista_aristas.index(d2.getElemento())))
            except:
              pass
            try:
              aux.append(lista_aristas.pop(lista_aristas.index(c2)))
            except:
              pass
              # print(f"{c2} no estaba en lista_aristas")
            while len(lista_aristas)>0 and not encontradas:
              ind_a = randint(0,len(lista_aristas)-1)
              d3 = Tabu(lista_aristas[ind_a], 0)
              a2 = Tabu(Arista(med, lista_aristas[ind_a].getOrigen(), self._mDist[med.getValue()-1][lista_aristas[ind_a].getOrigen().getValue()-1]),0)
              a3 = Tabu(Arista(med, lista_aristas[ind_a].getDestino(), self._mDist[med.getValue()-1][lista_aristas[ind_a].getDestino().getValue()-1]),0)
              if d3 not in dropT and a2 not in addT and a3 not in addT:
                encontradas = True
                drop.append(d1)
                drop.append(d2)
                drop.append(d3)
                add.append(a1)
                add.append(a2)
                add.append(a3)
                # print(f"add: {add}")
                # print(f"drop: {drop}")
              else:
                aux.append(lista_aristas.pop(ind_a))
                # print(f"lista_aristas dentro while: {lista_aristas}")
            if not encontradas:
              lista_aristas = lista_aristas + aux
              list_ind_v.pop(ind)
          else:
            # print("vertice no sirve, cambiando a otro")
            lista_aristas = lista_aristas + aux
            list_ind_v.pop(ind)
        if encontradas:
          secuencia = vertices[:]
          v = secuencia.pop(list_ind_v[ind])
          # print(f"v: {v}")
          ar = d3.getElemento()
          # print(f"origen: {ar.getOrigen()}")
          # print(f"destino: {ar.getDestino()}")
          # print(f"secuencia: {secuencia}")
          insert1 = secuencia.index(ar.getOrigen())
          insert2 = secuencia.index(ar.getDestino())
          if list_ind_v[ind] != 0:
            if insert1 < insert2:
              secuencia.insert(insert2,v)
            else:
              secuencia.insert(insert1,v)
          else:
            aux_l = []
            aux_l.append(v)
            if insert1 < insert2:
              aux_l = aux_l + secuencia[insert2:]
              aux_l = aux_l + secuencia[0:insert2]
            else:
              aux_l = aux_l + secuencia[insert1:]
              aux_l = aux_l + secuencia[0:insert1]
            secuencia = aux_l
          # for j in drop:
          #   wv = j.getElemento()
          #   costo -= wv.getPeso()
          # for k in add:
          #   vw = k.getElemento()
          #   costo += vw.getPeso()
          costo = self.calcCosto(secuencia)
        else:
          print("Se probaron todos los vértices sin éxito")
          secuencia = vertices
      else:
        print("CUIDADO!! TENURE MUY ALTO 3opt")
        secuencia = self._V
      # self.cargarDesdeSecuenciaDeVertices(secuencia)
      # asd = self.calcCosto(secuencia)
      # if costo != asd:
      #   print("ERROR DE COSTO")
      #   print(f"costo: {costo} y asd: {self.__costoAsociado}")
      #   print(f"add: {add}")
      #   print(f"drop: {drop}")
      # print(f"secuencia: {secuencia}")
      return round(costo,2), secuencia, add, drop

    def calcCosto(self, vertices: list):
      ind = 0
      acu = 0
      while ind < len(vertices)-1:
        acu += self._mDist[vertices[ind].getValue()-1][vertices[ind+1].getValue()-1]
        ind += 1
      return acu + self._mDist[vertices[0].getValue()-1][vertices[-1].getValue()-1]

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