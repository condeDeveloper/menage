"""A mesa, e o que exatamente esta sendo contado.

O problema dos casais, posto por Edouard Lucas em 1891: `n` casais sentam numa
mesa redonda de 2n lugares, alternando homem e mulher, e ninguem pode ficar ao
lado do proprio conjuge. De quantos jeitos da?

Fixando as mulheres nos lugares pares (o que divide o total por 2n e pelo
espelho, e e por isso que o numero de Lucas e o resultado vezes 2 * n!), sobra
escolher qual marido senta em cada lugar impar. O lugar impar 2j+1 fica entre a
mulher j e a mulher j+1, entao o marido que senta ali nao pode ser o j nem o
j+1. O que resta e contar permutacoes com duas proibicoes por posicao.
"""


def proibidos(n):
    """Para cada lugar impar, quais maridos nao podem sentar ali."""
    return [(j, (j + 1) % n) for j in range(n)]


def arranjo_valido(permutacao):
    """A permutacao poe um marido ao lado da propria esposa?

    `permutacao[j]` e o marido que senta no lugar impar `2j+1`.
    """
    n = len(permutacao)
    for j, marido in enumerate(permutacao):
        if marido == j or marido == (j + 1) % n:
            return False
    return True


def total_na_mesa(u, n):
    """O numero de Lucas: o jeito de sentar todo mundo, contando as mulheres.

    As mulheres podem ser colocadas de 2 * n! maneiras nos lugares pares (n!
    ordens e dois sentidos), e para cada uma delas ha `u` jeitos de sentar os
    maridos.
    """
    fatorial = 1
    for k in range(2, n + 1):
        fatorial *= k
    return 2 * fatorial * u
