import os
from datetime import datetime


def salvar_relatorio(jogos_15, jogos_18, estatisticas):
    os.makedirs("src/reports", exist_ok=True)

    data = datetime.now().strftime("%Y-%m-%d_%H-%M")
    caminho = f"src/reports/relatorio_{data}.txt"

    with open(caminho, "w", encoding="utf-8") as f:
        f.write("📊 RELATÓRIO FINAL — IA LOTOFÁCIL\n")
        f.write("=" * 50 + "\n\n")

        f.write("🔹 ESTATÍSTICAS DO TREINAMENTO\n")
        for k, v in estatisticas.items():
            f.write(f"{k}: {v}\n")

        f.write("\n" + "=" * 50 + "\n")
        f.write("🎯 10 JOGOS — 15 DEZENAS\n\n")

        for i, jogo in enumerate(jogos_15, 1):
            f.write(f"Jogo {i:02d}: {jogo}\n")

        f.write("\n" + "=" * 50 + "\n")
        f.write("🎯 7 JOGOS — 18 DEZENAS\n\n")

        for i, jogo in enumerate(jogos_18, 1):
            f.write(f"Jogo {i:02d}: {jogo}\n")

    print(f"\n📄 Relatório salvo em: {caminho}")
