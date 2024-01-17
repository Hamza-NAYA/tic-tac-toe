import pygame
import sys
import time
import ia as ia

pygame.init()

size = width, height = 1000, 800

colors1 = "#416165"
colors2 = "#FFE66D"
colors3 = "#F7FFF7"

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tic-Tac-Toe")

mediumFont = pygame.font.Font("Cinzel-VariableFont_wght.ttf", 28)
largeFont = pygame.font.Font("Cinzel-VariableFont_wght.ttf", 40)
moveFont = pygame.font.Font("Cinzel-VariableFont_wght.ttf", 60)

board = ia.initial_start()
user = None
ai_turn = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill(colors1)

    if user is None:
        title = largeFont.render("Jouer à Tic-Tac-Toe", True, colors3)
        titleRect = title.get_rect()
        titleRect.center = ((width/2), 50)
        screen.blit(title, titleRect)

        playXButton = pygame.Rect((width/8), (height/2), width/4, 50)
        playX = mediumFont.render("Jouer X", True, colors3)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, colors2, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width/8), (height/2), width/4, 50)
        playO = mediumFont.render("Jouer O", True, colors3)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, colors2, playOButton)
        screen.blit(playO, playORect)

        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ia.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ia.O
    else:
        tile_size = 150
        tile_origin = (width / 2 -(1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, colors2, rect, 3)

                if board[i][j] != ia.EMPTY:
                    move = moveFont.render(board[i][j], True, colors2)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)
        game_over = ia.terminal(board)
        player = ia.player(board)

        if game_over:
            winner = ia.winner(board)
            if winner is None:
                title = f"Egalité !"
            else:
                title = f"Perdu :{winner} a gagné"
        elif user == player:
            title = f"Jouer comme {user}"
        else:
            title = f"l'IA reflechi à son prochain coup"
        title = largeFont.render(title, True, colors3)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ia.minimax(board)
                board = ia.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ia.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ia.result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Rejouer", True, colors3)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, colors2, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ia.initial_start()
                    ai_turn = False

    pygame.display.flip()