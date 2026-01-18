# ==========================================================
# 📊 ESTATÍSTICAS — DEZENAS QUENTES E FRIAS
# ==========================================================

from collections import Counter
from src.db.memoria_sqlite import carregar_historico


def calcular_dezenas_quentes_frias():
    """
    Retorna duas listas:
    - dezenas quentes (mais frequentes)
    - dezenas frias (menos frequentes)
    """

    historico = carregar_historico()

    todas = []
    for concurso in historico:
        todas.extend(concurso)

    freq = Counter(todas)

    ordenadas = freq.most_common()

    dezenas_quentes = [n for n, _ in ordenadas[:8]]
    dezenas_frias = [n for n, _ in ordenadas[-8:]]

    return dezenas_quentes, dezenas_frias
