import json
import os
from collections import Counter
from src.db.memoria_sqlite import carregar_memoria_premiada

ARQUIVO_PERFIL = "src/memory/perfil_vencedor.json"


def gerar_perfil_vencedor():
    jogos = carregar_memoria_premiada()

    if not jogos:
        print("⚠️ Nenhum jogo premiado (11+) para aprendizado")
        return

    contador = Counter()
    pares = []
    somas = []

    for jogo in jogos:
        dezenas = jogo["dezenas"]
        contador.update(dezenas)
        pares.append(sum(1 for d in dezenas if d % 2 == 0))
        somas.append(sum(dezenas))

    # 🔥 TOP dezenas mais recorrentes
    top_dezenas = [int(d) for d, _ in contador.most_common(15)]

    perfil = {
        "top_dezenas": top_dezenas,
        "frequencia_dezenas": dict(contador),
        "media_pares": round(sum(pares) / len(pares), 2),
        "media_soma": round(sum(somas) / len(somas), 2),
        "total_jogos": len(jogos)
    }

    os.makedirs("src/memory", exist_ok=True)

    with open(ARQUIVO_PERFIL, "w", encoding="utf-8") as f:
        json.dump(perfil, f, indent=4, ensure_ascii=False)

    print(f"🧠 Perfil vencedor aprendido com {len(jogos)} jogos")


def obter_perfil_vencedor():
    """
    Retorna APENAS uma lista de dezenas (contrato fixo)
    """
    if not os.path.exists(ARQUIVO_PERFIL):
        return []

    with open(ARQUIVO_PERFIL, "r", encoding="utf-8") as f:
        perfil = json.load(f)

    return perfil.get("top_dezenas", [])
