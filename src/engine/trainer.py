from src.engine.motor_multicerebro import gerar_jogo
from src.engine.aprendiz import gerar_perfil_vencedor

from src.engine.avaliador import Avaliador
from src.db.memoria_sqlite import salvar_jogo_premiado
from src.utils.comparador import contar_acertos
from src.utils.dados import carregar_resultados


def treinar_sequencial():
    print("🧠 Treinamento sequencial iniciado")

    resultados = carregar_resultados()
    avaliador = Avaliador()

    for i in range(len(resultados) - 1, 0, -1):
        concurso_atual = resultados[i]["concurso"]
        dezenas_reais = resultados[i - 1]["dezenas"]

        jogo = gerar_jogo()
        pontos = contar_acertos(jogo, dezenas_reais)

        avaliador.registrar(pontos)

        print(
            f"📘 Concurso {concurso_atual} → tentando prever {concurso_atual - 1} | Pontos: {pontos}"
        )

        if pontos >= 11:
            print("💰 JOGO PREMIADO! Salvando na memória")
            salvar_jogo_premiado(concurso_atual, jogo, pontos)

    gerar_perfil_vencedor()
    avaliador.relatorio()

    print("✅ Treinamento finalizado")
