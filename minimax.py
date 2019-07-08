# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 19:20:01 2019

@author: filipe.teixeira
"""

from math import inf as infinity
from random import choice
import time
from os import system

OP_JOGADOR = ['X', 'O']
OP_PERGUNTA = ['S', 'N']
PESSOA = -1
IA = +1
TABULEIRO = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    ]


def iniciar_tabuleiro():
    """
    Função iniciar o tabuleiro
    :param estado: estado atual do tabuleiro
    :return: tabuleiro inicializado (zerado)
    """
    for coord_x, linha in enumerate(TABULEIRO):
        for coord_y, celula in enumerate(linha):
            if celula < 9:
                TABULEIRO[coord_x][coord_y] = 0


def avaliar(estado):
    """
    Função para avaliar vencedor
    :param estado: estado atual do tabuleiro
    :return: +1 se computador venceu; -1 se pessoa venceu; 0 se empate
    """
    if vencedor(estado, IA):
        pontuacao = +1
    elif vencedor(estado, PESSOA):
        pontuacao = -1
    else:
        pontuacao = 0

    return pontuacao


def vencedor(estado, jogador):
    """
    Verifica se algum jogador venceu. Possibilidades:
    * Três linhas     [X X X] or [O O O]
    * Três colunas    [X X X] or [O O O]
    * Duas diagonais  [X X X] or [O O O]
    :param estado: estado atual do tabuleiro
    :param jogador: pessoa ou IA
    :return: True se jogador venceu
    """
    estados_vencedores = [
        [estado[0][0], estado[0][1], estado[0][2]],
        [estado[1][0], estado[1][1], estado[1][2]],
        [estado[2][0], estado[2][1], estado[2][2]],
        [estado[0][0], estado[1][0], estado[2][0]],
        [estado[0][1], estado[1][1], estado[2][1]],
        [estado[0][2], estado[1][2], estado[2][2]],
        [estado[0][0], estado[1][1], estado[2][2]],
        [estado[2][0], estado[1][1], estado[0][2]],
    ]
    return [jogador, jogador, jogador] in estados_vencedores


def fim_de_jogo(estado):
    """
    Função verifica se houve vencedor
    :param estado: estado atual do tabuleiro
    :return: Verdadeiro se houve vencedor
    """
    return vencedor(estado, PESSOA) or vencedor(estado, IA)


def casas_vazias(estado):
    """
    Retornar casas vazias
    :param estado: estado atual do tabuleiro
    :return: lista de casas vazias
    """
    casas = []

    for coord_x, linha in enumerate(estado):
        for coord_y, celula in enumerate(linha):
            if celula == 0:
                casas.append([coord_x, coord_y])

    return casas


def validar_movimento(coord_x, coord_y):
    """
    O movimento é válido se a casa estiver vazia
    :param x: coordenada X
    :param y: coordenada Y
    :return: True se casa estiver vazia
    """
    return [coord_x, coord_y] in casas_vazias(TABULEIRO)


def marcar_movimento(coord_x, coord_y, jogador):
    """
    Se coordenadas do movimento for válido, marcar movimento no tabuleiro
    :param coord_x: coordenada X
    :param coord_y: coordenada Y
    :param jogador: jogador atual
    """
    if validar_movimento(coord_x, coord_y):
        TABULEIRO[coord_x][coord_y] = jogador
        movimento_marcado = True
    else:
        movimento_marcado = False

    return movimento_marcado


def minimax(estado, profundidade, jogador):
    """
    Função IA que escolhe o melhor movimento
    :param estado: estado atual do tabuleiro
    :param profundidade: índice do nó da árvore (0 <= profundidade <= 9),
    :param jogador: jogador atual
    :return: uma lista com [a melhor linha, melhor coluna, melhor pontuação]
    """
    if jogador == IA:
        melhor = [-1, -1, -infinity]
    else:
        melhor = [-1, -1, +infinity]

    if profundidade == 0 or fim_de_jogo(estado):
        pontuacao = avaliar(estado)
        return [-1, -1, pontuacao]

    for celula in casas_vazias(estado):
        coord_x, coord_y = celula[0], celula[1]
        estado[coord_x][coord_y] = jogador
        pontuacao = minimax(estado, profundidade - 1, -jogador)
        estado[coord_x][coord_y] = 0
        pontuacao[0], pontuacao[1] = coord_x, coord_y

        if jogador == IA:
            if pontuacao[2] > melhor[2]:
                melhor = pontuacao  # valor MAX
        else:
            if pontuacao[2] < melhor[2]:
                melhor = pontuacao  # valor MIN

    return melhor


def exibir_tabuleiro(estado, e_ia, e_pessoa):
    """
    Exibir o tabuleiro
    :param estado: estado atual do tabuleiro
    """
    caracteres = {
        -1: e_pessoa,
        +1: e_ia,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for linha in estado:
        for celula in linha:
            simbolo = caracteres[celula]
            print(f'| {simbolo} |', end='')
        print('\n' + str_line)


def jogada_ia(e_ia, e_pessoa):
    """
    Se profundidade < 9 executa função minimax,
    senão, escolhe uma jogada aleatória.
    :param e_ia: escolha da ia (X or O)
    :param e_pessoa: escolha da pessoa (X or O)
    """
    profundidade = len(casas_vazias(TABULEIRO))
    if profundidade == 0 or fim_de_jogo(TABULEIRO):
        return

    system('cls')
    print(f'A vez do computador [{e_ia}]')
    exibir_tabuleiro(TABULEIRO, e_ia, e_pessoa)

    if profundidade == 9:
        coord_x = choice([0, 1, 2])
        coord_y = choice([0, 1, 2])
    else:
        casa = minimax(TABULEIRO, profundidade, IA)
        coord_x, coord_y = casa[0], casa[1]

    marcar_movimento(coord_x, coord_y, IA)
    time.sleep(1)


def jogada_pessoa(e_ia, e_pessoa):
    """
    Pessoa joga com movimento válido.
    :param e_ia: escolha da ia (X or O)
    :param e_pessoa: escolha da pessoa (X or O)
    """
    profundidade = len(casas_vazias(TABULEIRO))
    if profundidade == 0 or fim_de_jogo(TABULEIRO):
        return

    # Movimentos válidos
    casa = -1
    movimentos = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    system('cls')
    print(f'A vez da pessoa [{e_pessoa}]')
    exibir_tabuleiro(TABULEIRO, e_ia, e_pessoa)

    while casa < 1 or casa > 9:
        casa = int(input('Informe a casa (1..9): '))
        coord = movimentos[casa]
        movimento = marcar_movimento(coord[0], coord[1], PESSOA)

        if not movimento:
            print('Jogada não permitida.')
            casa = -1


def main():
    """
    Função principal
    :return: retorna resultado do jogo
    """
    system('cls')
    e_pessoa = ''  # Escolha da pessoa (X ou O)
    e_ia = ''      # Escolha da IA (X or O)
    primeiro = ''  # Se pessoa é a primeira a jogar
    resultado = '' # Indica resultado do jogo (P: pessoa venceu / C: IA venceu / E: empate)
    qtd_casas_vazias = 9

    iniciar_tabuleiro()

    while e_pessoa not in OP_JOGADOR:
        print('')
        e_pessoa = input('Escolha X or O: ').upper()
        if e_pessoa not in OP_JOGADOR:
            print('Escolha não permitida.')

    # Escolha da IA
    if e_pessoa == 'X':
        e_ia = 'O'
    else:
        e_ia = 'X'

    # Definição de quem inicia o jogo (Pessoa ou IA)
    system('cls')
    while primeiro not in OP_PERGUNTA:
        primeiro = input('Iniciar jogando?[s/n]: ').upper()
        if primeiro not in OP_PERGUNTA:
            print('Opção inválida.')

    # Loop principal do jogo
    while (qtd_casas_vazias > 0 and not fim_de_jogo(TABULEIRO)):
        if primeiro == 'N':
            jogada_ia(e_ia, e_pessoa)
            primeiro = ''

        jogada_pessoa(e_ia, e_pessoa)
        jogada_ia(e_ia, e_pessoa)
        qtd_casas_vazias = len(casas_vazias(TABULEIRO))

    # Mensagem de fim de jogo
    if vencedor(TABULEIRO, PESSOA):
        system('cls')
        print(f'A vez da pessoa [{e_pessoa}]')
        exibir_tabuleiro(TABULEIRO, e_ia, e_pessoa)
        print('VOCÊ VENCEU!')
        resultado = 'P'
    elif vencedor(TABULEIRO, IA):
        system('cls')
        print(f'A vez do computador [{e_ia}]')
        exibir_tabuleiro(TABULEIRO, e_ia, e_pessoa)
        print('VOCÊ PERDEU!')
        resultado = 'C'
    else:
        system('cls')
        exibir_tabuleiro(TABULEIRO, e_ia, e_pessoa)
        print('EMPATE!')
        resultado = 'E'

    return resultado


if __name__ == '__main__':
    CONTINUAR = True
    CONT_PESSOA = 0
    CONT_IA = 0
    CONT_EMPATE = 0

    while CONTINUAR:
        RESULT = main()
        if RESULT == 'P':
            CONT_PESSOA += 1
        elif RESULT == 'C':
            CONT_IA += 1
        else:
            CONT_EMPATE += 1

        system('cls')
        PERGUNTA_CONTINUAR = ''
        while PERGUNTA_CONTINUAR not in OP_PERGUNTA:
            PERGUNTA_CONTINUAR = input('Continuar jogando?[s/n]: ').upper()
            if PERGUNTA_CONTINUAR not in OP_PERGUNTA:
                print('Opção inválida.')

            if PERGUNTA_CONTINUAR == 'N':
                CONTINUAR = False
                print()
                print('RESULTADO:')
                print('---------------')
                print(f'Vitórias: [{CONT_PESSOA}]')
                print(f'Derrotas: [{CONT_IA}]')
                print(f'Empates : [{CONT_EMPATE}]')
                print('---------------')
                if CONT_PESSOA > CONT_IA:
                    print('VOCÊ VENCEU O CONFRONTO GERAL!')
                elif CONT_IA > CONT_PESSOA:
                    print('VOCÊ PERDEU O CONFRONTO GERAL!')
                else:
                    print('HOUVE EMPATE NO CONFRONTO GERAL!')
            else:
                CONTINUAR = True
                