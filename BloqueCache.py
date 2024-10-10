# ------------------------------------------------------
# Implementacion de un bloque de la cache
# Puede tener más de una palabra
# Los datos se almacenan como un vector de dimensión igual al número de palabras que puede almacenar el bloque
# Cada bloque tiene: bit de validez, etiqueta y vector de datos
# ------------------------------------------------------
import numpy as nn


class BloqueCache:
    # Constructor
    def __init__(self, numero_palabras_bloque):
        self.numero_palabras_bloque = numero_palabras_bloque
        self.bit_validez = 0
        self.etiqueta = ""
        self.datos = nn.zeros(self.numero_palabras_bloque)

    def get_bit_validez(self):
        return self.bit_validez

    def get_etiqueta(self):
        return self.etiqueta

    # LEER
    # Si el bit está a cero o la etiqueta es diferente, es un fallo
    # Si el bit está a uno y la etiqueta es la misma, es un acierto
    # Devuelve acierto = 1 si es un acierto, o = 0 si es un fallo, y el vector de datos completo.
    # Si es un fallo devuelve el vector de datos vacio
    def leer(self, etiqueta):
        datos = []
        if self.bit_validez == 0 or self.etiqueta != etiqueta:
            acierto = 0
        else:
            acierto = 1
            datos = self.datos

        return acierto, datos

    # ESCRIBIR
    # Escribe los datos (el vector completo) en el bloque
    # Actualiza el bit de validez y la etiqueta
    def escribir(self, etiqueta, datos):
        self.bit_validez = 1
        self.etiqueta = etiqueta
        self.datos = datos
