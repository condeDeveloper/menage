"""Os quatro caminhos conferidos um contra o outro."""

import unittest
from math import comb, factorial

from menage import enumeracao, mascaras, touchard

RECORRENCIA = touchard.por_recorrencia(40)


class TestOsQuatroConcordam(unittest.TestCase):
    def test_enumeracao_contra_mascaras(self):
        for n in range(1, 10):
            self.assertEqual(enumeracao.contar(n), mascaras.contar(n), "n=%d" % n)

    def test_enumeracao_contra_touchard(self):
        for n in range(1, 10):
            self.assertEqual(enumeracao.contar(n), touchard.contar(n), "n=%d" % n)

    def test_mascaras_contra_touchard(self):
        for n in range(1, 17):
            self.assertEqual(mascaras.contar(n), touchard.contar(n), "n=%d" % n)

    def test_touchard_contra_a_recorrencia(self):
        for n in range(3, 41):
            self.assertEqual(touchard.contar(n), RECORRENCIA[n], "n=%d" % n)

    def test_a_sequencia_conhecida(self):
        # A000179 a partir de tres casais
        esperado = [1, 2, 13, 80, 579, 4738, 43387, 439792, 4890741]
        self.assertEqual([touchard.contar(n) for n in range(3, 12)], esperado)


class TestEnumeracao(unittest.TestCase):
    def test_listar_bate_com_contar(self):
        for n in range(1, 9):
            self.assertEqual(len(enumeracao.listar(n)), enumeracao.contar(n), "n=%d" % n)

    def test_quantas_olhadas_e_o_fatorial(self):
        for n in range(1, 12):
            self.assertEqual(enumeracao.quantas_olhadas(n), factorial(n), "n=%d" % n)

    def test_recusa_zero(self):
        with self.assertRaises(ValueError):
            enumeracao.contar(0)


class TestMascaras(unittest.TestCase):
    def test_o_custo_e_dois_elevado_a_n_vezes_n(self):
        self.assertEqual(mascaras.quantos_estados(10), 10240)
        self.assertEqual(mascaras.quantos_estados(16), 1048576)

    def test_recusa_zero(self):
        with self.assertRaises(ValueError):
            mascaras.contar(0)


class TestTouchard(unittest.TestCase):
    def test_a_soma_tem_n_mais_um_termos(self):
        for n in range(2, 20):
            self.assertEqual(len(touchard.termos(n)), n + 1, "n=%d" % n)

    def test_os_sinais_alternam(self):
        for n in range(2, 20):
            for k, t in enumerate(touchard.termos(n)):
                if t:
                    self.assertEqual(t < 0, k % 2 == 1, "n=%d k=%d" % (n, k))

    def test_o_primeiro_termo_e_o_fatorial(self):
        for n in range(2, 20):
            self.assertEqual(touchard.termos(n)[0], factorial(n), "n=%d" % n)

    def test_a_divisao_da_formula_e_sempre_exata(self):
        # 2n/(2n-k) * C(2n-k, k) e inteiro, mas so depois de multiplicar
        for n in range(2, 30):
            for k in range(n + 1):
                self.assertEqual(
                    (2 * n * comb(2 * n - k, k)) % (2 * n - k), 0, "n=%d k=%d" % (n, k)
                )

    def test_o_maior_termo_e_sempre_maior_que_o_resultado(self):
        for n in range(3, 40):
            self.assertGreater(touchard.maior_termo(n), touchard.contar(n), "n=%d" % n)

    def test_recusa_zero(self):
        with self.assertRaises(ValueError):
            touchard.contar(0)
