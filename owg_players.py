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
    
    def __init__(self, nome = 'JB'):
        self.nome = nome
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
    
    def avalia_posicao(self, strpos):
        if strpos not in self.knowledge.keys():
            # Nunca viu essa posição
            # Inicializa da prior
            self.__inicializa(strpos)

        # Obtém as ações para aquela posição, e os respectivos parâmetros da Beta
        acoes, rew = self.knowledge[strpos]    
        return acoes, rew
    
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


        
########################################################################
#    Míope - considera se o próximo movimento vai levar ao fim do jogo #
########################################################################
class miope(owg_player):
    ''' 
    Miope: olha se existe algum movimento vencedor na posição atual. Se tiver, joga. Caso contrário, sorteia aleatoriamente
    '''
    def __init__(self, nome = 'Míope'):

        self.nome = nome
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
    
    def avalia_posicao(self, strpos):
        if strpos not in self.knowledge.keys():
            # Nunca viu essa posição
            # Inicializa da prior
            self.__inicializa(strpos)

        # Obtém as ações para aquela posição, e os respectivos parâmetros da Beta
        acoes, rew = self.knowledge[strpos]    
        return acoes, rew
        
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
                
            # Verifica se há alguma ação vencedora para si ou para o oponente
            mov = None
            for i in range(3):
                # Verifica linhas 
                linha = strpos[(3*i):((3*i+3))]
                if linha in ['121', '020', '112', '002', '211', '200']:
                    j = linha.find('2')
                    mov = (i, j)
                    winner = linha[abs(j-1)]
                    break
                # Verifica colunas
                coluna = strpos[i:i+7:3]
                if coluna in ['121', '020', '112', '002', '211', '200']:
                    j = coluna.find('2')
                    mov = (j, i)
                    winner = coluna[abs(j-1)]
                    break
            # Verifica diagonais
            diagp = strpos[0:9:4]
            if diagp in ['121', '020', '112', '002', '211', '200']:
                j = diagp.find('2')
                mov = (j, j)
                winner = diagp[abs(j-1)]
            diags = strpos[2:7:2]
            if diags in ['121', '020', '112', '002', '211', '200']:
                j = diags.find('2')
                mov = (j, 2-j)
                winner = diags[abs(j-1)]
            
            if mov is not None:
                # Existe um movimento vencedor nessa posição. Joga esse movimento.
                movimento = mov
                acao = 3*mov[0] + mov[1]
            else:                

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
    
        
##############################################################################################
#    epsilon_edson - implementa a estratégia \epsilon-greedy: joga o movimento que parece    #
#              ótimo com probabilidade 1 - \epsilon, e joga aleatoriamente com probabilidade #
#              \epsilon                                                                      #
##############################################################################################
class epsilon_edson(owg_player):
    ''' 
    epsilon_edson - implementa a estratégia \epsilon-greedy
    '''
    def __init__(self, desconto = 1, epsilon = .1, nome = 'Epsilon Edson'):
        '''
        @args
        
        desconto -- fator de desconto para a recompensa
        epsilon -- probabilidade de realizar um movimento exploratório
        '''
        self.e = epsilon
        self.nome = nome
        self.desconto = desconto
        owg_player.__init__(self)
        
    def __inicializa(self, strpos):
        ''' 
        Cria o vetor de recompensa para a dada posição
        '''
        acoes = [i for i in range(len(strpos)) if strpos[i] == '2']
        rec = [0] * len(acoes)
        self.knowledge[strpos] = (acoes, rec)

    def avalia_posicao(self, strpos):
        if strpos not in self.knowledge.keys():
            # Nunca viu essa posição
            # Inicializa da prior
            self.__inicializa(strpos)

        # Obtém as ações para aquela posição, e os respectivos parâmetros da Beta
        acoes,rew = self.knowledge[strpos]    
        return acoes, rew
        
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

            # Recupera as ações possíveis e as recompensas estimadas
            acoes, rec = self.knowledge[strpos]
            
            # Decide se vai explorar ou exploitar
            u = np.random.uniform()
            if u < self.e:
                # Explora: sorteia ação uniformemente
                acao = np.random.choice(a = acoes)
            else:
                # Exploita: ação com máxima recompensa estimada
                acao = acoes[np.argmax(rec)]
            
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
                    n = len(self.jogo)
                    for i in range(n):
                        pos = self.jogo[i][0]
                        acao = self.jogo[i][1]
                        a, r = self.knowledge[pos]
                        r[a.index(acao)] += 1*self.desconto**(n-i)
                        self.knowledge[pos] = (a, r)

            return movimento
        else:
            if r == -1:
                # Perdi :-/
                # Distribui os castigos, i.e., soma 1 aos betas correspondentes a cada movimento
                # utilizado na partida
                n = len(self.jogo)
                for i in range(n):
                    pos = self.jogo[i][0]
                    acao = self.jogo[i][1]
                    a, r = self.knowledge[pos]
                    r[a.index(acao)] -= 1*self.desconto**(n-i)
                    self.knowledge[pos] = (a, r)
                    
            return None    
                      
        
