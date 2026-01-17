from collections import Counter

from src.engine.motor_multicerebro import gerar_jogo
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

from src.logger import log_treinamento

log_treinamento("🧠 Treinamento iniciado")

# ===============================
# ⚙️ CONFIGURAÇÃO DE APRENDIZADO
# ===============================

APRENDIZADO_MULTIPLO = True
MODO_FOCO_1415 = True  # ← ATIVO

CONFIG_JOGOS_TREINO = {
    16: 5,
    18: 3,
    20: 2
}

def treinar_sequencial():
    print("🧠 Treinamento sequencial iniciado")

    resultados = carregar_resultados()
    resultados = sorted(resultados, key=lambda x: x["concurso"])

    avaliador = Avaliador()
    contador_dezenas = Counter()

    historico_dezenas = []

    # 🔥 BUFFER DE APRENDIZADO FOCO 14/15
    jogos_foco_1415 = []

    for i in range(len(resultados) - 1):
        concurso_atual = resultados[i]["concurso"]
        dezenas_atual = resultados[i]["dezenas"]
        dezenas_reais = resultados[i + 1]["dezenas"]

        historico_dezenas.append(dezenas_atual)

        # ===============================
        # 🎓 TREINO MULTIPLO CONTROLADO
        # ===============================
        if APRENDIZADO_MULTIPLO:
            for tamanho, quantidade in CONFIG_JOGOS_TREINO.items():
                for _ in range(quantidade):
                    jogo = gerar_jogo()

                    pontos = contar_acertos(jogo, dezenas_reais)
                    avaliador.registrar(pontos)

                    contador_dezenas[len(jogo)] += 1

                    # 💾 Memória geral (>=11)
                    if pontos >= 11:
                        salvar_jogo_premiado(concurso_atual, jogo, pontos)

                    # 🔥 FOCO REAL 14/15 (aprendizado incremental)
                    if MODO_FOCO_1415 and pontos >= 14:
                        jogos_foco_1415.append({
                            "concurso": concurso_atual,
                            "jogo": jogo,
                            "pontos": pontos
                        })
                        log_treinamento(
                            f"🔥 FOCO 14/15 | Concurso {concurso_atual} | Pontos: {pontos}"
                        )

                    log_treinamento(
                        f"Concurso {concurso_atual} | Pontos: {pontos} | Tamanho: {len(jogo)}"
                    )

        else:
            jogo = gerar_jogo()
            pontos = contar_acertos(jogo, dezenas_reais)

            avaliador.registrar(pontos)
            contador_dezenas[len(jogo)] += 1

            if pontos >= 11:
                salvar_jogo_premiado(concurso_atual, jogo, pontos)

        print(
            f"📘 Concurso {concurso_atual} → previsão {concurso_atual + 1} | Últimos pontos: {pontos}"
        )

    # ===============================
    # 🔥 CONSOLIDA APRENDIZADO 14/15
    # ===============================
    if jogos_foco_1415:
        for item in jogos_foco_1415:
            salvar_jogo_premiado(
                item["concurso"],
                item["jogo"],
                item["pontos"]
            )

        log_treinamento(
            f"🔥 Total de jogos 14/15 aprendidos: {len(jogos_foco_1415)}"
        )

    # ===============================
    # 🧠 PERFIL VENCEDOR
    # ===============================
    gerar_perfil_vencedor()
    avaliador.relatorio()

    # ===============================
    # 🔥 ESTATÍSTICAS REAIS
    # ===============================
    dezenas_quentes, dezenas_frias = calcular_dezenas_quentes_frias()
    ultimo_resultado = resultados[-1]["dezenas"]

    # ===============================
    # ⚙️ CALIBRAÇÃO DE PESOS
    # ===============================
    jogos_1415 = carregar_jogos_premiados(min_pontos=14)

    if jogos_1415:
        pesos_calibrados = calibrar_pesos(jogos_1415)
        print("⚙️ Pesos calibrados:", pesos_calibrados)
        log_treinamento("⚙️ Pesos calibrados com jogos 14/15")
    else:
        pesos_calibrados = None
        print("⚠️ Sem jogos 14/15 suficientes")
        log_treinamento("⚠️ Sem jogos 14/15 para calibração")

    # ===============================
    # 🎯 GERAÇÃO FINAL
    # ===============================
    jogos_15, jogos_18 = gerar_jogos_finais(
        dezenas_quentes=dezenas_quentes,
        dezenas_frias=dezenas_frias,
        ultimo_resultado=ultimo_resultado,
        pesos=pesos_calibrados
    )

    # ===============================
    # 📄 RELATÓRIO
    # ===============================
    estatisticas = avaliador.resumo()
    estatisticas["dezenas_treinamento"] = dict(contador_dezenas)

    relatorio_avaliador = avaliador.relatorio_texto()

    salvar_relatorio(
        jogos_15,
        jogos_18,
        estatisticas,
        relatorio_avaliador
    )

    print("✅ Treinamento finalizado com sucesso")
