import pygame


class Personagem(pygame.sprite.Sprite):
    """Sprite animado extraído de um sprite sheet.

    Parâmetros
    ----------
    sprite_sheet : pygame.Surface
        Surface já carregada com convert_alpha().
    inicio : int
        Índice do primeiro frame (coluna) no sprite sheet.
    fim : int
        Índice exclusivo do último frame (coluna) no sprite sheet.
    velocidade : float
        Incremento do índice de animação por frame (ex: 0.05).
    y_linha : int
        Posição Y do recorte no sprite sheet (linha da sprite).
    tela_x : int
        Posição X central inicial na tela.
    tela_y : int
        Posição Y central inicial na tela.
    largura_frame : int
        Largura de cada frame no sprite sheet (em pixels, antes do scale).
    altura_frame : int
        Altura de cada frame no sprite sheet (em pixels, antes do scale).
    scale : float
        Fator de escala aplicado ao frame após o recorte (padrão: 2).
    """

    def __init__(
        self,
        sprite_sheet,
        inicio,
        fim,
        velocidade,
        y_linha,
        tela_x,
        tela_y,
        largura_frame,
        altura_frame,
        scale=2,
    ):
        pygame.sprite.Sprite.__init__(self)

        self.velocidade = velocidade
        self.animando = True
        self.imagens = []
        self.largura_frame = largura_frame
        self.altura_frame = altura_frame

        for i in range(inicio, fim):
            img = sprite_sheet.subsurface(
                (i * largura_frame, y_linha), (largura_frame, altura_frame)
            )
            img = pygame.transform.scale(
                img, (int(largura_frame * scale), int(altura_frame * scale))
            )
            self.imagens.append(img)

        self.index_lista = 0
        self.image = self.imagens[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = (tela_x, tela_y)

    def update(self):
        """Avança o frame de animação. Chamado automaticamente pelo Group."""
        if not self.animando:
            return
        self.index_lista += self.velocidade
        if self.index_lista >= len(self.imagens):
            self.index_lista = 0
        self.image = self.imagens[int(self.index_lista)]


# ---------------------------------------------------------------------------
# Posições iniciais fixas da bola (usadas também no reset do game.py)
# ---------------------------------------------------------------------------
X_BOLA_INICIAL = 500
Y_BOLA_INICIAL = 530


def criar_personagens(sprite_sheet, LARGURA, ALTURA):
    """Instancia e retorna todos os personagens do jogo.

    goleiro : Personagem
    bola : Personagem
    jogadores : list[Personagem]
        Lista ordenada: [brasil, espanha, argentina, franca, japao, inglaterra]
    todas_as_sprites : pygame.sprite.Group
        Group já com jogador_ativo (brasil), bola e goleiro adicionados.
    jogador_ativo : Personagem
        Referência ao jogador inicial (brasil).
    """

    goleiro = Personagem(
        sprite_sheet,
        inicio=0, fim=3,
        velocidade=0.03,
        y_linha=570,
        tela_x=400, tela_y=ALTURA - 340,
        largura_frame=115, altura_frame=150,
        scale=1.3,
    )

    bola = Personagem(
        sprite_sheet,
        inicio=3, fim=4,
        velocidade=0.1,
        y_linha=580,
        tela_x=X_BOLA_INICIAL, tela_y=Y_BOLA_INICIAL,
        largura_frame=130, altura_frame=100,
    )

    jogador_brasil = Personagem(
        sprite_sheet,
        inicio=0, fim=4,
        velocidade=0.05,
        y_linha=0,
        tela_x=LARGURA // 2 - 110, tela_y=ALTURA - 150,
        largura_frame=115, altura_frame=200,
    )
    jogador_espanha = Personagem(
        sprite_sheet,
        inicio=4, fim=8,
        velocidade=0.05,
        y_linha=0,
        tela_x=LARGURA // 2 - 110, tela_y=ALTURA - 150,
        largura_frame=115, altura_frame=200,
    )
    jogador_argentina = Personagem(
        sprite_sheet,
        inicio=0, fim=4,
        velocidade=0.05,
        y_linha=188,
        tela_x=LARGURA // 2 - 110, tela_y=ALTURA - 150,
        largura_frame=115, altura_frame=200,
    )
    jogador_franca = Personagem(
        sprite_sheet,
        inicio=4, fim=8,
        velocidade=0.05,
        y_linha=188,
        tela_x=LARGURA // 2 - 110, tela_y=ALTURA - 150,
        largura_frame=115, altura_frame=200,
    )
    jogador_japao = Personagem(
        sprite_sheet,
        inicio=0, fim=4,
        velocidade=0.05,
        y_linha=370,
        tela_x=LARGURA // 2 - 110, tela_y=ALTURA - 150,
        largura_frame=115, altura_frame=200,
    )
    jogador_inglaterra = Personagem(
        sprite_sheet,
        inicio=4, fim=8,
        velocidade=0.05,
        y_linha=370,
        tela_x=LARGURA // 2 - 110, tela_y=ALTURA - 150,
        largura_frame=115, altura_frame=200,
    )

    jogadores = [
        jogador_brasil,
        jogador_espanha,
        jogador_argentina,
        jogador_franca,
        jogador_japao,
        jogador_inglaterra,
    ]

    jogador_ativo = jogadores[0]

    todas_as_sprites = pygame.sprite.Group()
    todas_as_sprites.add(jogador_ativo)
    todas_as_sprites.add(bola)
    todas_as_sprites.add(goleiro)

    return goleiro, bola, jogadores, todas_as_sprites, jogador_ativo