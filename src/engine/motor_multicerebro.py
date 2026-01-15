import random
from src.db.memoria_sqlite import carregar_frequencia_dezenas
from src.engine.aprendiz import obter_perfil_vencedor
from src.engine.extrator_nucleo import extrair_nucleo_global, gerar_base_18_nucleo
from src.engine.cerebro_neural import avaliar_base
from src.engine.fechamento_automatico import gerar_fechamento



# ==================================
# 🎛️ CONFIGURAÇÃO DE TREINAMENTO
# ==================================

# Modo automático: escolhe aleatoriamente a quantidade de dezenas
MODO_TOTAL_DEZENAS_AUTOMATICO = True

# Se automático estiver desligado, usa este valor fixo
TOTAL_DEZENAS_FIXO = 18

# Intervalo permitido quando automático
INTERVALO_DEZENAS = [15, 16, 17, 18, 19, 20]


#TOTAL_DEZENAS = 18
UNIVERSO = list(range(1, 26))

MAX_PERFIL = 6
MIN_NUCLEO = 4
MAX_FREQ_DOMINANCIA = 10


def resolver_total_dezenas():
    """
    Decide quantas dezenas o motor vai usar neste ciclo.
    Não afeta fechamento nem geração final.
    """
    if MODO_TOTAL_DEZENAS_AUTOMATICO:
        return random.choice(INTERVALO_DEZENAS)
    return TOTAL_DEZENAS_FIXO





def gerar_jogo():
    perfil = obter_perfil_vencedor() or []
    freq_dict = carregar_frequencia_dezenas() or {}
    nucleo_data = extrair_nucleo_global()

    nucleo = nucleo_data.get("nucleo", [])
    satelites = nucleo_data.get("satelites", [])

    jogo = set()

    # ===============================
    # 1️⃣ NÚCLEO GLOBAL
    # ===============================
    if nucleo:
        jogo.update(random.sample(nucleo, min(4, len(nucleo))))

    # ===============================
    # 2️⃣ PERFIL VENCEDOR
    # ===============================
    perfil_filtrado = list(set(perfil) - jogo)
    if perfil_filtrado:
        jogo.update(random.sample(perfil_filtrado, min(MAX_PERFIL, len(perfil_filtrado))))

    # ===============================
    # 3️⃣ SATÉLITES
    # ===============================
    restantes = TOTAL_DEZENAS - len(jogo)
    if restantes > 0 and satelites:
        pool = list(set(satelites) - jogo)
        jogo.update(random.sample(pool, min(restantes, len(pool))))

    # ===============================
    # 4️⃣ FREQUÊNCIA HISTÓRICA
    # ===============================
    if freq_dict:
        ordenadas = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
        top_freq = [int(d) for d, _ in ordenadas[:MAX_FREQ_DOMINANCIA]]

        restantes = TOTAL_DEZENAS - len(jogo)
        pool = list(set(top_freq) - jogo)
        if restantes > 0 and pool:
            jogo.update(random.sample(pool, min(restantes, len(pool))))

    # ===============================
    # 5️⃣ ALEATORIEDADE FINAL
    # ===============================
    restantes = TOTAL_DEZENAS - len(jogo)
    if restantes > 0:
        pool = list(set(UNIVERSO) - jogo)
        jogo.update(random.sample(pool, restantes))

    return sorted(jogo)


# ==================================
# 🎛️ PARÂMETROS
# ==================================
TAMANHO_JOGO_FINAL = 15


def gerar_jogo_inteligente():
    # 1️⃣ GERAR BASE 18
    base = gerar_base_18_nucleo()

    # 2️⃣ CONSULTAR CÉREBRO NEURAL (consultivo)
    avaliacao = avaliar_base(base)

    if not avaliacao.get("aprovado", True):
        base = gerar_base_18_nucleo()

    # 3️⃣ GERAR FECHAMENTO
    jogos = gerar_fechamento(base, TAMANHO_JOGO_FINAL)

    return {
        "base_18": base,
        "avaliacao": avaliacao,
        "jogos": jogos
    }
