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
# 📤 CHECKPOINT GIT (SAÍDA CONTROLADA)
# ==========================================================

def git_checkpoint(concurso_atual):
    try:
        subprocess.run(
            ["git", "config", "--global", "user.name", "github-actions[bot]"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        subprocess.run(
            ["git", "config", "--global", "user.email", "github-actions[bot]@users.noreply.github.com"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        subprocess.run(
            ["git", "add", "."],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        diff = subprocess.run(
            ["git", "diff", "--cached", "--quiet"]
        )

        if diff.returncode != 0:
            mensagem_commit = (
                f"🧠 Checkpoint automático | Concurso {concurso_atual} | "
                f"{datetime.now():%Y-%m-%d %H:%M:%S}"
            )

            commit = subprocess.run(
                ["git", "commit", "-m", mensagem_commit],
                capture_output=True,
                text=True
            )

            push = subprocess.run(
                ["git", "push"],
                capture_output=True,
                text=True
            )

            # ===============================
            # 📤 SAÍDA ORGANIZADA
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
    jogos_foco_1415 = []

    for i in range(len(resultados) - 1):
        concurso_atual = resultados[i]["concurso"]
        dezenas_reais = resultados[i + 1]["dezenas"]

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
                        f"Concurso {concurso_atual} | Pontos: {pontos} | Tamanho: {len(jogo)}"
                    )

        print(
            f"📘 Concurso {concurso_atual} → previsão {concurso_atual + 1} | "
            f"Últimos pontos: {pontos}"
        )

        # 🚀 CHECKPOINT GIT
        git_checkpoint(concurso_atual)

    print("\n✅ Treinamento finalizado com sucesso")

# ==========================================================
# ▶️ EXECUÇÃO
# ==========================================================

if __name__ == "__main__":
    treinar_sequencial()
