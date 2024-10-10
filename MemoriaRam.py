# ----------------------------------------
# Memoria RAM
# Se usa un diccionario para ahorrar espacio, donde la clave es la dirección en hexadecimal
# ----------------------------------------
import math

from utils import numero_hex2bin, dec2bin, numero_bin2hex


class MemoriaRam:
    # Constructor
    def __init__(self, numero_bits_direccion):
        self.traza = False
        self.numero_bits_direccion = numero_bits_direccion
        self.memoria = {}

    # LEER PALABRA
    # Acceder a una posicion de memoria.
    # Si no esta en el diccionario, asumimos que el valor almacenado es 0
    def leer_palabra(self, direccion_hex):
        if direccion_hex in self.memoria:
            return self.memoria[direccion_hex]
        else:
            return 0

    # LEER BLOQUE
    # obtiene un bloque de memoria de numero_palabras_bloque palabras
    def leer_bloque(self, direccion_hex, numero_palabras_bloque):
        vdatos = []

        numero_bits_bloque = int(math.log(numero_palabras_bloque,2))

        if numero_palabras_bloque == 1:
            vdatos.append(self.leer_palabra(direccion_hex))
        else:
            direccion_binario = numero_hex2bin(direccion_hex)
            bits_final_prefijo = self.numero_bits_direccion - int(math.log(numero_palabras_bloque, 2))
            prefijo_direccion = direccion_binario[0:bits_final_prefijo]

            for i in range(numero_palabras_bloque):
                i_direccion_binario = prefijo_direccion + str(dec2bin(i, numero_bits_bloque))
                i_direccion_hex = numero_bin2hex(i_direccion_binario)
                vdatos.append(self.leer_palabra(i_direccion_hex))

        return vdatos

    # ESCRIBIR PALABRA
    # Guardar en la memoria
    def escribir_palabra(self, direccion_hex, dato):
        self.memoria[direccion_hex] = dato

    # Inicializa algunas posiciones
    def inicializar_memoria_ram(self):
        self.escribir_palabra("0000", 0)
        self.escribir_palabra("0001", 4)
        self.escribir_palabra("0002", 8)
        self.escribir_palabra("0003", 9)
        self.escribir_palabra("0004", 10)
        self.escribir_palabra("0005", 14)
        self.escribir_palabra("0006", 18)
        self.escribir_palabra("0007", 19)
        self.escribir_palabra("0008", 20)
        self.escribir_palabra("0009", 24)
        self.escribir_palabra("000A", 28)
        self.escribir_palabra("000B", 29)
        self.escribir_palabra("000C", 30)
        self.escribir_palabra("000D", 34)
        self.escribir_palabra("000E", 38)
        self.escribir_palabra("000F", 39)

    # Imprimir el contenido de la memoria RAM
    def mostrar(self):
        print("\n")
        print("----------------------")
        print("     MEMORIA RAM      ")
        print("----------------------")
        print("DIRECCIÓN -> CONTENIDO")
        for direccion in self.memoria:
            print(direccion + "  -> " + str(self.memoria[direccion]))
        print("----------------------")

    # Activar la traza para mostrar mensajes sobre el funcionamiento interno
    def activar_traza(self):
        self.traza = True