#############################################################################################
#    Cientista sovina - usa o modelo probabilístico mas é ganancioso para escolher a ação   #
#############################################################################################
class cientista_sovina(owg_player):
    ''' 
    Cientista sovina: usa o modelo probabilístico para aprender e atualizar as probabilidades, mas 
    é ganacioso na hora de decidir a ação (sempre escolhe a que tem maior probabilidade esperada de sucesso)
    '''
    def __init__(self, a = 1, b = 1, nome = 'Cientista sovina'):
        '''
        @args
        
        a, b -- hiperparâmetros iniciais da priori Beta
        '''
        self.a = a
        self.b = b
        self.nome = nome
        owg_player.__init__(self)
        
    def __inicializa(self, strpos):
        ''' 
        Cria o vetor de probabilidade uniforme para a dada posição
        '''
        acoes = [i for i in range(len(strpos)) if strpos[i] == '2']
        alfa = [self.a] * len(acoes)
        beta = [self.b] * len(acoes)
        self.knowledge[strpos] = (acoes, alfa, beta)

    def avalia_posicao(self, strpos):
        if strpos not in self.knowledge.keys():
            # Nunca viu essa posição
            # Inicializa da prior
            self.__inicializa(strpos)

        # Obtém as ações para aquela posição, e os respectivos parâmetros da Beta
        acoes, alfa, beta = self.knowledge[strpos]    
        rew = [a/(a+b) for a, b in zip(alfa,beta)]
        return acoes, rew
        
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
        

############################################################################################
#    Cientista        - usa o modelo probabilístico e equilibra exploração e exploitação   #
############################################################################################
class cientista(owg_player):
    ''' 
    Cientista cético: usa o modelo probabilístico beta-binomial e o terema de Bayes para aprender 
        e atualizar as probabilidades.
        Sorteia a ação, conforme probabilidades de sucesso, para equilibrar exploration e exploitation.
    '''
    def __init__(self, a = 1, b = 1, nome = 'Cientista'):
        '''
        @args 
        
        a, b -- números positivos, os parâmetros iniciais para cada priori Beta sobre as probabilidades de sucesso
        '''
        
        self.a = a
        self.b = b
        self.nome = nome
        owg_player.__init__(self)
        
    def __inicializa(self, strpos):
        '''
        Cria o vetor de probabilidade uniforme para a dada posição, e cria a lista de alfas e betas
        ''' 
        acoes = [i for i in range(len(strpos)) if strpos[i] == '2']
        alfa = [self.a] * len(acoes)
        beta = [self.b] * len(acoes)
        self.knowledge[strpos] = (acoes, alfa, beta)

    def avalia_posicao(self, strpos):
        if strpos not in self.knowledge.keys():
            # Nunca viu essa posição
            # Inicializa da prior
            self.__inicializa(strpos)

        # Obtém as ações para aquela posição, e os respectivos parâmetros da Beta
        acoes, alfa, beta = self.knowledge[strpos]    
        rew = [a/(a+b) for a, b in zip(alfa,beta)]
        return acoes, rew
        
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
            
            # Verifica se alguma ação do adversário leva à vitória
            
            
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
                       
        
        
