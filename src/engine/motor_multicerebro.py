import random
from src.db.memoria_sqlite import carregar_frequencia_dezenas
from src.engine.aprendiz import obter_perfil_vencedor

TOTAL_DEZENAS = 15
UNIVERSO = list(range(1, 26))


def gerar_jogo():
    perfil = obter_perfil_vencedor()
    freq_dict = carregar_frequencia_dezenas()

    jogo = set()

    # 1️⃣ Perfil vencedor (até 6 dezenas)
    if perfil:
        jogo.update(random.sample(perfil, min(6, len(perfil))))

    # 2️⃣ Frequência histórica
    if freq_dict:
        ordenadas = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
        frequentes = [int(n) for n, _ in ordenadas]

        restantes = TOTAL_DEZENAS - len(jogo)
        if restantes > 0:
            jogo.update(random.sample(frequentes, min(restantes, len(frequentes))))

    # 3️⃣ Aleatório controlado
    restantes = TOTAL_DEZENAS - len(jogo)
    if restantes > 0:
        pool = list(set(UNIVERSO) - jogo)
        jogo.update(random.sample(pool, restantes))

    return sorted(jogo)
