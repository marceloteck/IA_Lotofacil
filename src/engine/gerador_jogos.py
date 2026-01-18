"""
🧠 GERADOR CENTRAL DE JOGOS — IA SELETIVA
Geração extrema baseada em aprendizado + memória + anti-caos.
"""

import random
from typing import List

from src.engine.seletor_extremo import selecionar_top_jogos
from src.engine.estatisticas import calcular_dezenas_quentes_frias
from src.engine.motor_multicerebro import obter_total_dezenas_atual
from src.engine.aprendiz import obter_perfil_vencedor
from src.utils.dados import carregar_resultados
from src.utils.logger import logger


# ==================================================
# ⚙️ CONFIGURAÇÃO GLOBAL
# ==================================================
TOTAL_GERADOS = 500
TOP_15 = 10
TOP_18 = 7

DEZENAS_TOTAIS = list(range(1, 26))


# ==================================================
# 🎯 GERADOR BASE (ANTI-CAOS)
# ==================================================
def gerar_jogo_base(
    tamanho: int,
    dezenas_quentes: List[int],
    dezenas_frias: List[int],
    ultimo_resultado: List[int]
) -> List[int]:

    jogo = set()

    # 🔥 Quentes dominam, mas não totalizam
    alvo_quentes = int(tamanho * 0.45)
    while len(jogo) < alvo_quentes:
        jogo.add(random.choice(dezenas_quentes))

    # ♻️ Repetição leve do último concurso
    repetidas = random.sample(
        ultimo_resultado,
        k=min(4, len(ultimo_resultado))
    )
    jogo.update(repetidas)

    # ❄️ Frias entram pouco
    if random.random() < 0.2:
        jogo.add(random.choice(dezenas_frias))

    # 🎲 Completa com diversidade
    while len(jogo) < tamanho:
        jogo.add(random.choice(DEZENAS_TOTAIS))

    return sorted(jogo)


# ==================================================
# 🚀 SUPERGERAÇÃO CONTROLADA
# ==================================================
def supergerar_jogos(
    tamanho: int,
    total: int
) -> List[List[int]]:

    dezenas_quentes, dezenas_frias = calcular_dezenas_quentes_frias()
    resultados = carregar_resultados()
    ultimo_resultado = resultados[-1]["dezenas"]

    jogos = set()

    logger.info(f"🧠 Supergeração iniciada | {total} jogos ({tamanho} dezenas)")

    tentativas = 0
    while len(jogos) < total and tentativas < total * 5:
        jogo = tuple(
            gerar_jogo_base(
                tamanho,
                dezenas_quentes,
                dezenas_frias,
                ultimo_resultado
            )
        )
        jogos.add(jogo)
        tentativas += 1

        if len(jogos) % 100 == 0:
            logger.debug(f"🧠 Supergeração: {len(jogos)}/{total}")

    return [list(j) for j in jogos]


# ==================================================
# 🧠 GERADOR FINAL INTELIGENTE
# ==================================================
def gerar_jogos_inteligentes():

    print("\n🧠 GERANDO JOGOS COM IA SELETIVA — NÍVEL EXTREMO\n")

    perfil = obter_perfil_vencedor()
    if not perfil:
        print("❌ Nenhum aprendizado encontrado. Execute o treinamento.")
        return

    dezenas_motor = obter_total_dezenas_atual()
    logger.info(f"🧠 Motor ativo com {dezenas_motor} dezenas")

    # ===============================
    # 🎯 JOGOS 15
    # ===============================
    jogos_15_brutos = supergerar_jogos(15, TOTAL_GERADOS)

    jogos_15_finais = selecionar_top_jogos(
        jogos_15_brutos,
        top_n=TOP_15,
        timeout_segundos=8
    )

    # ===============================
    # 🎯 JOGOS 18
    # ===============================
    jogos_18_brutos = supergerar_jogos(18, TOTAL_GERADOS)

    jogos_18_finais = selecionar_top_jogos(
        jogos_18_brutos,
        top_n=TOP_18,
        timeout_segundos=8
    )

    # ===============================
    # 📊 SAÍDA
    # ===============================
    print("=" * 60)
    print("🎯 TOP JOGOS — 15 DEZENAS\n")

    for i, jogo in enumerate(jogos_15_finais, 1):
        print(f"Jogo {i:02d}: {jogo}")

    print("\n" + "=" * 60)
    print("🎯 TOP JOGOS — 18 DEZENAS\n")

    for i, jogo in enumerate(jogos_18_finais, 1):
        print(f"Jogo {i:02d}: {jogo}")

    print("\n✅ Jogos escolhidos por IA seletiva (anti-caos real)\n")


# ==================================================
# ▶️ EXECUÇÃO
# ==================================================
if __name__ == "__main__":
    gerar_jogos_inteligentes()
