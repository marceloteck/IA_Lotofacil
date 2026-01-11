from src.engine.memoria import listar_melhores

premios = listar_melhores()

print("\n🏆 JOGOS PREMIADOS (11+ pontos)\n")
for concurso, pontos, jogo in premios:
    print(f"Concurso {concurso} | {pontos} pontos | {jogo}")
