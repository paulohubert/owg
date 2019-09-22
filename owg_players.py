# Jogadores
import numpy as np

from owg_board import owg
from owg_player_base import owg_player

##################################################################
#    João Bobo - age aleatoriamente e não aprende com os erros   #
##################################################################
class jb (owg_player) : 
    ''' 
    Classe jb: é o jogador que não aprende; decide cada movimento aleatoriamente para sempre
    '''
    
    def __init__(self):
        self.nome = 'JB'
        owg_player.__init__(self)
        
    def __inicializa(self, strpos):
        '''
        Cria o vetor de probabilidade uniforme para as ações possíveis a partir da posição strpos.
        
        @args
        
        strpos -- uma string que representa a posição atual. A string tem nove posições, cada uma
                    correspondendo a uma célula do tabuleiro (da esquerda pra direita, de cima pra baixo).
                    '0' significa posição marcada pelo oponente, '1' significa posição marcada pelo próprio
                    jogador, e '2' significa posição vazia.
        '''
        # Cria o vetor de probabilidade uniforme para a dada posição
        
        # As ações possíveis são os quadrados vazios
        acoes = [i for i in range(len(strpos)) if strpos[i] == '2']
        
        # Cria as probabilidades da uniforme
        probs = [1/len(acoes)] * len(acoes)
        self.knowledge[strpos] = (acoes, probs)
    
    
    def joga(self, verbose = False):
        '''
        Dada a posição atual do tabuleiro, decide a ação. 
        '''
        
        # Primeiro verifica se jogo está rolando
        r, _ = self.board.check_result()
        if r is None:
            # Está rolando
            
            # Recupera string que representa o estado atual
            strpos = self.board.sstate
            if verbose:
                print(strpos)
            if strpos not in self.knowledge.keys():
                # Nunca viu essa posição
                self.__inicializa(strpos)
            # Obtém as ações possiveis e suas respectivas probabilidades de sucesso
            acoes, probs = self.knowledge[strpos]
            
            # Sorteia uma ação
            acao = np.random.choice(a = acoes, p = probs)
            
            # Constrói a dupla que representa o movimento
            movimento = (int(acao / 3), acao % 3)
            
            # Joga e armazena o movimento
            self.board.play(1, movimento)
            self.jogo.append((strpos, acao))
            
            return movimento
        else:
            return None  
        

############################################################################################
#    Cientista cético - usa o modelo probabilístico e equilibra exploração e exploitação   #
############################################################################################
class cientista(owg_player):
    ''' 
    Cientista cético: usa o modelo probabilístico beta-binomial e o terema de Bayes para aprender 
        e atualizar as probabilidades.
        Sorteia a ação, conforme probabilidades de sucesso, para equilibrar exploration e exploitation.
    '''
    def __init__(self, a = 1, b = 1):
        '''
        @args 
        
        a, b -- números positivos, os parâmetros iniciais para cada priori Beta sobre as probabilidades de sucesso
        '''
        
        self.a = a
        self.b = b
        self.nome = 'Cientista'
        owg_player.__init__(self)
        
    def __inicializa(self, strpos):
        '''
        Cria o vetor de probabilidade uniforme para a dada posição, e cria a lista de alfas e betas
        ''' 
        acoes = [i for i in range(len(strpos)) if strpos[i] == '2']
        alfa = [self.a] * len(acoes)
        beta = [self.b] * len(acoes)
        self.knowledge[strpos] = (acoes, alfa, beta)
        
    def joga(self, verbose = False):
        '''
        Dada a posição atual do tabuleiro, decide a ação. Aprende com o resultado
        '''

        # Primeiro verifica se jogo está rolando
        r, _ = self.board.check_result()
        if r is None:
            # Está rolando
            # Recupera a string que representa a posição
            strpos = self.board.sstate
            
            if verbose:
                print(strpos)
            if strpos not in self.knowledge.keys():
                # Nunca viu essa posição
                # Inicializa da prior
                self.__inicializa(strpos)

            # Obtém as ações para aquela posição, e os respectivos parâmetros da Beta
            acoes, alfa, beta = self.knowledge[strpos]
            
            # Sorteia as probabilidades de sucesso da Beta
            probs = [np.random.beta(a = param[0], b = param[1]) for param in zip(alfa, beta)]
            
            # Sorteia a ação conforme as probabilidades de sucesso sorteadas no passo anterior
            acao = acoes[np.argmax(probs)]

            # Constrói o par que representa o movimento
            movimento = (int(acao / 3), acao % 3)

            # Joga e armazena
            self.board.play(1, movimento)
            self.jogo.append((strpos, acao))
            
            # Verifica se ganhou o jogo
            r, _ = self.board.check_result()
            if r is not None:
                # Terminou o jogo
                if r == 1:
                    # Ganhei!
                    # Distribui as recompensas, i.e., soma 1 no alfa correspondente a cada movimento
                    # executado na partida
                    for i in range(len(self.jogo)):
                        pos = self.jogo[i][0]
                        acao = self.jogo[i][1]
                        a, al, be = self.knowledge[pos]
                        al[a.index(acao)] += 1
                        self.knowledge[pos] = (a, al, be)

            return movimento
        else:
            if r == -1:
                # Perdi :-/
                # Distribui os castigos, i.e., soma 1 no beta correspondente a cada movimento
                # executado na partida
                for i in range(len(self.jogo)):
                    pos = self.jogo[i][0]
                    acao = self.jogo[i][1]
                    a, al, be = self.knowledge[pos]
                    be[a.index(acao)] += 1
                    self.knowledge[pos] = (a, al, be)
                    
            return None        
    

