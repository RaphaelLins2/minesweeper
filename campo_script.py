import random as rng
from celulascript import cell

class campo:
    def __init__(self):
        #iniciando cada valor
        self.campo_tamanho_X = int(input('Qual a largura do campo?'))
        self.campo_tamanho_Y = int(input('Qual a altura do campo'))#tamanho que o player quer o campo

        self.campo_area = (campo_tamanho_X) * (campo_tamanho_Y)
        self.qnt_bomba_max80pc = int(campo_area*0.8) #definindo a quantidade máx de bombas sendo 80% pq sim

        self.qnt_bombas = int(input(f'quantas bombas você quer no campo? (qnt máx: {qnt_bomba_max80pc})'))#quantidade de bombas(no momento nao tem limite kkkkkk)

        self.coordenadas_bombas = []

    def bombas(self):
        for i in range(self.qnt_bombas):
            X = rng.randint(0,self.campo_tamanho_X-1)
            Y = rng.randint(0,self.campo_tamanho_Y-1)
            
            while ([X, Y]) in self.coordenadas_bombas: # checa por coordenadas de bombas duplicadas
                print(f"coordenada duplicada {X} {Y}!\nprocurando outra")
                X = rng.randint(0,self.campo_tamanho_X-1)
                Y = rng.randint(0,self.campo_tamanho_Y-1)
                print(f'testando as coordenadas {X} {Y}')
        
            print(f'criada uma bomba nas coordenadas {X} {Y}')
            
            self.coordenadas_bombas.append([X, Y]) #depois das checagens a bomba é adicionada na lista
            print('bomba adicionada na lista!')
        
        print(self.coordenadas_bombas)
        print(f'Lista de bombas pronta! com tamanho de: {len(self.coordenadas_bombas)}')
    
    def criador_campo(self):
        xcamp=0
        ycamp=0
        campo=[]#nessa lista será onde cada celula será salva

        for ycamp in range(self.campo_tamanho_Y): #possivelmente eu poderia ter usado um for loop no tamanho da area, mas essa versão funciona melhor por algum motivo
            for xcamp in range(self.campo_tamanho_X):
                campo.append(cell(False,xcamp,ycamp,self.coordenadas_bombas))


#criador de campo
campo_tamanho_X = int(input('Qual a largura do campo?'))
campo_tamanho_Y = int(input('Qual a altura do campo'))#tamanho que o player quer o campo

campo_area = (campo_tamanho_X) * (campo_tamanho_Y)
qnt_bomba_max80pc = int(campo_area*0.8) #definindo a quantidade máx de bombas sendo 80% pq sim

qnt_bombas = int(input(f'quantas bombas você quer no campo? (qnt máx: {qnt_bomba_max80pc})'))#quantidade de bombas(no momento nao tem limite kkkkkk)

coordenadas_bombas = [] # iniciando uma lista para ter as coordenadas de bombas

#geração das coordenadas de bombas
for i in range(qnt_bombas):
    X = rng.randint(0,campo_tamanho_X-1)
    Y = rng.randint(0,campo_tamanho_Y-1)
    
    while ([X, Y]) in coordenadas_bombas: # checa por coordenadas de bombas duplicadas
        print(f"coordenada duplicada {X} {Y}!\nprocurando outra")
        X = rng.randint(0,campo_tamanho_X-1)
        Y = rng.randint(0,campo_tamanho_Y-1)
        print(f'testando as coordenadas {X} {Y}')

    print(f'criada uma bomba nas coordenadas {X} {Y}')
    
    coordenadas_bombas.append([X, Y]) #depois das checagens a bomba é adicionada na lista
    print('bomba adicionada na lista!')
    
print(coordenadas_bombas)
print(f'Lista de bombas pronta! com tamanho de: {len(coordenadas_bombas)}')

#criando campo
xcamp=0
ycamp=0
campo=[]#nessa lista será onde cada celula será salva

for ycamp in range(campo_tamanho_Y): #possivelmente eu poderia ter usado um for loop no tamanho da area, mas essa versão funciona melhor por algum motivo
    for xcamp in range(campo_tamanho_X):
        campo.append(cell(False,xcamp,ycamp,coordenadas_bombas))