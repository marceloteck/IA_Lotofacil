import random
from src.database.connection import get_conn


def gerar_jogo(qtd=15):
    """
    Gera um jogo simples baseado em peso de frequência.
    Versão mínima funcional para o treinamento sequencial.
    """

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT numero, peso
        FROM frequencias
        ORDER BY peso DESC
    """)

    dados = cur.fetchall()
    conn.close()

    numeros = [n for n, _ in dados]
    pesos = [p for _, p in dados]

    # escolha ponderada
    jogo = set()
    while len(jogo) < qtd:
        escolhido = random.choices(numeros, weights=pesos, k=1)[0]
        jogo.add(escolhido)

    return sorted(jogo)
