import unittest
from itertools import permutations

from menage.mesa import arranjo_valido, proibidos, total_na_mesa


class TestProibicoes(unittest.TestCase):
    def test_cada_lugar_proibe_dois_maridos(self):
        self.assertEqual(proibidos(4), [(0, 1), (1, 2), (2, 3), (3, 0)])

    def test_o_ultimo_lugar_fecha_o_circulo(self):
        self.assertEqual(proibidos(5)[-1], (4, 0))

    def test_com_um_casal_so_a_proibicao_se_repete(self):
        self.assertEqual(proibidos(1), [(0, 0)])


class TestArranjo(unittest.TestCase):
    def test_a_identidade_nunca_serve(self):
        for n in range(1, 8):
            self.assertFalse(arranjo_valido(tuple(range(n))))

    def test_o_unico_arranjo_de_tres_casais(self):
        validos = [p for p in permutations(range(3)) if arranjo_valido(p)]
        self.assertEqual(validos, [(2, 0, 1)])

    def test_os_dois_arranjos_de_quatro_casais(self):
        validos = [p for p in permutations(range(4)) if arranjo_valido(p)]
        self.assertEqual(validos, [(2, 3, 0, 1), (3, 0, 1, 2)])

    def test_nenhum_valido_tem_marido_ao_lado_da_esposa(self):
        for n in range(3, 8):
            for p in permutations(range(n)):
                if arranjo_valido(p):
                    for j, marido in enumerate(p):
                        self.assertNotEqual(marido, j)
                        self.assertNotEqual(marido, (j + 1) % n)


class TestTotal(unittest.TestCase):
    def test_tres_casais_dao_doze_jeitos(self):
        self.assertEqual(total_na_mesa(1, 3), 12)

    def test_a_conta_e_dois_vezes_fatorial(self):
        self.assertEqual(total_na_mesa(1, 4), 2 * 24)
        self.assertEqual(total_na_mesa(13, 5), 2 * 120 * 13)
