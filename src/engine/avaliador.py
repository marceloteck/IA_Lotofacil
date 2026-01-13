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
