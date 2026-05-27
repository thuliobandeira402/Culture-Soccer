import random
import json
import urllib.request
import os

# ============================================================
#  CARREGA O BANCO DE PERGUNTAS DO ARQUIVO perguntas.json
# ============================================================

diretorio_atual = os.path.dirname(__file__)
caminho_json = os.path.join(diretorio_atual, "perguntas.json")

with open(caminho_json, "r", encoding="utf-8") as arquivo:
    BANCO_PERGUNTAS = json.load(arquivo)

# Lista que guarda quais perguntas já foram feitas (evita repetição)
perguntas_usadas = []


# -------------------------------------------------------
# Pega uma pergunta aleatória do banco, sem repetir
# -------------------------------------------------------
def pegar_pergunta(pais, nivel):
    lista = BANCO_PERGUNTAS[pais][nivel]

    # Monta uma lista só com as perguntas que ainda não foram usadas
    disponiveis = []
    for pergunta in lista:
        if pergunta not in perguntas_usadas:
            disponiveis.append(pergunta)

    # Se todas já foram usadas, reseta e começa de novo
    if len(disponiveis) == 0:
        pegar_pergunta_ia(pais, nivel)
        perguntas_usadas.clear()
        disponiveis = lista

    # Escolhe uma pergunta aleatória e marca como usada
    escolhida = random.choice(disponiveis)
    perguntas_usadas.append(escolhida)
    return escolhida


# -------------------------------------------------------
# Verifica se o jogador acertou
# -------------------------------------------------------
def verificar_resposta(pergunta, indice_escolhido):
    if indice_escolhido == pergunta["resposta"]:
        return True
    else:
        return False


# -------------------------------------------------------
# Gera uma pergunta nova via IA (Claude API)
# Só é chamada quando o banco local acabar
# -------------------------------------------------------
def pegar_pergunta_ia(pais, nivel):
    prompt = (
        "Gere 1 pergunta de quiz de nível " + nivel + " sobre a CULTURA do país: " + pais + ".\n"
        "Responda SOMENTE com JSON válido, sem texto extra.\n"
        "Formato:\n"
        '{"pergunta": "Texto?", "opcoes": ["A", "B", "C", "D"], "resposta": 0}\n'
        "Regras: exatamente 4 opcoes, resposta é o índice correto (0 a 3), em português."
    )

    corpo = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 500,
        "messages": [{"role": "user", "content": prompt}]
    }).encode("utf-8")

    requisicao = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=corpo,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        resposta = urllib.request.urlopen(requisicao, timeout=10)
        dados = json.loads(resposta.read().decode("utf-8"))
        texto = dados["content"][0]["text"].strip()
        pergunta = json.loads(texto)
        return pergunta
    except Exception as erro:
        print("Erro ao chamar a IA:", erro)
        return None


# -------------------------------------------------------
# Desenha a pergunta e as opções na tela do pygame
# -------------------------------------------------------
def desenhar_pergunta(tela, pergunta, fonte_grande, fonte_pequena, largura, altura):
    import pygame

    # Fundo escuro semitransparente atrás do texto
    fundo = pygame.Surface((largura - 40, 280))
    fundo.set_alpha(200)
    fundo.fill((10, 10, 50))
    tela.blit(fundo, (20, altura // 4))

    # Escreve o texto da pergunta (quebra linha se for longo)
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

    # Escreve as 4 opções
    letras = ["A", "B", "C", "D"]
    for i in range(4):
        texto_opcao = "[" + letras[i] + "] " + pergunta["opcoes"][i]
        superficie = fonte_pequena.render(texto_opcao, True, (255, 220, 50))
        tela.blit(superficie, (largura // 2 - superficie.get_width() // 2, y))
        y = y + fonte_pequena.get_height() + 6


def tela_chute(tela, fonte_grande, fonte_pequena, largura, altura, texto, lista_opcoes):
    import pygame

    # Fundo escuro semitransparente atrás do texto
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
    return sound.play()

