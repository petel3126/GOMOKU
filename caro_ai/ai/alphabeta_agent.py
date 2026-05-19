import math
from. import move_ordering as od
from. import evaluation as e
from.GameState import GameState
from. base_agent import BaseAgent
from caro_ai.game import board as b
EMPTY = " "
class AlphaBetaAgent(BaseAgent):
    def __init__(self, player, depth=4):
        super().__init__(player)
        self.depth = depth

    def choose_move(self, state):
        """
        Ghi đè phương thức từ BaseAgent.
        Hàm này là điểm bắt đầu để tìm nước đi tốt nhất.
        """
        board = state.board
        move = self.find_best_move( self.player, self.opponent, board, self.depth
        )
        return move

    def alpha_beta(self, board, depth, alpha, beta, maximizing):
        """
        Thuật toán Alpha-Beta Pruning dưới dạng một phương thức của class.
        """
        if depth == 0:
            return e.evaluate(board, self.player)
      
        moves = b.generate_moves(board, distance=2)
        
        if not moves:
            return 0

        if maximizing:
            moves = od.order_moves(board, moves, self.player, self.opponent)
            moves = moves[:10]
            
            best = -math.inf
            for r, c in moves:
                board[r][c] = self.player
                value = self.alpha_beta(board, depth - 1, alpha, beta, False)
                board[r][c] = " " # EMPTY
                
                best = max(best, value)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best
        else:
            moves = od.order_moves(board, moves, self.opponent, self.player)
            if depth >= 3:
                moves = moves[:10]
            else:
                moves = moves[:15]
            
            best = math.inf
            for r, c in moves:
                board[r][c] = self.opponent
                value = self.alpha_beta(board, depth - 1, alpha, beta, True)
                board[r][c] = " " # EMPTY
                
                best = min(best, value)
                beta = min(beta, best)
                if beta <= alpha:
                    break
            return best

    def find_best_move(self, player, opponent, board, depth):
     best_score = -math.inf
     best_move = None

    # =====================================================
    # GENERATE MOVES
    # =====================================================

     moves = b.generate_moves(board, distance=2)

    # =====================================================
    # AI WIN IMMEDIATELY
    # =====================================================

     for r, c in moves:

        board[r][c] = player

        if b.check_win(board, r, c, player):

            board[r][c] = EMPTY

            return (r, c)

        board[r][c] = EMPTY

    # =====================================================
    # BLOCK OPPONENT WIN
    # =====================================================

     for r, c in moves:

        board[r][c] = opponent

        if b.check_win(board, r, c, opponent):

            board[r][c] = EMPTY

            return (r, c)

        board[r][c] = EMPTY

    # =====================================================
    # MOVE ORDERING
    # =====================================================

     moves = od.order_moves(
        board,
        moves,
        player,
        opponent
    )

     moves = moves[:10]

    # =====================================================
    # SEARCH
    # =====================================================

     for r, c in moves:

        board[r][c] = player

        score = self.alpha_beta(
            board,
            depth - 1,
            -math.inf,
            math.inf,
            False
        )

        board[r][c] = EMPTY

        if score > best_score:

            best_score = score
            best_move = (r, c)

     return best_move