from collections import defaultdict


class Avaliador:
    def __init__(self):
        self.total = 0
        self.soma_pontos = 0
        self.soma_pesos = 0.0

        self.distribuicao = defaultdict(int)
        self.distribuicao_peso = defaultdict(float)

        self.premiados = 0

    def peso_aprendizado(self, pontos):
        if pontos >= 15:
            return 3.0
        elif pontos >= 14:
            return 2.0
        elif pontos >= 12:
            return 1.0
        elif pontos >= 11:
            return 0.4
        else:
            return 0.2

    def registrar(self, pontos):
        peso = self.peso_aprendizado(pontos)

        self.total += 1
        self.soma_pontos += pontos
        self.soma_pesos += peso

        self.distribuicao[pontos] += 1
        self.distribuicao_peso[pontos] += peso

        if pontos >= 11:
            self.premiados += 1

    # -------------------------------
    # MÉTRICAS
    # -------------------------------
    def media(self):
        return self.soma_pontos / self.total if self.total else 0

    def media_ponderada(self):
        return self.soma_pontos / self.soma_pesos if self.soma_pesos else 0

    def taxa(self):
        return (self.premiados / self.total) * 100 if self.total else 0

    def relatorio(self):
        print("\n📊 RELATÓRIO DE DESEMPENHO")
        print("-" * 40)
        print(f"Jogos avaliados        : {self.total}")
        print(f"Média simples          : {self.media():.2f}")
        print(f"Média ponderada        : {self.media_ponderada():.2f}")
        print(f"Jogos 11+              : {self.premiados}")
        print(f"Taxa premiada          : {self.taxa():.2f}%")

        print("\nDistribuição de pontos (peso):")
        for pontos in sorted(self.distribuicao):
            print(
                f"  {pontos} pontos → {self.distribuicao[pontos]} jogos "
                f"(peso acumulado: {self.distribuicao_peso[pontos]:.2f})"
            )

    def resumo(self):
        return {
            "Jogos avaliados": self.total,
            "Média simples": round(self.media(), 2),
            "Média ponderada": round(self.media_ponderada(), 2),
            "Jogos 11+": self.premiados,
            "Taxa premiada (%)": round(self.taxa(), 2)
        }

    def relatorio_texto(self):
        linhas = []
        linhas.append("📊 RELATÓRIO DE DESEMPENHO")
        linhas.append("-" * 40)
        linhas.append(f"Jogos avaliados        : {self.total}")
        linhas.append(f"Média simples          : {self.media():.2f}")
        linhas.append(f"Média ponderada        : {self.media_ponderada():.2f}")
        linhas.append(f"Jogos 11+              : {self.premiados}")
        linhas.append(f"Taxa premiada          : {self.taxa():.2f}%\n")

        linhas.append("Distribuição de pontos (peso):")
        for pontos in sorted(self.distribuicao):
            linhas.append(
                f"  {pontos} pontos → {self.distribuicao[pontos]} jogos "
                f"(peso: {self.distribuicao_peso[pontos]:.2f})"
            )

        return "\n".join(linhas) + "\n\n"
