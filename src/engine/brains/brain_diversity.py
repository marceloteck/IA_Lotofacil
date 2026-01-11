def diversidade(base, outras):
    score = 0
    for b in outras:
        inter = len(base & b)
        score -= inter * 2
    return score
