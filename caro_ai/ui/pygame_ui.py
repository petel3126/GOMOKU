import pygame
import sys

from caro_ai.ai.GameState import GameState
from caro_ai.ai.alphabeta_agent import AlphaBetaAgent
from caro_ai.game.board import check_win
from caro_ai.ui.menu_overlay import MenuOverlay
from caro_ai.ui.widgets import Button

pygame.init()

WIDTH = 800
HEIGHT = 800

BOARD_ROWS = 15
BOARD_COLS = 15
CELL_SIZE = 40

BOARD_X = 100
BOARD_Y = 100

LINE_COLOR = (40, 40, 40)
BG_COLOR = (245, 222, 179)
PLAYER_X_COLOR = (200, 50, 50)
PLAYER_O_COLOR = (50, 50, 200)


class CaroUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Caro AI - Minimax Alpha-Beta")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 35, bold=True)

        self.menu = MenuOverlay(WIDTH, HEIGHT)
        self.mode = "MENU"

        self.two_player_mode = False
        self.ai_first = False
        self.ai_sign = "O"
        self.human_sign = "X"
        self.ai = None

        self.undo_btn = Button(120, 730, 160, 45, "Undo", bg_color=(184, 134, 11))
        self.restart_btn = Button(320, 730, 160, 45, "Play Again", bg_color=(34, 139, 34))
        self.menu_btn = Button(520, 730, 160, 45, "Menu", bg_color=(128, 128, 128))

        self.state = GameState(
            board=[[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)],
            current_player="X",
        )
        self.game_over = False
        self.winner = None
        self.move_history = []
        self.undo_available = False

    def reset_game(self):
        board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        self.state = GameState(board=board, current_player="X")
        self.game_over = False
        self.winner = None
        self.ai = None
        self.move_history = []
        self.undo_available = False

        if self.two_player_mode:
            self.ai_sign = "O"
            self.human_sign = "X"
            return

        if self.ai_first:
            self.ai_sign = "X"
            self.human_sign = "O"
            self.ai = AlphaBetaAgent(player="X", depth=4)
            self.ai_move()
        else:
            self.ai_sign = "O"
            self.human_sign = "X"
            self.ai = AlphaBetaAgent(player="O", depth=4)

    def draw_piece(self, row, col, value):
        cx = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
        cy = BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2
        color = PLAYER_X_COLOR if value == "X" else PLAYER_O_COLOR

        if value == "X":
            s = 12
            pygame.draw.line(self.screen, color, (cx - s, cy - s), (cx + s, cy + s), 4)
            pygame.draw.line(self.screen, color, (cx + s, cy - s), (cx - s, cy + s), 4)
        elif value == "O":
            pygame.draw.circle(self.screen, color, (cx, cy), 15, 3)

    def color_for_player(self, player):
        return PLAYER_X_COLOR if player == "X" else PLAYER_O_COLOR

    def draw_status(self):
        if self.game_over:
            if self.winner == "DRAW":
                msg = "DRAW"
                color = LINE_COLOR
            elif self.two_player_mode:
                msg = f"PLAYER {self.winner} WIN"
                color = self.color_for_player(self.winner)
            else:
                msg = "AI WIN" if self.winner == "AI" else "YOU WIN"
                winner_sign = self.ai_sign if self.winner == "AI" else self.human_sign
                color = self.color_for_player(winner_sign)
        elif self.two_player_mode:
            msg = f"TURN: {self.state.current_player}"
            color = self.color_for_player(self.state.current_player)
        else:
            msg = "YOUR TURN" if self.state.current_player == self.human_sign else "AI THINKING"
            color = self.color_for_player(self.state.current_player)

        text = self.font.render(msg, True, color)
        rect = text.get_rect(center=(WIDTH // 2, 50))
        self.screen.blit(text, rect)

    def draw_board(self):
        self.screen.fill(BG_COLOR)

        for row in range(BOARD_ROWS + 1):
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (BOARD_X, BOARD_Y + row * CELL_SIZE),
                (BOARD_X + BOARD_COLS * CELL_SIZE, BOARD_Y + row * CELL_SIZE),
                1,
            )

        for col in range(BOARD_COLS + 1):
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (BOARD_X + col * CELL_SIZE, BOARD_Y),
                (BOARD_X + col * CELL_SIZE, BOARD_Y + BOARD_ROWS * CELL_SIZE),
                1,
            )

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                self.draw_piece(row, col, self.state.board[row][col])

        self.draw_status()

        if self.move_history and self.undo_available:
            self.undo_btn.draw(self.screen)

        if self.game_over:
            self.restart_btn.draw(self.screen)
            self.menu_btn.draw(self.screen)

    def is_board_full(self):
        return all(" " not in row for row in self.state.board)

    def player_move(self, mouse_pos):
        if self.game_over:
            return

        if not self.two_player_mode and self.state.current_player != self.human_sign:
            return

        mx, my = mouse_pos
        col = (mx - BOARD_X) // CELL_SIZE
        row = (my - BOARD_Y) // CELL_SIZE

        if not (0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS):
            return

        if self.state.board[row][col] != " ":
            return

        player = self.state.current_player if self.two_player_mode else self.human_sign
        self.state.board[row][col] = player
        self.move_history.append((row, col, player))
        self.undo_available = True

        if check_win(self.state.board, row, col, player):
            self.game_over = True
            self.winner = player if self.two_player_mode else "PLAYER"
            return

        if self.is_board_full():
            self.game_over = True
            self.winner = "DRAW"
            return

        if self.two_player_mode:
            self.state.current_player = "O" if player == "X" else "X"
            return

        self.state.current_player = self.ai_sign
        self.draw_board()
        pygame.display.update()
        self.ai_move()

    def ai_move(self):
        if self.game_over or self.ai is None:
            return

        move = self.ai.choose_move(self.state)
        if not move:
            self.game_over = True
            self.winner = "DRAW"
            return

        r, c = move
        self.state.board[r][c] = self.ai_sign
        self.move_history.append((r, c, self.ai_sign))

        if check_win(self.state.board, r, c, self.ai_sign):
            self.game_over = True
            self.winner = "AI"
            return

        if self.is_board_full():
            self.game_over = True
            self.winner = "DRAW"
            return

        self.state.current_player = self.human_sign

    def undo_move(self):
        if not self.move_history or not self.undo_available:
            return

        if self.two_player_mode:
            row, col, player = self.move_history.pop()
            self.state.board[row][col] = " "
            self.state.current_player = player
        else:
            if self.state.current_player == self.human_sign and self.move_history:
                last_row, last_col, last_player = self.move_history[-1]
                if last_player == self.ai_sign:
                    self.move_history.pop()
                    self.state.board[last_row][last_col] = " "

            if self.move_history:
                last_row, last_col, last_player = self.move_history[-1]
                if last_player == self.human_sign:
                    self.move_history.pop()
                    self.state.board[last_row][last_col] = " "

            self.state.current_player = self.human_sign

        self.game_over = False
        self.winner = None
        self.undo_available = False

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.mode == "MENU":
                    action = self.menu.handle_event(event)

                    if action == "play_human":
                        self.two_player_mode = False
                        self.ai_first = False
                        self.reset_game()
                        self.mode = "PLAYING"
                    elif action == "play_ai":
                        self.two_player_mode = False
                        self.ai_first = True
                        self.reset_game()
                        self.mode = "PLAYING"
                    elif action == "play_two_players":
                        self.two_player_mode = True
                        self.ai_first = False
                        self.reset_game()
                        self.mode = "PLAYING"
                    elif action == "quit":
                        pygame.quit()
                        sys.exit()

                elif self.mode == "PLAYING":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.undo_btn.is_clicked(event):
                            self.undo_move()
                        elif self.game_over:
                            if self.restart_btn.is_clicked(event):
                                self.reset_game()
                            elif self.menu_btn.is_clicked(event):
                                self.mode = "MENU"
                        else:
                            self.player_move(event.pos)

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.mode = "MENU"

            if self.mode == "MENU":
                self.menu.draw(self.screen)
            else:
                self.draw_board()

            pygame.display.update()
            self.clock.tick(60)
