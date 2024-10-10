# ----------------------------------------
# Memoria Cache
# Para almacenar los conjuntos se usa un vector
# Funciona para cual tipo de cache: correspondencia directa, totalmente asociativa o asociativa por conjuntos
# Será correspondencia directa cuando numero_conjuntos>1 y numero_bloques_conjunto==1
# Será totalmente asociativa cuando numero_conjuntos==1
# En otro caso es asociativa por conjuntos
# ----------------------------------------
import math

from ConjuntoCache import ConjuntoCache
from utils import dec2bin, bin2dec, numero_hex2bin, fancy_binario


class MemoriaCache:
    # Constructor
    def __init__(self, bits_direccion, numero_conjuntos, numero_bloques_conjunto, numero_palabras_bloque):
        self.traza = False
        self.bits_direccion = bits_direccion
        self.numero_conjuntos = numero_conjuntos
        self.numero_bloques_conjunto = numero_bloques_conjunto
        self.numero_palabras_bloque = numero_palabras_bloque
        self.conjuntos = []

        # creamos los conjuntos
        # Se inicializa con numero_conjuntos conjunto con numero_bloques_conjunto bloques vacios
        # (con el bit de validez a 0)
        for i in range(self.numero_conjuntos):
            conjunto = ConjuntoCache(i, numero_bloques_conjunto, numero_palabras_bloque)
            self.conjuntos.append(conjunto)

        # Cálculo de los bits en los que se debe descomponer la dirección de memoria para extraer los elementos
        if self.numero_palabras_bloque == 1:
            self.primer_bit_posicion_en_bloque = -1
            self.ultimo_bit_posicion_en_bloque = -1
        else:
            numero_bits_posicion_en_bloque = int(math.log(self.numero_palabras_bloque, 2))
            self.ultimo_bit_posicion_en_bloque = self.bits_direccion - 1
            self.primer_bit_posicion_en_bloque = self.ultimo_bit_posicion_en_bloque - numero_bits_posicion_en_bloque + 1

        if self.numero_conjuntos == 1:
            # Totalmente asociativa
            self.primer_bit_indice = -1
            self.ultimo_bit_indice = -1
            self.primer_bit_etiqueta = 0
            if self.primer_bit_posicion_en_bloque == -1:
                self.ultimo_bit_etiqueta = self.bits_direccion -1
            else:
                self.ultimo_bit_etiqueta = self.primer_bit_posicion_en_bloque - 1
        else:
            # Correspondencia directa o asociativa por conjuntos
            numero_bits_indice = int(math.log(self.numero_conjuntos, 2))
            if self.primer_bit_posicion_en_bloque == -1:
                self.ultimo_bit_indice = self.bits_direccion - 1
            else:
                self.ultimo_bit_indice = self.primer_bit_posicion_en_bloque - 1
            self.primer_bit_indice = self.ultimo_bit_indice - numero_bits_indice + 1

            self.primer_bit_etiqueta = 0
            self.ultimo_bit_etiqueta = self.primer_bit_indice - 1

    # Segmenta la direccion en etiqueta, indice_bloque, posicion_en_bloque, posicion_en_palabra
    def segmentar_direccion_memoria(self, direccion_hex):
        direccion_binario = numero_hex2bin(direccion_hex)

        # Los dos ultimos bits son la posicion en palabra (asumimos direcciones de 32 bits)
        if self.primer_bit_posicion_en_bloque == -1:
            posicion_en_bloque = ""
        else:
            posicion_en_bloque = direccion_binario[self.primer_bit_posicion_en_bloque:self.ultimo_bit_posicion_en_bloque + 1]

        if self.primer_bit_indice == -1:
            indice_conjunto = ""
        else:
            indice_conjunto = direccion_binario[self.primer_bit_indice:self.ultimo_bit_indice + 1]

        etiqueta = direccion_binario[self.primer_bit_etiqueta:self.ultimo_bit_etiqueta + 1]

        return etiqueta, indice_conjunto, posicion_en_bloque

    # LEER
    # A partir de la direccion y teniendo en cuenta el tipo, se busca en la caché.
    # Si está es un acierto y de vevuelve el vector de datos complero
    # Si no está es un fallo y devuelve un vector vacio
    def leer(self,direccion_memoria_hex):
        etiqueta, indice_conjunto, posicion_en_bloque = self.segmentar_direccion_memoria(direccion_memoria_hex)

        if self.traza:
            print(">>> Etiqueta: " + fancy_binario(etiqueta) +
                  ", Índice conjunto: " + fancy_binario(indice_conjunto) +
                  ", Posición en bloque: " + fancy_binario(posicion_en_bloque))

        if indice_conjunto == "":
            i_conjunto = 0
        else:
            i_conjunto = bin2dec(indice_conjunto)

        acierto, datos = self.conjuntos[i_conjunto].leer(etiqueta)
        return acierto, datos, posicion_en_bloque

    # ESCRIBIR
    # A partir de la dirección y teniendo en cuenta el tipo, escribe en el sitio correcto
    def escribir(self, direccion_memoria_hex, datos):
        etiqueta, indice_conjunto, posicion_en_bloque = self.segmentar_direccion_memoria(direccion_memoria_hex)

        if indice_conjunto == "":
            i_conjunto = 0
        else:
            i_conjunto = bin2dec(indice_conjunto)

        self.conjuntos[i_conjunto].escribir(etiqueta, datos)
        if self.traza:
            print(">>> Se escribe el contenido de la dirección 0x" + direccion_memoria_hex + " en el conjunto: " +
                  indice_conjunto)

        # Imprime el tipo de cache que es y el numero de palabras que puede almacenar

    def averiguar_tipo_cache(self):
        if self.numero_bloques_conjunto == 1:
            tipo_cache = "Correspondencia directa"
        elif self.numero_conjuntos == 1:
            tipo_cache = "Totalmente asociativa"
        else:
            tipo_cache = "Asociativa"

        print("\n")
        print("--------------------------------------------------------------------")
        print("Memoria Caché                      -> " + tipo_cache)
        print("Número de conjuntos                -> " + str(self.numero_conjuntos))
        print("Número de bloques en cada conjunto -> " + str(self.numero_bloques_conjunto))
        print("Número de palabras en cada bloque  -> " + str(self.numero_palabras_bloque))
        print("Esta cache puede almacenar         -> " + str(
            self.numero_conjuntos * self.numero_bloques_conjunto * self.numero_palabras_bloque) + " palabras")
        print("--------------------------------------------------------------------")
        print("Los bits de la etiqueta son                   -> [" +
              str(self.bits_direccion - 1 - self.primer_bit_etiqueta) + ", " +
              str(self.bits_direccion - 1 - self.ultimo_bit_etiqueta) + "]")
        if self.numero_conjuntos == 1:
            print("Los bits del índice son                       -> [-1,-1]")
        else:
            print("Los bits del índice son                       -> [" +
                  str(self.bits_direccion - 1 - self.primer_bit_indice) + ", " +
                  str(self.bits_direccion - 1 - self.ultimo_bit_indice) + "]")
        if self.numero_palabras_bloque == 1:
            print("Los bits de la posición dentro del bloque son -> [-1,-1]")
        else:
            print("Los bits de la posición dentro del bloque son -> [" +
                  str(self.bits_direccion - 1 - self.primer_bit_posicion_en_bloque) + ", " +
                  str(self.bits_direccion - 1 - self.ultimo_bit_posicion_en_bloque) + "]")

        print("--------------------------------------------------------------------")

    # Mostrar el contenido de la caché
    def mostrar(self):
        print("\n")
        print("----------------------")
        print("    MEMORIA CACHÉ     ")
        print("----------------------")

        numero_bits_conjunto = int(math.log(self.numero_conjuntos, 2))
        numero_bits_bloque = int(math.log(self.numero_bloques_conjunto, 2))
        i = 0
        for conjunto in self.conjuntos:
            print("Conjunto: " + dec2bin(i, numero_bits_conjunto))
            j = 0
            for bloque in conjunto.bloques:
                print("  Bloque: " + dec2bin(j, numero_bits_bloque) +
                      " -> Bit Validez: [" + str(bloque.get_bit_validez()) +
                      "], Etiqueta: [" + fancy_binario(bloque.get_etiqueta()) + "]")
                k = 0
                print("    --------")
                for palabra in bloque.datos:
                    print("    - " + str(palabra) + " -")
                    k += 1
                print("    --------")
                j += 1
            i += 1

    # Activar la traza para mostrar mensajes sobre el funcionamiento interno
    def activar_traza(self):
        self.traza = True
