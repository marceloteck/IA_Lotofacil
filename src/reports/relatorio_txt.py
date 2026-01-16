import os
from datetime import datetime


def salvar_relatorio(jogos_15, jogos_18, estatisticas, relatorio_avaliador):
    # 📁 Diretório base do projeto
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # 📁 src/reports/relatorios
    DIR_RELATORIOS = os.path.join(BASE_DIR, "relatorios")
    os.makedirs(DIR_RELATORIOS, exist_ok=True)

    # 🗓️ Nome do arquivo
    data = datetime.now().strftime("%Y-%m-%d_%H-%M")
    caminho = os.path.join(
        DIR_RELATORIOS,
        f"relatorio_{data}.txt"
    )


    with open(caminho, "w", encoding="utf-8") as f:
        f.write(relatorio_avaliador)
        f.write("=" * 50 + "\n\n")
        
        f.write("📊 RELATÓRIO FINAL — IA LOTOFÁCIL\n")
        f.write("=" * 50 + "\n\n")

        f.write("🔹 ESTATÍSTICAS DO TREINAMENTO\n")
        for k, v in estatisticas.items():
            f.write(f"{k}: {v}\n")

        # ==========================================
        # 🔢 NOVO BLOCO — DISTRIBUIÇÃO DE DEZENAS
        # ==========================================
        if "dezenas_treinamento" in estatisticas:
            f.write("\n" + "-" * 50 + "\n")
            f.write("🔢 DISTRIBUIÇÃO DE DEZENAS NO TREINAMENTO\n\n")

            for dezenas, total in sorted(estatisticas["dezenas_treinamento"].items()):
                f.write(f"{dezenas} dezenas → {total} ciclos\n")

        f.write("\n" + "=" * 50 + "\n")
        f.write("🎯 10 JOGOS — 15 DEZENAS\n\n")

        for i, jogo in enumerate(jogos_15, 1):
            f.write(f"Jogo {i:02d}: {jogo}\n")

        f.write("\n" + "=" * 50 + "\n")
        f.write("🎯 7 JOGOS — 18 DEZENAS\n\n")

        for i, jogo in enumerate(jogos_18, 1):
            f.write(f"Jogo {i:02d}: {jogo}\n")

    print(f"\n📄 Relatório salvo em: {caminho}")