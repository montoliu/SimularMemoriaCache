# -----------------------------------------------------
# Simulador memoria chaché
# Simula únicamene lecturas
# -----------------------------------------------------
# En este simulador se asume que siempre las direcciones de memoria tienen 32 bits
# y el tamaño de palabra también es de 32 bits (4 bytes)
# -----------------------------------------------------
import math
import numpy as nn

# ------------------------------------------------------
# Convierte un número en binario a decimal
# El número binario es un string e.g. "101"
# ------------------------------------------------------
def bin2dec(numero_binario):
    numero_decimal = 0

    j = len(numero_binario) - 1
    for i in range(len(numero_binario)):
        numero_decimal = numero_decimal + 2 ** i * int(numero_binario[j])
        j -= 1
    return numero_decimal


# ------------------------------------------------------
# Convierte un número decimal a binario
# El binario es un string e.g. "101"
# Se usa la función bin que transforma e.g. 3 en "0b11".
# En esta función se quita el "0b" para dejar el "11"
# ------------------------------------------------------
def dec2bin(numero_decimal, numero_bits):
    numero_binario  = bin(numero_decimal)
    numero_binario = numero_binario[2:len(numero_binario)]  # quita el "0b" del principio

    while len(numero_binario) < numero_bits:
        numero_binario = "0" + numero_binario
    return numero_binario


# ------------------------------------------------------
# Convierte un dígito en hexadecimal a cuatro dígitos en binario
# Ambos son strings
# ------------------------------------------------------
def digito_hex2bin(digito_hex):
    if digito_hex == "0":
        return "0000"
    elif digito_hex == "1":
        return "0001"
    elif digito_hex == "2":
        return "0010"
    elif digito_hex == "3":
        return "0011"
    elif digito_hex == "4":
        return "0100"
    elif digito_hex == "5":
        return "0101"
    elif digito_hex == "6":
        return "0110"
    elif digito_hex == "7":
        return "0111"
    elif digito_hex == "8":
        return "1000"
    elif digito_hex == "9":
        return "1001"
    elif digito_hex == "A":
        return "1010"
    elif digito_hex == "B":
        return "1011"
    elif digito_hex == "C":
        return "1100"
    elif digito_hex == "D":
        return "1101"
    elif digito_hex == "E":
        return "1110"
    elif digito_hex == "F":
        return "1111"


# ------------------------------------------------------
# Convierte cuatro digitos en binario a un digito en hexadecimal
# Ambos son strings
# ------------------------------------------------------
def digito_bin2hex(digito_bin):
    if digito_bin == "0000":
        return "0"
    elif digito_bin == "0001":
        return "1"
    elif digito_bin == "0010":
        return "2"
    elif digito_bin == "0011":
        return "3"
    elif digito_bin == "0100":
        return "4"
    elif digito_bin == "0101":
        return "5"
    elif digito_bin == "0110":
        return "6"
    elif digito_bin == "0111":
        return "7"
    elif digito_bin == "1000":
        return "8"
    elif digito_bin == "1001":
        return "9"
    elif digito_bin == "1010":
        return "A"
    elif digito_bin == "1011":
        return "B"
    elif digito_bin == "1100":
        return "C"
    elif digito_bin == "1101":
        return "D"
    elif digito_bin == "1110":
        return "E"
    elif digito_bin == "1111":
        return "F"


# ------------------------------------------------------
# Convierte un número binario a hexadecimal
# Ambos son strings
# va agrupando de 4 en 4 por la izquierda
# ------------------------------------------------------
def numero_bin2hex(numero_binario):
    n = numero_binario
    #añadir ceros a la izquierda para que sea el número de dígitos sea multiplo de 4
    while (len(n)%4 > 0):
        n = "0" + n

    numero_hex  = ""
    pos_final   = len(n)
    pos_inicial = pos_final - 4

    while (pos_inicial >= 0):
        numero_hex  = digito_bin2hex(n[pos_inicial:pos_final]) + numero_hex
        pos_final   = pos_final - 4
        pos_inicial = pos_final - 4

    return numero_hex


