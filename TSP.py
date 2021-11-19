from Grafo import Grafo

class TSP(object):
    def __init__(self, M: list, nroIntercambios, tenureADD, tenureDROP):
        self._G = Grafo (M)
        self.__soluciones = []
        self.__nroIntercambios=nroIntercambios*2    #corresponde al nro de vertices los intercambios. 1intercambio => 2 vertices
        self.__opt = opt
        self.__optimo = optimo
        self.__tenureADD =  tenureADD
        self.__tenureMaxADD = int(tenureADD*1.7)
        self.__tenureDROP =  tenureDROP
        self.__tenureMaxDROP = int(tenureDROP*1.7)
        self.__txt = clsTxt(str(nombreArchivo))
        self.__tiempoMaxEjec = float(tiempoEjec)
        self.__frecMatriz = []
        for i in range(0, len(self._G.getMatriz())):
            fila = []
            for j in range(0, len(self._G.getMatriz())):
                fila.append(0)
                j
            self.__frecMatriz.append(fila)
            i
        self.tabuSearch(solInicial)

    def printG(self):
        print(self._G)