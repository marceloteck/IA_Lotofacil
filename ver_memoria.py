from src.db.memoria_sqlite import carregar_memoria_premiada

premios = carregar_memoria_premiada(min_pontos=11)

print("\n🏆 JOGOS PREMIADOS (11+ pontos)\n")

if not premios:
    print("Nenhum jogo premiado encontrado.")
else:
    for p in premios:
        concurso = p["concurso"]
        pontos = p["pontos"]
        jogo = p["dezenas"]

        print(f"Concurso {concurso} | {pontos} pontos | {jogo}")
