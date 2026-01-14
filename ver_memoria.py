import os
from src.db.memoria_sqlite import carregar_memoria_premiada

# Configuração de caminhos
caminho_diretorio = os.path.join("src", "memory")
caminho_arquivo = os.path.join(caminho_diretorio, "memoriaSalva.txt")

# Garante que o diretório exista
os.makedirs(caminho_diretorio, exist_ok=True)

print("\n🏆 JOGOS PREMIADOS (Ordenados por Pontuação)\n")

jogos = carregar_memoria_premiada()

if not jogos:
    print("Nenhum jogo premiado encontrado.")
    # Opcional: limpa o arquivo txt se não houver dados
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write("Nenhum jogo premiado encontrado.\n")
else:
    # ORDENAÇÃO: Pega a lista 'jogos' e ordena pela chave 'pontos' de forma reversa (maior para menor)
    jogos_ordenados = sorted(jogos, key=lambda x: x['pontos'], reverse=True)

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        for j in jogos_ordenados:
            linha = f"{j['pontos']} pontos | {j['dezenas']}"
            
            # Mostra no console
            print(linha)
            # Salva no arquivo TXT
            f.write(linha + "\n")

    print(f"\n✅ {len(jogos_ordenados)} jogos salvos e ordenados em: {caminho_arquivo}")