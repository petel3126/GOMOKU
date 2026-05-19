# caro_ai/ui/menu_overlay.py
import pygame
from caro_ai.ui.widgets import Button

class MenuOverlay:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        center_x = screen_width // 2

        # Nút 1: Người chơi cầm X và đánh trước
        self.btn_human_first = Button(
            center_x - 125, 250, 250, 60, 
            "You First", bg_color=(70, 70, 70)
        )

        # Nút 2: AI cầm X và đánh trước
        self.btn_ai_first = Button(
            center_x - 125, 330, 250, 60, 
            "AI first", bg_color=(50, 50, 100) # Màu hơi xanh cho AI
        )

        # Nút 3: Thoát game
        self.quit_button = Button(
            center_x - 125, 410, 250, 60, 
            "Thoát Game", bg_color=(100, 30, 30)
        )

        self.title_font = pygame.font.SysFont("arial", 60, bold=True)

    def draw(self, screen):
        screen.fill((30, 30, 30)) # Nền Menu tối
        
        title = self.title_font.render("CARO AI", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.width // 2, 120))
        screen.blit(title, title_rect)

        self.btn_human_first.draw(screen)
        self.btn_ai_first.draw(screen)
        self.quit_button.draw(screen)

    def handle_event(self, event):
        if self.btn_human_first.is_clicked(event):
            return "play_human"
        
        if self.btn_ai_first.is_clicked(event):
            return "play_ai"

        if self.quit_button.is_clicked(event):
            return "quit"

        return None