# ------------------------------------------------------
# Implementacion de un conjunto (o línea) de la cache
# Puede tener más de un bloque
# Cada conjunto contiene un vector de Bloques.
# Cada conjunto está identificado por el indice.
# vtiempo se usa para saber cual es el bloque que hace más tiempo que no se accede.
# El más reciente será el que tenga vtiempo más pequeño.
# El que hace más tiempo que fue accedido será el que tenga el valor máximo.
# ------------------------------------------------------
import math

from BloqueCache import BloqueCache
from Cola import Cola
from utils import dec2bin


class ConjuntoCache:
    # Constructor
    def __init__(self, indice, numero_bloques, numero_palabras_bloque):
        self.indice = indice
        self.numero_bloques = numero_bloques
        self.numero_palabras_bloque = numero_palabras_bloque
        self.bloques = []
        self.cola = Cola(self.numero_bloques)
        self.numero_bits_bloque = int(math.log(self.numero_bloques, 2))

        # Se inicializa con numero_bloques bloques vacios (con el bit de validez a 0)
        for i in range(self.numero_bloques):
            bloque = BloqueCache(self.numero_palabras_bloque)
            self.bloques.append(bloque)

    # LEER
    # Busca el bloque con la etiqueta especificada. Si lo encuentra devuelve acierto==1 y el vector de datos
    # Además actualiza el contador de tiempo.
    # Si no encuentra es un fallo (acierto==0). Devuelve el vector vacio
    def leer(self, etiqueta):
        i = 0
        acierto = 0
        datos = []
        while i < self.numero_bloques and acierto == 0:
            acierto, datos = self.bloques[i].leer(etiqueta)
            i += 1

        # Si hay acierto actualiza la Cola
        if acierto:
            self.cola.mover_al_final(i - 1)

        return acierto, datos

    # ESCRIBIR
    # Busca el primer bloque vacio (bit validez == 0).
    # Si están todos ocupados reemplaza el que más tiempo hace que no se ha accedido (máximo en vtiempo)
    # datos es un vector
    def escribir(self, etiqueta, datos):
        i = 0
        while i < self.numero_bloques and self.bloques[i].get_bit_validez() == 1:
            i += 1

        if i < self.numero_bloques:
            # Escribir en el primer bloque vacio (el i)
            self.bloques[i].escribir(etiqueta, datos)
            self.cola.insertar_final(i)
        else:
            # Como están todos ocupados, se reemplaza por el que hace más tiempo que no ha sido accedido
            # Será el primero en la cola
            # El que se insertá será ahora el último
            posicion_a_reemplazar = int(self.cola.primero())
            self.cola.insertar_final(posicion_a_reemplazar)
            self.bloques[posicion_a_reemplazar].escribir(etiqueta, datos)
            print(">>> Se reemplaza el bloque " + dec2bin(posicion_a_reemplazar, self.numero_bits_bloque))