###############################################################################################
#    Cientista cauteloso - usa o modelo probabilístico, equilibra exploração e exploitação   #
#      e sempre verifica se o oponente tem um movimento vitorioso na próxima jogada           #
###############################################################################################
class cientista_cauteloso(owg_player):
    ''' 
    Cientista cauteloso: usa o modelo probabilístico beta-binomial e o terema de Bayes para aprender 
        e atualizar as probabilidades. Também verifica, a cada lance, se o oponente tem algum movimento vencedor
        Sorteia a ação, conforme probabilidades de sucesso, para equilibrar exploration e exploitation.
    '''
    def __init__(self, a = 1, b = 1, nome = 'Cientista cauteloso'):
        '''
        @args 
        
        a, b -- números positivos, os parâmetros iniciais para cada priori Beta sobre as probabilidades de sucesso
        '''
        
        self.a = a
        self.b = b
        self.nome = nome
        owg_player.__init__(self)
        
    def __inicializa(self, strpos):
        '''
        Cria o vetor de probabilidade uniforme para a dada posição, e cria a lista de alfas e betas
        ''' 
        acoes = [i for i in range(len(strpos)) if strpos[i] == '2']
        alfa = [self.a] * len(acoes)
        beta = [self.b] * len(acoes)
        self.knowledge[strpos] = (acoes, alfa, beta)

    def avalia_posicao(self, strpos):
        if strpos not in self.knowledge.keys():
            # Nunca viu essa posição
            # Inicializa da prior
            self.__inicializa(strpos)

        # Obtém as ações para aquela posição, e os respectivos parâmetros da Beta
        acoes, alfa, beta = self.knowledge[strpos]    
        rew = [a/(a+b) for a, b in zip(alfa,beta)]
        return acoes, rew
        
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
            
            # Verifica se há alguma ação vencedora para si ou para o oponente
            mov = None
            for i in range(3):
                # Verifica linhas 
                linha = strpos[(3*i):((3*i+3))]
                if linha in ['121', '020', '112', '002', '211', '200']:
                    j = linha.find('2')
                    mov = (i, j)
                    winner = linha[abs(j-1)]
                    break
                # Verifica colunas
                coluna = strpos[i:i+7:3]
                if coluna in ['121', '020', '112', '002', '211', '200']:
                    j = coluna.find('2')
                    mov = (j, i)
                    winner = coluna[abs(j-1)]
                    break
            # Verifica diagonais
            diagp = strpos[0:9:4]
            if diagp in ['121', '020', '112', '002', '211', '200']:
                j = diagp.find('2')
                mov = (j, j)
                winner = diagp[abs(j-1)]
            diags = strpos[2:7:2]
            if diags in ['121', '020', '112', '002', '211', '200']:
                j = diags.find('2')
                mov = (j, 2-j)
                winner = diags[abs(j-1)]
            
            if mov is not None:
                # Existe um movimento vencedor nessa posição. Joga esse movimento.
                movimento = mov
                acao = 3*mov[0] + mov[1]
            else:
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
             
        
################################################################################################
#    Cientista conciliador - usa o modelo probabilístico, equilibra exploração e exploitação   #
#       e sempre verifica se o oponente tem um movimento vitorioso na próxima jogada           #
#       Difere dos demais cientistas pois seu objetivo é empatar, e não vencer.                #
################################################################################################
class cientista_conciliador(cientista):
    ''' 
    Cientista conciliador: mesma coisa que o cientista, mas com objetivo de empatar
    '''
    def __init__(self, a = 1, b = 1, nome = 'Cientista conciliador'):
        '''
        @args 
        
        a, b -- números positivos, os parâmetros iniciais para cada priori Beta sobre as probabilidades de sucesso
        '''
        
        cientista.__init__(self, a, b, nome)
        
    def avalia_posicao(self, strpos):
        if strpos not in self.knowledge.keys():
            # Nunca viu essa posição
            # Inicializa da prior
            self.__inicializa(strpos)

        # Obtém as ações para aquela posição, e os respectivos parâmetros da Beta
        acoes, alfa, beta = self.knowledge[strpos]    
        rew = [a/(a+b) for a, b in zip(alfa,beta)]
        return acoes, rew
    
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
                if r == 0:
                    # Empatou!
                    # Distribui as recompensas, i.e., soma 1 no alfa correspondente a cada movimento
                    # executado na partida
                    for i in range(len(self.jogo)):
                        pos = self.jogo[i][0]
                        acao = self.jogo[i][1]
                        a, al, be = self.knowledge[pos]
                        al[a.index(acao)] += 1
                        self.knowledge[pos] = (a, al, be)
                else:
                    # Ganhei :-/
                    for i in range(len(self.jogo)):
                        pos = self.jogo[i][0]
                        acao = self.jogo[i][1]
                        a, al, be = self.knowledge[pos]
                        be[a.index(acao)] += 1
                        self.knowledge[pos] = (a, al, be)                        

            return movimento
        else:
            if r == 0:
                # Empatou
                # Distribui as recompensas, i.e., soma 1 no alfa correspondente a cada movimento
                # executado na partida
                for i in range(len(self.jogo)):
                    pos = self.jogo[i][0]
                    acao = self.jogo[i][1]
                    a, al, be = self.knowledge[pos]
                    al[a.index(acao)] += 1
                    self.knowledge[pos] = (a, al, be)                
            else:
                # Não empatou
                # Distribui os castigos, i.e., soma 1 no beta correspondente a cada movimento
                # executado na partida
                for i in range(len(self.jogo)):
                    pos = self.jogo[i][0]
                    acao = self.jogo[i][1]
                    a, al, be = self.knowledge[pos]
                    be[a.index(acao)] += 1
                    self.knowledge[pos] = (a, al, be)
                    
            return None
                       
            
            
