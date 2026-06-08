# Caro AI

Trò chơi Caro viết bằng Python và Pygame, hỗ trợ chơi với AI hoặc chơi 2 người trên cùng một máy. AI sử dụng thuật toán Alpha-Beta Pruning kết hợp hàm đánh giá thế cờ để chọn nước đi.

## Tính năng chính

- Giao diện đồ họa bằng Pygame.
- Bàn cờ Caro kích thước 15x15.
- Luật thắng: người chơi có 5 quân liên tiếp theo hàng ngang, hàng dọc hoặc đường chéo sẽ thắng.
- 3 chế độ chơi trong menu:
  - `You First`: người chơi đi trước, AI đi sau.
  - `AI first`: AI đi trước, người chơi đi sau.
  - `2 Players`: hai người chơi lần lượt đánh X và O.
- AI dùng Alpha-Beta Pruning với độ sâu tìm kiếm mặc định trong UI là 4.
- Có nút `Undo` để quay lại lượt gần nhất, mỗi lần chỉ quay lại được 1 bước.
- Có module đánh giá thế cờ, sắp xếp nước đi và sinh nước đi gần các quân đã đánh để giảm không gian tìm kiếm.
- Có thư mục test và tài liệu ghi chú cho benchmark/thử nghiệm.

## Cài đặt

Yêu cầu:

- Python 3.10 trở lên
- pip

Cài thư viện:

```bash
pip install -r requirements.txt
```

Nếu file `requirements.txt` gây lỗi vì dòng không hợp lệ, có thể cài trực tiếp các thư viện chính:

```bash
pip install pygame numpy pytest
```

## Chạy game

Từ thư mục `Caro_AI`, chạy:

```bash
python main.py
```

Game sẽ mở cửa sổ Pygame với menu chính.

## Cách chơi

1. Chọn chế độ chơi ở menu.
2. Nhấn chuột vào ô trống trên bàn cờ để đặt quân.
3. Quân `X` có màu đỏ, quân `O` có màu xanh.
4. Người nào tạo được 5 quân liên tiếp theo ngang, dọc hoặc chéo sẽ thắng.
5. Nhấn `Undo` để quay lại lượt gần nhất. Sau khi undo, cần đánh nước mới thì mới có thể undo tiếp.
6. Khi kết thúc ván, có thể chọn:
   - `Play Again` để chơi lại.
   - `Menu` để quay về menu.
7. Trong khi chơi, có thể nhấn phím `M` để quay về menu.

## Cấu trúc dự án

```text
Caro_AI/
├── main.py                     # Điểm khởi chạy game
├── requirements.txt            # Danh sách thư viện cần cài
├── caro_ai/
│   ├── app.py
│   ├── modes.py                # Enum các chế độ: normal, developer, benchmark
│   ├── ai/
│   │   ├── alphabeta_agent.py  # AI chính dùng Alpha-Beta Pruning
│   │   ├── minimax_agent.py    # Bản Minimax cơ bản
│   │   ├── evaluation.py       # Hàm đánh giá thế cờ
│   │   ├── move_ordering.py    # Sắp xếp nước đi theo độ ưu tiên
│   │   └── GameState.py        # Trạng thái bàn cờ
│   ├── game/
│   │   ├── board.py            # Tiện ích bàn cờ và sinh nước đi
│   │   ├── rules.py            # Kiểm tra điều kiện thắng
│   │   └── caro.py
│   ├── ui/
│   │   ├── pygame_ui.py        # Vòng lặp game và vẽ giao diện
│   │   ├── menu_overlay.py     # Menu chọn chế độ chơi
│   │   └── widgets.py          # Button và widget UI
│   ├── benchmark/              # Khung chạy benchmark
│   ├── config/                 # File cấu hình game/AI
│   └── utils/                  # Logger, visualizer
├── tests/                      # Unit tests
├── docs/                       # Tài liệu thuật toán và kết quả thử nghiệm
└── notebooks/                  # Notebook phân tích
```

## AI hoạt động như thế nào?

AI chính nằm trong `caro_ai/ai/alphabeta_agent.py`.

Quy trình chọn nước đi:

1. Sinh các nước đi hợp lệ gần những quân đã có trên bàn cờ.
2. Ưu tiên nước thắng ngay nếu có.
3. Chặn nước thắng ngay của đối thủ nếu cần.
4. Tìm nước tạo thế mạnh như bốn quân liên tiếp.
5. Chặn các thế nguy hiểm của đối thủ, ví dụ ba quân mở.
6. Sắp xếp nước đi theo điểm heuristic.
7. Chạy Alpha-Beta Pruning để tìm nước có điểm tốt nhất.

Hàm đánh giá trong `caro_ai/ai/evaluation.py` chấm điểm dựa trên các mẫu thế cờ như:

- `XXXXX`: thắng.
- `_XXXX_`: bốn mở.
- `XXXX_`, `_XXXX`: bốn bị chặn một đầu.
- `_XXX_`: ba mở.
- `_XX_`: hai mở.

Điểm phòng thủ được nhân trọng số cao hơn để AI ưu tiên chặn các mối nguy hiểm từ người chơi.

## Chạy test

Từ thư mục `Caro_AI`, chạy:

```bash
pytest
```

## Ghi chú phát triển

- Kích thước bàn cờ trong giao diện hiện được đặt trực tiếp trong `caro_ai/ui/pygame_ui.py` là 15x15.
- File `caro_ai/config/game_settings.json` đang có cấu hình 6x7, thắng 4, nhưng giao diện Pygame hiện không dùng cấu hình này.
- AI trong giao diện đang dùng `AlphaBetaAgent(player=..., depth=4)`.
- Các file trong `docs/` và `benchmark/` hiện đóng vai trò khung/placeholder để mở rộng phân tích thuật toán sau này.
