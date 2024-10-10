# ----------------------------------------
# Sistema de Memoria
# Consiste en una memoria RAM y una memoria caché
# ----------------------------------------
from MemoriaCache import MemoriaCache
from MemoriaRam import MemoriaRam
from utils import numero_hex2bin, bin2dec, fancy_binario


class SistemaMemoria:
    def __init__(self, numero_conjuntos, numero_bloques_conjunto, numero_palabras_bloque):
        self.traza = False
        self.numero_conjuntos = numero_conjuntos
        self.numero_bloques_conjunto = numero_bloques_conjunto
        self.numero_palabras_bloque = numero_palabras_bloque
        self.memoria_ram = MemoriaRam(16)
        self.memoria_cache = MemoriaCache(16, self.numero_conjuntos, self.numero_bloques_conjunto, self.numero_palabras_bloque)

        # inicializamos la ram con algunos datos
        self.memoria_ram.inicializar_memoria_ram()

    # LEER
    # Para leer una dirección, primero miramos si está en la caché.
    # Si está, devolvemos el dato
    # Si no está, obtenemos el bloque completo de la RAM y lo copiamos en la caché
    def leer(self, direccion_hex):
        # miramos si está en la caché
        if self.traza:
            print(">>> Se va a buscar la dirección " + fancy_binario(numero_hex2bin(direccion_hex)) + " en la cache")

        acierto, vdatos, posicion_en_bloque = self.memoria_cache.leer(direccion_hex)

        if acierto == 1 and self.traza:
            print(">>> ACIERTO -> Se devuelve el dato directamente de la cache")

        else:
            if self.traza:
                print(">>> FALLO -> Se accede a la RAM para obtener el dato")

            # si no está en la caché, vamos a la RAM y traemos el bloque completo
            vdatos = self.memoria_ram.leer_bloque(direccion_hex, self.numero_palabras_bloque)
            # escribimos en la caché el bloque
            self.memoria_cache.escribir(direccion_hex, vdatos)

        # devolvemos la palabra concreta dentro del bloque
        return vdatos[bin2dec(posicion_en_bloque)]

    # Imprimer información sobre la caché interna
    def print_info_cache(self):
        self.memoria_cache.averiguar_tipo_cache()

    # Mostrar el contenido de la CACHÉ
    def mostrar_memoria_cache(self):
        self.memoria_cache.mostrar()

    # Mostrar el contenido de la RAM
    def mostrar_memoria_ram(self):
        self.memoria_ram.mostrar()

    # Activa que aparezcan mensajes sobre el funcionamiento interno de la memoria
    def activar_traza(self):
        self.traza = True
        self.memoria_ram.activar_traza()
        self.memoria_cache.activar_traza()

