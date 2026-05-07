# Trí tuệ nằm trong cơ thể — Scene 1

Hiện thực hoá Manim cho **Scene 1** của tập 1 *"Cá chết vẫn biết bơi"* — series video phong cách 3Blue1Brown đặt câu hỏi *"trong một sinh vật thông minh, trí tuệ nằm ở đâu — trong não, hay trong cả cơ thể?"*

Scene 1 ứng với phút **0:35 – 2:00** trong kịch bản: từ lúc cá schematic chia BRAIN/BODY, đến khoảnh khắc não tắt, đến split 2 pane `θ_brain` vs `θ_body`, kết bằng công thức `θ = (θ_brain, θ_body)`.

---

## Yêu cầu

- **Python 3.9+** (khuyến nghị 3.10 hoặc 3.11)
- **Manim Community Edition** ≥ 0.18
- **FFmpeg** (Manim cần để ghép video)
- *Không cần LaTeX* — file dùng `MarkupText` cho subscript thay vì `MathTex`

## Cài đặt

### macOS

```bash
brew install py3cairo ffmpeg pango pkg-config scipy
pip install manim
```

### Ubuntu / WSL

```bash
sudo apt update
sudo apt install libcairo2-dev libpango1.0-dev ffmpeg python3-pip
pip install manim
```

### Windows (PowerShell)

```powershell
pip install manim
```

