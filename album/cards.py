from album.database import get_unlocked_cards

POSICOES_CARTAS = {
    'brasil':     (11,  11),
    'espanha':   (273,  11),
    'argentina': (534,  11),
    'franca':     (11, 260),
    'japao':     (273, 260),
    'inglaterra':(534, 260),
}

def desenhar_album(tela, carta_bloqueada, posicoes = POSICOES_CARTAS):
    cartas_j1 = get_unlocked_cards('jogador1')
    cartas_j2 = get_unlocked_cards('jogador2')
    desbloqueadas = cartas_j1 | cartas_j2  # union dos dois jogadores

    for pais, (x, y) in posicoes.items():
        if pais not in desbloqueadas:
            tela.blit(carta_bloqueada, (x, y))