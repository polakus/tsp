from Vertice import Vertice

class Arista(object):
    def __init__(self,origen,destino, peso):
        self._origen = origen
        self._destino = destino
        self._peso = peso
        self._frecuencia = 0
    
    def incFrecuencia(self):
        self._frecuencia+=1

    def getFrecuencia(self):
        return self._frecuencia

    def setOrigen(self, origen):
        self._origen = origen
            
    def setDestino(self, destino):
        self._destino = destino

    def setPeso(self, peso):
        self._peso = peso
    
    def getOrigen(self):
        return self._origen

    def getDestino(self):
        return self._destino

    def getPeso(self):
        return self._peso

    def tieneOrigen(self,V):
        return (V == self.getOrigen())
    
    def tieneDestino(self,V):
        return (V == self.getDestino())

    def mismoVertice(self, A):
        return (self._origen == A.getOrigen() or self._origen == A.getDestino() or self._destino == A.getOrigen() or self._destino == A.getDestino())
    
    def getAristaInvertida(self):
            return Arista(self._destino, self._origen, self._peso)
    
    def __eq__(self, A):
        eq = ((self.getOrigen() == A.getOrigen()) and (self.getDestino() == A.getDestino())) or ((self.getOrigen() == A.getDestino()) and (self.getDestino() == A.getOrigen()))
        return ((self.__class__ == A.__class__) and eq)
        
    def __str__(self):
        return "(" + str(self._origen) + "," + str(self._destino) + "," + str(self._peso) + ")"

    def __repr__(self):
        return str(self)

    def __hash__(self):
            origen = self._origen.getValue()
            destino = self._destino.getValue()
            return int(((origen+destino)*(origen+destino+1))/2+destino)