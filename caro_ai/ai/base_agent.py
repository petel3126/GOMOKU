from. GameState import GameState
class BaseAgent:

    def __init__(self, player):
        self.player = player
        self.opponent = 'O' if player == 'X' else 'X'
    
    def choose_move(self, state):
        raise NotImplementedError
    
    def get_valid_moves(self, state):

        """ tra ve danh sach o trong """
        moves = []
        board = state.board 

        for row in range(len(board)):
            for col in range(len(board[0])):

                if board[row][col] == " ":
                    moves.append((row,col))

        return moves 
    
    def is_valid_move(self,state,move):
    
        """ kiem tra nuoc di hop le """

        row,col = move 
        board = state.board 
        return board[row][col] == " "
    
    def make_move(self, state, move, player):
        """tao state moi sau khi danh"""

        row, col = move 

        # copy board 
        new_board = [r[:] for r in state.board]

        # danh quan 
        new_board[row][col] = player 

        # doi luot 
        next_player = 'O' if player == 'X' else 'X'
        return GameState(new_board, next_player)
