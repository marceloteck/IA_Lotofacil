from collections import Counter

from src.engine.motor_multicerebro import gerar_jogo, obter_total_dezenas_atual
from src.engine.aprendiz import gerar_perfil_vencedor
from src.engine.avaliador import Avaliador
from src.engine.estatisticas import calcular_dezenas_quentes_frias
from src.engine.gerador_final import gerar_jogos_finais
from src.engine.calibrador_pesos import calibrar_pesos

from src.db.memoria_sqlite import (
    salvar_jogo_premiado,
    carregar_jogos_premiados
)

from src.utils.comparador import contar_acertos
from src.utils.dados import carregar_resultados
from src.reports.relatorio_txt import salvar_relatorio

# ===============================
# ⚙️ CONFIGURAÇÃO DE APRENDIZADO
# ===============================

APRENDIZADO_MULTIPLO = True

CONFIG_JOGOS_TREINO = {
    16: 5,   # 5 jogos de 16 dezenas
    18: 3,   # 3 jogos de 18 dezenas
    20: 2    # 2 jogos de 20 dezenas
}



def treinar_sequencial():
    print("🧠 Treinamento sequencial iniciado")

    # ===============================
    # 📥 CARREGA RESULTADOS OFICIAIS
    # ===============================
    resultados = carregar_resultados()

    # Garantir ordem cronológica (antigo → novo)
    resultados = sorted(resultados, key=lambda x: x["concurso"])

    avaliador = Avaliador()
    contador_dezenas = {}

    # ===============================
    # 📊 HISTÓRICO GLOBAL
    # ===============================
    historico_dezenas = []

    for i in range(len(resultados) - 1):
        concurso_atual = resultados[i]["concurso"]
        dezenas_atual = resultados[i]["dezenas"]
        dezenas_reais = resultados[i + 1]["dezenas"]

        historico_dezenas.append(dezenas_atual)

        # ===============================
        # 🎓 APRENDIZADO
        # ===============================
        if APRENDIZADO_MULTIPLO:
            for _ in range(10):  # 10 jogos por concurso
                jogo = gerar_jogo()

                pontos = contar_acertos(jogo, dezenas_reais)
                avaliador.registrar(pontos)

                total_dezenas_usadas = len(jogo)
                contador_dezenas[total_dezenas_usadas] = (
                    contador_dezenas.get(total_dezenas_usadas, 0) + 1
                )

                print(
                    f"📘 Concurso {concurso_atual} → previsão {concurso_atual + 1} | Pontos: {pontos}"
                )

                if pontos >= 11:
                    print("💰 JOGO PREMIADO! Salvando na memória")
                    salvar_jogo_premiado(concurso_atual, jogo, pontos)

        else:
            jogo = gerar_jogo()
            pontos = contar_acertos(jogo, dezenas_reais)
            avaliador.registrar(pontos)

            total_dezenas_usadas = len(jogo)
            contador_dezenas[total_dezenas_usadas] = (
                contador_dezenas.get(total_dezenas_usadas, 0) + 1
            )

        print(
            f"📘 Concurso {concurso_atual} → previsão {concurso_atual + 1} | Pontos: {pontos}"
        )

        if pontos >= 11:
            print("💰 JOGO PREMIADO! Salvando na memória")
            salvar_jogo_premiado(concurso_atual, jogo, pontos)






        # 📊 Controle de tamanho dos jogos
        total_dezenas_usadas = obter_total_dezenas_atual()
        contador_dezenas[total_dezenas_usadas] = (
            contador_dezenas.get(total_dezenas_usadas, 0) + 1
        )

        print(
            f"📘 Concurso {concurso_atual} → previsão {concurso_atual + 1} | Pontos: {pontos}"
        )

        # 💰 Salva memória premiada (>=11)
        if pontos >= 11:
            print("💰 JOGO PREMIADO! Salvando na memória")
            salvar_jogo_premiado(concurso_atual, jogo, pontos)

    # ===============================
    # 🧠 PERFIL VENCEDOR (como já existia)
    # ===============================
    gerar_perfil_vencedor()
    avaliador.relatorio()

    # ===============================
    # 🔥 ESTATÍSTICAS REAIS DO HISTÓRICO
    # ===============================
    dezenas_quentes, dezenas_frias = calcular_dezenas_quentes_frias()

    # Último resultado conhecido
    ultimo_resultado = resultados[-1]["dezenas"]

    # ===============================
    # 🧠 CALIBRAÇÃO AUTOMÁTICA DE PESOS
    # ===============================
    jogos_1415 = carregar_jogos_premiados(min_pontos=14)

    if jogos_1415:
        pesos_calibrados = calibrar_pesos(jogos_1415)
        print("⚙️ Pesos calibrados automaticamente:", pesos_calibrados)
    else:
        pesos_calibrados = None
        print("⚠️ Ainda não há jogos 14/15 suficientes para calibração")

    # ===============================
    # 🎯 GERAÇÃO FINAL DE JOGOS
    # ===============================
    jogos_15, jogos_18 = gerar_jogos_finais(
        dezenas_quentes=dezenas_quentes,
        dezenas_frias=dezenas_frias,
        ultimo_resultado=ultimo_resultado,
        pesos=pesos_calibrados  # ← NOVO (opcional e seguro)
    )

    # ===============================
    # 📄 RELATÓRIO FINAL
    # ===============================
    estatisticas = avaliador.resumo()
    estatisticas["dezenas_treinamento"] = contador_dezenas

    relatorio_avaliador = avaliador.relatorio_texto()

    salvar_relatorio(
        jogos_15,
        jogos_18,
        estatisticas,
        relatorio_avaliador
    )

    print("✅ Treinamento finalizado com sucesso")
