# Tabuleiro e interface gráfica

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

class owg:
    '''
    Classe owg: define o tabuleiro e as regras do jogo, aceita movimentos e mantém a posição atual do jogo
    na memória.
    
    '''
    def __init__(self):
        self.state = np.empty(shape = (3, 3))
        self.cur = None
        self.state[:] = np.nan
        self.__convert_state()
        self.starter = 0
        self.a = None
        
        # Gera conjunto de pontos para as figuras
                
        # Número de pontos para desenhar o X
        N = 2000
        
        # Número de pontos para desenharo O
        Nbola = 10000
        
        # X
        self.xx = np.random.normal(loc = 0, scale = 0.05, size = N)
        self.yx1 = 2*self.xx + np.random.normal(scale = 0.1/3, size = N) 
        self.yx2 = -2*self.xx + np.random.normal(scale = 0.1/3, size = N) 

        # Bola
        self.xb = np.random.normal(loc = 0, scale = 0.05, size = Nbola)
        self.yb = np.random.normal(scale = 0.1, size = Nbola)         
        self.s = np.random.normal(loc = 2, scale = 0.1, size = Nbola)
        self.eps = np.random.normal(scale = 0.008/5)

    def reset(self):
        '''
        Reseta o tabuleiro, para começar novo jogo
        '''
        self.state = np.empty(shape = (3, 3))
        self.state[:] = np.nan
        self.__convert_state()
        self.starter = 1 - self.starter
        self.cur = None
        
    def __check_move(self, i, j):
        return np.isnan(self.state[i,j])
    
    def play(self, jogador, movimento):
        '''
        Jogador faz o movimento
        
        
        @args
        
        jogador -- 0, 1 ou None. Se None, o tabuleiro realiza a jogada para o próximo jogador. 
                        0 ou 1 para representar um jogador específico. Em tese esse parâmetro não preciso ser 
                        utilizado a menos que você queira manter um controle de erro sobre quem está jogando 
                        naquela vez.
        movimento -- uma tupla (linha, coluna), linha \in [0,1,2] e coluna \in [0,1,2]. O jogador atual marca
                        a posição linha, coluna.
                        
        
        @returns
        
        Retorna True se bem-sucedida
        
        '''
        i = movimento[0]
        j = movimento[1]
        
        if not self.__check_move(i,j):
            #raise ValueError("Erro! movimento ({},{}) não permitido".format(i,j))
            print("Erro! movimento ({},{}) não permitido".format(i,j))
            return False
        
        if jogador is None:
            if self.cur is None:
                self.cur = 0
            jogador = self.cur
            
        if jogador not in [0,1]:
            raise ValueError("Erro! jogador deve ser 0 ou 1")
        
        if self.cur is None:
            self.cur = jogador
        else:
            if self.cur != jogador:
                raise ValueError("Erro! Não é a vez do jogador {}".format(jogador))
        
        self.state[i,j] = jogador
        self.__convert_state()
        self.cur = 1 - self.cur
        return True
        
    def check_result(self):
        '''
        Método para verificar se o jogo acabou, usando a soma das colunas / linhas.        
        
        @returns
        
        resultado, motivo -- resultado é None se o jogo não acabou ainda; 1 se o jogador 1 ganhou;
                                -1 se o jogador 0 ganhou; 0 se foi empate.
                             motivo é None se o jogo não acabou ainda, ou se foi empate. Caso contrário, dá
                             as coordenadas da linha, coluna ou diagonal que causou o fim do jogo
                                
        ''' 
        colsum = self.state.sum(axis = 1)
        if np.any(colsum == 3):
            # 1 ganhou
            i = int(np.where(colsum == 3)[0])
            return 1, (3,i)
        elif np.any(colsum == 0):
            # 0 ganhou
            i = int(np.where(colsum == 0)[0])
            return -1, (3,i)
        rowsum = self.state.sum(axis= 0)
        if np.any(rowsum == 3):
            # 1 ganhou
            i = int(np.where(rowsum == 3)[0])
            return 1, (i,3)
        elif np.any(rowsum == 0):
            # 0 ganhou
            i = int(np.where(rowsum == 0)[0])
            return -1, (i,3)
        # Diagonal
        diag = self.state[0,0] + self.state[1,1] + self.state[2,2]
        if diag == 0:
            return -1, (-3,-3)
        elif diag == 3:
            return 1, (-3,-3)
        
        # Segunda diagonal
        diag = self.state[0,2] + self.state[1,1] + self.state[2,0]
        if diag == 0:
            return -1, (3,3)
        elif diag == 3:
            return 1, (3, 3)
        
        
        if np.any(np.isnan(self.state)):
            # ainda não acabou
            return None, None
        else:
            # empatou
            return 0, None
        
    def __convert_state(self):
        '''
        Interna, para converter o estado do tabuleiro num inteiro em base 3
        0 = O, 1 = X, None = empty position
        '''

        istate = 0
        tmpstate = self.state.copy()
        tmpstate[np.isnan(tmpstate)] = 2
        tmpstate = tmpstate.flatten().astype(int)

        sstate = np.array2string(tmpstate, separator = "", prefix= "")[1:-1]
            
        self.istate = int(sstate, 3)
        self.sstate = sstate

   
    def start_free(self, p1 = None):
        '''
        Inicia a janela com o tabuleiro para jogo entre dois humanos.
        Se um jogador robô é passado como argumento, inclui a opção de exibir a avaliação deste jogador
        para qualquer posição
        
        '''

        # Reseta o tabuleiro atual
        self.reset()
        
        # Método para capturar os eventos de clique no tabuleiro
        def onclick(self, event):
            if self.a is not None:
                self.show_pos(self.sstate)
                self.a = None
            if event.button == 3:
                # Right-click: avalia posição
                if p1 is not None:
                    strpos = self.sstate
                    if self.cur == 0:
                        # Inverte posição 
                        strpos = "".join(['0' if strpos[i] == '1' else '1' if strpos[i] == '0' else strpos[i] for i in range(len(strpos))])
                    a, r = p1.avalia_posicao(strpos)
                    self.plot_rewards(a, r)
                    self.a = a
                    

            else:
                ix, iy = event.xdata, event.ydata
                if ix is not None and iy is not None:
                    r, tipo = self.check_result()

                    if r is not None:
                        # Jogo acabou, redesenha
                        plt.cla()
                        plt.vlines(x = 1/2, ymin = 0, ymax = 3)
                        plt.vlines(x = 1, ymin = 0, ymax = 3)
                        plt.hlines(y = 1, xmin = 0, xmax = 3/2)
                        plt.hlines(y = 2, xmin = 0, xmax = 3/2)
                        plt.axis('off')
                        self.reset()
                    else:
                        # Jogo não acabou, desenha o símbolo correspondente ao jogador atual no quadrado clicado
                        if ix > 0.0 and ix < 1.5:
                            if ix <= 0.5:
                                i = 0
                            elif ix <= 1.:
                                i = 1
                            else:
                                i = 2
                        else:
                            i = None

                        if iy > 0.0 and iy <= 3:
                            if iy <= 1.:
                                j = 0
                            elif iy <= 2:
                                j = 1
                            else:
                                j = 2
                        else:
                            j = None

                        if i is not None and j is not None:
                            # Se o clique foi num quadrado válido do tabuleiro

                            # Executa o movimento
                            res = self.play(None, (i,j))

                            if res:
                                # Centro do quadrado
                                xc = i/2 + .235
                                yc = 0.5 + j 
                                if self.cur:
                                    # Jogador anterior é o X
                                    x = self.xx + xc
                                    y = self.yx1 + yc
                                    y2 = self.yx2 + yc                    
                                    plt.scatter(x, y, s =  self.s, c = 'blue')
                                    plt.scatter(x, y2, s =  self.s, c = 'blue')    
                                else:
                                    # Jogador anterior é o O
                                    x = self.xb + xc
                                    y = self.yb + yc
                                    z = [z for z in zip(x,y) if .25*(z[1]-yc)**2 + (z[0]-xc)**2 >= 0.008 + self.eps ]
                                    x = [zz[0] for zz in z]
                                    y = [zz[1] for zz in z]
                                    plt.scatter(x, y, s =  self.s, c = 'orange')


                            # Verifica se o jogo acabou após esse movimento
                            r, tipo = self.check_result()

                            if r is not None:
                                if r == 0:
                                    print("Empate")
                                elif r == 1:
                                    print("X ganhou")
                                    # Desenha no tabuleiro a reta que indica o motivo da vitória
                                    if tipo[0] == 3 and tipo[1] != 3:
                                        # Ganhou na coluna
                                        col = tipo[1]
                                        xr = np.repeat(0.25 + col*0.5, 10)
                                        yr = np.linspace(0, 3, 10)
                                        plt.plot(xr, yr, '-', color = 'red', linewidth = 5)
                                    elif tipo[1] == 3 and tipo[0] != 3:
                                        # Ganhou na linha
                                        lin = tipo[0]
                                        xr = np.linspace(0, 1.5, 10)
                                        yr = np.repeat(0.5 + lin, 10)
                                        plt.plot(xr, yr, '-', color = 'red', linewidth = 5)
                                    elif tipo[0] == 3:
                                        # Ganhou na diagonal principal
                                        xr = np.linspace(0., 1.5, 10)
                                        yr = np.linspace(3, 0, 10)
                                        plt.plot(xr, yr, '-', color = 'red', linewidth = 5)
                                    else:
                                        # Ganhou na diagonal secundária
                                        xr = np.linspace(0., 1.5, 10)
                                        yr = np.linspace(0, 3, 10)
                                        plt.plot(xr, yr, '-', color = 'red', linewidth = 5)                        
                                elif r == -1:
                                    print("O ganhou")
                                    if tipo[0] == 3 and tipo[1] != 3:
                                        # Ganhou na coluna
                                        col = tipo[1]
                                        xr = np.repeat(0.25 + col*0.5, 10)
                                        yr = np.linspace(0, 3, 10)
                                        plt.plot(xr, yr, '-', color = 'red', linewidth = 5)
                                    elif tipo[1] == 3 and tipo[0] != 3:
                                        # Ganhou na linha
                                        lin = tipo[0]
                                        xr = np.linspace(0, 1.5, 10)
                                        yr = np.repeat(0.5 + lin, 10)
                                        plt.plot(xr, yr, '-', color = 'red', linewidth = 5)
                                    elif tipo[0] == 3:
                                        # Ganhou na diagonal principal
                                        xr = np.linspace(0, 1.5, 10)
                                        yr = np.linspace(3, 0, 10)
                                        plt.plot(xr, yr, '-', color = 'red', linewidth = 5)
                                    else:
                                        # Ganhou na diagonal secundária
                                        xr = np.linspace(0, 1.5, 10)
                                        yr = np.linspace(0, 3, 10)
                                        plt.plot(xr, yr, '-', color = 'red', linewidth = 5)                        

                plt.show()


        fig = plt.figure(figsize = (10, 10))

        plt.vlines(x = 1/2, ymin = 0, ymax = 3)
        plt.vlines(x = 1, ymin = 0, ymax = 3)
        plt.hlines(y = 1, xmin = 0, xmax = 3/2)
        plt.hlines(y = 2, xmin = 0, xmax = 3/2)
        plt.axis('off')

        cid = fig.canvas.mpl_connect('button_press_event', lambda l:onclick(self, l))


        plt.show()        
        
        
    def start(self, p1):
        '''
        Tabuleiro para humano x computador (p1)
        
        @args
        
        p1 -- um objeto da classe owg_player
        '''
        
        p1.reset()

        
        self.reset()
        
        # Função para capturar o evento de clique no tabuleiro
        def onclick(self, event):
            ix, iy = event.xdata, event.ydata
            if ix is not None and iy is not None:
                # Checa o resultado
                r, tipo = self.check_result()

                if r is not None:
                    # Jogo acabou, redesenha o tabuleiro
                    plt.cla()
                    plt.vlines(x = 1/2, ymin = 0, ymax = 3)
                    plt.vlines(x = 1, ymin = 0, ymax = 3)
                    plt.hlines(y = 1, xmin = 0, xmax = 3/2)
                    plt.hlines(y = 2, xmin = 0, xmax = 3/2)
                    plt.axis('off')
                    self.reset()
                    self.cur = 1 - self.starter
                    p1.reset()

                    # Verifica quem começa o próximo jogo
                    if self.starter == 0:
                        # Computador joga
                        movimento = p1.joga()

                        # Processa o movimento proposto
                        if movimento is not None:
                            res = self.play(None, movimento)
                            i = movimento[0]
                            j = movimento[1]
                            if res:
                                # Centro do quadrado
                                xc = i/2 + .235
                                yc = 0.5 + j 
                                if self.cur:
                                    x = self.xx + xc
                                    y = self.yx1 + yc
                                    y2 = self.yx2 + yc                    
                                    plt.scatter(x, y, s =  self.s, c = 'blue')
                                    plt.scatter(x, y2, s =  self.s, c = 'blue')    
                                else:
                                    x = self.xb + xc
                                    y = self.yb + yc
                                    z = [z for z in zip(x,y) if .25*(z[1]-yc)**2 + (z[0]-xc)**2 >= 0.008 + self.eps]
                                    x = [zz[0] for zz in z]
                                    y = [zz[1] for zz in z]
                                    plt.scatter(x, y, s =  self.s, c = 'orange')                
                else:
                    # Jogo não acabou
                    # Processa as coordenadas do clique, se for movimento válido realiza o movimento
                    if ix > 0.0 and ix < 1.5:
                        if ix <= 0.5:
                            i = 0
                        elif ix <= 1.:
                            i = 1
                        else:
                            i = 2
                    else:
                        i = None

                    if iy > 0.0 and iy <= 3:
                        if iy <= 1.:
                            j = 0
                        elif iy <= 2:
                            j = 1
                        else:
                            j = 2
                    else:
                        j = None

                    if i is not None and j is not None:
                        res = self.play(None, (i,j))
                        if res:
                            # Centro do quadrado
                            xc = i/2 + .235
                            yc = 0.5 + j 
                            if self.cur:
                                x = self.xx + xc
                                y = self.yx1 + yc
                                y2 = self.yx2 + yc                    
                                plt.scatter(x, y, s =  self.s, c = 'blue')
                                plt.scatter(x, y2, s =  self.s, c = 'blue')    
                            else:
                                x = self.xb + xc
                                y = self.yb + yc
                                z = [z for z in zip(x,y) if .25*(z[1]-yc)**2 + (z[0]-xc)**2 >= 0.008 + self.eps ]
                                x = [zz[0] for zz in z]
                                y = [zz[1] for zz in z]
                                plt.scatter(x, y, s =  self.s, c = 'orange')


                        # Verifica o resultado após o movimento
                        r, tipo = self.check_result()

                        if r is not None:
                            # Acabou
                            if r == 0:
                                print("Empate")
                            elif r == 1:
                                print("X ganhou")
                                # Desenha a linha que indica o motivo da vitória
                                if tipo[0] == 3 and tipo[1] != 3:
                                    # Ganhou na coluna
                                    col = tipo[1]
                                    xr = np.repeat(0.25 + col*0.5, 10)
                                    yr = np.linspace(0, 3, 10)
                                    plt.plot(xr, yr, '-', color = 'red', linewidth = 5)
                                elif tipo[1] == 3 and tipo[0] != 3:
                                    # Ganhou na linha
                                    lin = tipo[0]
                                    xr = np.linspace(0, 1.5, 10)
                                    yr = np.repeat(0.5 + lin, 10)
                                    plt.plot(xr, yr, '-', color = 'red', linewidth = 5)
                                elif tipo[0] == 3:
                                    # Ganhou na diagonal principal
                                    xr = np.linspace(0., 1.5, 10)
                                    yr = np.linspace(3, 0, 10)
                                    plt.plot(xr, yr, '-', color = 'red', linewidth = 5)
                                else:
                                    # Ganhou na diagonal secundária
                                    xr = np.linspace(0., 1.5, 10)
                                    yr = np.linspace(0, 3, 10)
                                    plt.plot(xr, yr, '-', color = 'red', linewidth = 5)                        
                            elif r == -1:
                                print("O ganhou")
                                # Desenha a linha que indica o motivo da vitória
                                if tipo[0] == 3 and tipo[1] != 3:
                                    # Ganhou na coluna
                                    col = tipo[1]
                                    xr = np.repeat(0.25 + col*0.5, 10)
                                    yr = np.linspace(0, 3, 10)
                                    plt.plot(xr, yr, '-', color = 'red', linewidth = 5)
                                elif tipo[1] == 3 and tipo[0] != 3:
                                    # Ganhou na linha
                                    lin = tipo[0]
                                    xr = np.linspace(0, 1.5, 10)
                                    yr = np.repeat(0.5 + lin, 10)
                                    plt.plot(xr, yr, '-', color = 'red', linewidth = 5)
                                elif tipo[0] == 3:
                                    # Ganhou na diagonal principal
                                    xr = np.linspace(0, 1.5, 10)
                                    yr = np.linspace(3, 0, 10)
                                    plt.plot(xr, yr, '-', color = 'red', linewidth = 5)
                                else:
                                    # Ganhou na diagonal secundária
                                    xr = np.linspace(0, 1.5, 10)
                                    yr = np.linspace(0, 3, 10)
                                    plt.plot(xr, yr, '-', color = 'red', linewidth = 5)                        

                    # Comunica o movimento atual ao robô
                    p1.comunica((i,j))     
                    # Robô joga
                    movimento = p1.joga()

                    # Processa o movimento
                    if movimento is not None:
                        res = self.play(None, movimento)
                        i = movimento[0]
                        j = movimento[1]
                        if res:
                            # Centro do quadrado
                            xc = i/2 + .235
                            yc = 0.5 + j 
                            if self.cur:
                                x = self.xx + xc
                                y = self.yx1 + yc
                                y2 = self.yx2 + yc                    
                                plt.scatter(x, y, s =  self.s, c = 'blue')
                                plt.scatter(x, y2, s =  self.s, c = 'blue')    
                            else:
                                x = self.xb + xc
                                y = self.yb + yc
                                z = [z for z in zip(x,y) if .25*(z[1]-yc)**2 + (z[0]-xc)**2 >= 0.008 + self.eps ]
                                x = [zz[0] for zz in z]
                                y = [zz[1] for zz in z]
                                plt.scatter(x, y, s =  self.s, c = 'orange')


                        # Verifica se o jogo acabou após movimento do robô
                        r, tipo = self.check_result()

                        if r is not None:
                            if r == 0:
                                print("Empate")
                            elif r == 1:
                                print("X ganhou")
                                if tipo[0] == 3 and tipo[1] != 3:
                                    # Ganhou na coluna
                                    col = tipo[1]
                                    xr = np.repeat(0.25 + col*0.5, 10)
                                    yr = np.linspace(0, 3, 10)
                                    plt.plot(xr, yr, '-', color = 'red', linewidth = 5)
                                elif tipo[1] == 3 and tipo[0] != 3:
                                    # Ganhou na linha
                                    lin = tipo[0]
                                    xr = np.linspace(0, 1.5, 10)
                                    yr = np.repeat(0.5 + lin, 10)
                                    plt.plot(xr, yr, '-', color = 'red', linewidth = 5)
                                elif tipo[0] == 3:
                                    # Ganhou na diagonal principal
                                    xr = np.linspace(0., 1.5, 10)
                                    yr = np.linspace(3, 0, 10)
                                    plt.plot(xr, yr, '-', color = 'red', linewidth = 5)
                                else:
                                    # Ganhou na diagonal secundária
                                    xr = np.linspace(0., 1.5, 10)
                                    yr = np.linspace(0, 3, 10)
                                    plt.plot(xr, yr, '-', color = 'red', linewidth = 5)                        
                            elif r == -1:
                                print("O ganhou")
                                if tipo[0] == 3 and tipo[1] != 3:
                                    # Ganhou na coluna
                                    col = tipo[1]
                                    xr = np.repeat(0.25 + col*0.5, 10)
                                    yr = np.linspace(0, 3, 10)
                                    plt.plot(xr, yr, '-', color = 'red', linewidth = 5)
                                elif tipo[1] == 3 and tipo[0] != 3:
                                    # Ganhou na linha
                                    lin = tipo[0]
                                    xr = np.linspace(0, 1.5, 10)
                                    yr = np.repeat(0.5 + lin, 10)
                                    plt.plot(xr, yr, '-', color = 'red', linewidth = 5)
                                elif tipo[0] == 3:
                                    # Ganhou na diagonal principal
                                    xr = np.linspace(0, 1.5, 10)
                                    yr = np.linspace(3, 0, 10)
                                    plt.plot(xr, yr, '-', color = 'red', linewidth = 5)
                                else:
                                    # Ganhou na diagonal secundária
                                    xr = np.linspace(0, 1.5, 10)
                                    yr = np.linspace(0, 3, 10)
                                    plt.plot(xr, yr, '-', color = 'red', linewidth = 5)                                                        


                plt.show()


        fig = plt.figure(figsize = (10, 10))

        plt.vlines(x = 1/2, ymin = 0, ymax = 3)
        plt.vlines(x = 1, ymin = 0, ymax = 3)
        plt.hlines(y = 1, xmin = 0, xmax = 3/2)
        plt.hlines(y = 2, xmin = 0, xmax = 3/2)
        plt.axis('off')
        
        
        # Quem começa?
        if self.starter == 0:
            # Robô começa
            movimento = p1.joga()

            # Processa movimento
            if movimento is not None:
                res = self.play(None, movimento)
                i = movimento[0]
                j = movimento[1]
                if res:
                    # Centro do quadrado
                    xc = i/2 + .235
                    yc = 0.5 + j 
                    if self.cur:
                        x = self.xx + xc
                        y = self.yx1 + yc
                        y2 = self.yx2 + yc                    
                        plt.scatter(x, y, s = self.s, c = 'blue')
                        plt.scatter(x, y2, s =  self.s, c = 'blue')    
                    else:
                        x = self.xb + xc
                        y = self.yb + yc
                        z = [z for z in zip(x,y) if .25*(z[1]-yc)**2 + (z[0]-xc)**2 >= 0.008 + self.eps ]
                        x = [zz[0] for zz in z]
                        y = [zz[1] for zz in z]
                        plt.scatter(x, y, s =  self.s, c = 'orange')

        cid = fig.canvas.mpl_connect('button_press_event', lambda l:onclick(self, l))


        plt.show()                
        
        
    def show_pos(self, strpos, rewards = None):
        '''
        Inicia a janela com o tabuleiro numa determinada posição, e 
        mostra os rewards associados com cada possível movimento (para o jogador X)
        
        '''


        # Reseta o tabuleiro atual
        #self.reset()

        def draw(i, j, cur):
            '''
            Desenha o símbolo correspondente ao jogador atual, na casa (i,j)
            '''
            xc = i/2 + .235
            yc = 0.5 + j 
            if cur:
                # Jogador atual é o X
                x = self.xx + xc
                y = self.yx1 + yc
                y2 = self.yx2 + yc                    
                plt.scatter(x, y, s =  self.s, c = 'blue')
                plt.scatter(x, y2, s =  self.s, c = 'blue')    
            else:
                # Jogador atual é o O
                x = self.xb + xc
                y = self.yb + yc
                z = [z for z in zip(x,y) if .25*(z[1]-yc)**2 + (z[0]-xc)**2 >= 0.008 + self.eps ]
                x = [zz[0] for zz in z]
                y = [zz[1] for zz in z]
                plt.scatter(x, y, s =  self.s, c = 'orange')     
                
                
        def draw_alpha(i, j, cur, alpha, reward):
            '''
            Desenha o símbolo X na casa (i,j), com transparência alpha
            '''
            xc = i/2 + .235
            yc = 0.5 + j 

            x = self.xx + xc
            y = self.yx1 + yc
            y2 = self.yx2 + yc                    
            plt.scatter(x, y, s =  self.s, c = 'gray', alpha = alpha)
            plt.scatter(x, y2, s =  self.s, c = 'gray', alpha = alpha)         
            plt.annotate("%5.2f" % reward, (xc-0.03, yc+0.3), color = 'black', fontsize = 16)
        

        # Desenha o tabuleiro
        if rewards is not None:
            fig = plt.figure(figsize = (10, 10))        
        plt.cla()
        plt.vlines(x = 1/2, ymin = 0, ymax = 3)
        plt.vlines(x = 1, ymin = 0, ymax = 3)
        plt.hlines(y = 1, xmin = 0, xmax = 3/2)
        plt.hlines(y = 2, xmin = 0, xmax = 3/2)
        plt.axis('off')

        
        

        pos = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
        for l in range(len(pos)):
            c = strpos[l]
            if c in ('0','1'):
                # Linha
                cur = int(c)
                i = pos[l][0]
                j = pos[l][1]
                draw(i,j, 1-cur)
   
        if rewards is not None:        
            mov = rewards[0]
            rew = rewards[1]

            # Converte as recompensas numa escala [0,1] para a transparência dos pontos
            maxr = max(rew)
            minr = min(rew)
            d = maxr - minr
            if d > 0:
                minr = minr - abs(d)*0.1
                maxr = maxr + abs(d)*0.1
                alphas = [(r-minr)/(maxr-minr) for r in rew]
            else:
                alphas = [0.5]*len(rew)

            for (m,r, a) in zip(mov, rew, alphas):
                i = pos[m][0]
                j = pos[m][1]
                draw_alpha(i, j, 1, a, r)


        plt.show()   
        
    def plot_rewards(self, mov, rew):
        '''
        Mostra os rewards associados com cada possível movimento (para o jogador X)
        sem inicializar / desenhar o tabuleiro
        
        '''

                
        def draw_alpha(i, j, cur, alpha, reward):
            '''
            Desenha o símbolo X na casa (i,j), com transparência alpha
            '''
            xc = i/2 + .235
            yc = 0.5 + j 

            if cur:
                x = self.xx + xc
                y = self.yx1 + yc
                y2 = self.yx2 + yc                    
                plt.scatter(x, y, s = self.s, c = 'gray', alpha = alpha)
                plt.scatter(x, y2, s = self.s, c = 'gray', alpha = alpha)       
                plt.annotate("%5.2f" % reward, (xc-0.03, yc+0.3), color = 'gray', fontsize = 16)      

            else:
                # Jogador atual é o O
                x = self.xb + xc
                y = self.yb + yc
                z = [z for z in zip(x,y) if .25*(z[1]-yc)**2 + (z[0]-xc)**2 >= 0.008 + self.eps ]
                x = [zz[0] for zz in z]
                y = [zz[1] for zz in z]
                plt.scatter(x, y, s =  self.s, c = 'gray', alpha = alpha)     
                plt.annotate("%5.2f" % reward, (xc-0.03, yc+0.4), color = 'gray', fontsize = 16)      
                

        pos = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]

        # Converte as recompensas numa escala ]0,1[ para a transparência dos pontos
        maxr = max(rew)
        minr = min(rew)
        d = maxr - minr
        if d > 0:
            minr = minr - abs(d)*0.1
            maxr = maxr + abs(d)*0.1
            alphas = [(r-minr)/(maxr-minr) for r in rew]
        else:
            alphas = [0.5]*len(rew)

        for (m,r, a) in zip(mov, rew, alphas):
            i = pos[m][0]
            j = pos[m][1]
            if self.cur is None:
                draw_alpha(i, j, 1, a, r)    
            else:
                draw_alpha(i, j, 1-self.cur, a, r)
  
        plt.show()        