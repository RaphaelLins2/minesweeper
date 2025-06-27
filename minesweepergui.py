import pygame
import sys
import time
from minesweepertry import campo, campo_tamanho_X, campo_tamanho_Y, coordenadas_bombas  # importa do seu arquivo atual

jogo_perdido = False
jogo_vencido = False

#começar timer

mostrou_timer = False
timer_comecou = False


# Configurações
TAM_CELULA = 25
LARGURA = campo_tamanho_X * TAM_CELULA
ALTURA = campo_tamanho_Y * TAM_CELULA
FPS = 60

# Cores
COR_FUNDO = (20, 20, 20)
COR_GRADE = (100, 100, 100)
COR_REVELADO = (80, 80, 80)
COR_BANDEIRA = (0,250,0)
COR_TEXTO = (200, 200, 200)
COR_T1=(70,130,180)
COR_T2=(0,100,0)
COR_T3=(200,0,0)
COR_T4=(0,0,100)
COR_T5=(100,0,0)
COR_T6=(0,50,100)
COR_T7=(80,0,180)
COR_T8=(80,80,80)
COR_BOMBA = (200, 50, 50)

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Campo Minado Broxa")
fonte = pygame.font.SysFont(None, 30)
relogio = pygame.time.Clock()

# Função para desenhar o campo
def desenhar_campo():
    for celula in campo:
        x = celula.cordX * TAM_CELULA
        y = celula.cordY * TAM_CELULA
        ret = pygame.Rect(x, y, TAM_CELULA, TAM_CELULA)

        if celula.revelada :
            pygame.draw.rect(tela, COR_REVELADO, ret)
            if celula.bomba:
                pygame.draw.circle(tela, COR_BOMBA, ret.center, TAM_CELULA // 4)
            else:
                if celula.num_bombas > 0:
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
                if celula.num_bombas == 0 :
                    celula.revelar_adjacente(campo, campo_tamanho_X, campo_tamanho_Y, coordenadas_bombas)
        elif celula.bandeira:
            pygame.draw.rect(tela, COR_BANDEIRA, ret)
        else:
            pygame.draw.rect(tela, COR_FUNDO, ret)

        pygame.draw.rect(tela, COR_GRADE, ret, 1)

# Função para pegar célula ao clicar
def pegar_celula_por_coordenada(px, py):
    x = px // TAM_CELULA
    y = py // TAM_CELULA
    for celula in campo:
        if celula.cordX == x and celula.cordY == y:
            return celula
    return None

def checar_vitoria():
    for c in campo:
        if not c.bomba and not c.revelada:
            return False
    return True

# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and not (jogo_perdido or jogo_vencido):
            if timer_comecou == False:
                start_time = time.perf_counter()
                timer_comecou =True
            mx, my = pygame.mouse.get_pos()
            cel = pegar_celula_por_coordenada(mx, my)
            
            if cel and not cel.revelada:
                perdeu = cel.revelar(campo, coordenadas_bombas, campo_tamanho_X, campo_tamanho_Y)
                if perdeu:
                    jogo_perdido = True
                    for c in campo:
                        if c.bomba:
                            c.revelada = True
                elif checar_vitoria():
                    jogo_vencido = True
                    for c in campo:
                        c.revelada = True
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 3 and not (jogo_perdido or jogo_vencido):
            mx, my = pygame.mouse.get_pos()
            cel = pegar_celula_por_coordenada(mx, my)
            if cel and not cel.revelada:
                if cel.bandeira:
                    cel.bandeira = False
                else:
                    cel.bandeira = True



    tela.fill(COR_FUNDO)
    desenhar_campo()
    
    if jogo_perdido:
        if mostrou_timer == False:
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            execution_time = str(round(execution_time, 2))
            print(f"Programa executado em: {execution_time} segundos")
            mostrou_timer = True
        msg = fonte.render(f"tempo:{(execution_time)}", True, (255, 0, 0))
        tela.blit(msg, (20, 10))
    
    if jogo_vencido:
        if mostrou_timer == False:
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            execution_time = str(round(execution_time, 2))
            print(f"Programa executado em: {execution_time} segundos")
            mostrou_timer = True
        msg = fonte.render(f"tempo: {(execution_time)}", True, (0, 255, 0))
        tela.blit(msg, (20, 10))
    
    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()

    
    pygame.display.flip()
    relogio.tick(FPS)
