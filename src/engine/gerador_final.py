import random
from src.engine.aprendiz import obter_perfil_vencedor
from src.db.memoria_sqlite import carregar_frequencia_dezenas

UNIVERSO = list(range(1, 26))


def gerar_jogo_custom(tamanho):
    perfil = obter_perfil_vencedor()
    freq = carregar_frequencia_dezenas()

    jogo = set()

    # 🔹 Perfil vencedor (até 40%)
    if perfil:
        qtd = min(int(tamanho * 0.4), len(perfil))
        jogo.update(random.sample(perfil, qtd))

    # 🔹 Frequência histórica
    if freq:
        ordenadas = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        frequentes = [int(n) for n, _ in ordenadas]

        restantes = tamanho - len(jogo)
        if restantes > 0:
            jogo.update(random.sample(frequentes, min(restantes, len(frequentes))))

    # 🔹 Aleatório controlado
    restantes = tamanho - len(jogo)
    if restantes > 0:
        pool = list(set(UNIVERSO) - jogo)
        jogo.update(random.sample(pool, restantes))

    return sorted(jogo)


def gerar_jogos_finais():
    jogos_15 = [gerar_jogo_custom(15) for _ in range(10)]
    jogos_18 = [gerar_jogo_custom(18) for _ in range(7)]

    return jogos_15, jogos_18
