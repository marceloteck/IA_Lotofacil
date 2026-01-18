# src/engine/filtro_identidade.py

class FiltroIdentidade:
    """
    🧠 Filtro histórico anti-repetição
    Bloqueia identidade total e repulsa similaridade extrema
    """

    def __init__(self, historico, limite_intersecao=14):
        self.historico = [set(j) for j in historico]
        self.limite = limite_intersecao

    def avaliar(self, jogo):
        """
        Retorna:
        - valido (bool)
        - penalidade (float)
        """
        jogo_set = set(jogo)
        maior_intersecao = 0

        for concurso in self.historico:
            inter = len(jogo_set & concurso)

            if inter == len(jogo_set):
                return False, -9999  # identidade total

            maior_intersecao = max(maior_intersecao, inter)

        # Penalização suave
        penalidade = 0
        if maior_intersecao == 14:
            penalidade = -18
        elif maior_intersecao == 13:
            penalidade = -9
        elif maior_intersecao == 12:
            penalidade = -4

        return True, penalidade
