import random
from src.db.memoria_sqlite import carregar_frequencia_dezenas
from src.engine.aprendiz import obter_perfil_vencedor

TOTAL_DEZENAS = 15
UNIVERSO = list(range(1, 26))


def gerar_jogo():
    perfil = obter_perfil_vencedor()
    freq = carregar_frequencia_dezenas()

    jogo = set()

    # Perfil vencedor
    if perfil:
        jogo.update(random.sample(perfil, min(6, len(perfil))))

    # Frequência premiada
    if freq:
        ordenadas = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        top = [n for n, _ in ordenadas[:15]]

        faltam = TOTAL_DEZENAS - len(jogo)
        if faltam > 0:
            jogo.update(random.sample(top, min(faltam, len(top))))

    # Diversidade
    faltam = TOTAL_DEZENAS - len(jogo)
    if faltam > 0:
        pool = list(set(UNIVERSO) - jogo)
        jogo.update(random.sample(pool, faltam))

    return sorted(jogo)
