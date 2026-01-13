from src.engine.motor_multicerebro import gerar_jogo
from src.engine.avaliador import contar_pontos
from src.db.banco import carregar_concursos
from src.engine.aprendiz import gerar_perfil_vencedor
from src.db.memoria_sqlite import salvar_memoria


def treinar_sequencial():
    print("🧠 Treinamento sequencial iniciado")

    concursos = carregar_concursos()

    for i in range(len(concursos) - 1):
        concurso_atual, _ = concursos[i]
        proximo_concurso, resultado_real = concursos[i + 1]

        jogo = gerar_jogo()
        pontos = contar_pontos(jogo, resultado_real)

        print(
            f"📘 Concurso {concurso_atual} → tentando prever {proximo_concurso}"
            f" | Pontos: {pontos}"
        )

        if pontos >= 11:
            print("💰 JOGO PREMIADO! Salvando na memória")
            salvar_memoria(concurso_atual, jogo, pontos)

    gerar_perfil_vencedor()
    print("✅ Treinamento finalizado")
