import pygame
from pygame.locals import *
from sys import exit
from utils.utils import *
from album.database import *
from album.cards import *
from core.personagens import criar_personagens, X_BOLA_INICIAL, Y_BOLA_INICIAL
import os

criar_tabela()

LARGURA = 800
ALTURA = 600

pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Culture Soccer')


fonte = pygame.font.SysFont('arial', 40, True, True)
fonte_pequena = pygame.font.SysFont('arial', 28, True, False)

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'images')
diretorio_audio = os.path.join(diretorio_principal, 'audio')
diretorio_sprites = os.path.join(diretorio_imagens, 'sprites')
sprite_sheet = pygame.image.load(os.path.join(diretorio_sprites, 'itens.png')).convert_alpha()
diretorio_menus = os.path.join(diretorio_imagens, 'menus')

musica_fundo = os.path.join(diretorio_audio, 'BoxCat Games - Tricks.mp3')
click_sound = os.path.join(diretorio_audio, 'smw_kick.wav')
som_gol = os.path.join(diretorio_audio, 'gol.mp3')
som_perdeu_gol = os.path.join(diretorio_audio, 'perdeu-gol.mp3')
gol = pygame.mixer.Sound(som_gol)
perdeu_gol = pygame.mixer.Sound(som_perdeu_gol)
clique = pygame.mixer.Sound(click_sound)
pygame.mixer.music.load(musica_fundo)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.15)
# ---------imagens dos menus------------
imagem_penalti = pygame.image.load(os.path.join(diretorio_menus, 'penalti.jpg'))
imagem_penalti = pygame.transform.scale(imagem_penalti, (LARGURA, ALTURA))
imagem_inicial = pygame.image.load(os.path.join(diretorio_menus, 'tela_inicial.png'))
imagem_inicial = pygame.transform.scale(imagem_inicial, (LARGURA, ALTURA))
imagem_escolha_pais = pygame.image.load(os.path.join(diretorio_menus, 'escolha-pais.png'))
imagem_escolha_pais = pygame.transform.scale(imagem_escolha_pais, (LARGURA, ALTURA))
imagem_dificuldade = pygame.image.load(os.path.join(diretorio_menus, 'tela_dificuldade.png'))
imagem_dificuldade = pygame.transform.scale(imagem_dificuldade, (LARGURA, ALTURA))
imagem_album = pygame.image.load(os.path.join(diretorio_menus, 'album.png'))
imagem_album = pygame.transform.scale(imagem_album, (LARGURA, ALTURA))
clock = pygame.time.Clock()
carta_bloqueada = pygame.image.load(os.path.join(diretorio_menus, 'carta_bloqueada.png')).convert_alpha()

#------------------------------------- PERSONAGENS -----------------------------
x_bola = X_BOLA_INICIAL
y_bola = Y_BOLA_INICIAL
x_bola_destino = X_BOLA_INICIAL
y_bola_destino = 200
bola_movendo = False
goleiro_pulando = False
x_goleiro = 400
x_goleiro_destino = 300

goleiro, bola, jogadores, todas_as_sprites, jogador_ativo = criar_personagens(
    sprite_sheet, LARGURA, ALTURA
)

# ---------- controle de telas ----------
tela_inicial = True
tela_paises = False
tela_dificuldade = False
tela_penalti = False
tela_album = False
# ---------- controle do jogo ----------
pais_selecionado = None
dificuldade_selecionada = None
pontos_jogador_1 = 0
pontos_jogador_2 = 0
round_atual = 0
quantidade_de_rounds = 6
jogo = False
chutando = False
estado_jogo = 'PERGUNTA'
 
# turno_atual: 1 = vez do jogador 1, 2 = vez do jogador 2
turno_atual = 1
 
# aguardando_resposta: True = pergunta está na tela esperando o jogador apertar A/B/C/D
aguardando_resposta = False
pergunta_atual = None

# logica do penalti: esperar o usuario chutar, goleiro escolher canto, verificar
mensagem_penalti = ''
tempo_penalti = 0
DURACAO_PENALTI = 120