# ------------------------------------------------------
# Convierte un número en hexadecimal a su correspondiente en binario
# Ambos números son strings
# ------------------------------------------------------
def numero_hex2bin(numero_hex):
    numero_binario = ""
    for i in range(len(numero_hex)):
        numero_binario = numero_binario + digito_hex2bin(numero_hex[i])
    return numero_binario


# ------------------------------------------------------
# Implementacion de un bloque de la cache
# Puede tener más de una palabra
# Los datos se almacenan como un vector de dimensión igual al número de palabras que puede almacenar el bloque
# Cada bloque tiene: bit de validez, etiqueta y vector de datos
# ------------------------------------------------------
class BloqueCache:
    # Constructor
    def __init__(self, numero_palabras_bloque):
        self.numero_palabras_bloque = numero_palabras_bloque
        self.bit_validez            = 0
        self.etiqueta               = ""
        self.datos                  = nn.zeros(self.numero_palabras_bloque)

    def getBitValidez(self):
        return self.bit_validez

    def getEtiqueta(self):
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
            acierto              = 1
            datos                = self.datos

        return acierto, datos

    # ESCRIBIR
    # Escribe los datos (el vector completo) en el bloque
    # Actualiza el bit de validez y la etiqueta
    def escribir(self, etiqueta, datos):
        self.bit_validez    = 1
        self.etiqueta       = etiqueta
        self.datos          = datos

# ------------------------------------------------------
# Implementacion de un conjunto de la cache
# Puede tener más de un bloque
# Cada conjunto contiene un vector de Bloques.
# Cada conjunto está identificado por el indice.
# vtiempo se usa para saber cual es el bloque que hace más tiempo que no se accede.
# El más reciente será el que tenga vtiempo más pequeño.
# El que hace más tiempo que fue accedido será el que tenga el valor máximo.
# ------------------------------------------------------
class ConjuntoCache:
    # Constructor
    def __init__(self, indice, numero_bloques, numero_palabras_bloque):
        self.indice                 = indice
        self.numero_bloques         = numero_bloques
        self.numero_palabras_bloque = numero_palabras_bloque
        self.bloques                = []
        self.vtiempo                = nn.zeros(self.numero_bloques)
        self.numero_bits_bloque     = int(math.log(self.numero_bloques,2))

        # Se inicializa con numero_bloques bloques vacios (con el bit de validez a 0)
        for i in range(self.numero_bloques):
            bloque = BloqueCache(self.numero_palabras_bloque)
            self.bloques.append(bloque)


    # LEER
    # Busca el bloque con la etiqueta especificada. Si lo encuentra devuelve acierto==1 y el vector de datos
    # Además actualiza el contador de tiempo.
    # Si no encuentra es un fallo (acierto==0). Devuelve el vector vacio
    def leer(self, etiqueta):
        i       = 0
        acierto = 0
        datos    = []
        while i < self.numero_bloques and acierto == 0:
            acierto, datos  = self.bloques[i].leer(etiqueta)
            i              += 1

        # Si hay acierto actualiza vtiempo incrementando en 1 el resto
        # El actual es el i-1
        if acierto == 1:
            for j in range(self.numero_bloques):
                if j != i - 1:
                    self.vtiempo[j] += 1

        return acierto, datos


    # ESCRIBIR
    # Busca el primer bloque vacio (bit validez == 0).
    # Si están todos ocupados reemplaza el que más tiempo hace que no se ha accedido (máximo en vtiempo)
    # datos es un vector
    def escribir(self, etiqueta, datos):
        i = 0
        while i < self.numero_bloques and self.bloques[i].getBitValidez() == 1:
            i += 1

        if i < self.numero_bloques:
            # Escribir en el primer bloque vacio (el i)
            self.bloques[i].escribir(etiqueta, datos)
        else:
            # Como están todos ocupados, se reemplaza por el que hace más tiempo que no ha sido accedido
            # Será el máximo en vtiempo
            posicion_a_reemplazar = nn.argmax(self.vtiempo)
            self.bloques[posicion_a_reemplazar].escribir(etiqueta, datos)
            self.vtiempo[posicion_a_reemplazar] = 0
            print(">>> Se reemplaza el bloque " + dec2bin(posicion_a_reemplazar,self.numero_bits_bloque))


