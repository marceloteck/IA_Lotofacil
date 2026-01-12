import json
from collections import Counter
from src.db.memoria_sqlite import carregar_memoria_premiada

ARQUIVO_PERFIL = "src/memory/perfil_vencedor.json"

def gerar_perfil_vencedor():
    jogos = carregar_memoria_premiada()

    if not jogos:
        print("⚠️ Nenhum jogo premiado para aprendizado")
        return

    contador = Counter()
    pares = []
    somas = []

    for jogo in jogos:
        dezenas = jogo["dezenas"]
        contador.update(dezenas)
        pares.append(sum(1 for d in dezenas if d % 2 == 0))
        somas.append(sum(dezenas))

    perfil = {
        "frequencia_dezenas": dict(contador),
        "media_pares": sum(pares) / len(pares),
        "media_soma": sum(somas) / len(somas),
        "total_jogos": len(jogos)
    }

    with open(ARQUIVO_PERFIL, "w", encoding="utf-8") as f:
        json.dump(perfil, f, indent=4)

    print("🧠 Perfil vencedor atualizado com sucesso")
