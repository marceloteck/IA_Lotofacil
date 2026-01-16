from collections import defaultdict


class Avaliador:
    def __init__(self):
        self.total = 0
        self.soma_pontos = 0
        self.distribuicao = defaultdict(int)
        self.premiados = 0

    def registrar(self, pontos):
        self.total += 1
        self.soma_pontos += pontos
        self.distribuicao[pontos] += 1
        if pontos >= 11:
            self.premiados += 1

    def relatorio(self):
        media = round(self.soma_pontos / self.total, 2) if self.total else 0
        taxa_premio = round((self.premiados / self.total) * 100, 2) if self.total else 0

        print("\n📊 RELATÓRIO DE DESEMPENHO")
        print("-" * 40)
        print(f"Jogos avaliados : {self.total}")
        print(f"Média de pontos : {media}")
        print(f"Jogos 11+       : {self.premiados}")
        print(f"Taxa premiada  : {taxa_premio}%")
        print("\nDistribuição de pontos:")

        for pontos in sorted(self.distribuicao):
            print(f"  {pontos} pontos → {self.distribuicao[pontos]} jogos")

    def resumo(self):
        return {
            "Jogos avaliados": self.total,
            "Média de pontos": round(self.soma_pontos / self.total, 2) if self.total else 0,
            "Jogos 11+": self.premiados,
            "Taxa premiada (%)": round((self.premiados / self.total) * 100, 2) if self.total else 0
        }

    def relatorio_texto(self):
        linhas = []
        linhas.append("📊 RELATÓRIO DE DESEMPENHO")
        linhas.append("-" * 40)
        linhas.append(f"Jogos avaliados : {self.total}")
        linhas.append(f"Média de pontos : {self.media():.2f}")
        linhas.append(f"Jogos 11+       : {self.premiados}")
        linhas.append(f"Taxa premiada  : {self.taxa():.2f}%\n")

        linhas.append("Distribuição de pontos:")
        for pontos, qtd in sorted(self.distribuicao.items()):
            linhas.append(f"  {pontos} pontos → {qtd} jogos")

        return "\n".join(linhas) + "\n\n"
