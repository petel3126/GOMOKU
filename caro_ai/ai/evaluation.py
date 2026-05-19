from caro_ai.game import board as b 
from .base_agent import BaseAgent

PATTERNS = {

    # WIN
    "XXXXX": 100000000,

    # OPEN FOUR
    "_XXXX_": 5000000,

    # CLOSED FOUR
    "XXXX_": 1000000,
    "_XXXX": 1000000,

    # BROKEN FOUR
    "XX_XX": 800000,
    "XXX_X": 800000,
    "X_XXX": 800000,

    # OPEN THREE
    "_XXX_": 700000,

    # BROKEN THREE
    "_XX_X_": 15000,
    "_X_XX_": 15000,
    "_X_X_X_": 7000,

    # OPEN TWO
    "_XX_": 5000,

    # SMALL
    "_X_X_": 1000,
}

# ==========================================================
# GET ALL LINES


def get_all_lines(board):

    lines = []

    rows = len(board)
    cols = len(board[0])

    # hang ngang

    for r in range(rows):
        lines.append(board[r])

    # hang doc
 
    for c in range(cols):

        line = []

        for r in range(rows):
            line.append(board[r][c])

        lines.append(line)

    # cheo chinh
    for start_row in range(rows):

        line = []

        r = start_row
        c = 0

        while r < rows and c < cols:

            line.append(board[r][c])

            r += 1
            c += 1

        if len(line) >= 5:
            lines.append(line)

    for start_col in range(1, cols):

        line = []

        r = 0
        c = start_col

        while r < rows and c < cols:

            line.append(board[r][c])

            r += 1
            c += 1

        if len(line) >= 5:
            lines.append(line)

    # cheo phu

    for start_row in range(rows):

        line = []

        r = start_row
        c = cols - 1

        while r < rows and c >= 0:

            line.append(board[r][c])

            r += 1
            c -= 1

        if len(line) >= 5:
            lines.append(line)

    for start_col in range(cols - 2, -1, -1):

        line = []

        r = 0
        c = start_col

        while r < rows and c >= 0:

            line.append(board[r][c])

            r += 1
            c -= 1

        if len(line) >= 5:
            lines.append(line)

    return lines

# ==========================================================
# BUILD LINE STRING
# ==========================================================

def build_line_string(line, player, opponent):

    s = ""

    for cell in line:

        if cell == player:
            s += "X"

        elif cell == opponent:
            s += "O"

        else:
            s += "_"

    return s

def evaluate_patterns(board, player, opponent):

    score = 0

    lines = get_all_lines(board)

    for line in lines:

        s = build_line_string( line, player, opponent)

        for pattern, value in PATTERNS.items():

            count = s.count(pattern)

            score += count * value

    return score

# ==========================================================
# EVALUATE
# ==========================================================

def evaluate(board, ai_player):
    EMPTY = " "
    AI = ai_player
    HUMAN = "O" if AI == "X" else "X"

    if b.board_has_win(board, AI):
        return 999999999

    if b.board_has_win(board, HUMAN):
        return -999999999

    attack = evaluate_patterns( board, AI, HUMAN 
    )

    defense = evaluate_patterns( board, HUMAN , AI
    )


    return attack - defense * 2.0