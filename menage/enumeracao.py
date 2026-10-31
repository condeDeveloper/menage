"""O primeiro caminho: gerar todas as n! permutacoes e olhar uma por uma.

E o mais burro dos tres, e por isso e o juiz dos outros dois. Nao usa formula,
nao usa recorrencia e nao sabe nada sobre o problema: so monta cada permutacao e
pergunta se ela serve.
"""

from itertools import permutations

from .mesa import arranjo_valido


def contar(n):
    """Quantas permutacoes de `n` maridos evitam as duas proibicoes."""
    if n < 1:
        raise ValueError("%d nao e um numero de casais" % n)
    return sum(1 for p in permutations(range(n)) if arranjo_valido(p))


def listar(n):
    """As permutacoes que servem, em ordem lexicografica."""
    return [p for p in permutations(range(n)) if arranjo_valido(p)]


def quantas_olhadas(n):
    """Quantas permutacoes a enumeracao precisa olhar: todas elas."""
    total = 1
    for k in range(2, n + 1):
        total *= k
    return total
