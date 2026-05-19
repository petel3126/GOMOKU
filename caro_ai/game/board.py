BOARD_SIZE = 15
EMPTY = " "




def __init__(self, size=15):

        self.size = size

        self.grid = [
            [" " for _ in range(size)]
            for _ in range(size)
        ]
def place_move(self, row, col, player):

    if self.grid[row][col] == " ":

        self.grid[row][col] = player
        return True

    return False
def undo_move(self, row, col):

    self.grid[row][col] = " "

def is_empty(self, row, col):

    return self.grid[row][col] == " "

def check_win(board, row, col, player):

    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1)
    ]

    for dr, dc in directions:

        count = 1

        # forward
        for i in range(1, 5):

            nr = row + dr * i
            nc = col + dc * i

            if (
                0 <= nr < 15 and
                0 <= nc < 15 and
                board[nr][nc] == player
            ):

                count += 1

            else:
                break

        # backward
        for i in range(1, 5):

            nr = row - dr * i
            nc = col - dc * i

            if (
                0 <= nr < 15 and
                0 <= nc < 15 and
                board[nr][nc] == player
            ):

                count += 1

            else:
                break

        if count >= 5:
            return True

    return False
def board_has_win(board, player):

    for r in range(15):
        for c in range(15):

            if board[r][c] == player:

                if check_win(board, r, c, player):
                    return True

    return False

def has_neighbor(board, row, col):

    for dr in range(-1, 2):
        for dc in range(-1, 2):

            if dr == 0 and dc == 0:
                continue

            nr = row + dr
            nc = col + dc

            if (
                0 <= nr < BOARD_SIZE and
                0 <= nc < BOARD_SIZE
            ):

                if board[nr][nc] != EMPTY:
                    return True

    return False

def generate_moves(board, distance=2):

    moves = set()

    has_piece = False

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):

            if board[r][c] != EMPTY:

                has_piece = True

                for dr in range(-distance, distance + 1):
                    for dc in range(-distance, distance + 1):

                        nr = r + dr
                        nc = c + dc

                        if (
                            0 <= nr < BOARD_SIZE and
                            0 <= nc < BOARD_SIZE and
                            board[nr][nc] == EMPTY
                        ):

                            if has_neighbor(board, nr, nc):
                                moves.add((nr, nc))

    if not has_piece:
        return [(BOARD_SIZE // 2, BOARD_SIZE // 2)]

    return list(moves)

def is_full(self):

    for row in self.grid:
        if " " in row:
            return False

    return True

def reset(self):

    self.grid = [
        [" " for _ in range(self.size)]
        for _ in range(self.size)
    ]
