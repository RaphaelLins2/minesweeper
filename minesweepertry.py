import random as rng

class cell:
    #iniciando as variaveis para cada celula
    def __init__(self, bomba, cordX, cordY):
        self.bomba = bomba
        self.cordX = cordX
        self.cordY = cordY
        self.revelada = False
    
    #descobrir se a própria celula é uma bomba ou não
    def descobrir_se_bomba(self, coords_bombas):
        if [self.cordX, self.cordY] in coords_bombas: #compara a própria coordenada na lista de bombas para descobrir se é uma bomba
            self.bomba = True

    def dizer_se_bomba(self):
        #simplesmente retorna verdadeiro ou 
        #falso com base se é ou não uma bomba
        return self.bomba

    def perguntar_se_bomb(self, campo):
        #checa num raio quadrado de 1 se os vizinhos tem ou não uma bomba
        if self.bomba == True:
            #caso seja uma bomba, não precisa checar bombas ao redor
            print('Eu sou uma bomba! :D')
            pass
        else:
            #iniciando variavel de bombas na redondeza
            bombas_ao_redor = 0
            #olhando numa area de raio igual a 1 na celula
            for cx in [-1, 0, 1]:
                for cy in [-1, 0, 1]:
                    if cx == 0 and cy == 0:
                        continue #pular a própria coordenada mesmo que não necessário
                    vizinho_x = self.cordX + cx
                    vizinho_y = self.cordY + cy

                    #checando primeiramente para ver se o vizinho está dentro dos limites
                    if 0 <= vizinho_x < len(campo[0]) and 0 <= vizinho_y < len(campo):
                        #dando a localização do vizinho
                        vizinho = campo[vizinho_y][vizinho_x]
                        if vizinho.dizer_se_bomba():
                            #pegando a informação de bomba do vizinho caso ele tenha
                            bombas_ao_redor +=1

        #definindo a variavel de bombas ao redor dentro da variavel
        #para poder usar em outras areas do código

            return bombas_ao_redor

    def revelar(self, campo, lista_bombas):
        self.descobrir_se_bomba(lista_bombas)
        if self.bomba == True:
            print("eu era uma bomba! você perdeu kkk")
            return True
        else:
            print(f'bombas perto {self.perguntar_se_bomb(campo)}')
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
    X = rng.randint(0,campo_tamanho_X)
    Y = rng.randint(0,campo_tamanho_Y)
    

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
print('Lista de bombas pronta!')

# ideia de código para gerar campo: fazer uma lista grande msm
# já que o código se guia pelas coordenadas de cada célula
# apenas teriamos que colocar um somador automático indo primeiro
# de 0 até o tamanho do campo desejado para x então 
# repitindo o mesmo código pela quantidade de vezes que tenhamos 
# linhas y pedidas, até que se forme um campo. Para adicionar
# as bombas, perguntaremos ao código de geração de bomba se na 
# nossa coordenada é uma bomba ou não, também poderiamos integrar 
# o código em um só 

#criando campo

campo =[cell(False,X,Y) for i in range(campo_area)] 


#print(campo)

#gameplay

print('jogando campo minado broxa!')

valor_max_Y_campo = len(campo)/campo_tamanho_X
print(f'o tamanho do campo em Y é: {valor_max_Y_campo}')



x=int(input('diga uma coordenada x para revelar!'))
y=int(input('diga uma coordenada y para revelar!'))
id_bomba =  x + (campo_tamanho_X*(y-1))
print(campo[id_bomba])
campo[id_bomba].revelar(campo, coordenadas_bombas)

while True:
    x=int(input('diga uma coordenada x para revelar!'))
    y=int(input('diga uma coordenada y para revelar!'))

    

    say = campo(cell)
    
    if say.revelar(campo, coordenadas_bombas) == True:
        break
