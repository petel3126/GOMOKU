# widgets.py
import pygame


class Button:
    def __init__(self, x, y, width, height, text,
                 bg_color=(70, 70, 70),
                 hover_color=(100, 100, 100),
                 text_color=(255, 255, 255)):

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color

        self.font = pygame.font.SysFont("arial", 28)

    def draw(self, screen):

        mouse_pos = pygame.mouse.get_pos()

        color = self.bg_color

        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color

        pygame.draw.rect(screen, color, self.rect, border_radius=10)

        text_surface = self.font.render(
            self.text,
            True,
            self.text_color
        )

        text_rect = text_surface.get_rect(center=self.rect.center)

        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True

        return False