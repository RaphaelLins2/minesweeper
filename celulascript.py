class cell:
    #iniciando as variaveis para cada celula
    def __init__(self, bomba, cordX, cordY, cordsbombs):
        self.bomba = bomba
        self.cordX = cordX
        self.cordY = cordY
        self.revelada = False
        self.checada = False
        self.bandeira = False
        self.num_bombas = 0
        self.descobrir_se_bomba(cordsbombs)
    
    #descobrir se a própria celula é uma bomba ou não
    def descobrir_se_bomba(self, coords_bombas):
        if self.bomba == True:
            print('já era uma bomba')
        else:
            print('não era uma bomba antes')
        
        coords = [self.cordX, self.cordY]
        if coords in coords_bombas: #compara a própria coordenada na lista de bombas para descobrir se é uma bomba
            self.bomba = True
            print(f'a celula {self} nas coordenadas {[self.cordX], [self.cordY]}era uma bomba')

    def dizer_se_bomba(self):
        #simplesmente retorna verdadeiro ou 
        #falso com base se é ou não uma bomba

        #sim isso é muito menos ineficiente do que só pedir o self.bomba direto, 
        #mas eu fiz isso no inicio e faz com que algumas partes do código funcione, 
        #e agora eu estou com preguiça de trocar porém com planos futuros
        return self.bomba

    def perguntar_se_bomb(self, Tamanho_X_max, campo, tamanho_y_max):
        #pergunta as celulas ao redor pela informação de bomba
        print(f"perguntando bombas ao redor de {[self.cordX,self.cordY]} ")
        self.checada == True
        if self.bomba: #caso ela seja uma bomba ela ignora o resto do código já que foi revelada e o player perdeu
            print('Eu sou uma bomba! :D')
            return 0

        #faz uma conta para atualizar quantas bombas cada celula está perto de.
        self.num_bombas = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0: #não se auto checa já que não é uma bomba
                    continue

                nx = self.cordX + dx
                ny = self.cordY + dy

                # Verifica se vizinho está dentro dos limites do campo
                if 0 <= nx < Tamanho_X_max and 0 <= ny < tamanho_y_max:
                    id_vizinho = nx + ny * Tamanho_X_max
                    if campo[id_vizinho].dizer_se_bomba(): #caso ele seja uma bomba ele é adicionado ao contador
                        self.num_bombas += 1
                        print(f'Bomba Perto nas coordenadas {nx} {ny}!')
        #retorna o número de bombas totais
        return self.num_bombas

    def revelar(self, campo, lista_bombas, Tamanho_X_max, tamanho_y_max):
        self.checada == True #nao remover isto agora pois em alguma parte do código ele é usado para decidir a vitória
        if self.bandeira == True: #se for uma bandeira não tem como revelar
            return
        else:
            self.descobrir_se_bomba(lista_bombas) #descobre se é uma bomba
            print(f'descobrindo se eu: {self.cordX} {self.cordY} sou uma bomba')
            if self.bomba == True: #caso seja o player perde
                print("eu era uma bomba! você perdeu kkk")
                return True
            else: #caso não, ela apenas se revela e faz a contagem de bombas
                print(f'bombas perto {self.perguntar_se_bomb(Tamanho_X_max, campo, tamanho_y_max)}')
                self.revelada = True
                return False
    
    def revelar_adjacente(self, campo, Tamanho_X_max, tamanho_y_max, lista_bombas):
        #similar ao código de contagem de bombas, porém ele checa as celulas ao redor e revela elas
        #isso é usado exclusivamente para o zerospread (sujeito a mudanças)
        for px in [-1, 0, 1]:
            for py in [-1, 0, 1]:
                if px == 0 and py == 0:
                    continue

                mx = self.cordX + px
                my = self.cordY + py

                if 0 <= mx < Tamanho_X_max and 0 <= my < tamanho_y_max:
                    id_vizinho = mx + my * Tamanho_X_max
                    if campo[id_vizinho].revelada == False:
                        campo[id_vizinho].revelar(campo, lista_bombas, Tamanho_X_max, tamanho_y_max)