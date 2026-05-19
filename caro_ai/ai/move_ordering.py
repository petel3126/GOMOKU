import math
from caro_ai.game import board as b
from. import evaluation as e

# ==========================================================
# CONFIG
# ==========================================================

EMPTY = " "
BOARD_SIZE = 15

#
def score_move(board, row, col, player, opponent):

    # ----------------------
    # WIN MOVE
    # ----------------------

    board[row][col] = player

    if b.check_win(board, row, col, player):

        board[row][col] = EMPTY

        return 1000000000

    # ----------------------
    # BLOCK OPPONENT WIN
    # ----------------------

    board[row][col] = opponent

    if b.check_win(board, row, col, opponent):

        board[row][col] = EMPTY

        return 999999999

    # ----------------------
    # HEURISTIC
    # ----------------------

    board[row][col] = player

    score = 0

    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1)
    ]

    for dr, dc in directions:

        line = ""

        for k in range(-5, 6):

            nr = row + dr * k
            nc = col + dc * k

            if (
                0 <= nr < BOARD_SIZE and
                0 <= nc < BOARD_SIZE
            ):

                cell = board[nr][nc]

                if cell == player:
                    line += "X"

                elif cell == opponent:
                    line += "O"

                else:
                    line += "_"

            else:
                line += "#"

        # ----------------------
        # ATTACK
        # ----------------------

        for pattern, value in e.PATTERNS.items():

            if pattern in line:
                score += line.count(pattern) * value
        # ----------------------
        # DEFENSE
        # ----------------------

        line_opp = (
            line
            .replace("X", "T")
            .replace("O", "X")
            .replace("T", "O")
        )

        for pattern, value in e.PATTERNS.items():

            count = line_opp.count(pattern)

            if pattern == "_XXXX_":

                score += count * value * 6

            elif pattern == "_XX_X_":

                score += count * value * 5

            elif pattern == "_X_XX_":
                score += count * value * 5

            elif pattern == "_XXX_":
                score += count * value * 5

            else:

                score += count * value * 0.8
    # ----------------------
    # CENTER BONUS
    # ----------------------

    center = BOARD_SIZE // 2

    dist = abs(row - center) + abs(col - center)

    score += max(0, 20 - dist)

    board[row][col] = EMPTY

    return score

# ==========================================================
# ORDER MOVES
# ==========================================================

def order_moves(board, moves, player, opponent):

    scored = []

    for r, c in moves:

        score = score_move(
            board,
            r,
            c,
            player,
            opponent
        )

        scored.append(
            (score, r, c)
        )

    scored.sort(reverse=True)

    return [
        (r, c)
        for score, r, c in scored
    ]