texto_chute = 'Escolha em qual canto irá chutar'
texto_defesa = 'Escolha para qual lado irá pular'
opcoes_chute = ["A (esquerda)", "S (meio)", "D (direita)"]
opcoes_defesa = ['H (esquerda)', 'j (meio)', 'K (direita)']
mensagem_perdeu = 'Você perdeu o penalti!!'
mensagem_acertou = "GOOOOL!!"
escolha_chute = False
escolha_defesa = False
resposta_chute = -1
resposta_defesa = -1
acertou_penalti = False




# mostrar_resultado: True = mostra "acertou/errou" por um tempo antes de passar o turno
mostrar_resultado = False
mensagem_resultado = ''
tempo_resultado = 0          # conta quantos frames a mensagem fica na tela
DURACAO_RESULTADO = 120      # 120 frames = 2 segundos (a 60fps)
 
resposta_escolhida = -1

while True:
    clock.tick(60)
    tela.fill((255, 255, 255))
    if tela_inicial:
        tela.blit(imagem_inicial, (0, 0))
    elif tela_paises:
       tela.blit(imagem_escolha_pais, (0, 0)) 
    elif tela_dificuldade:
        tela.blit(imagem_dificuldade, (0, 0))
    elif tela_penalti:
        tela.blit(imagem_penalti, (0, 0))
    elif tela_album:
        tela.blit(imagem_album, (0, 0))
        desenhar_album(tela, carta_bloqueada)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            # tela inicial 
            if tela_inicial:
                if event.key == K_RETURN:
                    comecou = True
                    tela_inicial = False
                    tela_paises = True
                    som_exec(clique)
            if event.key == pygame.K_0:
                    pygame.quit()

            if tela_album:
                if event.key == K_RETURN:
                    tela_album = False
                    tela_paises = True
                    som_exec(clique)

            # tela album
            if event.key == pygame.K_TAB:
                tela_album = True
                som_exec(clique)
                tela_inicial = False
                tela_paises = False
                tela_dificuldade = False    
                tela_penalti = False
                


            # --- tela de países: 1 a 6 escolhe o país ---
            elif tela_paises and not tela_dificuldade:
                if event.key == pygame.K_1:
                    todas_as_sprites.remove(jogador_ativo)
                    jogador_ativo = jogadores[0]
                    todas_as_sprites.add(jogador_ativo)
                    pais_selecionado = 'brasil'
                    som_exec(clique)
                    tela_paises = False
                    tela_dificuldade = True
                elif event.key == pygame.K_2:
                    todas_as_sprites.remove(jogador_ativo)
                    jogador_ativo = jogadores[1]
                    todas_as_sprites.add(jogador_ativo)
                    pais_selecionado = 'espanha'
                    som_exec(clique)
                    tela_paises = False
                    tela_dificuldade = True
                elif event.key == pygame.K_3:
                    todas_as_sprites.remove(jogador_ativo)
                    jogador_ativo = jogadores[2]
                    todas_as_sprites.add(jogador_ativo)
                    pais_selecionado = 'argentina'
                    som_exec(clique)
                    tela_paises = False
                    tela_dificuldade = True
                elif event.key == pygame.K_4:
                    todas_as_sprites.remove(jogador_ativo)
                    jogador_ativo = jogadores[3]
                    todas_as_sprites.add(jogador_ativo)
                    pais_selecionado = 'franca'
                    som_exec(clique)
                    tela_paises = False
                    tela_dificuldade = True
                elif event.key == pygame.K_5:
                    todas_as_sprites.remove(jogador_ativo)
                    jogador_ativo = jogadores[4]
                    todas_as_sprites.add(jogador_ativo)
                    pais_selecionado = 'japao'
                    som_exec(clique)
                    tela_paises = False
                    tela_dificuldade = True
                elif event.key == pygame.K_6:
                    todas_as_sprites.remove(jogador_ativo)
                    jogador_ativo = jogadores[5]
                    todas_as_sprites.add(jogador_ativo)
                    pais_selecionado = 'inglaterra'
                    tela_paises = False
                    tela_dificuldade = True
                
 
            # ---- tela de dificuldade: 1=fácil, 2=médio, 3=difícil ---
            elif tela_dificuldade:
                if event.key == pygame.K_1:
                    dificuldade_selecionada = 'facil'
                    som_exec(clique)
                    tela_dificuldade = False
                    tela_penalti = True
                    jogo = True
                    pergunta_atual = pegar_pergunta(pais_selecionado, dificuldade_selecionada)
                    aguardando_resposta = True
                elif event.key == pygame.K_2:
                    dificuldade_selecionada = 'medio'
                    som_exec(clique)
                    tela_dificuldade = False
                    tela_penalti = True
                    jogo = True
                    pergunta_atual = pegar_pergunta(pais_selecionado, dificuldade_selecionada)
                    aguardando_resposta = True
                elif event.key == pygame.K_3:
                    dificuldade_selecionada = 'dificil'
                    som_exec(clique)
                    tela_dificuldade = False
                    tela_penalti = True
                    jogo = True
                    pergunta_atual = pegar_pergunta(pais_selecionado, dificuldade_selecionada)
                    aguardando_resposta = True
 
            # --- tela do pênalti: jogador responde A/B/C/D ---
            elif tela_penalti and aguardando_resposta and not mostrar_resultado:
                resposta_escolhida = -1
                if event.key == pygame.K_a:
                    resposta_escolhida = 0
                    som_exec(clique)
                elif event.key == pygame.K_b:
                    som_exec(clique)
                    resposta_escolhida = 1
                elif event.key == pygame.K_c:
                    som_exec(clique)
                    resposta_escolhida = 2
                elif event.key == pygame.K_d:
                    som_exec(clique)
                    resposta_escolhida = 3
                
            # -- tela chute ----
            if tela_penalti and estado_jogo == 'CHUTE':   
                resposta_chute = -1
                if event.key == pygame.K_a:
                    som_exec(clique)
                    resposta_chute = 0
                elif event.key == pygame.K_s:
                    som_exec(clique)
                    resposta_chute = 1
                elif event.key == pygame.K_d:
                    som_exec(clique)
                    resposta_chute = 2

                if resposta_chute != -1:
                    escolha_chute = False
                    escolha_defesa = True
                    estado_jogo = 'DEFESA'

            # --- tela defesa --
            elif tela_penalti and estado_jogo == 'DEFESA':
                resposta_defesa = -1
                if event.key == pygame.K_h:
                    som_exec(clique)
                    resposta_defesa = 0
                elif event.key == pygame.K_j:
                    som_exec(clique)
                    resposta_defesa = 1
                elif event.key == pygame.K_k:
                    som_exec(clique)
                    resposta_defesa = 2
                
                if resposta_defesa != -1:
                    goleiro.animando = False
                    if resposta_defesa == 0:       # esquerda                        
                        goleiro.index_lista = 2
                        x_goleiro_destino = 200
                    elif resposta_defesa == 1:   # meio
                        goleiro.index_lista = 0
                        x_goleiro_destino = 400
                        velocidade_goleiro = 0
                    elif resposta_defesa == 2:   # direita
                        goleiro.index_lista = 1
                        x_goleiro_destino = 500
                    goleiro.image = goleiro.imagens[int(goleiro.index_lista)]
                    escolha_defesa = False
                    if resposta_chute == resposta_defesa:
                        mensagem_penalti = 'DEFENDEU!!'
                        acertou_penalti = False
                        som_exec(perdeu_gol)
                    else:
                        mensagem_penalti = 'GOOOOL!!'
                        som_exec(gol)
                        acertou_penalti = True

                    chutando = True
                    goleiro_pulando = True
                    estado_jogo = 'ANIMACAO'
                    tempo_penalti = 0
                    bola_movendo = True
                    if resposta_chute == 0:      # esquerda
                        x_bola_destino = 200
                    elif resposta_chute == 1:    # meio
                        x_bola_destino = 400
                    elif resposta_chute == 2:    # direita
                        x_bola_destino = 550
                    y_bola_destino = 200

            
 
    # ---------- lógica do jogo  ----------
    if jogo:
        # anima os sprites
        for jogador in jogadores:
            if not chutando:
                if jogador.index_lista > 1.5:
                    jogador.index_lista = 0
                if not goleiro_pulando:     
                    goleiro.index_lista = 0
 
        todas_as_sprites.update()
        todas_as_sprites.draw(tela)
 
        # mostra de quem é o turno
        if turno_atual == 1:
            texto_turno = fonte.render('Jogador 1', True, (0, 0, 0))
        else:
            texto_turno = fonte.render('Jogador 2', True, (0, 0, 0))
        tela.blit(texto_turno, (LARGURA // 2 - 100, 0))
 
        # mostra pontuação
        texto_pontos = fonte_pequena.render(
            'J1: ' + str(pontos_jogador_1) + '   J2: ' + str(pontos_jogador_2),
            True, (255, 255, 0)
        )
        tela.blit(texto_pontos, (10, 10))
 
        # desenhar a pergunta enquanto espera resposta
        if aguardando_resposta:
            desenhar_pergunta(tela, pergunta_atual, fonte_pequena, fonte_pequena, LARGURA, ALTURA)
    
        # espera a resposta do chute
        if escolha_chute:
            tela_chute(tela, fonte_pequena, fonte_pequena, LARGURA, ALTURA, texto_chute, opcoes_chute)

        # espera a resposta da defesa
        if escolha_defesa:
            escolha_chute = False
            tela_chute(tela, fonte_pequena, fonte_pequena, LARGURA, ALTURA, texto_defesa, opcoes_defesa)

        # --- processa resposta da pergunta ---
        if resposta_escolhida != -1 and estado_jogo == 'PERGUNTA':
            aguardando_resposta = False
            mostrar_resultado = True
            tempo_resultado = 0
            if verificar_resposta(pergunta_atual, resposta_escolhida):
                mensagem_resultado = 'Parabéns, você acertou!!'
            else:
                mensagem_resultado = 'Você errou!!'
            estado_jogo = 'RESULTADO'
            resposta_escolhida = -1

        # ---- animação da bola ----
        if estado_jogo == 'ANIMACAO':
            goleiro_pulando = True
            for jogador in jogadores:
                if chutando:
                    if jogador.index_lista > 3.5:
                        jogador.index_lista = 0

            
            #--- movimento bola e goleiro
            if bola_movendo:
                velocidade_bola = 8

                if bola.rect.y > y_bola_destino:
                    bola.rect.y -= velocidade_bola
                if bola.rect.x < x_bola_destino:
                    bola.rect.x += velocidade_bola
                elif bola.rect.x > x_bola_destino:
                    bola.rect.x -= velocidade_bola

                if goleiro_pulando:
                    velocidade_goleiro = 10
                    
                    if abs(goleiro.rect.centerx - x_goleiro_destino) > velocidade_goleiro:
                        if goleiro.rect.centerx > x_goleiro_destino:
                            goleiro.rect.x -= velocidade_goleiro
                        else:
                            goleiro.rect.x += velocidade_goleiro
                    else:
                        goleiro.rect.centerx = x_goleiro_destino

                if abs(bola.rect.y - y_bola_destino) < velocidade_bola:
                    bola_movendo = False
                    goleiro_pulando = False
                    estado_jogo = 'RESULTADO_PENALTI'
                
            


        if estado_jogo == 'PERGUNTA' and chutando:
                chutando = False
                goleiro_pulando = False

        # --- resultado da resposta -----
        if estado_jogo == 'RESULTADO':          
            mensagem_resultado_formatted = fonte.render(mensagem_resultado, True, (255, 255, 0))
            tela.blit(mensagem_resultado_formatted, (LARGURA // 2 - mensagem_resultado_formatted.get_width() // 2,ALTURA // 2))

            tempo_resultado += 1

            if tempo_resultado >= DURACAO_RESULTADO:
                mostrar_resultado = False
                if mensagem_resultado == 'Parabéns, você acertou!!':
                    estado_jogo = 'CHUTE'
                    escolha_chute = True
                else:
                    # Trocar de turno
                    som_exec(perdeu_gol)
                    round_atual += 1
                    if round_atual >= quantidade_de_rounds:
                        jogo = False
                    else:
                        turno_atual = 2 if turno_atual == 1 else 1
                        estado_jogo = 'PERGUNTA'
                        aguardando_resposta = True
                        pergunta_atual = pegar_pergunta(pais_selecionado, dificuldade_selecionada)


        # ---- resultado -- chute mostrar tela
        if estado_jogo == 'RESULTADO_PENALTI':
            texto = fonte.render(mensagem_penalti, True, (255, 255, 0))
            tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2))
            tempo_penalti += 1

            if tempo_penalti >= DURACAO_PENALTI:
                # pontua gol para quem chutou
                if acertou_penalti:
                    if turno_atual == 1:
                        pontos_jogador_1 += 1
                    else:
                        pontos_jogador_2 += 1

                # proximo round e verifica fim de jogo
                round_atual += 1
                bola.rect.center = (x_bola, y_bola)  
                goleiro.rect.center = (400, ALTURA - 340)
                goleiro.animando = True
                bola_movendo = False
                if round_atual >= quantidade_de_rounds:
                    jogo = False
                else:
                    # troca o turno 
                    if turno_atual == 1:
                        turno_atual = 2
                    else:
                        turno_atual = 1
                    estado_jogo = 'PERGUNTA'
                    aguardando_resposta = True
                    pergunta_atual = pegar_pergunta(pais_selecionado, dificuldade_selecionada)

        
    # tela de fim de jogo e reset
    if not jogo and round_atual >= quantidade_de_rounds:
        tela.fill((0, 0, 0))
        if pontos_jogador_1 > pontos_jogador_2:
            unlock_card('jogador1', pais_selecionado)
            unlock_card('jogador2', pais_selecionado)
            fim = fonte.render('Jogador 1 venceu!', True, (255, 255, 0))
        elif pontos_jogador_2 > pontos_jogador_1:
            unlock_card('jogador1', pais_selecionado)
            unlock_card('jogador2', pais_selecionado)
            fim = fonte.render('Jogador 2 venceu!', True, (255, 255, 0))
        else:
            unlock_card('jogador1', pais_selecionado)
            unlock_card('jogador2', pais_selecionado)
            fim = fonte.render('EMPATE!', True, (100, 200, 255))

        pontos_texto = fonte_pequena.render(
            f'Jogador 1: {pontos_jogador_1}  x  Jogador 2: {pontos_jogador_2}',
            True, (200, 200, 200)
        )
        voltar_texto = fonte_pequena.render('Pressione R para voltar ao inicio', True, (180, 180, 180))

        tela.blit(fim, (LARGURA // 2 - fim.get_width() // 2, ALTURA // 2 - 60))
        tela.blit(pontos_texto, (LARGURA // 2 - pontos_texto.get_width() // 2, ALTURA // 2 + 10))
        tela.blit(voltar_texto, (LARGURA // 2 - voltar_texto.get_width() // 2, ALTURA // 2 + 60))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            round_atual = 0
            pontos_jogador_1 = 0
            pontos_jogador_2 = 0
            turno_atual = 1
            estado_jogo = 'PERGUNTA'
            jogo = False
            tela_inicial = True
            tela_paises = False
            tela_dificuldade = False
            tela_penalti = False
            tela_album = False
            bola.rect.center = (x_bola, y_bola)
            goleiro.rect.center = (400, ALTURA - 340)
            goleiro.animando = True
        
    pygame.display.flip()