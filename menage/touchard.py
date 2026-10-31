"""O terceiro caminho: a formula fechada de Touchard, de 1934.

    U(n) = soma de k=0 ate n de (-1)^k * (2n / (2n - k)) * C(2n - k, k) * (n-k)!

Ela responde n = 1.000 em milissegundos, enquanto a enumeracao nao termina nem
para n = 20 e a tabela de mascaras precisaria de 2^1000 estados.

O preco e o cancelamento: os termos alternam de sinal e o maior deles fica em
quinze vezes a resposta, de vinte casais em diante. Em aritmetica inteira isso
nao custa nada, porque o Python nao perde digito. Em ponto flutuante custa os
ultimos digitos: a partir de vinte e dois casais o double ja nao devolve o valor
exato, com erro relativo na casa de 10^-15. O medidor mede os dois.
"""

from math import comb, factorial


def termos(n):
    """Os n+1 termos da soma de Touchard, com sinal, sem somar."""
    saida = []
    for k in range(n + 1):
        valor = 2 * n * comb(2 * n - k, k) * factorial(n - k) // (2 * n - k)
        saida.append(-valor if k % 2 else valor)
    return saida


def contar(n):
    """U(n) pela formula de Touchard."""
    if n < 1:
        raise ValueError("%d nao e um numero de casais" % n)
    if n == 1:
        return 0
    return sum(termos(n))


def maior_termo(n):
    """O maior termo em valor absoluto, que e quem decide o cancelamento."""
    return max(abs(t) for t in termos(n))


def por_recorrencia(ate):
    """A recorrencia de Muir, que da a mesma sequencia sem binomial nenhum.

        (n - 2) * U(n) = n * (n - 2) * U(n-1) + n * U(n-2) + 4 * (-1)^(n+1)

    Vale de n = 3 em diante. E um quarto caminho, e ele existe aqui porque usa
    uma identidade completamente diferente da de Touchard: se os dois
    concordarem em cinquenta valores, nenhum dos dois esta errado por acaso.
    """
    u = {1: 0, 2: 0, 3: 1}
    for n in range(4, ate + 1):
        sinal = 4 if (n + 1) % 2 == 0 else -4
        u[n] = (n * (n - 2) * u[n - 1] + n * u[n - 2] + sinal) // (n - 2)
    return {n: u[n] for n in sorted(u) if n <= ate}