#############################################################################################
#    Cientista sovina - usa o modelo probabilístico mas é ganancioso para escolher a ação   #
#############################################################################################
class cientista_sovina(owg_player):
    ''' 
    Cientista sovina: usa o modelo probabilístico para aprender e atualizar as probabilidades, mas 
    é ganacioso na hora de decidir a ação (sempre escolhe a que tem maior probabilidade esperada de sucesso)
    '''
    def __init__(self, a = 1, b = 1):
        '''
        @args
        
        a, b -- hiperparâmetros iniciais da priori Beta
        '''
        self.a = a
        self.b = b
        self.nome = 'Cientista sovina'
        owg_player.__init__(self)
        
    def __inicializa(self, strpos):
        ''' 
        Cria o vetor de probabilidade uniforme para a dada posição
        '''
        acoes = [i for i in range(len(strpos)) if strpos[i] == '2']
        alfa = [self.a] * len(acoes)
        beta = [self.b] * len(acoes)
        self.knowledge[strpos] = (acoes, alfa, beta)
        
    def joga(self, verbose = False):
        '''
        Dada a posição atual do tabuleiro, decide a ação. Aprende com o resultado.
        '''
        
        # Primeiro verifica se jogo está rolando
        r, _ = self.board.check_result()
        if r is None:
            # Está rolando
            
            # Recupera a string que representa a posição atual
            strpos = self.board.sstate
            
            if verbose:
                print(strpos)
            if strpos not in self.knowledge.keys():
                # Nunca viu essa posição
                self.__inicializa(strpos)

            # Recupera as ações possíveis e seus respectivos parâmetros
            acoes, alfa, beta = self.knowledge[strpos]
            
            # Calcula a probabilidade esperada de sucesso para cada posição
            probs = [param[0] / (param[0] + param[1]) for param in zip(alfa, beta)]
            # Escolhe a ação com maior prob esperada de sucesso
            acao = acoes[np.argmax(probs)]
            
            # Constrói a dupla que define a ação
            movimento = (int(acao / 3), acao % 3)

            # Joga e armazena
            self.board.play(1, movimento)
            self.jogo.append((strpos, acao))
            
            # Verifica se ganhou o jogo
            r, _ = self.board.check_result()
            if r is not None:
                if r == 1:
                    # Ganhei!
                    # Distribui as recompensas, i.e., soma 1 aos alfas correspondentes a cada movimento
                    # utilizado na partida
                    for i in range(len(self.jogo)):
                        pos = self.jogo[i][0]
                        acao = self.jogo[i][1]
                        a, al, be = self.knowledge[pos]
                        al[a.index(acao)] += 1
                        self.knowledge[pos] = (a, al, be)

            return movimento
        else:
            if r == -1:
                # Perdi :-/
                # Distribui os castigos, i.e., soma 1 aos betas correspondentes a cada movimento
                # utilizado na partida
                for i in range(len(self.jogo)):
                    pos = self.jogo[i][0]
                    acao = self.jogo[i][1]
                    a, al, be = self.knowledge[pos]
                    be[a.index(acao)] += 1
                    self.knowledge[pos] = (a, al, be)
                    
            return None      