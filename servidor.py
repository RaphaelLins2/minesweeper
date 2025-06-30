import socket
import threading
import pickle
from campo_script import campo

HOST = socket.gethostbyname(socket.gethostname())
PORTA = 65432
clientes = []

campo_jogo = campo()
campo_jogo.gerar_campo()

def tratar_cliente(conn, addr):
    print(f"Conectado com {addr}")
    # Envia tamanho do campo
    conn.send(pickle.dumps((campo_jogo.campo_tamanho_X, campo_jogo.campo_tamanho_Y)))
    
    # Envia estado inicial
    conn.sendall(pickle.dumps(campo_jogo.campo_list))

    while True:
        try:
            dados = conn.recv(1024)
            if not dados:
                break
            comando = pickle.loads(dados)
            tipo, x, y = comando
            print(f"Comando recebido: {tipo} {x} {y}")
            
            id_celula = x + y * campo_jogo.campo_tamanho_X
            cel = campo_jogo.campo_list[id_celula]

            if tipo == "revelar":
                cel.revelar(campo_jogo.campo_list, campo_jogo.coordenadas_bombas,
                            campo_jogo.campo_tamanho_X, campo_jogo.campo_tamanho_Y)
            elif tipo == "bandeira":
                cel.bandeira = not cel.bandeira
            elif tipo == "reiniciar":
                campo_jogo.gerar_campo()

            # Envia o campo atualizado de volta
            # Envia o campo atualizado para todos os clientes conectados
            for c in clientes[:]:  # usa uma cópia para evitar erro se alguém for removido
                try:
                    c.sendall(pickle.dumps(campo_jogo.campo_list))
                except:
                    print("Um cliente desconectou.")
                    clientes.remove(c)
            

        except Exception as e:
            print("Erro:", e)
            break
        
    conn.close()


def main():
    print(f"Hosteando o jogo em {HOST}:{PORTA}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORTA))
        s.listen()
        while True:
            conn, addr = s.accept()
            clientes.append(conn)
            thread = threading.Thread(target=tratar_cliente, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    main()
