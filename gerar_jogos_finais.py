from src.engine.seletor_jogos import SeletorJogos

seletor = SeletorJogos(usar_nn=True)
jogos_finais = seletor.gerar_jogos_filtrados()

for i, jogo in enumerate(jogos_finais, 1):
    print(f"Jogo {i}: {jogo}")
