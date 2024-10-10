# ---------------------------------------------------------
# Implementa una cola FIFO básica
# ---------------------------------------------------------
import numpy as nn


class Cola:
    def __init__(self,numero_elementos):
        self.numero_elementos = numero_elementos
        self.cola = nn.zeros(self.numero_elementos)

    def insertar_final(self, nuevo):
        for i in range(self.numero_elementos-1):
            self.cola[i] = self.cola[i+1]

        self.cola[self.numero_elementos-1] = nuevo

    def mover_al_final(self, elemento):
        for i in range(self.numero_elementos - 1):
            if self.cola[i] == elemento:
                j = i
                while j < self.numero_elementos - 1:
                    self.cola[j] = self.cola[j+1]
                    j += 1
        self.cola[self.numero_elementos - 1] = elemento

    def primero(self):
        return self.cola[0]
