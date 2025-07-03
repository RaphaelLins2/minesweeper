import socket
import threading # usando threading para conseguir aguentar mais de um player
import pickle # biblioteca para (des)serializar objetos em python, deixando mais eficiente a troca entre computadores
import time
from campo_script import campo
from cronometro_script import Cronometro

# 1 - setando o servidor para escutar socket

def obter_ip_local():
    try:
        # Conecta a um servidor externo (sem realmente enviar dados) para descobrir o IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))  # Usa o DNS do Google como destino
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return f"Erro ao obter IP: {e}"

#primeiro pegamos o ip da máquina para que as outras se conectem
host = obter_ip_local()
#selecionando uma porta para rodar o serviço
porta = 65432
#criando uma lista de clientes ativo
clientes = []




def echo_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #configurando a porta que o socket vai ver usando ipv4 e tcp
        #colocando o socket para funcionar no ip do host e na porta especificada
        s.bind((host, porta))

        #agora ele vai ficar vendo tudo o que chega nessa porta para um pedido para o servidor nesse socket que acabamos de criar
        s.listen()

        #agora o progama ficara esperando uma conexão, ou seja ele ficará 
        # parado nessa linha até que um cliente se conecte
        conexao, endereco = s.accept()
        # conexao - um novo objeto socket usado para mandar e receber dados nessa conexão
        # add - o endereço ipv4 do cliente 

    # 3 - Troca de dados

        with conexao:
            # quando a conexão for feita o servidor ira dizer com quem ele se conectou 
            print(f"conexão estabelecida com: {endereco}")
            while True:
                # enquanto verdadeiro o servidor ira receber em conexao até 1kb
                # conexao sendo o socket do cliente e 1kb sendo o 1024  
                dados = conexao.recv(1024)
                if not dados:
                    #se o servidor não receber nada do cliente ele quebra este loop 
                    print("nenhum dado recebido, quebrando o loop")
                    break
                #fazendo um simples echo
                conexao.sendall(dados)

#criando campo

campo_jogo = campo()
campo_jogo.gerar_campo()#criando um campo



def checar_vitoria():
    for c in campo_jogo.campo_list:
        if not c.bomba and not c.revelada and not c.bandeira:
            return False
    return True

def tratar_cliente(conexao, endereco):
    #estados do jogo
    mostrou_timer = False
    timer_comecou = False
    cron = Cronometro()
    jogo_perdido    = False
    jogo_vencido    = False

    print(f'Conectado com {endereco}')

    # enviando com a serialização do pickle as informações de tamanho de campo 
    conexao.send(pickle.dumps((campo_jogo.campo_tamanho_X, campo_jogo.campo_tamanho_Y)))
    # mandando a lista do campo inteiro usando o pickle 
    conexao.sendall(pickle.dumps(campo_jogo.campo_list))


    #loop para escutar os comandos do cliente
    while True:
        #timer flags
        

        try:

            #fica esperando o cliente mandar algo de até 1kb
            dados = conexao.recv(1024)
            if not dados:
                break # se o cliente não mandar nada o loop quebra 

            #decodifiando o comando do player
            comando = pickle.loads(dados)
            tipo, x, y = comando

            #identificando a célula
            id_celula = x + y * campo_jogo.campo_tamanho_X
            cel = campo_jogo.campo_list[id_celula]
            

            if tipo == "revelar" and jogo_perdido == False and jogo_vencido == False:
                if timer_comecou == False:
                    print('timer iniciado')
                    cron.iniciar
                    timer_comecou = True
                # revela a célula caso seja mandado o comando 
                if cel and not cel.revelada:
                    perdeu = cel.revelar(campo_jogo.campo_list, campo_jogo.coordenadas_bombas, campo_jogo.campo_tamanho_X, campo_jogo.campo_tamanho_Y)
                    if perdeu:
                        print('jogo perdido')
                        jogo_perdido = True
                        for c in campo_jogo.campo_list:
                            if c.bomba:
                                c.revelada = True 
                        cron.mostrar_tempo()
                        
                    elif checar_vitoria():
                        print('jogo ganho')
                        jogo_vencido = True
                        for c in campo_jogo.campo_list: #mostra todas as bombas após vencer
                            c.revelada = True
                        cron.mostrar_tempo()
                        

            elif tipo == "bandeira" and jogo_perdido == False and jogo_vencido == False:
                # fica trocando o estado da bandeira
                cel.bandeira = not cel.bandeira

            elif tipo == "reiniciar":
                campo_jogo.gerar_campo()
                jogo_perdido = False
                jogo_vencido = False
                timer_comecou = False

            elif tipo == "retransmitir":
                lista_serializada = pickle.dumps(campo_jogo.campo_list)
                conexao.sendall(lista_serializada)
                print(f"Reenviado campo para {endereco} após pedido de retransmissão.")
            # por algum motivo o retransmetir pode causar um loop infinito que deixa o jogo injogvél
            # possivelmente deve haver com o fato de que o retransmitir atualiza todos os clientes ao mesmo tempo
            # ver isso de imediato 

            
            
            #enviando de volta o campo pós comando para o cliente que fez o comando especificamente
            #temos que mudar isso para que ele mande isso para todos os clientes ao mesmo tempo
            # código antigo > conexao.sendall(pickle.dumps(campo_jogo.campo_list))
            #código novo:
            for c in clientes[:]:  # usa uma cópia para evitar erro se alguém for removido
                try:
                    c.sendall(pickle.dumps(campo_jogo.campo_list))
                except:
                    print("Um cliente desconectou.")
                    clientes.remove(c)

        except Exception as e:
            print(f'Erro: {e}')
            break
    conexao.close()

def main():
    print(f"Hosteando o jogo em {host}:{porta}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        soc.bind((host, porta))
        soc.listen()
        while True:
            conexao, endereco = soc.accept()
            clientes.append(conexao)
            thread = threading.Thread(target=tratar_cliente, args=(conexao, endereco))
            thread.start()

if __name__ == "__main__":
    main()
