import random
import json
import urllib.request
import os



diretorio_atual = os.path.dirname(__file__)
caminho_json = os.path.join(diretorio_atual, "perguntas.json")

with open(caminho_json, "r", encoding="utf-8") as arquivo:
    BANCO_PERGUNTAS = json.load(arquivo)


perguntas_usadas = []





def pegar_pergunta(pais, nivel):
    """Pega uma pergunta aleatória do banco, sem repetir"""
    lista = BANCO_PERGUNTAS[pais][nivel]

   
    disponiveis = []
    for pergunta in lista:
        if pergunta not in perguntas_usadas:
            disponiveis.append(pergunta)

    
    if len(disponiveis) == 0:
        perguntas_usadas.clear()
        disponiveis = lista

    
    escolhida = random.choice(disponiveis)
    perguntas_usadas.append(escolhida)
    return escolhida



def verificar_resposta(pergunta, indice_escolhido):

    """Verificar se o jogador acertou"""
    if indice_escolhido == pergunta["resposta"]:
        return True
    else:
        return False






def desenhar_pergunta(tela, pergunta, fonte_grande, fonte_pequena, largura, altura):
    """Desenha a pergunta e as opções na tela do pygame"""
    import pygame

    # Fundo escuro semitransparente atrás do texto
    fundo = pygame.Surface((largura - 40, 280))
    fundo.set_alpha(200)
    fundo.fill((10, 10, 50))
    tela.blit(fundo, (20, altura // 4))

    
    palavras = pergunta["pergunta"].split()
    linha = ""
    y = altura // 4 + 10

    for palavra in palavras:
        teste = linha + " " + palavra
        if fonte_grande.size(teste)[0] < largura - 60:
            linha = teste
        else:
            superficie = fonte_grande.render(linha, True, (255, 255, 255))
            tela.blit(superficie, (largura // 2 - superficie.get_width() // 2, y))
            y = y + fonte_grande.get_height() + 4
            linha = palavra
    # Última linha
    superficie = fonte_grande.render(linha, True, (255, 255, 255))
    tela.blit(superficie, (largura // 2 - superficie.get_width() // 2, y))
    y = y + fonte_grande.get_height() + 15

    
    letras = ["A", "B", "C", "D"]
    for i in range(4):
        texto_opcao = "[" + letras[i] + "] " + pergunta["opcoes"][i]
        superficie = fonte_pequena.render(texto_opcao, True, (255, 220, 50))
        tela.blit(superficie, (largura // 2 - superficie.get_width() // 2, y))
        y = y + fonte_pequena.get_height() + 6


def tela_chute(tela, fonte_grande, fonte_pequena, largura, altura, texto, lista_opcoes):
    """tela de chute"""
    import pygame

   
    fundo = pygame.Surface((largura - 40, 280))
    fundo.set_alpha(200)
    fundo.fill((10, 10, 50))
    tela.blit(fundo, (20, altura // 4))

    
    palavras = texto
    linha = ""
    y = altura // 4 + 10

    for palavra in palavras:
        teste = linha + " " + palavra
        if fonte_grande.size(teste)[0] < largura - 60:
            linha = teste
        else:
            superficie = fonte_grande.render(linha, True, (255, 255, 255))
            tela.blit(superficie, (largura // 2 - superficie.get_width() // 2, y))
            y = y + fonte_grande.get_height() + 4
            linha = palavra
    
    superficie = fonte_grande.render(linha, True, (255, 255, 255))
    tela.blit(superficie, (largura // 2 - superficie.get_width() // 2, y))
    y = y + fonte_grande.get_height() + 15

    
    letras = lista_opcoes
    for i in range(3):
        texto_opcao = "[" + letras[i] + "]"
        superficie = fonte_pequena.render(texto_opcao, True, (255, 220, 50))
        tela.blit(superficie, (largura // 2 - superficie.get_width() // 2, y))
        y = y + fonte_pequena.get_height() + 6

def som_exec(sound):
    """Executar algum efeito sonoro"""
    return sound.play()

