import random as rng

class cell:
    #iniciando as variaveis para cada celula
    def __init__(self, bomba, cordX, cordY, cordsbombs):
        self.bomba = bomba
        self.cordX = cordX
        self.cordY = cordY
        self.revelada = False
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
        return self.bomba

    def perguntar_se_bomb(self, Tamanho_X_max, campo, tamanho_y_max):
        if self.bomba:
            print('Eu sou uma bomba! :D')
            return 0

        bombas_ao_redor = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                nx = self.cordX + dx
                ny = self.cordY + dy

                # Verifica se vizinho está dentro dos limites do campo
                if 0 <= nx < Tamanho_X_max and 0 <= ny < tamanho_y_max:
                    id_vizinho = nx + ny * Tamanho_X_max
                    if campo[id_vizinho].dizer_se_bomba():
                        bombas_ao_redor += 1
                        print(f'Bomba Perto nas coordenadas {nx} {ny}!')

        return bombas_ao_redor

    def revelar(self, campo, lista_bombas, Tamanho_X_max, tamanho_y_max):
        self.descobrir_se_bomba(lista_bombas)
        print(f'checando ao redor de minhas coordenadas {self.cordX} {self.cordY}')
        if self.bomba == True:
            print("eu era uma bomba! você perdeu kkk")
            return True
        else:
            print(f'bombas perto {self.perguntar_se_bomb(Tamanho_X_max, campo, tamanho_y_max)}')
            self.revelada = True
            
            return False


class campor:
    def __init__(self):
        pass



#para colocar as bombas no campo pediremos quantas bombas o player quer jogar com
#colocaremos em um loop de for escolhendo uma coordenada x e y nova toda vez até 
#que tenhamos colocado todas as bombas 

#criador de campo
campo_tamanho_X = int(input('Qual a largura do campo?'))
campo_tamanho_Y = int(input('Qual a altura do campo'))
campo_area = (campo_tamanho_X) * (campo_tamanho_Y)
qnt_bomba_max80pc = int(campo_area*0.8) #definindo a quantidade máx de bombas sendo 80% pq sim
qnt_bombas = int(input(f'quantas bombas você quer no campo? (qnt máx: {qnt_bomba_max80pc})'))


coordenadas_bombas = [] # iniciando uma lista para ter as coordenadas de bombas
for i in range(qnt_bombas):
    X = rng.randint(1,campo_tamanho_X)
    Y = rng.randint(1,campo_tamanho_Y)
    

    if ([X, Y]) in coordenadas_bombas:
        print(f"coordenada duplicada {X} {Y}!\nprocurando outra")
        while ([X, Y]) in coordenadas_bombas:
            X = rng.randint(0,campo_tamanho_X)
            Y = rng.randint(0,campo_tamanho_Y)
            print(f'testando as coordenadas {X} {Y}')

    print(f'criada uma bomba nas coordenadas {X} {Y}')
    #precisa ser checada as coordenadas das bombas 
    #já criadas para que não tenha bombas duplicadas
    
    coordenadas_bombas.append([X, Y])
    print('bomba adicionada na lista!')
    print(coordenadas_bombas)
print(f'Lista de bombas pronta! com tamanho de: {len(coordenadas_bombas)}')
'''
# ideia de código para gerar campo: fazer uma lista grande msm
# já que o código se guia pelas coordenadas de cada célula
# apenas teriamos que colocar um somador automático indo primeiro
# de 0 até o tamanho do campo desejado para x então 
# repitindo o mesmo código pela quantidade de vezes que tenhamos 
# linhas y pedidas, até que se forme um campo. Para adicionar
# as bombas, perguntaremos ao código de geração de bomba se na 
# nossa coordenada é uma bomba ou não, também poderiamos integrar 
# o código em um só 
'''

#criando campo
xcamp=0
ycamp=0
campo=[]


for ycamp in range(campo_tamanho_Y):
    for xcamp in range(campo_tamanho_X):
        campo.append(cell(False,xcamp,ycamp,coordenadas_bombas))
#print(campo)

#gameplay
if __name__ == "__main__":
    print('jogando campo minado broxa!')

    while True:
        x=int(input('diga uma coordenada x para revelar!'))
        y=int(input('diga uma coordenada y para revelar!'))

        if y == 0:
            id_bomba =  x + (campo_tamanho_X*(y))
        else:
            id_bomba =  x + (campo_tamanho_X*(y))

        campo[id_bomba].revelar(campo, coordenadas_bombas, campo_tamanho_X, campo_tamanho_Y)

