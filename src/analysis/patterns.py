PRIMOS = {2, 3, 5, 7, 11, 13, 17, 19, 23}
FIBONACCI = {1, 2, 3, 5, 8, 13, 21}
MOLDURA = {1,2,3,4,5,6,10,11,15,16,20,21,22,23,24,25}

def contar_impares(dezenas):
    return sum(1 for d in dezenas if d % 2 != 0)

def contar_primos(dezenas):
    return sum(1 for d in dezenas if d in PRIMOS)

def contar_multiplos_3(dezenas):
    return sum(1 for d in dezenas if d % 3 == 0)

def contar_fibonacci(dezenas):
    return sum(1 for d in dezenas if d in FIBONACCI)

def contar_moldura(dezenas):
    return sum(1 for d in dezenas if d in MOLDURA)

def contar_repetidas(dezenas, anterior):
    if not anterior:
        return 0
    return len(set(dezenas) & set(anterior))
