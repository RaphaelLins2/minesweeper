
import pygame
import socket
import pickle
import sys
import select

# Configuração da conexão
HOST = input("Digite o IP do host: ")
PORTA = 65432

# Cliente se conecta ao servidor
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORTA))
print("Conectado ao servidor!")

# Recebe tamanho do campo
tamanho = pickle.loads(s.recv(1024))
TAM_X, TAM_Y = tamanho
TAM_CELULA = 25
LARGURA = TAM_X * TAM_CELULA
ALTURA = TAM_Y * TAM_CELULA

# Inicializa Pygame
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Campo Minado Online (Cliente)")
fonte = pygame.font.SysFont(None, 30)
relogio = pygame.time.Clock()

# Cores
COR_FUNDO = (20, 20, 20)
COR_GRADE = (100, 100, 100)
COR_REVELADO = (80, 80, 80)
COR_BOMBA = (200, 50, 50)
COR_BANDEIRA = (0, 250, 0)
COR_TXT = (200, 200, 200)
COR_T1=(70,130,180)
COR_T2=(0,100,0)
COR_T3=(200,0,0)
COR_T4=(0,0,100)
COR_T5=(100,0,0)
COR_T6=(0,50,100)
COR_T7=(80,0,180)
COR_T8=(120,120,120)

# Loop principal
def main():
    campo_remoto = []

    while True:
        # Recebe o estado do campo
        try:
            ready = select.select([s], [], [], 0.01)  # timeout curtíssimo
            if ready[0]:
                try:
                    campo_remoto = pickle.loads(s.recv(65536))
                except Exception as e:
                    
                    print("Erro ao receber dados do servidor:", e)
                    
        except:
            print("Erro ao receber dados do servidor.")
            break

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                s.close()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                x = mx // TAM_CELULA
                y = my // TAM_CELULA
                tipo = "revelar" if evento.button == 1 else "bandeira"
                s.sendall(pickle.dumps((tipo, x, y)))
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    print('reiniciando o campo')
                    tipo = "reiniciar"
                    s.sendall(pickle.dumps((tipo, 0, 0)))
 

        # Desenha o campo
        tela.fill(COR_FUNDO)
        for celula in campo_remoto:
            x = celula.cordX * TAM_CELULA
            y = celula.cordY * TAM_CELULA
            ret = pygame.Rect(x, y, TAM_CELULA, TAM_CELULA)

            if celula.revelada:
                pygame.draw.rect(tela, COR_REVELADO, ret)
                if celula.bomba:
                    pygame.draw.circle(tela, COR_BOMBA, ret.center, TAM_CELULA // 4)
                elif celula.num_bombas > 0:
                    match(celula.num_bombas):
                        case(1):
                            texto = fonte.render(str(celula.num_bombas), True, COR_T1)
                        case(2):
                            texto = fonte.render(str(celula.num_bombas), True, COR_T2)
                        case(3):
                            texto = fonte.render(str(celula.num_bombas), True, COR_T3)
                        case(4):
                            texto = fonte.render(str(celula.num_bombas), True, COR_T4)
                        case(5):
                            texto = fonte.render(str(celula.num_bombas), True, COR_T5)
                        case(6):
                            texto = fonte.render(str(celula.num_bombas), True, COR_T6)
                        case(7):
                            texto = fonte.render(str(celula.num_bombas), True, COR_T7)
                        case(8):
                            texto = fonte.render(str(celula.num_bombas), True, COR_T8)
                    tela.blit(texto, (x + TAM_CELULA // 4, y + TAM_CELULA // 4))
            elif celula.bandeira:
                pygame.draw.rect(tela, COR_BANDEIRA, ret)
            else:
                pygame.draw.rect(tela, COR_FUNDO, ret)

            pygame.draw.rect(tela, COR_GRADE, ret, 1)

        pygame.display.flip()
        relogio.tick(60)

if __name__ == "__main__":
    main()
