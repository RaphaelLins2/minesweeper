import pygame
import sys
from minesweepertry import campo, campo_tamanho_X, campo_tamanho_Y, coordenadas_bombas  # importa do seu arquivo atual

jogo_perdido = False
jogo_vencido = False


# Configurações
TAM_CELULA = 40
LARGURA = campo_tamanho_X * TAM_CELULA
ALTURA = campo_tamanho_Y * TAM_CELULA
FPS = 60

# Cores
COR_FUNDO = (20, 20, 20)
COR_GRADE = (50, 50, 50)
COR_REVELADO = (80, 80, 80)
COR_TEXTO = (200, 200, 200)
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

        if celula.revelada:
            pygame.draw.rect(tela, COR_REVELADO, ret)
            if celula.bomba:
                pygame.draw.circle(tela, COR_BOMBA, ret.center, TAM_CELULA // 4)
            else:
                n = celula.perguntar_se_bomb(campo_tamanho_X, campo, campo_tamanho_Y)
                if n > 0:
                    texto = fonte.render(str(n), True, COR_TEXTO)
                    tela.blit(texto, (x + TAM_CELULA // 4, y + TAM_CELULA // 4))
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



    tela.fill(COR_FUNDO)
    desenhar_campo()
    if jogo_perdido:
        msg = fonte.render("Você perdeu! Aperte ESC para sair.", True, (255, 0, 0))
        tela.blit(msg, (20, 10))
    
    if jogo_vencido:
        msg = fonte.render("Você venceu! Parabéns! ESC para sair.", True, (0, 255, 0))
        tela.blit(msg, (20, 10))
    
    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()

    
    pygame.display.flip()
    relogio.tick(FPS)