# ----------------------------------------
# Memoria Cache
# Para almacenar los conjuntos se usa un vector
# Funciona para cual tipo de cache: correspondencia directa, totalmente asociativa o asociativa por conjuntos
# Será correspondencia directa cuando numero_conjuntos>1 y numero_bloques_conjunto==1
# Será totalmente asociativa cuando numero_conjuntos==1
# En otro caso es asociativa por conjuntos
# ----------------------------------------
class MemoriaCache:
    # Constructor
    def __init__(self, numero_conjuntos, numero_bloques_conjunto, numero_palabras_bloque):
        self.traza                   = False
        self.numero_conjuntos        = numero_conjuntos
        self.numero_bloques_conjunto = numero_bloques_conjunto
        self.numero_palabras_bloque  = numero_palabras_bloque
        self.conjuntos               = []

        # creamos los conjuntos
        # Se inicializa con numero_conjuntos conjunto con numero_bloques_conjunto bloques vacios (con el bit de validez a 0)
        for i in range(self.numero_conjuntos):
            conjunto = ConjuntoCache(i, numero_bloques_conjunto, numero_palabras_bloque)
            self.conjuntos.append(conjunto)

        # Cálculo de los bits en los que se debe descomponer la dirección de memoria para extraer los elementos
        if self.numero_palabras_bloque == 1:
            self.primer_bit_posicion_en_bloque = -1
            self.ultimo_bit_posicion_en_bloque = -1
        else:
            numero_bits_posicion_en_bloque     = int(math.log(self.numero_palabras_bloque, 2))
            self.ultimo_bit_posicion_en_bloque = 29
            self.primer_bit_posicion_en_bloque = self.ultimo_bit_posicion_en_bloque - numero_bits_posicion_en_bloque + 1

        if self.numero_conjuntos == 1:
            # Totalmente asociativa
            self.primer_bit_indice   = -1
            self.ultimo_bit_indice   = -1
            self.primer_bit_etiqueta = 0
            if self.primer_bit_posicion_en_bloque == -1:
                self.ultimo_bit_etiqueta = 29
            else:
                self.ultimo_bit_etiqueta = self.primer_bit_posicion_en_bloque - 1
        else:
            # Correspondencia directa o asociativa por conjuntos
            numero_bits_indice = int(math.log(self.numero_conjuntos, 2))
            if self.primer_bit_posicion_en_bloque == -1:
                self.ultimo_bit_indice = 29
            else:
                self.ultimo_bit_indice = self.primer_bit_posicion_en_bloque - 1
            self.primer_bit_indice = self.ultimo_bit_indice - numero_bits_indice + 1

            self.primer_bit_etiqueta = 0
            self.ultimo_bit_etiqueta = self.primer_bit_indice - 1


    # Segmenta la direccion en etiqueta, indice_bloque, posicion_en_bloque, posicion_en_palabra
    def segmentarDireccionMemoria(self, direccion_hex):
        direccion_binario = numero_hex2bin(direccion_hex)

        # Los dos ultimos bits son la posicion en palabra (asumimos direcciones de 32 bits)
        posicion_en_palabra = direccion_binario[30:32]
        if self.primer_bit_posicion_en_bloque == -1:
            posicion_en_bloque = ""
        else:
            posicion_en_bloque  = direccion_binario[self.primer_bit_posicion_en_bloque:self.ultimo_bit_posicion_en_bloque + 1]

        if self.primer_bit_indice == -1:
            indice_conjunto = ""
        else:
            indice_conjunto = direccion_binario[self.primer_bit_indice:self.ultimo_bit_indice + 1]

        etiqueta = direccion_binario[self.primer_bit_etiqueta:self.ultimo_bit_etiqueta + 1]

        return etiqueta, indice_conjunto, posicion_en_bloque, posicion_en_palabra


    # LEER
    # A partir de la direccion y teniendo en cuenta el tipo, se busca en la caché.
    # Si está es un acierto y de vevuelve el vector de datos complero
    # Si no está es un fallo y devuelve un vector vacio
    def leer(self,direccion_memoria_hex):
        etiqueta, indice_conjunto, posicion_en_bloque, posicion_en_palabra = self.segmentarDireccionMemoria(direccion_memoria_hex)

        if self.traza:
            print(">>> Etiqueta: "          + etiqueta           +
                  ", Índice conjunto: "     + indice_conjunto    +
                  ", Posición en bloque: "  + posicion_en_bloque +
                  ", Posición en palabra: " + posicion_en_palabra)

        if indice_conjunto == "":
            i_conjunto = 0
        else:
            i_conjunto = bin2dec(indice_conjunto)

        acierto, datos = self.conjuntos[i_conjunto].leer(etiqueta)
        return acierto, datos, posicion_en_bloque

    # ESCRIBIR
    # A partir de la dirección y teniendo en cuenta el tipo, escribe en el sitio correcto
    def escribir(self, direccion_memoria_hex, datos):
        etiqueta, indice_conjunto, posicion_en_bloque, posicion_en_palabra = self.segmentarDireccionMemoria(direccion_memoria_hex)

        if indice_conjunto == "":
            i_conjunto = 0
        else:
            i_conjunto = bin2dec(indice_conjunto)

        self.conjuntos[i_conjunto].escribir(etiqueta, datos)
        if self.traza:
            print(">>> Se escribe el contenido de la dirección 0x" + direccion_memoria_hex + " en el conjunto: " + indice_conjunto)

        # Imprime el tipo de cache que es y el numero de palabras que puede almacenar

    def averiguarTipoCache(self):
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
        print("Los bits de la etiqueta son                   -> [" + str(self.primer_bit_etiqueta) + ", " + str(
            self.ultimo_bit_etiqueta) + "]")
        print("Los bits del índice son                       -> [" + str(self.primer_bit_indice) + ", " + str(
            self.ultimo_bit_indice) + "]")
        print(
            "Los bits de la posición dentro del bloque son -> [" + str(self.primer_bit_posicion_en_bloque) + ", " + str(
                self.ultimo_bit_posicion_en_bloque) + "]")
        print("Los bits de la posición dentro de la palabra  -> [30, 31]")
        print("--------------------------------------------------------------------")


    # Mostrar el contenido de la caché
    def mostrar(self):
        print("\n")
        print("----------------------")
        print("    MEMORIA CACHÉ     ")
        print("----------------------")

        numero_bits_conjunto = int(math.log(self.numero_conjuntos, 2))
        numero_bits_bloque   = int(math.log(self.numero_bloques_conjunto, 2))
        i = 0
        for conjunto in self.conjuntos:
            print("Conjunto: " + dec2bin(i, numero_bits_conjunto))
            j = 0
            for bloque in conjunto.bloques:
                print("  Bloque: " + dec2bin(j, numero_bits_bloque) + " -> Bit Validez: [" + str(bloque.getBitValidez()) + "], Etiqueta: [" + bloque.getEtiqueta() + "]")
                k = 0
                print("    --------")
                for palabra in bloque.datos:
                    print("    - " + str(palabra) + " -")
                    k += 1
                print("    --------")
                j += 1
            i += 1

    # Activar la traza para mostrar mensajes sobre el funcionamiento interno
    def activarTraza(self):
        self.traza = True

