"""Roda as contagens e imprime as tabelas do README.

    python -m ferramentas.medidor
    python -m ferramentas.medidor --completo   # enumeracao ate 11 casais

Nenhum numero do README foi digitado a mao, e todos estao presos em
testes/test_medidas.py.
"""

import sys
import time
from math import exp, factorial

from menage import enumeracao, mascaras, touchard
from menage.mesa import total_na_mesa

COMPLETO = "--completo" in sys.argv
ATE_ENUMERACAO = 11 if COMPLETO else 9
ATE_MASCARAS = 16
ATE_FORMULA = 60


def milhar(n):
    return "{:,}".format(n).replace(",", ".")


def main():
    comeco = time.time()

    print("## Os quatro caminhos\n")
    recorrencia = touchard.por_recorrencia(ATE_MASCARAS)
    print("| casais | enumeracao | mascaras | Touchard | recorrencia de Muir | concordam |")
    print("|---|---|---|---|---|---|")
    for n in range(1, ATE_MASCARAS + 1):
        e = enumeracao.contar(n) if n <= ATE_ENUMERACAO else None
        m = mascaras.contar(n)
        t = touchard.contar(n)
        r = recorrencia[n]
        valores = [v for v in (e, m, t, r) if v is not None]
        print(
            "| %d | %s | %s | %s | %s | %s |"
            % (
                n,
                milhar(e) if e is not None else "nao terminou",
                milhar(m),
                milhar(t),
                milhar(r),
                "sim" if len(set(valores)) == 1 else "NAO",
            )
        )

    print("\n## O custo de cada caminho\n")
    print("| casais | permutacoes olhadas | estados das mascaras | quantas vezes menos |")
    print("|---|---|---|---|")
    for n in (8, 10, 12, 14, 16, 20):
        p = enumeracao.quantas_olhadas(n)
        e = mascaras.quantos_estados(n)
        print("| %d | %s | %s | %s |" % (n, milhar(p), milhar(e), milhar(p // e)))

    print("\n## O cancelamento da formula de Touchard\n")
    print("| casais | maior termo | resultado | o maior termo e quantas vezes o resultado |")
    print("|---|---|---|---|")
    for n in (5, 10, 20, 40, 60):
        maior = touchard.maior_termo(n)
        resultado = touchard.contar(n)
        print(
            "| %d | %s | %s | %s |"
            % (n, milhar(maior), milhar(resultado), milhar(maior // resultado))
        )
    print()
    print("digitos do maior termo e do resultado em n = 60: %d e %d"
          % (len(str(touchard.maior_termo(60))), len(str(touchard.contar(60)))))

    print("\n## Somar os mesmos termos em ponto flutuante\n")
    primeiro_erro = None
    for n in range(3, ATE_FORMULA + 1):
        certo = touchard.contar(n)
        em_float = sum(float(t) for t in touchard.termos(n))
        if em_float != float(certo) and primeiro_erro is None:
            primeiro_erro = n
    print("| casais | inteiro | double | erro relativo |")
    print("|---|---|---|---|")
    for n in (15, 20, 30, 60):
        certo = touchard.contar(n)
        em_float = sum(float(t) for t in touchard.termos(n))
        erro = abs(em_float - certo) / certo
        print("| %d | %s | %.6e | %.3e |" % (n, milhar(certo), em_float, erro))
    print()
    print("o primeiro n em que o double ja nao devolve o valor exato: %d" % primeiro_erro)

    print("\n## A fatia de arranjos que sobra\n")
    alvo = exp(-2)
    print("| casais | U(n) | n! | U(n)/n! | distancia de e^-2 |")
    print("|---|---|---|---|---|")
    for n in (3, 5, 10, 20, 40, 60):
        u = touchard.contar(n)
        f = factorial(n)
        razao = u / f
        print(
            "| %d | %s | %s | %.6f | %+.6f |"
            % (n, milhar(u), milhar(f) if n <= 20 else "%d digitos" % len(str(f)), razao, razao - alvo)
        )
    print()
    print("e^-2 = %.6f" % alvo)

    print("\n## Os numeros de Lucas: a mesa inteira\n")
    print("| casais | jeitos de sentar todo mundo |")
    print("|---|---|")
    for n in range(3, 11):
        print("| %d | %s |" % (n, milhar(total_na_mesa(touchard.contar(n), n))))

    print("\n(medido em %.1f s)" % (time.time() - comeco))


if __name__ == "__main__":
    main()
