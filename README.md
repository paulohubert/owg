# owg

Projeto jogo da velha reinforcement learning
Basics Of Reinforcement Learning - ENDS 2019
@author paulo.hubert@fgv.br

O código implementa dois algoritmos de aprendizagem por reforço:

Thompson sampling: o modelo Beta-Binomial para probabilidades de sucesso, ação escolhida ao acaso
Thompson sampling ganancioso: o mesmo modelo, mas a ação é escolhida para maximizar a probabilidade esperada de sucesso

Há um notebook de exemplo que executa o treinamento dos algoritmos via self-learning, i.e., o robô joga contra outro robô para adquirir experiência.

O arquivo 'job1m.pkl' armazena um jogador pré-treinado.

Há também uma interface gráfica rudimentar, que permite que você jogue contra algum robô.

## ToDo

1. Explorar a simetria do tabuleiro para acelerar aprendizagem
2. Explorar estratégias híbridas (i.e., incluir alguma inteligência além do aprendizado estatístico)

