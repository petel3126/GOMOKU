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

    def move_creates_four(self, board, row, col, player, opponent):
        board[row][col] = player

        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1)
        ]

        four_patterns = [
            "_XXXX_",
            "XXXX_",
            "_XXXX",
            "XX_XX",
            "XXX_X",
            "X_XXX"
        ]

        for dr, dc in directions:
            line = ""

            for k in range(-5, 6):
                nr = row + dr * k
                nc = col + dc * k

                if 0 <= nr < len(board) and 0 <= nc < len(board[0]):
                    cell = board[nr][nc]

                    if cell == player:
                        line += "X"
                    elif cell == opponent:
                        line += "O"
                    else:
                        line += "_"
                else:
                    line += "#"

            for pattern in four_patterns:
                if pattern in line:
                    board[row][col] = EMPTY
                    return True

        board[row][col] = EMPTY
        return False

    def find_four_moves(self, board, moves, player, opponent):
        four_moves = []

        for r, c in moves:
            if self.move_creates_four(board, r, c, player, opponent):
                four_moves.append((r, c))

        return four_moves

    def find_open_three_blocks(self, board, opponent):
        blocks = set()
        rows = len(board)
        cols = len(board[0])

        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1)
        ]

        for r in range(rows):
          for c in range(cols):
            for dr, dc in directions:

                # Mẫu 5 ô: . X X X .
                cells = []

                for i in range(5):
                    nr = r + dr * i
                    nc = c + dc * i

                    if not (0 <= nr < rows and 0 <= nc < cols):
                        break

                    cells.append((nr, nc))

                if len(cells) == 5:
                    values = [board[nr][nc] for nr, nc in cells]

                    if values == [EMPTY, opponent, opponent, opponent, EMPTY]:
                        blocks.add(cells[0])
                        blocks.add(cells[4])

                # Mẫu 6 ô: . X . X X . hoặc . X X . X .
                cells = []

                for i in range(6):
                    nr = r + dr * i
                    nc = c + dc * i

                    if not (0 <= nr < rows and 0 <= nc < cols):
                        break

                    cells.append((nr, nc))

                if len(cells) == 6:
                    values = [board[nr][nc] for nr, nc in cells]

                    if values == [EMPTY, opponent, EMPTY, opponent, opponent, EMPTY]:
                        blocks.add(cells[2])

                    elif values == [EMPTY, opponent, opponent, EMPTY, opponent, EMPTY]:
                        blocks.add(cells[3])

        return list(blocks)

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
    # AI CREATE FOUR BEFORE BLOCKING OPEN THREE
    # =====================================================

     four_moves = self.find_four_moves(
        board,
        moves,
        player,
        opponent
    )

     if four_moves:
        ordered_four_moves = od.order_moves(
            board,
            four_moves,
            player,
            opponent
        )

        return ordered_four_moves[0]

    # =====================================================
    # BLOCK OPPONENT OPEN THREE
    # =====================================================

     open_three_blocks = self.find_open_three_blocks(board, opponent)
     open_three_blocks = [
        move for move in open_three_blocks
        if move in moves
     ]

     if open_three_blocks:
        ordered_blocks = od.order_moves(
            board,
            open_three_blocks,
            player,
            opponent
        )

        return ordered_blocks[0]

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
