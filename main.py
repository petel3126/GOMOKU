import pygame
from caro_ai.ui.pygame_ui import CaroUI
import sys
def main():
    try:
        # Khởi tạo instance của game
        game = CaroUI()
        
        # Chạy vòng lặp game
        game.run()
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()