# O problema dos casais

Édouard Lucas, 1891: `n` casais sentam numa mesa redonda de `2n` lugares,
alternando homem e mulher, e ninguém pode ficar ao lado do próprio cônjuge. De
quantos jeitos dá?

A resposta sai por **quatro caminhos que não compartilham código**: gerar todas
as permutações e olhar uma por uma, uma tabela de máscaras de bits que nunca
monta uma permutação inteira, a fórmula fechada de Touchard de 1934, e a
recorrência de Muir, que usa uma identidade completamente diferente. Python
puro, sem dependência nenhuma.

## Os quatro achados

1. **Os quatro caminhos concordam em todos os 16 tamanhos conferidos**, até
   2.649.391.469.058 arranjos com dezesseis casais. A enumeração chega a nove
   casais; daí em diante ela não termina e a tabela diz isso, em vez de repetir
   um número que eu saberia de outro lugar.
2. **A troca de `n!` por `2ⁿ·n` vale 116 bilhões de vezes com vinte casais.**
   São 2.432.902.008.176.640.000 permutações contra 20.971.520 estados. O truque
   é só um: duas permutações que já sentaram o mesmo conjunto de maridos valem a
   mesma coisa daí para a frente.
3. **Somar os termos de Touchard em ponto flutuante começa a errar em 22
   casais.** Até 21 o `double` devolve o valor exato; de 22 em diante não. O
   erro é pequeno — 2,1 × 10⁻¹⁵ com trinta casais — mas o valor exato se perde,
   e em aritmetica inteira ele não custa nada.
4. **A fatia de arranjos que sobram converge para `e⁻²` por baixo, e devagar.**
   Com cinco casais é 0,1083; com sessenta ainda é 0,1331, contra 0,1353. Só
   três casais ficam **acima** do alvo, com 0,1667.

## As tabelas

Tudo abaixo sai de `python -m ferramentas.medidor`. Nenhum número foi digitado à
mão, e todos estão presos em `testes/test_medidas.py`.

### Os quatro caminhos

| casais | enumeração | máscaras | Touchard | recorrência de Muir |
|---|---|---|---|---|
| 3 | 1 | 1 | 1 | 1 |
| 4 | 2 | 2 | 2 | 2 |
| 5 | 13 | 13 | 13 | 13 |
| 6 | 80 | 80 | 80 | 80 |
| 7 | 579 | 579 | 579 | 579 |
| 8 | 4.738 | 4.738 | 4.738 | 4.738 |
| 9 | 43.387 | 43.387 | 43.387 | 43.387 |
| 10 | não terminou | 439.792 | 439.792 | 439.792 |
| 12 | não terminou | 59.216.642 | 59.216.642 | 59.216.642 |
| 14 | não terminou | 10.927.434.464 | 10.927.434.464 | 10.927.434.464 |
| 16 | não terminou | 2.649.391.469.058 | 2.649.391.469.058 | 2.649.391.469.058 |

Com `--completo` a enumeração vai a onze casais.

### O custo de cada caminho

| casais | permutações olhadas | estados das máscaras | quantas vezes menos |
|---|---|---|---|
| 8 | 40.320 | 2.048 | 19 |
| 10 | 3.628.800 | 10.240 | 354 |
| 12 | 479.001.600 | 49.152 | 9.745 |
| 14 | 87.178.291.200 | 229.376 | 380.067 |
| 16 | 20.922.789.888.000 | 1.048.576 | 19.953.527 |
| 20 | 2.432.902.008.176.640.000 | 20.971.520 | 116.009.807.976 |

### O cancelamento da fórmula de Touchard

| casais | maior termo | resultado | razão |
|---|---|---|---|
| 5 | 240 | 13 | 18 |
| 10 | 7.257.600 | 439.792 | 16 |
| 20 | 4.865.804.016.353.280.000 | 312.400.218.671.253.762 | 15 |
| 40 | 1,63 × 10⁴⁸ | 1,07 × 10⁴⁷ | 15 |
| 60 | 83 algarismos | 82 algarismos | 15 |

