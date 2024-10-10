# -----------------------------------------------------
# Simulador memoria chaché
# Simula únicamene lecturas
# -----------------------------------------------------
# En este simulador se asume que siempre las direcciones de memoria tienen 16 bits
# y el tamaño de palabra también es de 16 bits
# Cada registro de la RAM tiene un tamaño de 16 bits
# -----------------------------------------------------
from SistemaMemoria import SistemaMemoria


# --------------------------------------------
# --------------------------------------------
def probar_memoria_cache(numero_conjuntos, numero_bloques_conjunto, numero_palabras_bloque):
    sistema_memoria = SistemaMemoria(numero_conjuntos, numero_bloques_conjunto, numero_palabras_bloque)

    sistema_memoria.print_info_cache()
    sistema_memoria.activar_traza()

    sistema_memoria.mostrar_memoria_ram()
    sistema_memoria.mostrar_memoria_cache()

    vlectura = ["0000", "0003", "0008", "0002"]

    for direccion in vlectura:
        print("\nLECTURA dirección -> 0x" + direccion)
        dato = sistema_memoria.leer(direccion)
        print("Se obtiene el dato (en decimal): " + str(dato) + "\n")
        sistema_memoria.mostrar_memoria_cache()


# ----------------------------------------
# MAIN
# ----------------------------------------
if __name__ == "__main__":
    print("--------------------------------------------------------------------")
    print("---     Simulador de un sistema de memoria con memoria caché     ---")
    print("--------------------------------------------------------------------")

    # Correspondencia directa con tamaño de bloque == 1
    # numero_conjuntos = 4
    # numero_bloques_conjunto = 1
    # numero_palabras_bloque = 1
    # probar_memoria_cache(numero_conjuntos, numero_bloques_conjunto, numero_palabras_bloque)

    # Correspondencia directa con tamaño de bloque > 1
    numero_conjuntos = 4
    numero_bloques_conjunto = 1
    numero_palabras_bloque = 2
    probar_memoria_cache(numero_conjuntos, numero_bloques_conjunto, numero_palabras_bloque)
    #
    # # Totalmente asociativa con tamaño de bloque == 1
    # numero_conjuntos = 1
    # numero_bloques_conjunto = 4
    # numero_palabras_bloque = 1
    # probar_memoria_cache(numero_conjuntos, numero_bloques_conjunto, numero_palabras_bloque)
    #
    # # Totalmente asociativa con tamaño de bloque > 1
    # numero_conjuntos = 1
    # numero_bloques_conjunto = 4
    # numero_palabras_bloque = 2
    # probar_memoria_cache(numero_conjuntos, numero_bloques_conjunto, numero_palabras_bloque)
    #
    # # Asociativa con tamaño de bloque == 1
    # numero_conjuntos = 8
    # numero_bloques_conjunto = 4
    # numero_palabras_bloque = 1
    # probar_memoria_cache(numero_conjuntos, numero_bloques_conjunto, numero_palabras_bloque)
    #
    # # Asociativa con tamaño de bloque > 1
    # numero_conjuntos = 8
    # numero_bloques_conjunto = 4
    # numero_palabras_bloque = 2
    # probar_memoria_cache(numero_conjuntos, numero_bloques_conjunto, numero_palabras_bloque)
    #

