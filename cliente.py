import socket
import pickle

HOST = input("Digite o IP do host: ")
PORTA = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORTA))
    print("Conectado ao servidor!")

    tamanho = pickle.loads(s.recv(1024))
    print(f"Tamanho do campo recebido: {tamanho}")

    while True:
        cmd = input("Digite comando (ex: cavar 2 3): ")
        s.sendall(pickle.dumps(cmd))
        resposta = pickle.loads(s.recv(4096))
        print("Campo atualizado recebido.")
        # Aqui você exibiria o campo na tela (usar print por enquanto ou adaptar a interface Pygame depois)
