# ==========================================================
# 🧠 TREINAMENTO IA LOTOFÁCIL — CHECKPOINT GIT ORGANIZADO
# ==========================================================

import subprocess
from datetime import datetime
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

# ==========================================================
# 🔔 LOG INICIAL
# ==========================================================

log_treinamento("🧠 Treinamento iniciado")

# ==========================================================
# ⚙️ CONFIGURAÇÃO DE APRENDIZADO
# ==========================================================

APRENDIZADO_MULTIPLO = True
MODO_FOCO_1415 = True

CONFIG_JOGOS_TREINO = {
    16: 5,
    18: 3,
    20: 2
}

# ==========================================================
# 📤 CHECKPOINT GIT COM RETORNO ORGANIZADO
# ==========================================================

def git_checkpoint(concurso_atual):
    try:
        subprocess.run(
            ["git", "config", "--global", "user.name", "github-actions[bot]"],
            check=False
        )
        subprocess.run(
            ["git", "config", "--global", "user.email", "github-actions[bot]@users.noreply.github.com"],
            check=False
        )

        subprocess.run(["git", "add", "."], check=False)

        resultado = subprocess.run(
            ["git", "diff", "--cached", "--quiet"]
        )

        if resultado.returncode != 0:
            mensagem_commit = (
                f"🧠 Checkpoint automático | Concurso {concurso_atual} | "
                f"{datetime.now():%Y-%m-%d %H:%M:%S}"
            )

            subprocess.run(
                ["git", "commit", "-m", mensagem_commit],
                check=False
            )
            subprocess.run(["git", "push"], check=False)

            # ===============================
            # 📤 SAÍDA ORGANIZADA NO CONSOLE
            # ===============================
            print("\n" + "=" * 50)
            print("📤 COMMIT REALIZADO NO GITHUB")
            print(mensagem_commit)
            print("=" * 50 + "\n")

            log_treinamento(f"📤 Git push realizado | Concurso {concurso_atual}")

        else:
            print("\n" + "=" * 50)
            print("📭 NENHUMA ALTERAÇÃO PARA COMMIT")
            print("=" * 50 + "\n")

            log_treinamento("📭 Nenhuma alteração para commit")

    except Exception as e:
        print("\n" + "=" * 50)
        print("❌ ERRO NO CHECKPOINT GIT")
        print(str(e))
        print("=" * 50 + "\n")

        log_treinamento(f"❌ Erro no checkpoint Git: {e}")

# ==========================================================
# 🧠 TREINAMENTO SEQUENCIAL
# ==========================================================

def treinar_sequencial():
    print("🧠 Treinamento sequencial iniciado\n")

    resultados = carregar_resultados()
    resultados = sorted(resultados, key=lambda x: x["concurso"])

    avaliador = Avaliador()
    contador_dezenas = Counter()
    historico_dezenas = []

    jogos_foco_1415 = []

    for i in range(len(resultados) - 1):
        concurso_atual = resultados[i]["concurso"]
        dezenas_atual = resultados[i]["dezenas"]
        dezenas_reais = resultados[i + 1]["dezenas"]

        historico_dezenas.append(dezenas_atual)

        # ===============================
        # 🎓 TREINO MULTIPLO
        # ===============================
        if APRENDIZADO_MULTIPLO:
            for tamanho, quantidade in CONFIG_JOGOS_TREINO.items():
                for _ in range(quantidade):
                    jogo = gerar_jogo()

                    pontos = contar_acertos(jogo, dezenas_reais)
                    avaliador.registrar(pontos)
                    contador_dezenas[len(jogo)] += 1

                    if pontos >= 11:
                        salvar_jogo_premiado(concurso_atual, jogo, pontos)

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

        # ===============================
        # 📘 RETORNO DO TREINAMENTO
        # ===============================
        print(
            f"📘 Concurso {concurso_atual} → previsão {concurso_atual + 1} | "
            f"Últimos pontos: {pontos}"
        )

        # ===============================
        # 🚀 CHECKPOINT GIT AO FINAL
        # ===============================
        git_checkpoint(concurso_atual)

    # ===============================
    # 🔥 CONSOLIDA FOCO 14/15
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
    # 🔥 ESTATÍSTICAS
    # ===============================
    dezenas_quentes, dezenas_frias = calcular_dezenas_quentes_frias()
    ultimo_resultado = resultados[-1]["dezenas"]

    # ===============================
    # ⚙️ CALIBRAÇÃO DE PESOS
    # ===============================
    jogos_1415 = carregar_jogos_premiados(min_pontos=14)

    if jogos_1415:
        calibrar_pesos(jogos_1415)
        log_treinamento("⚙️ Pesos calibrados com jogos 14/15")
    else:
        log_treinamento("⚠️ Sem jogos 14/15 para calibração")

    # ===============================
    # 🎯 GERAÇÃO FINAL
    # ===============================
    jogos_15, jogos_18 = gerar_jogos_finais(
        dezenas_quentes=dezenas_quentes,
        dezenas_frias=dezenas_frias,
        ultimo_resultado=ultimo_resultado,
        pesos=None
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

    print("\n✅ Treinamento finalizado com sucesso")

# ==========================================================
# ▶️ EXECUÇÃO
# ==========================================================

if __name__ == "__main__":
    treinar_sequencial()