###############################################################################################
#    Cientista esperto - usa o modelo probabilístico, equilibra exploração e exploitação,     #
#      sempre verifica se o oponente tem um movimento vitorioso na próxima jogada, e          #
#      aplica a recompensa para a posição inversa (i.e. aprende com os erros do oponente      #
###############################################################################################
class cientista_esperto(owg_player):
    ''' 
    Cientista cauteloso: usa o modelo probabilístico beta-binomial e o terema de Bayes para aprender 
        e atualizar as probabilidades. Também verifica, a cada lance, se o oponente tem algum movimento vencedor.
        Aplica recompensa à posição inversa (i.e. aprende com os erros do oponente.
        Sorteia a ação, conforme probabilidades de sucesso, para equilibrar exploration e exploitation.
    '''
    def __init__(self, a = 1, b = 1, nome = 'Cientista cauteloso'):
        '''
        @args 
        
        a, b -- números positivos, os parâmetros iniciais para cada priori Beta sobre as probabilidades de sucesso
        '''
        
        self.a = a
        self.b = b
        self.nome = nome
        owg_player.__init__(self)
        
    def __inicializa(self, strpos):
        '''
        Cria o vetor de probabilidade uniforme para a dada posição, e cria a lista de alfas e betas
        ''' 
        acoes = [i for i in range(len(strpos)) if strpos[i] == '2']
        alfa = [self.a] * len(acoes)
        beta = [self.b] * len(acoes)
        self.knowledge[strpos] = (acoes, alfa, beta)

    def avalia_posicao(self, strpos):
        if strpos not in self.knowledge.keys():
            # Nunca viu essa posição
            # Inicializa da prior
            self.__inicializa(strpos)

        # Obtém as ações para aquela posição, e os respectivos parâmetros da Beta
        acoes, alfa, beta = self.knowledge[strpos]    
        rew = [a/(a+b) for a, b in zip(alfa,beta)]
        return acoes, rew
        
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
            
            # Verifica se há alguma ação vencedora para si ou para o oponente
            mov = None
            for i in range(3):
                # Verifica linhas 
                linha = strpos[(3*i):((3*i+3))]
                if linha in ['121', '020', '112', '002', '211', '200']:
                    j = linha.find('2')
                    mov = (i, j)
                    winner = linha[abs(j-1)]
                    break
                # Verifica colunas
                coluna = strpos[i:i+7:3]
                if coluna in ['121', '020', '112', '002', '211', '200']:
                    j = coluna.find('2')
                    mov = (j, i)
                    winner = coluna[abs(j-1)]
                    break
            # Verifica diagonais
            diagp = strpos[0:9:4]
            if diagp in ['121', '020', '112', '002', '211', '200']:
                j = diagp.find('2')
                mov = (j, j)
                winner = diagp[abs(j-1)]
            diags = strpos[2:7:2]
            if diags in ['121', '020', '112', '002', '211', '200']:
                j = diags.find('2')
                mov = (j, 2-j)
                winner = diags[abs(j-1)]
            
            if mov is not None:
                # Existe um movimento vencedor nessa posição. Joga esse movimento.
                movimento = mov
                acao = 3*mov[0] + mov[1]
            else:
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