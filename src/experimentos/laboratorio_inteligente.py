import os
import csv
import datetime
import statistics
from collections import Counter

from src.engine.motor_multicerebro import gerar_jogo
from src.engine.avaliador import contar_acertos
from src.db.memoria_sqlite import carregar_jogos_memoria

# NN consultiva (opcional)
try:
    from src.engine.cerebro_neural import avaliar_ciclo
    NN_ATIVA = True
except ImportError:
    NN_ATIVA = False


# ===============================
# 📁 PASTA DE RELATÓRIOS
# ===============================
BASE_DIR = os.path.dirname(__file__)
RELATORIOS_DIR = os.path.join(BASE_DIR, "relatorios")
os.makedirs(RELATORIOS_DIR, exist_ok=True)

DATA_TAG = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")


# ===============================
# 🎛️ ESTRATÉGIAS
# ===============================
ESTRATEGIAS = [
    {"nome": "padrao", "usar_nn": False},
    {"nome": "nucleo_forte", "usar_nn": False},
    {"nome": "nn_consultiva", "usar_nn": True},
]

CICLOS = 50
LIMITE_OVERFITTING = 0.70


# ===============================
# 🔁 EXECUTA CICLO
# ===============================
def executar_ciclo(concursos):
    pontos = []
    dezenas_usadas = Counter()

    for concurso_real in concursos:
        jogo = gerar_jogo()
        p = contar_acertos(jogo, concurso_real)
        pontos.append(p)

        if p >= 11:
            dezenas_usadas.update(jogo)

    return pontos, dezenas_usadas


# ===============================
# 📊 MÉTRICAS
# ===============================
def coletar_metricas(pontos):
    return {
        "media": statistics.mean(pontos),
        "taxa_11": sum(1 for p in pontos if p >= 11) / len(pontos),
        "desvio": statistics.pstdev(pontos),
    }


# ===============================
# 🚨 OVERFITTING
# ===============================
def detectar_overfitting(metricas, dezenas_usadas):
    if metricas["taxa_11"] > LIMITE_OVERFITTING:
        return True

    if dezenas_usadas:
        top = dezenas_usadas.most_common(5)
        concentracao = sum(v for _, v in top) / sum(dezenas_usadas.values())
        if concentracao > 0.45:
            return True

    return False


# ===============================
# 🧪 LABORATÓRIO
# ===============================
def executar_laboratorio():
    memoria = carregar_jogos_memoria()
    concursos = [j for j, _ in memoria[-500:]]

    ranking = []
    relatorio_txt = []

    for estrategia in ESTRATEGIAS:
        medias = []
        taxas = []

        for _ in range(CICLOS):
            pontos, dezenas = executar_ciclo(concursos)
            m = coletar_metricas(pontos)

            # Avaliação NN (consultiva)
            if estrategia["usar_nn"] and NN_ATIVA:
                score_nn = avaliar_ciclo(pontos)
                if score_nn < 0.5:
                    continue  # descarta ciclo fraco

            medias.append(m["media"])
            taxas.append(m["taxa_11"])

        media_final = statistics.mean(medias)
        taxa_final = statistics.mean(taxas)

        ranking.append({
            "estrategia": estrategia["nome"],
            "media": media_final,
            "taxa_11": taxa_final
        })

        relatorio_txt.append(
            f"Estratégia: {estrategia['nome']}\n"
            f"  Média pontos: {media_final:.2f}\n"
            f"  Taxa 11+: {taxa_final*100:.2f}%\n"
            "-" * 40
        )

    salvar_relatorio_txt(relatorio_txt)
    salvar_ranking_csv(ranking)


# ===============================
# 💾 SALVAR RELATÓRIOS
# ===============================
def salvar_relatorio_txt(linhas):
    caminho = os.path.join(RELATORIOS_DIR, f"laboratorio_{DATA_TAG}.txt")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))


def salvar_ranking_csv(ranking):
    ranking = sorted(ranking, key=lambda x: x["taxa_11"], reverse=True)
    caminho = os.path.join(RELATORIOS_DIR, f"ranking_estrategias_{DATA_TAG}.csv")

    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["estrategia", "media", "taxa_11"])
        writer.writeheader()
        for r in ranking:
            writer.writerow(r)


# ===============================
# 🚀 MAIN
# ===============================
if __name__ == "__main__":
    print("\n🧪 LABORATÓRIO INTELIGENTE INICIADO\n")
    executar_laboratorio()
    print("✅ Relatórios e ranking gerados com sucesso\n")
