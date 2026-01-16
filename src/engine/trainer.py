from src.engine.motor_multicerebro import gerar_jogo
from src.engine.aprendiz import gerar_perfil_vencedor

from src.engine.avaliador import Avaliador
from src.db.memoria_sqlite import salvar_jogo_premiado
from src.utils.comparador import contar_acertos
from src.utils.dados import carregar_resultados

from src.engine.gerador_final import gerar_jogos_finais
from src.reports.relatorio_txt import salvar_relatorio

from src.engine.motor_multicerebro import obter_total_dezenas_atual


def treinar_sequencial():
    print("🧠 Treinamento sequencial iniciado")

    resultados = carregar_resultados()
    # 🔥 GARANTIR ORDEM CRONOLÓGICA (antigo → novo)
    resultados = sorted(resultados, key=lambda x: x["concurso"])
    
    avaliador = Avaliador()

    contador_dezenas = {}
    
    for i in range(len(resultados) - 1):
        concurso_atual = resultados[i]["concurso"]
        dezenas_reais = resultados[i + 1]["dezenas"]     

        jogo = gerar_jogo()
        pontos = contar_acertos(jogo, dezenas_reais)

        avaliador.registrar(pontos)

        total_dezenas_usadas = obter_total_dezenas_atual()
        contador_dezenas[total_dezenas_usadas] = (
            contador_dezenas.get(total_dezenas_usadas, 0) + 1
        )


        print(
            f"📘 Concurso {concurso_atual} → tentando prever {concurso_atual + 1} | Pontos: {pontos}"
        )

        if pontos >= 11:
            print("💰 JOGO PREMIADO! Salvando na memória")
            salvar_jogo_premiado(concurso_atual, jogo, pontos)

    gerar_perfil_vencedor()
    avaliador.relatorio()

    jogos_15, jogos_18 = gerar_jogos_finais()
    estatisticas = avaliador.resumo()


    estatisticas["dezenas_treinamento"] = contador_dezenas

    relatorio_avaliador = avaliador.relatorio_texto()


    salvar_relatorio(jogos_15, jogos_18, estatisticas, relatorio_avaliador)


    print("✅ Treinamento finalizado")
