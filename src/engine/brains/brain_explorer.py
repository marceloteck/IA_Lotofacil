import random

def gerar_base_exploracao(todas, tamanho=18):
    return set(random.sample(todas, tamanho))
