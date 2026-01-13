from src.db.memoria_sqlite import carregar_memoria_premiada

print("\n🏆 JOGOS PREMIADOS (11+ pontos)\n")

jogos = carregar_memoria_premiada()

if not jogos:
    print("Nenhum jogo premiado encontrado.")
else:
    for j in jogos:
        print(f"{j['pontos']} pontos | {j['dezenas']}")
