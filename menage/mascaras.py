"""O segundo caminho: programacao dinamica sobre quem ja sentou.

Em vez de montar a permutacao inteira e depois conferir, este caminho preenche
um lugar de cada vez e guarda SO o conjunto de maridos ja sentados, como uma
mascara de bits. Duas permutacoes diferentes que usaram o mesmo conjunto de
maridos valem a mesma coisa daqui para a frente, entao elas sao somadas e nunca
mais separadas.

Troca n! por 2^n * n. Em dez casais sao 3.628.800 permutacoes contra 10.240
estados; em dezesseis, 20.922.789.888.000 contra 1.048.576.
"""

from .mesa import proibidos


def contar(n):
    """O mesmo numero da enumeracao, sem gerar permutacao nenhuma."""
    if n < 1:
        raise ValueError("%d nao e um numero de casais" % n)
    proibicao = [(1 << a) | (1 << b) for a, b in proibidos(n)]
    atual = {0: 1}
    for lugar in range(n):
        veto = proibicao[lugar]
        seguinte = {}
        for usados, quantos in atual.items():
            livres = ~usados & ((1 << n) - 1) & ~veto
            resto = livres
            while resto:
                bit = resto & -resto
                chave = usados | bit
                seguinte[chave] = seguinte.get(chave, 0) + quantos
                resto -= bit
        atual = seguinte
    return sum(atual.values())


def quantos_estados(n):
    """Quantos estados a tabela de mascaras visita, no pior caso."""
    return (1 << n) * n