Nếu Windows lỗi cairo/pango, dùng WSL cho nhẹ hoặc cài MSYS2 theo [hướng dẫn chính thức](https://docs.manim.community/en/stable/installation/windows.html).

### Kiểm tra cài đặt

```bash
manim --version
```

Phải in ra `Manim Community v0.x.y`. Nếu được rồi thì sẵn sàng chạy.

---

## Cách chạy

`cd` vào thư mục chứa `scene1.py`:

```bash
# Preview nhanh — 480p, render khoảng 30 giây. Dùng khi đang chỉnh.
manim -pql scene1.py Scene1MainQuestion

# Chất lượng cao — 1080p 60fps. Dùng để review nội bộ.
manim -pqh scene1.py Scene1MainQuestion

# 4K — chậm nhưng đẹp. Dùng khi xuất bản.
manim -pqk scene1.py Scene1MainQuestion
```

**Giải nghĩa các cờ:**

| Cờ | Ý nghĩa |
|----|---------|
| `-p` | Tự động phát video sau khi render xong |
| `-q{l,m,h,k}` | Quality: low / medium / high / 4K |
| `-s` | Chỉ render **frame cuối** ra PNG (cực nhanh, dùng khi đang sửa layout) |
| `-n start,end` | Chỉ render từ animation thứ `start` đến `end` |
| `--prerun` | Estimate thời gian render và bắt lỗi sớm (theo workflow của Grant) |

Output mặc định nằm tại:

```
media/videos/scene1/<resolution>/Scene1MainQuestion.mp4
```

---

## Workflow lặp nhanh (theo Grant Sanderson)

Khi đang tinker visual, đừng render full mỗi lần. Có hai mẹo lớn:

**1. Render frame cuối ra ảnh:**

```bash
manim -sql scene1.py Scene1MainQuestion
```

Trong vài giây có ảnh PNG để kiểm tra layout — không cần chờ animate.

**2. Chỉ render một đoạn nhất định:**

Đếm số lần `self.play(...)` trước đoạn cần xem (gọi đó là `N`), rồi:

```bash
manim -pql scene1.py Scene1MainQuestion -n N,N+5
```

Ví dụ chỉ muốn xem PART E (mạng nơ-ron nhấp nháy) — đếm xem có khoảng 17 `self.play` trước nó, chạy `-n 17,33`. Nhanh gấp 5-10 lần render full.

---

## Cấu trúc Scene 1

File `scene1.py` chia thành 6 PART ứng với 6 nhịp của kịch bản:

| PART | Thời gian* | Nội dung |
|------|------------|----------|
| **A** | 0–10s | Cá xuất hiện, highlight BRAIN (đỏ) + BODY (xanh) |
| **B** | 10–20s | Não fade out — thân vẫn dao động theo dòng nước |
| **C** | 20–22s | Sweep aside, chuẩn bị split 2 pane |
| **D** | 22–40s | Pane trái: `θ_brain` (NN, *fast, flexible*). Pane phải: `θ_body` (cá + dots, *slow, rigid*) |
| **E** | 40–55s | NN nhấp nháy liên tục; body chỉ pulse rất nhẹ → tương phản tốc độ |
| **F** | 55–70s | Đóng bằng `θ = (θ_brain, θ_body)` — cả hai đều là tham số |

*Visual khoảng 60-70s; có thể giãn thêm bằng `self.wait()` để khớp voiceover khi mix âm thanh.

### Hai chỗ bạn có thể muốn chỉnh đầu tiên

1. **PART A — `self.wait(3.0)`** sau khi BRAIN/BODY hiện ra. Tăng nếu VO ở đoạn này dài hơn.
2. **PART E — `for _ in range(8)`**. Số lần flicker mạng nơ-ron. Tăng để cảnh "não học liên tục" kéo dài hơn.

### Helpers tái sử dụng

`scene1.py` tách hai helper sẽ dùng lại ở các Scene/Tập sau:

- `create_fish(color, stroke_width)` — cá schematic, không cần SVG ngoài
- `create_neural_net(layer_sizes, ...)` — mạng MLP đơn giản, trả về cả group, edges, layers để animate riêng từng phần

---

## Bảng màu (3Blue1Brown style)

Định nghĩa trong file:

| Tên | Hex | Dùng cho |
|-----|-----|----------|
| `BG_COLOR` | `#1C1C1C` | Nền bảng đen xanh đậm |
| `BLUE_3B1B` | `#3B82F6` | Màu chủ đạo (BODY, NN nodes) |
| `YELLOW_3B1B` | `#FBBF24` | Highlight (subscript, dots, công thức) |
| `RED_BRAIN` | `#EF4444` | BRAIN region |
| `GRAY_LIGHT` | `#E5E7EB` | Text chính, đường viền cá |
| `GRAY_DIM` | `#6B7280` | Edges NN khi không active, divider |

---

## Roadmap

Đã làm:

- [x] Scene 1 — Câu hỏi chính

Chưa làm (tham khảo file kịch bản gốc):

- [ ] Scene 0 — Cold open: con cá chết "bơi" trong dòng nước
- [ ] Scene 2 — Sự đa dạng kinh ngạc của mắt sinh học (6 cards)
- [ ] Scene 3 — Cú twist sọc ngựa vằn
- [ ] Scene 4+ — Pixel reduction, optimization landscape, v.v.

Tập 2 và 3 mới có dàn ý, chưa có chi tiết Manim.

---

## Troubleshooting

**`No module named 'manim'`** — chưa cài hoặc cài nhầm Python environment. Chạy `which python` và `which pip` để chắc.

**`OSError: cannot load Pango` / `cairo not found`** — thiếu system library. Quay lại bước cài đặt OS tương ứng.

**Font Việt hoặc ký tự `θ` hiển thị thành ô vuông** — máy thiếu font có Greek + Vietnamese. Cài DejaVu hoặc Noto:

```bash
# Ubuntu
sudo apt install fonts-dejavu fonts-noto

# macOS — DejaVu mặc định đã có
```

Hoặc đổi sang font cụ thể trong code:

```python
Text("BRAIN", font="DejaVu Sans", weight=BOLD, ...)
```

**Render rất chậm** — thử `-ql` thay vì `-qh`. Đoạn flicker NN ở PART E có nhiều animation nhỏ; giảm `range(8)` xuống `range(4)` khi preview.

**Muốn dùng `MathTex` (LaTeX) cho công thức đẹp hơn** — cài LaTeX (`texlive-full` trên Linux, MacTeX trên macOS, MiKTeX trên Windows), rồi đổi `MarkupText` thành `MathTex` với cú pháp `r"\theta_{\text{brain}}"`.

---

## Tham khảo

- Kịch bản gốc: `3blue1brown_script.md`
- [Manim Community docs](https://docs.manim.community/)
- [3Blue1Brown channel](https://www.youtube.com/@3blue1brown) — Grant Sanderson
- Tutorial *"Computational Design of Diverse Morphologies and Sensors for Vision and Robotics"* — nguồn nội dung khoa học

---

*Sản xuất thật cần đối chiếu lại số liệu với paper gốc và xin phép sử dụng footage từ các project được trích dẫn (xem mục Phụ lục trong kịch bản).*
