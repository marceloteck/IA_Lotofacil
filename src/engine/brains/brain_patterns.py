PRIMOS = {2,3,5,7,11,13,17,19,23}
FIBO = {1,2,3,5,8,13,21}

def contar_padroes(base):
    return {
        "impares": sum(1 for n in base if n % 2 == 1),
        "primos": sum(1 for n in base if n in PRIMOS),
        "fibo": sum(1 for n in base if n in FIBO)
    }

def score_padroes(base):
    p = contar_padroes(base)
    score = 0

    if 8 <= p["impares"] <= 9:
        score += 3
    if 5 <= p["primos"] <= 6:
        score += 3
    if 3 <= p["fibo"] <= 5:
        score += 2

    return score
