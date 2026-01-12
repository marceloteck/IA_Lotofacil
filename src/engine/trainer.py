from src.engine.motor_multicerebro import gerar_jogo
from src.engine.avaliador import contar_pontos
from src.engine.memoria import (
    inicializar_memoria,
    salvar_jogo_premiado
)
from src.db.banco import carregar_concursos
from src.engine.aprendiz import gerar_perfil_vencedor

def treinar_sequencial():
    print("🧠 Treinamento sequencial iniciado (BLOCO 6)")

    inicializar_memoria()

    concursos = carregar_concursos()

    for i in range(len(concursos) - 1):
        concurso_atual, resultado_atual = concursos[i]
        proximo_concurso, resultado_real = concursos[i + 1]

        jogo = gerar_jogo()

        pontos = contar_pontos(jogo, resultado_real)

        print(
            f"📘 Concurso {concurso_atual} → tentando prever {proximo_concurso}"
            f" | Pontos: {pontos}"
        )

        # 🔥 AQUI ESTÁ A REGRA MAIS IMPORTANTE DO PROJETO
        if pontos >= 11:
            print("💰 JOGO PREMIADO! Salvando na memória")
            salvar_jogo_premiado(
                concurso_previsto=proximo_concurso,
                jogo=jogo,
                pontos=pontos
            )
    gerar_perfil_vencedor()

    print("✅ Treinamento finalizado")