# ----------------------------------------
# Memoria RAM
# Se usa un diccionario para ahorrar espacio, donde la clave es la dirección en hexadecimal
# ----------------------------------------
class MemoriaRam:
    # Constructor
    def __init__(self, numero_bits_direccion):
        self.traza                 = False
        self.numero_bits_direccion = numero_bits_direccion
        self.memoria               = {}

    # LEER PALABRA
    # Acceder a una posicion de memoria.
    # Si no esta en el diccionario, asumimos que el valor almacenado es 0
    def leerPalabra(self, direccion_hex):
        if direccion_hex in self.memoria:
            return self.memoria[direccion_hex]
        else:
            return 0

    # LEER BLOQUE
    # obtiene un bloque de memoria de numero_palabras_bloque palabras
    def leerBloque(self, direccion_hex, numero_palabras_bloque):
        vdatos = []

        numero_bits_bloque = int(math.log(numero_palabras_bloque,2))

        if numero_palabras_bloque == 1:
            vdatos.append(self.leerPalabra(direccion_hex))
        else:
            direccion_binario  = numero_hex2bin(direccion_hex)
            bits_final_prefijo = 32 - 2 - int(math.log(numero_palabras_bloque, 2))
            prefijo_direccion  = direccion_binario[0:bits_final_prefijo]

            for i in range(numero_palabras_bloque):
                i_direccion_binario = prefijo_direccion + str(dec2bin(i, numero_bits_bloque)) + "00"
                i_direccion_hex     = numero_bin2hex(i_direccion_binario)
                vdatos.append(self.leerPalabra(i_direccion_hex))

        return vdatos

    # ESCRIBIR PALABRA
    # Guardar en la memoria
    def escribirPalabra(self, direccion_hex, dato):
        self.memoria[direccion_hex] = dato

    # Inicializa algunas posiciones
    def inicializarMemoriaRam(self):
        self.escribirPalabra("00000000", 0)
        self.escribirPalabra("00000004", 4)
        self.escribirPalabra("00000008", 8)
        self.escribirPalabra("0000000C", 9)
        self.escribirPalabra("00000010", 10)
        self.escribirPalabra("00000014", 14)
        self.escribirPalabra("00000018", 18)
        self.escribirPalabra("0000001C", 19)
        self.escribirPalabra("00000020", 20)
        self.escribirPalabra("00000024", 24)
        self.escribirPalabra("00000028", 28)
        self.escribirPalabra("0000002C", 29)
        self.escribirPalabra("00000030", 30)
        self.escribirPalabra("00000034", 34)
        self.escribirPalabra("00000038", 38)
        self.escribirPalabra("0000003C", 39)
        self.escribirPalabra("00000040", 40)
        self.escribirPalabra("00000044", 44)
        self.escribirPalabra("00000048", 48)
        self.escribirPalabra("0000004C", 49)
        self.escribirPalabra("00000050", 50)
        self.escribirPalabra("00000054", 54)
        self.escribirPalabra("00000058", 58)
        self.escribirPalabra("0000005C", 59)

    # Imprimir el contenido de la memoria RAM
    def mostrar(self):
        print("\n")
        print("----------------------")
        print("     MEMORIA RAM      ")
        print("----------------------")
        print("DIRECCIÓN -> CONTENIDO")
        for direccion in self.memoria:
            print (direccion + "  -> " + str(self.memoria[direccion]))
        print("----------------------")


    # Activar la traza para mostrar mensajes sobre el funcionamiento interno
    def activarTraza(self):
        self.traza = True

