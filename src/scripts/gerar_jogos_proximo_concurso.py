"""
🔮 GERADOR DE JOGOS — PRÓXIMO CONCURSO (COM CÉREBRO SELETOR)
Gera muitos jogos, aplica viés estatístico, score 14/15
e elimina agressivamente os jogos fracos.
"""

from src.engine.gerador_final import gerar_jogos_finais
from src.engine.aprendiz import obter_perfil_vencedor
from src.engine.motor_multicerebro import obter_total_dezenas_atual
from src.engine.estatisticas import calcular_dezenas_quentes_frias
from src.utils.dados import carregar_resultados


# ===============================
# ⚙️ CONFIGURAÇÕES AVANÇADAS
# ===============================

MODO_EXTREMO = True
SUPER_GERACAO = 1000     # Quantos jogos gerar
TOP_FINAL = 10          # Quantos sobreviverão

PESO_QUENTES = 3
PESO_REPETIDAS = 2
PESO_PARES = 1.5


# ===============================
# 🧠 FUNÇÕES DO CÉREBRO SELETOR
# ===============================

def score_proximidade_1415(jogo, dezenas_quentes, ultimo_resultado):
    """
    Calcula quão próximo este jogo está
    do padrão histórico de 14/15 pontos.
    """
    score = 0

    # 🔥 Dezenas quentes
    score += len(set(jogo) & set(dezenas_quentes)) * PESO_QUENTES

    # 🔁 Repetidas do último concurso
    score += len(set(jogo) & set(ultimo_resultado)) * PESO_REPETIDAS

    # ⚖️ Pares / Ímpares
    pares = sum(1 for d in jogo if d % 2 == 0)
    if 7 <= pares <= 9:
        score += PESO_PARES

    return score


def filtrar_e_selecionar(jogos, dezenas_quentes, ultimo_resultado, top_n):
    """
    Aplica score, ordena e elimina jogos fracos.
    """
    jogos_com_score = []

    for jogo in jogos:
        score = score_proximidade_1415(
            jogo,
            dezenas_quentes,
            ultimo_resultado
        )
        jogos_com_score.append((score, jogo))

    # 🔥 Ordenação brutal (melhores primeiro)
    jogos_com_score.sort(reverse=True, key=lambda x: x[0])

    # ✂️ Eliminação agressiva
    selecionados = [jogo for _, jogo in jogos_com_score[:top_n]]

    return selecionados


# ===============================
# 🎯 GERADOR PRINCIPAL
# ===============================

def gerar_jogos_proximo_concurso():
    print("\n🔮 GERANDO JOGOS PARA O PRÓXIMO CONCURSO (MODO INTELIGENTE)\n")

    # ===============================
    # 🔎 VERIFICA APRENDIZADO
    # ===============================
    perfil = obter_perfil_vencedor()
    if not perfil:
        print("❌ Nenhum perfil vencedor encontrado.")
        print("➡️ Execute o treinamento pelo menos uma vez.")
        return

    # ===============================
    # 🔥 ESTATÍSTICAS
    # ===============================
    dezenas_quentes, dezenas_frias = calcular_dezenas_quentes_frias()

    # ===============================
    # 📊 ÚLTIMO RESULTADO
    # ===============================
    resultados = carregar_resultados()
    resultados = sorted(resultados, key=lambda x: x["concurso"])
    ultimo_resultado = resultados[-1]["dezenas"]

    # ===============================
    # 🧠 SUPER GERAÇÃO
    # ===============================
    jogos_brutos_15 = []
    jogos_brutos_18 = []

    for _ in range(SUPER_GERACAO):
        jogos_15, jogos_18 = gerar_jogos_finais(
            dezenas_quentes,
            dezenas_frias,
            ultimo_resultado
        )
        jogos_brutos_15.extend(jogos_15)
        jogos_brutos_18.extend(jogos_18)

    # ===============================
    # 🧠 CÉREBRO SELETOR
    # ===============================
    jogos_15_finais = filtrar_e_selecionar(
        jogos_brutos_15,
        dezenas_quentes,
        ultimo_resultado,
        TOP_FINAL
    )

    jogos_18_finais = filtrar_e_selecionar(
        jogos_brutos_18,
        dezenas_quentes,
        ultimo_resultado,
        TOP_FINAL
    )

    # ===============================
    # 🧠 INFO DO MOTOR
    # ===============================
    dezenas_motor = obter_total_dezenas_atual()
    print(f"🧠 Motor ativo com {dezenas_motor} dezenas\n")

    print("=" * 60)
    print("🎯 TOP JOGOS — 15 DEZENAS (SELECIONADOS)\n")

    for i, jogo in enumerate(jogos_15_finais, 1):
        print(f"Jogo {i:02d}: {jogo}")

    print("\n" + "=" * 60)
    print("🎯 TOP JOGOS — 18 DEZENAS (SELECIONADOS)\n")

    for i, jogo in enumerate(jogos_18_finais, 1):
        print(f"Jogo {i:02d}: {jogo}")

    print("\n✅ Jogos finais escolhidos por IA seletiva (anti-caos)\n")


if __name__ == "__main__":
    gerar_jogos_proximo_concurso()
