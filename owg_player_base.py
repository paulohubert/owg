# Classe base para os jogadores
import numpy as np
from owg_board import owg

class owg_player:
    '''
    Classe para representar um jogador genérico. Implementa os métodos em comum.
    Os jogadores específicos com suas estratégias serão classes herdadas desta.
    '''
    def __init__(self):
        # board é um objeto owg
        # knowledge é um dicionário 'posicao' : [probabilidades], que atribui probabilidades a cada movimento na posição posicao
        # jogo é uma lista de pares ordenados (posição, ação) para guardar o histórico dos movimentos
        # O jogador sempre se considera internamente o jogador 1 (é irrelevante se ele é o X ou a O)
        self.knowledge = dict()
        self.board = owg()
        self.jogo = []
        
    def comunica(self, movimento, verbose = False):
        '''
        Jogador recebe informação sobre movimento do oponente, e altera seu estado interno.
        
        @args
        
        movimento -- dupla (i,j) com i a linha e j a coluna do movimento
        
        
        '''
        # Comunica o movimento do oponente
        self.board.play(0, movimento)
        if verbose:
            print("Comunica", movimento, self.board.state)


    def __inicializa(self, strpos):
        '''
        Método virtual, para ser sobrescrito pelos jogadores específicos
        '''
        pass
    
    def joga(self, verbose = False):
        '''
        Método virtual, para ser sobrescrito pelos jogadores específicos
        '''
        pass
    
    def reset(self):
        '''
        Reseta o estado do jogo atual
        '''
        self.board.reset()
        self.jogo = []

        