# ----------------------------------------
# Sistema de Memoria
# Consiste en una memoria RAM y una memoria caché
# ----------------------------------------
class SistemaMemoria:
    def __init__(self, numero_conjuntos, numero_bloques_conjunto, numero_palabras_bloque):
        self.traza                   = False
        self.numero_conjuntos        = numero_conjuntos
        self.numero_bloques_conjunto = numero_bloques_conjunto
        self.numero_palabras_bloque  = numero_palabras_bloque
        self.memoria_ram             = MemoriaRam(32)
        self.memoria_cache           = MemoriaCache(self.numero_conjuntos, self.numero_bloques_conjunto, self.numero_palabras_bloque)

        # inicializamos la ram con algunos datos
        self.memoria_ram.inicializarMemoriaRam()

    # LEER
    # Para leer una dirección, primero miramos si está en la caché.
    # Si está, devolvemos el dato
    # Si no está, obtenemos el bloque completo de la RAM y lo copiamos en la caché
    def leer(self, direccion_hex):
        # miramos si está en la caché
        if self.traza:
            print(">>> Se va a buscar la dirección " + numero_hex2bin(direccion_hex) + " en la cache")

        acierto, vdatos, posicion_en_bloque = self.memoria_cache.leer(direccion_hex)

        if acierto == 1 and self.traza:
            print(">>> ACIERTO -> Se devuelve el dato directamente de la cache")

        else:
            if self.traza:
                print(">>> FALLO -> Se accede a la RAM para obtener el dato")

            # si no está en la caché, vamos a la RAM y traemos el bloque completo
            vdatos = self.memoria_ram.leerBloque(direccion_hex, self.numero_palabras_bloque)
            # escribimos en la caché el bloque
            self.memoria_cache.escribir(direccion_hex, vdatos)

        # devolvemos la palabra concreta dentro del bloque
        return vdatos[bin2dec(posicion_en_bloque)]

    # Imprimer información sobre la caché interna
    def printInfoCache(self):
        self.memoria_cache.averiguarTipoCache()

    # Mostrar el contenido de la CACHÉ
    def mostrarMemoriaCache(self):
        self.memoria_cache.mostrar()

    # Mostrar el contenido de la RAM
    def mostrarMemoriaRAM(self):
        self.memoria_ram.mostrar()

    # Activa que aparezcan mensajes sobre el funcionamiento interno de la memoria
    def activarTraza(self):
        self.traza = True
        self.memoria_ram.activarTraza()
        self.memoria_cache.activarTraza()


