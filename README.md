# OWG - old woman's game (aka tic-tac-toe aka jogo-da-velha)

Projeto jogo da velha reinforcement learning
Basics Of Reinforcement Learning - ENDS 2019
@author paulo.hubert@fgv.br

O objetivo é ilustrar os conceitos de aprendizagem por reforço num contexto simples e familiar.

Disclaimer: Dada a simplicidade do jogo, seria possível construir um robô melhor ou igual com menos carga computacional. Mesmo este robô usando RL pode ser melhorado. Ao final deste documento aponto algumas possíveis melhorias.

Número de posições possíveis com pelo menos duas casas livres = $3^7 \times 72 = 157.464$ (número de possibilidades para um tabuleiro com $7$ casas, e $3$ possibilidades por casa - O, X e vazio - vezes o número de maneiras possíveis de escolher as duas casas livres). 

## Conteúdo

*owg_board.py*: classe que implementa o tabuleiro
*owg_player_base.py*: classe base para os jogadores
*owg_players.py*: implementação dos jogadores
*oldwomansgame.ipynb*: notebook que ilustra o uso das classes
*cientista_1MM.pkl*: objeto da classe *cientista* pré-treinado contra si mesmo por 1.000.000 de jogos
*cientista_cauteloso_1MM.pkl*: objeto da classe *cientista_cauteloso* pré-treinado contra si mesmo por 1.000.000 de jogos
*epsilon_edson_1MM.pkl*: objeto da classe *epsilon_edson* pré-treinado contra si mesmo por 1.000.000 de jogos

## Métodos

O código implementa seis algoritmos de aprendizagem para o jogo da velha:

1. Aleatório (não aprende e joga ao acaso)
2. Míope (1-step look-ahead, olha se o próximo lance pode terminar o jogo e caso positivo joga esse lance)
3. Epsilon-edson (método $\epsilon$-greedy)
4. Cientista sovina (Thomspon sampling - ver abaixo - escolhendo sempre a ação com maior probabilidade esperada de vitória)
5. Cientista (Thompson sampling sorteando a ação com base nas probabilidades de vitória estimadas)
6. Cientista cauteloso (combina Thompson sampling com 1-step look-ahead)
7. Cientistas conciliador (cientista cauteloso mas cujo objetivo é aprender a empatar)

Há um notebook de exemplo que executa o treinamento dos algoritmos via self-learning, i.e., o robô joga contra outro robô para adquirir experiência.

Há também uma interface gráfica rudimentar, feita com pyplot, que permite que você jogue contra algum robô. Também está implementado um tabuleiro para humano x humano, com a opção de incluir um robô no tabuleiro para visualizar o aprendizado do robô em uma determinada posição.

### Método $\epsilon$-greedy

Confrontado com uma posição do tabuleiro, o robô escolhe o movimento com maior recompensa estimada até o momento. Para permitir alguma exploração das possibilidades, com probabilidade $\epsilon$ o robô escolhe uma posição aleatoriamente.

Esta estratégia é implementada pelo jogador *epsilon_edson*
 
### Modelo Beta-Binomial

Para uma certa posição $x$, com $k(x)$ casas livres, tenho $n(x)$ ações possíveis. A partir de agora, vou ignorar o $x$, mantendo sempre em mente que teremos um modelo desses abaixo para cada uma das $157.464$ posições.

Para cada uma das $k$ ações possíveis, defino uma probabilidade $\pi(i)$: a probabilidade de vitória caso o jogador escolha a a ação $i$ ($i=1,...k$)

Observo $n_i$ jogos começando da mesma posição, e escolho sempre a ação $i$. Conto o número de vitórias $v_i$. Repito isso para todas as $k$ posições; ou seja, observo $(v_i, n_i)$ para $i=1,...,k$. 

Supondo que conheço as probabilidades $\pi(i)$, a probabilidade associada ao número de jogos e vitórias observadas (a verossimilhança) é uma binomial:

$P(v_i | n_i, \pi(i)) \propto \pi(i)^{v_i}(1-\pi(i))^{n_i-v_i}$

Considerando agora todas as posições, e supondo que os resultados dos jogos são independentes (condicionalmente a $\pi$), temos a verossimilhança conjunta de todas as posições:

$P(\mathbf{v} | \mathbf{n}, \mathbf{\pi}) \propto \prod_{i=1}^k \pi(i)^{v_i}(1-\pi(i))^{n_i-v_i}$

Como não conheço $\pi$, vou modelar minha ignorância usando uma distribuição de probabilidade para esses valores (uma priori). Por questões matemáticas, escolho uma distribuição Beta para cada possível ação:

$P(\pi(i)) \propto \pi(i)^{\alpha_i - 1}(1-\pi(i))^{\beta_i-1}$

Onde $\alpha_i$ e $\beta_i$ são hiperparâmetros que vamos precisar escolher (em lugar de aprender seus valores). 

### Aprendizagem e o teorema de Bayes

Eu começo então dizendo que a probabilidade de vitória do movimento $i$ tem distribuição a priori Beta com hiperparâmetros $\alpha_i$ e $\beta_i$; jogo uma vez e escolho o movimento $i$. Como incorporo essa nova informação?

Pelo teorema de Bayes, e usando a propriedade de conjugação entre priori Beta e verossimilhança binomial, sei que a nova distribuição de $\pi(i)$ é de novo uma Beta, mas agora com parâmetros $(\alpha_i + 1, \beta_i)$ em caso de vitória, e $(\alpha_i, \beta_i+1)$ em caso de derrota. 

Portanto a equação de aprendizagem desse modelo, para cada posição $x$ e cada possível movimento $i_x$, é:

$\begin{align}
&\alpha_i(t+1) = \alpha_i(t) + r_i(t) \\
&\beta_i(t+1) = \beta_i(t) + (1-r_i(t))
\end{align}$

onde $r_i(t) = 1$ no caso de vitória, e $0$ caso contrário.

Observação: agora temos uma interpretação para os hiperparâmetros $\alpha$ e $\beta$; eles representam quantas vitórias e quantas derrotas o robô viu até o momento em que começa a nova rodada de aprendizagem.

### Decisão

O robô chegou numa posição $x$ com diversas ações possíveis. Ele tem uma distribuição de probabilidade para a probabilidade de vitória (a probabilidade de uma probabilidade...) de cada lance. O que fazer?

1. Olhar o valor esperado de probabilidade de vitória para cada movimento; escolher o movimento com maior valor esperado. Esta estratégia é implementada pelo jogador *cientista_sovina*
2. Sortear uma probabilidade de vitória para cada movimento, conforme a distribuição atual; escolher o movimento com maior valor sorteado. Esta estratégia é implementada pelo jogador *cientista*

## Possíveis melhorias

1. Explorar a simetria do tabuleiro para acelerar aprendizagem
2. Aprender com os erros do oponente: atualizar os parâmetros considerando também o jogo do ponto de vista do adversário
3. Empacotar código do treinamento 
4. Melhorar performance, paralelizar treinamento
5. Impĺementar busca em árvore para n-step look ahead
6. Refactor: separar funções de aprendizagem e decisão, melhorar estrutura de herança, empacotar métodos da interface gráfica

