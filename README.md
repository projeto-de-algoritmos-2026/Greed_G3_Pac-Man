# G03_Greed_PacMan_Knapsack

**Conteúdo da Disciplina**: Greed

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 22/1008033  |  Fernando Gabriel Dos Santos Carrijo |
| 20/0035703  |  Breno Alexandre Soares Garcia |

## Sobre
O projeto **PacMan_Knapsack** é uma simulação inspirada na dinâmica do Pac-Man, adaptada para aplicar uma estratégia gulosa baseada no problema da **Mochila (Knapsack)**.

O mapa do jogo é representado como um grid navegável, onde o jogador deve escolher quais itens coletar antes que sua energia acabe. Cada item possui uma pontuação e um custo associado ao deslocamento necessário para alcançá-lo. Assim, o desafio passa a ser maximizar a pontuação coletada respeitando uma capacidade limitada de movimentos ou energia.

Na modelagem do problema:
* **Mapa:** representa o ambiente navegável em formato de grid.
* **Posições:** representam células livres, paredes, itens e a posição atual do jogador.
* **Itens:** representam pontos, frutas e power-ups disponíveis para coleta.
* **Valor:** representa a pontuação obtida ao coletar um item.
* **Peso/Custo:** representa a energia ou quantidade de movimentos necessária para alcançar o item.
* **Capacidade:** representa o limite de energia disponível para o jogador.

O sistema utiliza uma abordagem gulosa para escolher os itens mais vantajosos com base na razão entre valor e custo:
* **Valor:** pontuação do item.
* **Custo:** distância até o item ou energia necessária para coletá-lo.
* **Critério guloso:** priorizar itens com maior relação `valor / custo`.

## Objetivo
Aplicar o conceito de algoritmos gulosos por meio de uma simulação interativa, mostrando como uma estratégia baseada em **Knapsack** pode decidir quais itens devem ser coletados para maximizar a pontuação dentro de um limite de energia.

## Técnica Utilizada
**Knapsack com estratégia gulosa**

A cada rodada, o algoritmo avalia os itens ainda disponíveis no mapa e escolhe aquele que apresenta a melhor razão entre pontuação e custo de deslocamento. Caso o jogador ainda tenha energia suficiente para alcançar o item, ele é coletado e a energia restante é atualizada. O processo se repete até que não existam mais itens possíveis de serem coletados.

Essa abordagem mantém a essência do Pac-Man, pois o jogador continua navegando pelo mapa e coletando itens, mas o foco técnico do trabalho passa a ser a tomada de decisão gulosa.

## Funcionalidades
* Representação do mapa em formato de grid.
* Distribuição de pontos, frutas e power-ups pelo mapa.
* Definição de energia máxima para o jogador.
* Cálculo do custo de deslocamento até cada item.
* Seleção gulosa dos itens com melhor razão `valor / custo`.
* Atualização da energia restante após cada coleta.
* Exibição da pontuação total obtida.
* Visualização da ordem de coleta escolhida pelo algoritmo.
* Comparação entre itens coletados e itens ignorados por falta de energia.

## Exemplo de Aplicação
Considere que o jogador possui 20 unidades de energia. Cada item no mapa possui uma pontuação e uma distância até a posição atual do jogador:

| Item | Pontuação | Custo | Valor/Custo |
| -- | -- | -- | -- |
| Ponto comum | 10 | 2 | 5.0 |
| Fruta | 50 | 8 | 6.25 |
| Power-up | 30 | 4 | 7.5 |

Pela estratégia gulosa, o algoritmo prioriza o **Power-up**, pois ele possui a melhor relação entre pontuação e custo. Em seguida, recalcula ou reavalia os próximos itens disponíveis até que a energia acabe.

## Vídeo

Segue o vídeo feito pela dupla: [Link](https://www.youtube.com/watch?v=INSERIR_LINK_DO_VIDEO)

## Screenshots

![Execução principal](assets/print_1.png)
> *Figura 1: Mapa em grid com jogador, paredes e itens coletáveis.*

![Escolha gulosa](assets/print_2.png)
> *Figura 2: Ordem de coleta definida pela razão valor/custo.*

![Resultado final](assets/print_3.png)
> *Figura 3: Pontuação obtida, energia restante e itens ignorados.*

## Instalação
**Linguagem**: `Python 3.8+`<br>
**Framework/Biblioteca**: `Pygame`<br>

**Pré-requisitos:**
É necessário ter o Python instalado na máquina. Para executar a interface gráfica da simulação, instale também a biblioteca `pygame`.

**Passo a passo da instalação:**

1. Clone este repositório:
```bash
git clone https://github.com/projeto-de-algoritmos-2026/G03_Greed_PacMan_Knapsack
```

2. Acesse a pasta do projeto:
```bash
cd G03_Greed_PacMan_Knapsack
```

3. Instale as dependências:
```bash
pip install pygame
```

4. Execute o projeto:
```bash
python main.py
```

## Uso
Ao iniciar a aplicação, o mapa será carregado com itens distribuídos pelo grid. O jogador começa com uma quantidade limitada de energia e o algoritmo guloso decide a sequência de itens a serem coletados.

Cada item é avaliado pela relação entre sua pontuação e o custo para alcançá-lo. O jogador coleta os itens mais vantajosos enquanto houver energia suficiente.

Ao final da execução, a aplicação mostra:
* A ordem de coleta escolhida.
* A pontuação total acumulada.
* A energia utilizada.
* Os itens que não puderam ser coletados.

Essa proposta combina a temática de jogo com a aplicação prática de uma técnica gulosa, mantendo uma visualização simples e intuitiva do processo de decisão.
