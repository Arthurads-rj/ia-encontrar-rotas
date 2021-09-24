import pygame
import math
from queue import PriorityQueue

#config. janela
LARGURA = 700
JANELA = pygame.display.set_mode((LARGURA, LARGURA))
pygame.display.set_caption('Algoritmo de Path Finding A*')

#cores
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
ROXO = (128, 0, 128)
LARANJA = (255, 165, 0)
CINZA = (128, 128, 128)
TURQUESA = (64, 224, 208)

class Lugar:
    def __init__(self, linha, coluna, largura, total_linhas):
        self.linha = linha
        self.coluna = coluna
        self.x = linha * largura
        self.y = coluna * largura
        self.cor = BRANCO
        self.vizinhos = []
        self.largura = largura
        self.total_linhas = total_linhas

    def pegar_pos(self):
        #pegar as colunas primeiro, depois linhas
        return self.linha, self.coluna

    def fechado(self):
        return self.cor == VERMELHO

    def aberto(self):
        return self.cor == VERDE

    def barreira(self):
        return self.cor == PRETO

    def começo(self):
        return self.cor == LARANJA

    def fim(self):
        return self.cor == ROXO

    def reset(self):
        self.cor = BRANCO

    def tornar_fechado(self):
        self.cor = VERMELHO

    def tornar_aberto(self):
        self.cor = VERDE

    def tornar_barreira(self):
        self.cor = PRETO

    def tornar_começo(self):
        self.cor = LARANJA

    def tornar_fim(self):
        self.cor = ROXO

    def tornar_caminho(self):
        self.cor = TURQUESA

    def desenhar(self, janela):
        pygame.draw.rect(janela, self.cor, (self.x, self.y, self.largura, self.largura))

    def atualizar_vizinho(self, grid):
        self.vizinhos = []
        if self.linha < self.total_linhas -1 and not grid[self.linha + 1][self.coluna].barreira(): #MOVER PRA BAIXO
            self.vizinhos.append(grid[self.linha + 1][self.coluna])

        if self.linha > 0 and not grid[self.linha - 1][self.coluna].barreira(): #MOVER PRA CIMA
            self.vizinhos.append(grid[self.linha - 1][self.coluna])

        if self.coluna < self.total_linhas -1 and not grid[self.linha][self.coluna + 1].barreira(): #MOVER PRA DIREITA
            self.vizinhos.append(grid[self.linha][self.coluna + 1])

        if self.linha > 0 and not grid[self.linha][self.coluna - 1].barreira(): #MOVER PRA ESQUERDA
            self.vizinhos.append(grid[self.linha][self.coluna - 1])


    def __menorque__(self):
        return False

def h(p1, p2):
    x1, y1, = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruir_caminho(veio_de, atual, desenhar):
    while atual in veio_de:
        atual = veio_de[atual]
        atual.tornar_caminho()
        desenhar()


def algoritmo(desenhar, grid, começo, fim):
    contagem = 0
    set_aberto = PriorityQueue()
    set_aberto.put((0, contagem, começo))
    veio_de = {}
    numero_g = {lugar: float("inf") for linha in grid for lugar in linha}
    numero_g[começo] = 0
    numero_f = {lugar: float("inf") for linha in grid for lugar in linha}
    numero_f[começo] = h(começo.pegar_pos(), fim.pegar_pos())

    set_aberto_hash = {começo}

    while not set_aberto.empty():
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()

        atual = set_aberto.get()[2]
        set_aberto_hash.remove(atual)

        if atual == fim:
            #fazer o caminho
            reconstruir_caminho(veio_de, fim, desenhar)
            fim.tornar_fim()
            começo.tornar_começo()
            return True

        for vizinho in atual.vizinhos:
            numero_g_temporario = numero_g[atual] + 1

            if numero_g_temporario < numero_g[vizinho]:
                veio_de[vizinho] = atual
                numero_g[vizinho] = numero_g_temporario
                numero_f[vizinho] = numero_g_temporario + h(vizinho.pegar_pos(), fim.pegar_pos())
                if vizinho not in set_aberto_hash:
                    contagem += 1
                    set_aberto.put((numero_f[vizinho], contagem, vizinho))
                    set_aberto_hash.add(vizinho)
                    vizinho.tornar_aberto()

        desenhar()

        if atual != começo:
            atual.tornar_fechado()

    return False

def fazer_grid(linhas, largura):
    grid = []
    espaço = largura // linhas
    for c in range(linhas):
        grid.append([])
        for i in range(linhas):
            lugar = Lugar(c, i, espaço, linhas)
            grid[c].append(lugar)

    return grid

def desenhar_grid(janela, linhas, largura):
    espaço = largura // linhas
    for c in range(linhas):
        pygame.draw.line(janela, CINZA, (0, c * espaço), (largura, c * espaço))
        for i in range(linhas):
            pygame.draw.line(janela, CINZA, (i * espaço, 0),(i * espaço, largura))

def desenhar(janela, grid, linhas, largura):
    janela.fill(BRANCO)

    for linha in grid:
        for lugar in linha:
            lugar.desenhar(janela)

    desenhar_grid(janela, linhas, largura)
    pygame.display.update()

def pegar_pos_clicada(pos, linhas, largura):
    espaço = largura // linhas
    y, x = pos

    linha = y // espaço
    coluna = x // espaço

    return linha, coluna

def main(janela, largura):
    LINHAS = 50
    grid = fazer_grid(LINHAS, largura)

    começo = None
    fim = None

    run = True

    while run:
        desenhar(janela, grid, LINHAS, largura)
        for eventos in pygame.event.get():
            if eventos.type == pygame.QUIT:
                run = False


            if pygame.mouse.get_pressed()[0]: #BOTAO ESQUERDO
                pos = pygame.mouse.get_pos()
                linha, coluna = pegar_pos_clicada(pos, LINHAS, largura)
                lugar = grid[linha][coluna]
                if not começo and lugar != fim:
                    começo = lugar
                    começo.tornar_começo()

                elif not fim and lugar != começo:
                    fim = lugar
                    fim.tornar_fim()

                elif lugar != fim and lugar != começo:
                    lugar.tornar_barreira()

            elif pygame.mouse.get_pressed()[2]: #BOTAO DIREITO
                pos = pygame.mouse.get_pos()
                linha, coluna = pegar_pos_clicada(pos, LINHAS, largura)
                lugar = grid[linha][coluna]
                lugar.reset()
                if lugar == começo:
                    começo = None
                elif lugar == fim:
                    fim = None

            if eventos.type == pygame.KEYDOWN:
                if eventos.key == pygame.K_SPACE and começo and fim:
                    for linha in grid:
                        for lugar in linha:
                            lugar.atualizar_vizinho(grid)

                    algoritmo(lambda: desenhar(janela, grid, LINHAS, largura), grid, começo, fim)

                if eventos.key == pygame.K_c:
                    começo = None
                    fim = None
                    grid = fazer_grid(LINHAS, largura)


    pygame.quit()

main(JANELA, LARGURA)