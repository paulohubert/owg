# owg

Projeto jogo da velha reinforcement learning
Basics Of Reinforcement Learning - ENDS 2019
@author paulo.hubert@fgv.br

O objetivo é ilustrar os conceitos de aprendizagem por reforço num contexto simples e familiar.

Disclalimer: Dada a simplicidade do jogo, seria possível construir um robô melhor ou igual com menos carga computacional. Mesmo este robô usando RL pode ser melhorado. 

## Métodos

O código implementa dois algoritmos de aprendizagem por reforço:

Thompson sampling: o modelo Beta-Binomial para probabilidades de sucesso, ação escolhida ao acaso
Thompson sampling ganancioso: o mesmo modelo, mas a ação é escolhida para maximizar a probabilidade esperada de sucesso

Há um notebook de exemplo que executa o treinamento dos algoritmos via self-learning, i.e., o robô joga contra outro robô para adquirir experiência.

O arquivo 'job1m.pkl' armazena um jogador pré-treinado.

Há também uma interface gráfica rudimentar, que permite que você jogue contra algum robô.

## ToDo

1. Explorar a simetria do tabuleiro para acelerar aprendizagem
2. Aprender com os erros do oponente: atualizar os parâmetros considerando também o jogo do ponto de vista do adversário
3. Empacotar código do treinamento 
4. Melhorar performance, paralelizar treinamento
5. Impĺementar busca em árvore para n-step look ahead
6. Implementar jogador que considera o empate o sucesso, e qualquer outro resultado um fracasso
7. Refactor: separar funções de aprendizagem e decisão, melhorar estrutura de herança

