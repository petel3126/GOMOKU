import pygame
import sys

from caro_ai.ai.GameState import GameState
from caro_ai.ai.alphabeta_agent import AlphaBetaAgent
from caro_ai.game.board import check_win
from caro_ai.ui.menu_overlay import MenuOverlay
from caro_ai.ui.widgets import Button

pygame.init()

# =========================================================
# CONFIG GIAO DIỆN
# =========================================================
WIDTH = 800
HEIGHT = 800

BOARD_ROWS = 15  
BOARD_COLS = 15  
CELL_SIZE = 40

BOARD_X = 100
BOARD_Y = 100

LINE_COLOR = (40, 40, 40)
BG_COLOR = (245, 222, 179)    # Màu nền gỗ sáng khi chơi
PLAYER_COLOR = (200, 50, 50)  # Đỏ cho Người chơi
AI_COLOR = (50, 50, 200)      # Xanh cho AI


class CaroUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Caro AI - Minimax Alpha-Beta")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 35, bold=True)
        
        # Khởi tạo Menu Overlay từ file bạn gửi
        self.menu = MenuOverlay(WIDTH, HEIGHT)
        self.mode = "MENU"  # Trạng thái ban đầu là MENU
        
        # Quản lý chế độ chơi
        self.ai_first = False 
        self.ai_sign = 'O'
        self.human_sign = 'X'
        
        # Các nút bấm điều hướng khi kết thúc ván (Game Over)
        self.restart_btn = Button(220, 730, 160, 45, "Play Again", bg_color=(34, 139, 34))
        self.menu_btn = Button(420, 730, 160, 45, "Menu", bg_color=(128, 128, 128))
        
        self.game_over = False
        self.winner = None

    def reset_game(self):
        """Khởi tạo lại ma trận bàn cờ dựa vào chế độ chơi được chọn từ Menu"""
        board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        
        # Quy ước: Nước đầu tiên của ván luôn luôn là quân 'X'
        self.state = GameState(board=board, current_player='X') 
        self.game_over = False
        self.winner = None

        if self.ai_first:
            # AI DI TRC
            self.ai_sign = 'X'
            self.human_sign = 'O'
            self.ai = AlphaBetaAgent(player='X', depth=4)
            
            # AI DI TRC -> tu dong cho nuoc dau tien o giua
            self.ai_move()
        else:
            # NG di truoc
            self.ai_sign = 'O'
            self.human_sign = 'X'
            self.ai = AlphaBetaAgent(player='O', depth=4)

    def draw_board(self):
        """Vẽ toàn bộ bàn cờ và quân cờ"""
        self.screen.fill(BG_COLOR)
        
        # Vẽ lưới các ô vuông (15 ô cần 16 đường thẳng)
        for row in range(BOARD_ROWS + 1):
            pygame.draw.line(self.screen, LINE_COLOR, 
                (BOARD_X, BOARD_Y + row * CELL_SIZE),
                (BOARD_X + BOARD_COLS * CELL_SIZE, BOARD_Y + row * CELL_SIZE), 1)
        for col in range(BOARD_COLS + 1):
            pygame.draw.line(self.screen, LINE_COLOR,
                (BOARD_X + col * CELL_SIZE, BOARD_Y),
                (BOARD_X + col * CELL_SIZE, BOARD_Y + BOARD_ROWS * CELL_SIZE), 1)

        # Vẽ các quân cờ động dựa theo quân thực tế đang nắm giữ
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                value = self.state.board[row][col]
                cx = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
                cy = BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2

                # Vẽ quân của NGƯỜI CHƠI (Màu đỏ)
                if value == self.human_sign:
                    if self.human_sign == 'X':
                        s = 12
                        pygame.draw.line(self.screen, PLAYER_COLOR, (cx-s, cy-s), (cx+s, cy+s), 4)
                        pygame.draw.line(self.screen, PLAYER_COLOR, (cx+s, cy-s), (cx-s, cy+s), 4)
                    else:
                        pygame.draw.circle(self.screen, PLAYER_COLOR, (cx, cy), 15, 3)

                # Vẽ quân của AI (Màu xanh)
                elif value == self.ai_sign:
                    if self.ai_sign == 'X':
                        s = 12
                        pygame.draw.line(self.screen, AI_COLOR, (cx-s, cy-s), (cx+s, cy+s), 4)
                        pygame.draw.line(self.screen, AI_COLOR, (cx+s, cy-s), (cx-s, cy+s), 4)
                    else:
                        pygame.draw.circle(self.screen, AI_COLOR, (cx, cy), 15, 3)

        # Hiện giao diện thông báo kết quả khi Game Over
        if self.game_over:
            msg = "AI WIN" if self.winner == 'AI' else "YOU !"
            color = AI_COLOR if self.winner == 'AI' else PLAYER_COLOR
            text = self.font.render(msg, True, color)
            rect = text.get_rect(center=(WIDTH // 2, 50))
            self.screen.blit(text, rect)
            
            # Đổ dữ liệu 2 nút Chơi Lại / Menu lên màn hình
            self.restart_btn.draw(self.screen)
            self.menu_btn.draw(self.screen)

    def player_move(self, mouse_pos):
        """Xử lý lượt đánh của con người"""
        if self.game_over or self.state.current_player != self.human_sign:
            return

        mx, my = mouse_pos
        col = (mx - BOARD_X) // CELL_SIZE
        row = (my - BOARD_Y) // CELL_SIZE

        if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
            if self.state.board[row][col] == " ":
                self.state.board[row][col] = self.human_sign
                
                # Kiểm tra thắng cuộc cho Người
                if check_win(self.state.board, row, col, self.human_sign):
                    self.game_over = True
                    self.winner = 'PLAYER'
                else:
                    # Đổi lượt sang cho AI
                    self.state.current_player = self.ai_sign
                    
                    # Vẽ cập nhật ngay quân cờ vừa đánh trước khi AI bắt đầu chặn đứng mạch suy nghĩ
                    self.draw_board()
                    pygame.display.update()
                    
                    self.ai_move()

    def ai_move(self):
        """Kích hoạt AI tìm kiếm nước đi"""
        if self.game_over: 
            return
        
        move = self.ai.choose_move(self.state)
        if move:
            r, c = move
            self.state.board[r][c] = self.ai_sign
            
            # Kiểm tra thắng cuộc cho AI
            if check_win(self.state.board, r, c, self.ai_sign):
                self.game_over = True
                self.winner = 'AI'
            else:
                # Trả lượt lại cho Con người
                self.state.current_player = self.human_sign

    def run(self):
        """Vòng lặp chạy Game chính xử lý luồng nhận tín hiệu từ Menu của bạn"""
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # 1. PHÂN PHỐI SỰ KIỆN Ở TRẠNG THÁI MENU
                if self.mode == "MENU":
                    action = self.menu.handle_event(event)
                    
                    # Đón nhận chuỗi "play_human" từ nút số 1 của bạn
                    if action == "play_human":
                        self.ai_first = False
                        self.reset_game()
                        self.mode = "PLAYING"
                        
                    # Đón nhận chuỗi "play_ai" từ nút số 2 của bạn
                    elif action == "play_ai":
                        self.ai_first = True
                        self.reset_game()
                        self.mode = "PLAYING"
                        
                    # Đón nhận chuỗi "quit" từ nút Thoát Game
                    elif action == "quit":
                        pygame.quit()
                        sys.exit()
                
                # 2. PHÂN PHỐI SỰ KIỆN Ở TRẠNG THÁI ĐANG CHƠI TRÊN BÀN CỜ
                elif self.mode == "PLAYING":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.game_over:
                            # Nếu kết thúc ván, kiểm tra tương tác nút điều hướng
                            if self.restart_btn.is_clicked(event):
                                self.reset_game()
                            elif self.menu_btn.is_clicked(event):
                                self.mode = "MENU"
                        else:
                            # Nếu đang chơi, xử lý vị trí click cờ thông thường
                            self.player_move(event.pos)
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:  # Nhấn phím M nhanh để rút lui về Menu
                            self.mode = "MENU"

            # Render đồ họa dựa theo trạng thái màn hình hiện tại
            if self.mode == "MENU":
                self.menu.draw(self.screen)
            else:
                self.draw_board()
            
            pygame.display.update()
            self.clock.tick(60)

