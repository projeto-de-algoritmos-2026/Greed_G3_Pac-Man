# Greed_G3_Pac-Man

**Conteúdo da Disciplina**: Algoritmos Ambiciosos

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 20/0035703  |  Breno Alexandre Soares Garcia |
| 22/1008033  |  Fernando Gabriel Dos Santos Carrijo |

## Sobre
O projeto **Greed_G3_Pac-Man** é uma simulação com interface gráfica inspirada no Pac-Man, adaptada para aplicar uma estratégia gulosa baseada no problema da **Mochila (Knapsack)**.

No jogo, o Pac-Man possui uma quantidade limitada de energia e precisa decidir quais itens coletar no mapa. Cada item possui uma pontuação, e o custo para coletá-lo é calculado pela distância mínima entre a posição atual do jogador e a posição do item. A escolha gulosa prioriza o item com a melhor relação entre pontuação e custo.

O projeto possui dois modos de uso:
* **Modo manual:** o jogador controla o Pac-Man com as setas ou teclas WASD.
* **Modo automático:** o algoritmo calcula a rota de maior pontuação e executa um passe por vez.

A energia inicial foi balanceada para `75`, permitindo que o modo automático consiga coletar todos os itens do mapa, mas sem sobrar energia demais.

Na modelagem do problema:
* **Jogador:** representa o Pac-Man, indicado por `P`.
* **Mapa:** representa o ambiente navegável em formato de grid.
* **Paredes:** bloqueiam a movimentação, indicadas por `#`.
* **Itens:** representam pontos, frutas, power-ups e cerejas.
* **Valor:** representa a pontuação obtida ao coletar um item.
* **Custo:** representa a energia gasta para chegar até o item.
* **Capacidade:** representa a energia total disponível para o Pac-Man.

## Técnica Utilizada
**Knapsack com busca por maior pontuação**

O projeto modela a coleta de itens como uma variação do problema da mochila: existe uma capacidade limitada de energia, itens com valores diferentes e custos de deslocamento entre posições do mapa.

O primeiro critério usado no projeto foi a razão:

```text
valor / custo
```

Na versão atual, o **Passe automático** usa uma busca com memorização para avaliar rotas possíveis e escolher a continuação com maior pontuação final, considerando:

* valor dos itens coletados;
* custo de deslocamento;
* bônus por combo de frutas;
* bônus por energia restante após a vitória.

Embora o custo seja obtido a partir de caminhos no grid, o foco do trabalho continua sendo a tomada de decisão sobre quais itens coletar dentro de uma capacidade limitada.

## Regras de Pontuação
Além da pontuação dos itens, o projeto possui dois bônus:

* **Bônus de energia:** após a vitória, cada unidade de energia restante adiciona `10` pontos à pontuação final.
* **Combo de frutas:** ao coletar frutas (`F` ou `C`) consecutivamente em até `6` movimentos, o jogador recebe `60` pontos extras.

Com a primeira pontuação manual observada, a pontuação ajustada mínima seria:

```text
280 pontos + (29 energia restante * 10) = 570 pontos
```

O passe automático usa uma busca por rotas com memorização para encontrar a melhor continuação possível considerando itens, combos e bônus de energia. Assim, o botão **Passe automático** já segue o caminho de maior pontuação.

## Itens do Mapa
| Símbolo | Item | Pontuação |
| -- | -- | -- |
| `.` | Ponto comum | 10 |
| `O` | Power-up | 30 |
| `F` | Fruta | 50 |
| `C` | Cereja | 80 |

## Funcionalidades
* Representação do mapa em interface gráfica.
* Energia limitada para o jogador.
* Cálculo do custo de deslocamento até cada item.
* Seleção gulosa por maior razão `valor / custo`.
* Atualização da pontuação e da energia após cada coleta.
* Exibição da rota escolhida em cada rodada com `*`.
* Relatório final com itens coletados, itens ignorados, energia usada e pontuação total.
* Interface gráfica com mapa colorido, painel de status e controles de execução.
* Modo manual controlado por setas ou WASD.
* Modo automático otimizado com execução por passe ou contínua.
* Algoritmo de busca para maior pontuação final possível integrado ao passe automático.
* Testes unitários para validação da lógica principal.

## Vídeo

Segue o vídeo feito pela dupla: [Link](Link)

## Screenshots

![Figura 1](assets/figura1.svg)
> *Figura 1: Execução inicial com mapa, Pac-Man e itens coletáveis.*

![Figura 2](assets/figura2.svg)
> *Figura 2: Rodada da simulação mostrando a rota escolhida pela estratégia gulosa.*

![Figura 3](assets/figura3.svg)
> *Figura 3: Resultado final com pontuação, energia restante e itens ignorados.*

## Instalação
**Linguagem**: `Python 3.8+`<br>
**Framework/Biblioteca**: `Tkinter`<br>

**Pré-requisitos:**
É necessário ter o Python instalado na máquina. O projeto utiliza `tkinter`, biblioteca que já acompanha a instalação padrão do Python na maioria dos ambientes.

**Passo a passo da instalação:**

1. Clone este repositório:
```bash
git clone https://github.com/projeto-de-algoritmos-2026/Greed_G3_Pac-Man
```

2. Acesse a pasta do projeto:
```bash
cd Greed_G3_Pac-Man
```

3. Execute o projeto:
```bash
python main.py
```

## Uso
Ao executar o projeto, a interface gráfica é aberta com o mapa, os itens, a pontuação, a energia restante e a melhor escolha gulosa disponível no momento.

```bash
python main.py
```

Controles do modo manual:
* `Setas`: movimentam o Pac-Man.
* `W`, `A`, `S`, `D`: também movimentam o Pac-Man.
* `Espaço`: executa uma rodada automática.
* `R`: reinicia a simulação.

Botões da interface:
* **Modo manual:** ativa o controle do jogador.
* **Passe automático:** executa o próximo passo da rota de maior pontuação.
* **Jogo automático:** executa a rota otimizada automaticamente até vencer ou até não haver mais item possível.
* **Resetar:** reinicia o jogo.

Em cada rodada, o algoritmo:
* Testa as próximas rotas possíveis a partir da posição atual.
* Soma o valor dos itens encontrados em cada rota.
* Considera combos de frutas e bônus de energia restante.
* Escolhe a continuação com maior pontuação final prevista.
* Move o Pac-Man até o item.
* Coleta todos os itens encontrados no caminho.
* Atualiza energia e pontuação.

Também é possível executar a versão textual automática no terminal:

```bash
python main.py --terminal
```

Para executar os testes:

```bash
python -m unittest discover
```

## Estrutura do Projeto
```text
.
├── main.py
├── src
│   ├── config.py
│   ├── game.py
│   ├── greedy.py
│   ├── grid.py
│   ├── maps.py
│   ├── models.py
│   ├── optimizer.py
│   └── ui.py
└── tests
    └── test_greedy.py
```
