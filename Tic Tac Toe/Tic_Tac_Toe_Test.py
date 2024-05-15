import sys
import pygame
import numpy as np



# Initialize Pygame
pygame.init()

# Colors
white = (255, 255, 255)
grey = (180, 180, 180)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

# Size
width = 300
height = 300
line_width = 5
board_rows = 3
board_cols = 3
square_size = width // board_cols
circle_radius = square_size // 3
circle_width = 15
cross_width = 25

# Game screen setup
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(black)

# Board initialization (3x3 board)
board = np.zeros((board_rows, board_cols))

# Function to draw the grid lines
def draw_lines(color=white):
    for i in range(1, board_rows):
        # Draw horizontal lines
        pygame.draw.line(screen, color, (0, square_size * i), (board_cols * square_size, square_size * i), line_width)
        # Draw vertical lines
        pygame.draw.line(screen, color, (square_size * i, 0), (square_size * i, board_rows * square_size), line_width)

# Function to draw the figures (circles and crosses)
def draw_figure(color=white):
    for row in range(board_rows):
        for col in range(board_cols):
            if board[row][col] == 1:
                pygame.draw.circle(
                    screen,       # Surface to draw on
                    color,        # Color of the circle
                    (int(col * square_size + square_size // 2), int(row * square_size + square_size // 2)),  # Center of the circle
                    circle_radius, # Radius of the circle
                    circle_width  # Width of the circle's border (0 for filled circle)
                )
            elif board[row][col] == 2:
                pygame.draw.line(
                    screen,
                    color,
                    (col * square_size + square_size // 4, row * square_size + square_size // 4), # Start
                    (col * square_size + 3 * square_size // 4, row * square_size + 3 * square_size // 4), # End
                    cross_width
                )
                pygame.draw.line(
                    screen,
                    color,
                    (col * square_size + square_size // 4, row * square_size + 3 * square_size // 4), # Start
                    (col * square_size + 3 * square_size // 4, row * square_size + square_size // 4), # End
                    cross_width
                )

# Function to mark a square with the player's move
def mark_square(row, col, player):
    board[row][col] = player

# Function to check if a square is available
def avail_square(row, col):
    return board[row][col] == 0

# Function to check if the board is full
def is_full_board():
    for row in range(board_rows):
        for col in range(board_cols):
            if board[row][col] == 0:
                return False
    return True

# Function to check if a player has won
def check_win(player):
    # Vertical win check
    for col in range(board_cols):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    # Horizontal win check
    for row in range(board_rows):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    # Diagonal win check
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False

# Minimax algorithm for AI to find the best move
def minimax(minimax_board, depth, is_maximizing):
    if check_win(2): 
        return float('inf')
    elif check_win(1):
        return float('-inf')
    elif is_full_board():
        return 0
    
    if is_maximizing:
        best_score = -1000
        for row in range(board_rows):
            for col in range(board_cols):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for row in range(board_rows):
            for col in range(board_cols):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

# Function to find the best move for the AI
def best_move():
    best_score = -1000
    move = (-1, -1)
    for row in range(board_rows):
        for col in range(board_cols):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
                    
    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    
    return False

# Function to restart the game
def restart_game():
    screen.fill(black)
    draw_lines()
    for row in range(board_rows):
        for col in range(board_cols):
            board[row][col] = 0

# Draw the initial grid lines
draw_lines()
player = 1
gameover = False
obj=class1()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and not gameover:
            mouseX = event.pos[0] // square_size
            mouseY = event.pos[1] // square_size
            
            if avail_square(mouseY, mouseX):
                mark_square(mouseY, mouseX, player)
                if check_win(player):
                    gameover = True
                player = player % 2 + 1
                
                if not gameover:
                    if best_move():
                        if check_win(2):
                            gameover = True
                        player = player % 2 + 1
                        
                if not gameover:
                    if is_full_board():
                        gameover = True
                        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                gameover = False
                player = 1

    if not gameover:
        draw_figure()
    else:
        if check_win(1):
            draw_figure(green)
            draw_lines(green)
        elif check_win(2):
            draw_figure(red)
            draw_lines(red)
        else:
            draw_figure(grey)
            draw_lines(grey)
    pygame.display.update()

