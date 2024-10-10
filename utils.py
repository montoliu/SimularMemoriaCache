# Añade un espacio cada 4 bits para hacer más legible el binario
def fancy_binario(numero):
    s = ""
    i = 0
    for bit in numero:
        s = s + bit
        i += 1
        if i % 4 == 0:
            s = s + " "
    return s


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
    numero_binario = bin(numero_decimal)
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

    numero_hex = ""
    pos_final = len(n)
    pos_inicial = pos_final - 4

    while pos_inicial >= 0:
        numero_hex = digito_bin2hex(n[pos_inicial:pos_final]) + numero_hex
        pos_final = pos_final - 4
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
