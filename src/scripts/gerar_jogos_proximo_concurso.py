"""
🔮 GERADOR DE JOGOS — PRÓXIMO CONCURSO
Usa todo o aprendizado da IA sem rodar treinamento.
"""

from src.engine.gerador_final import gerar_jogos_finais
from src.engine.aprendiz import obter_perfil_vencedor
from src.engine.motor_multicerebro import obter_total_dezenas_atual


def gerar_jogos_proximo_concurso():
    print("\n🔮 GERANDO JOGOS PARA O PRÓXIMO CONCURSO\n")

    # 🔎 Garantir que existe aprendizado
    perfil = obter_perfil_vencedor()
    if not perfil:
        print("❌ Nenhum perfil vencedor encontrado.")
        print("➡️ Execute o treinamento pelo menos uma vez.")
        return

    # 🎯 Geração final
    jogos_15, jogos_18 = gerar_jogos_finais()

    # 📊 Info do motor
    dezenas_motor = obter_total_dezenas_atual()

    print(f"🧠 Motor ativo com {dezenas_motor} dezenas no momento\n")

    print("=" * 50)
    print("🎯 10 JOGOS — 15 DEZENAS\n")

    for i, jogo in enumerate(jogos_15, 1):
        print(f"Jogo {i:02d}: {jogo}")

    print("\n" + "=" * 50)
    print("🎯 7 JOGOS — 18 DEZENAS\n")

    for i, jogo in enumerate(jogos_18, 1):
        print(f"Jogo {i:02d}: {jogo}")

    print("\n✅ Jogos gerados com base no aprendizado atual\n")


if __name__ == "__main__":
    gerar_jogos_proximo_concurso()
