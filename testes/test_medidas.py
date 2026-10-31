"""Os numeros do README, presos."""

import unittest
from math import exp, factorial

from menage import enumeracao, mascaras, touchard
from menage.mesa import total_na_mesa


class TestContagens(unittest.TestCase):
    def test_os_dezesseis_primeiros(self):
        esperado = [
            0, 0, 1, 2, 13, 80, 579, 4738, 43387, 439792, 4890741, 59216642,
            775596313, 10927434464, 164806435783, 2649391469058,
        ]
        self.assertEqual([touchard.contar(n) for n in range(1, 17)], esperado)

    def test_os_tres_caminhos_ate_nove(self):
        for n in range(1, 10):
            valor = touchard.contar(n)
            self.assertEqual(enumeracao.contar(n), valor, "n=%d" % n)
            self.assertEqual(mascaras.contar(n), valor, "n=%d" % n)


class TestCusto(unittest.TestCase):
    def test_a_tabela_de_custo(self):
        esperado = {
            8: (40320, 2048, 19),
            10: (3628800, 10240, 354),
            12: (479001600, 49152, 9745),
            14: (87178291200, 229376, 380067),
            16: (20922789888000, 1048576, 19953527),
            20: (2432902008176640000, 20971520, 116009807976),
        }
        for n, (p, e, razao) in esperado.items():
            self.assertEqual(enumeracao.quantas_olhadas(n), p, "n=%d" % n)
            self.assertEqual(mascaras.quantos_estados(n), e, "n=%d" % n)
            self.assertEqual(p // e, razao, "n=%d" % n)


class TestCancelamento(unittest.TestCase):
    def test_o_maior_termo_fica_em_quinze_vezes(self):
        esperado = {5: 18, 10: 16, 20: 15, 40: 15, 60: 15}
        for n, razao in esperado.items():
            self.assertEqual(
                touchard.maior_termo(n) // touchard.contar(n), razao, "n=%d" % n
            )

    def test_digitos_em_sessenta_casais(self):
        self.assertEqual(len(str(touchard.maior_termo(60))), 83)
        self.assertEqual(len(str(touchard.contar(60))), 82)

    def test_enquanto_os_termos_cabem_em_2_53_a_soma_e_exata(self):
        # este e o limite que NAO depende da versao do Python: enquanto todo
        # termo cabe num double sem perder digito, a soma fecha exata
        for n in range(3, 41):
            if touchard.maior_termo(n) >= 2 ** 53:
                continue
            certo = touchard.contar(n)
            em_float = sum(float(t) for t in touchard.termos(n))
            self.assertEqual(em_float, float(certo), "n=%d devia bater" % n)

    def test_o_ultimo_tamanho_que_cabe_e_dezessete(self):
        self.assertLess(touchard.maior_termo(17), 2 ** 53)
        self.assertGreater(touchard.maior_termo(18), 2 ** 53)

    def test_passando_disso_a_exatidao_vira_sorte(self):
        # de 18 em diante o double as vezes acerta e as vezes nao, e QUANDO ele
        # erra depende da versao do Python: 3.13 so erra a partir de 22, e 3.11
        # ja erra em 19. Prender o primeiro erro seria prender a implementacao
        erram = [
            n
            for n in range(18, 41)
            if sum(float(t) for t in touchard.termos(n)) != float(touchard.contar(n))
        ]
        self.assertTrue(erram)
        self.assertGreater(len(erram), 10)

    def test_quando_o_double_erra_o_erro_e_minusculo(self):
        # nao importa QUAIS n erram nesta versao: quando erram, erram pouco
        houve = 0
        for n in range(18, 61):
            certo = touchard.contar(n)
            em_float = sum(float(t) for t in touchard.termos(n))
            if em_float == float(certo):
                continue
            houve += 1
            self.assertLess(abs(em_float - certo) / certo, 1e-14, "n=%d" % n)
        self.assertGreater(houve, 10)


class TestRazao(unittest.TestCase):
    def test_a_razao_de_cada_tamanho(self):
        esperado = {
            3: 0.166667,
            5: 0.108333,
            10: 0.121195,
            20: 0.128406,
            40: 0.131910,
            60: 0.133061,
        }
        for n, razao in esperado.items():
            medido = touchard.contar(n) / factorial(n)
            self.assertAlmostEqual(medido, razao, places=6, msg="n=%d" % n)

    def test_depois_de_cinco_ela_so_sobe(self):
        anterior = 0.0
        for n in range(5, 61):
            razao = touchard.contar(n) / factorial(n)
            self.assertGreater(razao, anterior, "n=%d" % n)
            anterior = razao

    def test_ela_nunca_passa_do_alvo_depois_de_cinco(self):
        for n in range(5, 61):
            self.assertLess(touchard.contar(n) / factorial(n), exp(-2), "n=%d" % n)

    def test_tres_casais_ficam_acima_do_alvo(self):
        self.assertGreater(touchard.contar(3) / factorial(3), exp(-2))


class TestLucas(unittest.TestCase):
    def test_os_numeros_da_mesa(self):
        esperado = {
            3: 12,
            4: 96,
            5: 3120,
            6: 115200,
            7: 5836320,
            8: 382072320,
            9: 31488549120,
            10: 3191834419200,
        }
        for n, total in esperado.items():
            self.assertEqual(total_na_mesa(touchard.contar(n), n), total, "n=%d" % n)
