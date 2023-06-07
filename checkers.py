import pygame
from copy import deepcopy

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS
WHITE = (255, 255, 255)
GREY=(163, 194, 194)
BLACK=(0,0,0)
GREEN=(0, 204, 0)
FPS = 60
CROWN = pygame.transform.scale(pygame.image.load('D://May//Project//crown.png'), (65, 40))



class Board:
    def __init__(self):
        self.board = []
        self.black_left = self.white_left = 12
        self.black_kings = self.white_kings = 0
        self.create_board()
    
    def draw_squares(self, win):#first white and alternate  and even 
        win.fill(GREY)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win,(WHITE), (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):#ai will evaluate
        return ((self.white_left - self.black_left)) + ((self.white_kings  - self.black_kings)*0.5)#1 no of pices and 0.5 no of king  

    def get_all_piece(self, color):# get current all pieces left on the table
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.black_kings += 1 

    def get_piece(self, row, col):#position
        return self.board[row][col]

    def create_board(self): #creating pieces
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):#capture pieces
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BLACK:
                    self.black_left -= 1
                else:
                    self.white_left -= 1
    
    def winner(self):
        if self.black_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return BLACK
        
        return None 
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BLACK or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))#by diagonal
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):#skip means capture opponent move-->basically jump
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves



class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK

    def get_board(self):
        return self.board
    
    def ai_move(self,board):
        self.board=board
        self.change_turn()



class Piece:
    PADDING = 30
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True
    
    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)



def minimax(position,depth,max_player,game,alpha,beta):
    if depth==0 or position.winner()!=None:
        return position.evaluate(),position
    
    if max_player:
        maxEval=float('-inf')
        best_move=None
        for move in get_all_moves(position,WHITE,game):
            evaluation=minimax(move,depth-1,False,game,alpha,beta)[0]
            maxEval=max(maxEval,evaluation)
            if maxEval==evaluation:
                best_move=move
            alpha = max(alpha,maxEval)
            if alpha >= beta:
                continue

        return maxEval,best_move

    else:
        minEval=float('inf')
        best_move=None
        for move in get_all_moves(position,WHITE,game):
            evaluation=minimax(move,depth-1,True,game,alpha,beta)[0]
            minEval=min(minEval,evaluation)
            if minEval==evaluation:
                best_move=move
            beta = min(beta,minEval)
            if alpha >= beta:
                continue
        return minEval,best_move


def simulate_move(piece, move, board, game, skip): # search for all possible moves
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board



def get_all_moves(board, color, game):
    moves = []
    capture_moves = []

    for piece in board.get_all_piece(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            if skip:  # If capturing move, add to capture_moves
                capture_moves.append(new_board)
            else:
                moves.append(new_board)

    # If there are capture_moves available, return capture_moves
    if capture_moves:
        return capture_moves
    else:
        return moves



def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()



WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col




def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    white_wins_image = pygame.image.load("D://May//Project//wwin.png")  # Load the image for white winning
    black_wins_image = pygame.image.load("D://May//Project//bwin.png")  # Load the image for black winning
    # Resize the images
    image_width = 800  # Set the desired width of the images
    image_height = 800  # Set the desired height of the images
    white_wins_image = pygame.transform.scale(white_wins_image, (image_width, image_height))
    black_wins_image = pygame.transform.scale(black_wins_image, (image_width, image_height))

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 3, True, game, float("-inf"), float("inf"))
            game.ai_move(new_board)

        if game.winner() == WHITE:  # Check if white player wins
            # Display the white_wins_image on the screen
            WIN.blit(white_wins_image, (0, 0))
            pygame.display.update()
            pygame.time.delay(4000)  # Delay for 4 seconds before quitting the game
            run = False
        elif game.winner() == BLACK:  # Check if black player wins
            # Display the black_wins_image on the screen
            WIN.blit(black_wins_image, (0, 0))
            pygame.display.update()
            pygame.time.delay(4000)  # Delay for 4 seconds before quitting the game
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()

main()








