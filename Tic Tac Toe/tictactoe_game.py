import sys
import pygame
import numpy as np

class tictactoe():
    
    def __init__(self) -> None:
        # Colors
        self.white = (255, 255, 255)
        self.grey = (180, 180, 180)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.black = (0, 0, 0)

        # Size
        self.width = 300
        self.height = 300
        self.line_width = 5
        self.board_rows = 3
        self.board_cols = 3
        self.square_size = self.width // self.board_cols
        self.circle_radius = self.square_size // 3
        self.circle_width = 15
        self.cross_width = 25
        
        # Game screen setup
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Tic Tac Toe')
        self.screen.fill(self.black)

        # Board initialization (3x3 board)
        self.board = np.zeros((self.board_rows, self.board_cols))
        

        # Draw the initial grid lines
        self.draw_lines()
        self.player = 1
        self.gameover = False
        
        # Function to draw the grid lines
    def draw_lines(self, color=None):
        if color is None:
            color = self.white
        for i in range(1, self.board_rows):
            # Draw horizontal lines
            pygame.draw.line(self.screen, color, (0, self.square_size * i), (self.board_cols * self.square_size, self.square_size * i), self.line_width)
            # Draw vertical lines
            pygame.draw.line(self.screen, color, (self.square_size * i, 0), (self.square_size * i, self.board_rows * self.square_size), self.line_width)

    # Function to draw the figures (circles and crosses)
    def draw_figure(self, color=None):
        if color is None:
            color = self.white
        for row in range(self.board_rows):
            for col in range(self.board_cols):
                if self.board[row][col] == 1:
                    pygame.draw.circle(
                        self.screen,       # Surface to draw on
                        color,        # Color of the circle
                        (int(col * self.square_size + self.square_size // 2), int(row * self.square_size + self.square_size // 2)),  # Center of the circle
                        self.circle_radius, # Radius of the circle
                        self.circle_width  # Width of the circle's border (0 for filled circle)
                    )
                elif self.board[row][col] == 2:
                    pygame.draw.line(
                        self.screen,
                        color,
                        (col * self.square_size + self.square_size // 4, row * self.square_size + self.square_size // 4), # Start
                        (col * self.square_size + 3 * self.square_size // 4, row * self.square_size + 3 * self.square_size // 4), # End
                        self.cross_width
                    )
                    pygame.draw.line(
                        self.screen,
                        color,
                        (col * self.square_size + self.square_size // 4, row * self.square_size + 3 * self.square_size // 4), # Start
                        (col * self.square_size + 3 * self.square_size // 4, row * self.square_size + self.square_size // 4), # End
                        self.cross_width
                    )
                    

     # Function to mark a square with the player's move
    def mark_square(self,row, col, player):
        self.board[row][col] = player

    # Function to check if a square is available
    def avail_square(self, row, col):
        return self.board[row][col] == 0

    # Function to check if the board is full
    def is_full_board(self):
        for row in range(self.board_rows):
            for col in range(self.board_cols):
                if self.board[row][col] == 0:
                    return False
        return True

    def check_win(self, player):
        # Vertical win check
        for col in range(self.board_cols):
            if self.board[0][col] == player and self.board[1][col] == player and self.board[2][col] == player:
                return True
        # Horizontal win check
        for row in range(self.board_rows):
            if self.board[row][0] == player and self.board[row][1] == player and self.board[row][2] == player:
                return True
        # Diagonal win check
        if self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player:
            return True
        if self.board[0][2] == player and self.board[1][1] == player and self.board[2][0] == player:
            return True
        return False
    

    # Minimax algorithm for AI to find the best move
    def minimax(self, minimax_board, depth, is_maximizing):
        if self.check_win(2): 
            return float('inf')
        elif self.check_win(1):
            return float('-inf')
        elif self.is_full_board():
            return 0
    
        if is_maximizing:
            best_score = -1000
            for row in range(self.board_rows):
                for col in range(self.board_cols):
                    if minimax_board[row][col] == 0:
                        minimax_board[row][col] = 2
                        score = self.minimax(minimax_board, depth + 1, False)
                        minimax_board[row][col] = 0
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = 1000
            for row in range(self.board_rows):
                for col in range(self.board_cols):
                    if minimax_board[row][col] == 0:
                        minimax_board[row][col] = 1
                        score = self.minimax(minimax_board, depth + 1, True)
                        minimax_board[row][col] = 0
                        best_score = min(score, best_score)
            return best_score
        
    # Function to find the best move for the AI
    def best_move(self):
        best_score = -1000
        move = (-1, -1)
        for row in range(self.board_rows):
            for col in range(self.board_cols):
                if self.board[row][col] == 0:
                    self.board[row][col] = 2
                    score = self.minimax(self.board, 0, False)
                    self.board[row][col] = 0
                    if score > best_score:
                        best_score = score
                        move = (row, col)
                    
        if move != (-1, -1):
            self.mark_square(move[0], move[1], 2)
            return True
    
        return False

    # Function to restart the game
    def restart_game(self):
        self.screen.fill(self.black)
        self.draw_lines()
        for row in range(self.board_rows):
            for col in range(self.board_cols):
                self.board[row][col] = 0
     

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
        
                if event.type == pygame.MOUSEBUTTONDOWN and not self.gameover:
                    mouseX = event.pos[0] // self.square_size
                    mouseY = event.pos[1] // self.square_size
            
                    if self.avail_square(mouseY, mouseX):
                        self.mark_square(mouseY, mouseX, self.player)
                        if self.check_win(self.player):
                            self.gameover = True
                        self.player = self.player % 2 + 1
                
                        if not self.gameover:
                            if self.best_move():
                                if self.check_win(2):
                                    self.gameover = True
                                self.player = self.player % 2 + 1
                        
                        if not self.gameover:
                            if self.is_full_board():
                                self.gameover = True
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart_game()
                        self.gameover = False
                        self.player = 1

            if not self.gameover:
                self.draw_lines()
                self.draw_figure()
            else:
                if self.check_win(1):
                    self.draw_figure(self.green)
                    self.draw_lines(self.green)
                elif self.check_win(2):
                    self.draw_figure(self.red)
                    self.draw_lines(self.red)
                else:
                    self.draw_figure(self.grey)
                    self.draw_lines(self.grey)
            pygame.display.update()

        


       
    
    