# --------------------------------------------
# --------------------------------------------
def ProbarMemoriaCache(numero_conjuntos, numero_bloques_conjunto, numero_palabras_bloque):
    sistema_memoria = SistemaMemoria(numero_conjuntos, numero_bloques_conjunto, numero_palabras_bloque)

    sistema_memoria.printInfoCache()
    sistema_memoria.activarTraza()

    sistema_memoria.mostrarMemoriaRAM()
    sistema_memoria.mostrarMemoriaCache()

    vlectura = ["00000000", "00000004", "00000008", "0000000C"]

    for direccion in vlectura:
        print("\nLECTURA dirección -> 0x" + direccion)
        dato = sistema_memoria.leer(direccion)
        print("Se obtiene el dato (en decimal): " + str(dato) + "\n")

    sistema_memoria.mostrarMemoriaCache()

    vlectura = ["00000010", "00000014", "00000000", "00000020"]

    for direccion in vlectura:
        print("\nLECTURA dirección -> 0x" + direccion)
        dato = sistema_memoria.leer(direccion)
        print("Se obtiene el dato (en decimal): " + str(dato) + "\n")

    sistema_memoria.mostrarMemoriaCache()

    vlectura = ["00000000", "00000024", "00000004", "00000020"]

    for direccion in vlectura:
        print("\nLECTURA dirección -> 0x" + direccion)
        dato = sistema_memoria.leer(direccion)
        print("Se obtiene el dato (en decimal): " + str(dato) + "\n")

    sistema_memoria.mostrarMemoriaCache()


# ----------------------------------------
# MAIN
# ----------------------------------------
if __name__ == "__main__":
    print("--------------------------------------------------------------------")
    print("---     Simulador de un sistema de memoria con memoria caché     ---")
    print("--------------------------------------------------------------------")

    # Correspondencia directa con tamaño de bloque == 1
    numero_conjuntos        = 1
    numero_bloques_conjunto = 4
    numero_palabras_bloque  = 1
    ProbarMemoriaCache(numero_conjuntos, numero_bloques_conjunto, numero_palabras_bloque)

    # Correspondencia directa con tamaño de bloque > 1
    numero_conjuntos        = 4
    numero_bloques_conjunto = 1
    numero_palabras_bloque  = 2
    ProbarMemoriaCache(numero_conjuntos, numero_bloques_conjunto, numero_palabras_bloque)

    # Totalmente asociativa con tamaño de bloque == 1
    numero_conjuntos        = 1
    numero_bloques_conjunto = 4
    numero_palabras_bloque  = 1
    ProbarMemoriaCache(numero_conjuntos, numero_bloques_conjunto, numero_palabras_bloque)

    # Totalmente asociativa con tamaño de bloque > 1
    numero_conjuntos        = 1
    numero_bloques_conjunto = 4
    numero_palabras_bloque  = 2
    ProbarMemoriaCache(numero_conjuntos, numero_bloques_conjunto, numero_palabras_bloque)

    # Asociativa con tamaño de bloque == 1
    numero_conjuntos        = 8
    numero_bloques_conjunto = 4
    numero_palabras_bloque  = 1
    ProbarMemoriaCache(numero_conjuntos, numero_bloques_conjunto, numero_palabras_bloque)

    # Asociativa con tamaño de bloque > 1
    numero_conjuntos        = 8
    numero_bloques_conjunto = 4
    numero_palabras_bloque  = 2
    ProbarMemoriaCache(numero_conjuntos, numero_bloques_conjunto, numero_palabras_bloque)


