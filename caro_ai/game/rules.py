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