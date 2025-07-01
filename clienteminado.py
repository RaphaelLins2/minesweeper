import socket
import pickle
import pygame

# configura a conexão
host = str(input("Qual o ip do servidor? "))
porta = 65432

# cliente se conecta com o servidor (IPV4/TCP)
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((host,porta))

#recebendo as informações do campo
dados = soc.recv(1024)
tamanho = pickle.loads(dados)
tam_x, tam_y = tamanho
tam_cel = 25
largura = tam_x * tam_cel
altura = tam_y * tam_cel

def echo_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # mesma coisa do servidor praticamente, ele cria um socket ipv4 tcp
        # e na linha de baixo fica em loop até se conectar com o servidor tendo o host e a port dele
        s.connect((host, porta))


    # 3 - troca de dados
        s.sendall(b"Hello, world")
        # o "b" diz que a mensagem será mandada em unidades de 8bits  

        dados = s.recv(1024)
        #agora já que o servidor não tem mais uso pro cliente e não temos nenhum loop
        #a conexão é desligada


    print(f'Recebemos: {dados}')