Os termos alternam de sinal e o maior deles fica estável em quinze vezes o
resultado. Não é um cancelamento catastrófico, mas é o bastante para o `double`
não dar conta:

| casais | inteiro | double | erro relativo |
|---|---|---|---|
| 15 | 164.806.435.783 | exato | 0 |
| 20 | 312.400.218.671.253.762 | exato | 0 |
| 30 | 34.682.040.826.614.983.472.734.095.531.712 | 3,468204 × 10³¹ | 2,078 × 10⁻¹⁵ |
| 60 | 1,107199898… × 10⁸¹ | 1,107200 × 10⁸¹ | 1,141 × 10⁻¹⁵ |

O primeiro tamanho em que o `double` já não devolve o valor exato é **22**.

### A fatia de arranjos que sobra

| casais | U(n)/n! | distância de e⁻² |
|---|---|---|
| 3 | 0,166667 | +0,031331 |
| 5 | 0,108333 | −0,027002 |
| 10 | 0,121195 | −0,014140 |
| 20 | 0,128406 | −0,006929 |
| 40 | 0,131910 | −0,003425 |
| 60 | 0,133061 | −0,002274 |

`e⁻² = 0,135335`. De cinco casais em diante a razão só sobe, e nunca alcança o
alvo — as duas coisas estão em teste.

### Os números de Lucas: a mesa inteira

| casais | jeitos de sentar todo mundo |
|---|---|
| 3 | 12 |
| 4 | 96 |
| 5 | 3.120 |
| 6 | 115.200 |
| 7 | 5.836.320 |
| 8 | 382.072.320 |
| 9 | 31.488.549.120 |
| 10 | 3.191.834.419.200 |

## O que as medidas me corrigiram

- **Esperava um cancelamento catastrófico na fórmula de Touchard.** Os termos
  alternam de sinal e chegam a `n!`, então eu contava ver o maior termo milhares
  de vezes maior que o resultado. A razão é **quinze**, e fica em quinze de vinte
  a sessenta casais. O que quebra o `double` não é a razão: é o tamanho absoluto
  dos termos, que passa de 2⁵³.
- **Achei que a razão `U(n)/n!` subisse desde o começo.** Ela cai de três para
  cinco casais — 0,1667 para 0,1083 — e só depois sobe. Três casais são o único
  tamanho acima de `e⁻²`, e é porque lá existe **um** arranjo só.
- **Escrevi no código que o ponto flutuante "custaria o resultado inteiro".**
  Custa quinze dígitos depois da vírgula: o erro relativo em sessenta casais é
  1,1 × 10⁻¹⁵. A frase estava num comentário, que é onde um exagero não quebra
  teste nenhum — e por isso o comentário foi corrigido junto com a medida.
- **Esperava que a enumeração chegasse a onze ou doze casais sem apuro.** Onze
  já são 39.916.800 permutações e pedem `--completo`; doze são 479 milhões, e a
  tabela do README diz "não terminou" em vez de copiar o valor que a fórmula
  dá — que é a regra da casa.

## Como está organizado

```
menage/mesa.py         o que está sendo contado, e por que a proibição é dupla
menage/enumeracao.py   o primeiro caminho: todas as n! permutações, uma a uma
menage/mascaras.py     o segundo caminho: tabela sobre o conjunto de já sentados
menage/touchard.py     o terceiro e o quarto: a fórmula de 1934 e a recorrência
ferramentas/medidor.py roda tudo e imprime as tabelas acima
testes/                37 testes
```

## Rodar

```bash
python -m unittest discover -s testes -t . -v   # a bateria inteira
python -m ferramentas.medidor                   # recalcula as tabelas deste README
python -m ferramentas.medidor --completo        # enumeração até onze casais
```

Sem `pip install`: não há dependência. Precisa de Python 3.11 ou mais novo.

## Licença

MIT.
