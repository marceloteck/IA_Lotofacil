from statistics import mean

def calibrar_pesos(jogos_premiados):
    """
    Recebe lista de:
    {
        'dezenas': [...],
        'pontos': 14 ou 15
    }
    Retorna pesos calibrados
    """

    metricas = {
        "quentes": [],
        "frias": [],
        "repetidas": [],
        "pares": [],
    }

    for jogo in jogos_premiados:
        dezenas = set(jogo["dezenas"])

        metricas["quentes"].append(jogo.get("q_quentes", 0))
        metricas["frias"].append(jogo.get("q_frias", 0))
        metricas["repetidas"].append(jogo.get("q_repetidas", 0))
        metricas["pares"].append(jogo.get("q_pares", 0))

    pesos = {
        "peso_quentes": round(20 / (mean(metricas["quentes"]) + 1), 2),
        "peso_frias": round(5 / (mean(metricas["frias"]) + 1), 2),
        "peso_repetidas": round(30 / (mean(metricas["repetidas"]) + 1), 2),
        "peso_pares": round(10 / (mean(metricas["pares"]) + 1), 2),
    }

    return pesos
