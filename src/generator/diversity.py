# src/generator/diversity.py

def diversidade(jogo, jogos_anteriores, limite=12):
    """
    Garante que um novo jogo não seja muito parecido com os anteriores
    """
    for anterior in jogos_anteriores:
        intersecao = len(set(jogo) & set(anterior))
        if intersecao >= limite:
            return False
    return True
