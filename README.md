# Trí tuệ nằm trong cơ thể — Tập 1

Hiện thực hoá Manim cho **toàn bộ Tập 1 — *"Cá chết vẫn biết bơi"*** trong series video phong cách 3Blue1Brown đặt câu hỏi *"trong một sinh vật thông minh, trí tuệ nằm ở đâu — trong não, hay trong cả cơ thể?"*

Repo gồm **8 scene**, ứng với 8 phân cảnh trong kịch bản:

| File | Scene | Phút | Nội dung |
|------|-------|------|----------|
| `scene0.py` | 0 — Cold open | 0:00 – 0:35 | Cá chết "bơi" trong dòng nước |
| `scene1.py` | 1 — Câu hỏi chính | 0:35 – 2:00 | Brain vs body, split θ_brain / θ_body |
| `scene2.py` | 2 — Đa dạng mắt sinh học | 2:00 – 5:30 | 6 cards: mèo/dê, đại bàng, sò điệp, cá hang, tarsier, bướm |
| `scene3.py` | 3 — Cú twist sọc ngựa vằn | 5:30 – 7:30 | Trực giác sai, câu trả lời thật là muỗi |
| `scene4.py` | 4 — Định nghĩa toán học | 7:30 – 11:00 | Design space, U(θ), pipeline, 2 nhánh tối ưu |
| `scene5.py` | 5 — Carl Sims 1994 | 11:00 – 13:00 | Voxel creatures + transform sang cá |
| `scene6.py` | 6 — Setup tập 2 | 13:00 – 17:00 | Pixel reduction 128 → 4 → cliffhanger |
| `scene7.py` | 7 — Outro & credits | 17:00 – cuối | Thanks to + Patreon + logo channel |

Tổng độ dài visual: ~17–18 phút (trước khi chèn voiceover/giãn nhịp).

---

## Yêu cầu

- **Python 3.9+** (khuyến nghị 3.10 hoặc 3.11)
- **Manim Community Edition** ≥ 0.18
- **FFmpeg**
- **Font Montserrat** (cho text tiếng Việt) — xem mục dưới
- *Không cần LaTeX* — file dùng `MarkupText` cho subscript thay vì `MathTex`

## Cài đặt

### macOS

```bash
brew install py3cairo ffmpeg pango pkg-config scipy
brew install --cask font-montserrat
pip install manim
```

### Ubuntu / WSL

```bash
sudo apt update
sudo apt install libcairo2-dev libpango1.0-dev ffmpeg python3-pip fonts-montserrat
pip install manim
```

### Windows (PowerShell)

```powershell
pip install manim
# Font Montserrat: tải từ https://fonts.google.com/specimen/Montserrat → cài cả family
```

Nếu Windows lỗi cairo/pango, dùng WSL cho nhẹ hoặc cài MSYS2 theo [hướng dẫn chính thức](https://docs.manim.community/en/stable/installation/windows.html).

### Kiểm tra cài đặt

```bash
manim --version           # phải in Manim Community v0.x.y
fc-list | grep Montserrat # Linux/macOS — phải có ít nhất Regular + Bold
```

---

## Font tiếng Việt — quy tắc

Repo dùng **Montserrat** cho text tiếng Việt vì nó có Vietnamese subset đầy đủ (ă/â/ê/ô/ơ/ư + dấu thanh + đ). Text tiếng Anh giữ font mặc định của Manim (Sans) để đồng nhất với style toán học của 3Blue1Brown.

Trong code, dùng helper từ `common.py`:

```python
from common import vn, vn_markup

# Text tiếng Việt → dùng vn() (tự áp Montserrat)
title = vn("Trí tuệ nằm trong cơ thể", font_size=44, weight=BOLD)

# Text tiếng Anh → dùng Text() bình thường (font mặc định)
header = Text("BRAIN", font_size=28, weight=BOLD)

# Markup tiếng Việt với inline color span
caption = vn_markup(
    'mắt  <span foreground="#FBBF24">≈</span>  não',
    font_size=40,
)

# MarkupText tiếng Anh thuần (subscript, công thức) → MarkupText() bình thường
formula = MarkupText('θ<sub>brain</sub>', font_size=44)
```

**Quy tắc đơn giản:** câu/từ có dấu tiếng Việt → `vn()`. Còn lại → `Text()` hoặc `MarkupText()` mặc định.

Nếu hệ thống chưa cài Montserrat, Pango sẽ fallback sang DejaVu Sans — vẫn render được, chỉ không đẹp bằng và có thể có khoảng cách dấu hơi lệch.

---

## Cách chạy

`cd` vào thư mục chứa các file, đặt cả 8 file scene + `common.py` cùng một chỗ:

```bash
# Render từng scene riêng
manim -pql scene0.py Scene0ColdOpen
manim -pql scene1.py Scene1MainQuestion
manim -pql scene2.py Scene2EyeDiversity
manim -pql scene3.py Scene3ZebraTwist
manim -pql scene4.py Scene4MathFormulation
manim -pql scene5.py Scene5CarlSims
manim -pql scene6.py Scene6Cliffhanger
manim -pql scene7.py Scene7Outro
```

**Render tất cả + ghép thành 1 file final:**

```bash
# 1. Render hết với chất lượng cao
for s in 0 1 2 3 4 5 6 7; do
  manim -qh scene${s}.py
done

# 2. Ghép bằng ffmpeg (yêu cầu list.txt liệt kê đường dẫn output)
cd media/videos
ls -1 scene*/1080p60/*.mp4 | sort | sed "s/^/file '/;s/$/'/" > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy tap1_full.mp4
```

### Giải nghĩa các cờ Manim

| Cờ | Ý nghĩa |
|----|---------|
| `-p` | Tự động phát video sau khi render xong |
| `-q{l,m,h,k}` | Quality: low (480p) / medium (720p) / high (1080p) / 4K |
| `-s` | Chỉ render **frame cuối** ra PNG (cực nhanh, dùng khi đang sửa layout) |
| `-n start,end` | Chỉ render từ animation thứ `start` đến `end` |
| `--prerun` | Estimate thời gian render và bắt lỗi sớm (theo workflow của Grant) |

Output mặc định nằm tại:

```
media/videos/<scene_name>/<resolution>/<ClassName>.mp4
```

---

## Workflow lặp nhanh (theo Grant Sanderson)

Khi đang tinker visual, đừng render full mỗi lần. Hai mẹo lớn:

**1. Render frame cuối ra ảnh (kiểm tra layout):**

```bash
manim -sql scene2.py Scene2EyeDiversity
```

**2. Chỉ render một đoạn:**

Đếm số `self.play(...)` trước đoạn cần xem (gọi đó là `N`), rồi:

```bash
manim -pql scene2.py Scene2EyeDiversity -n N,N+5
```

Ví dụ chỉ muốn xem Card 4 trong Scene 2 — đếm xem có ~38 `self.play` trước nó, chạy `-n 38,55`. Nhanh gấp 5–10 lần render full.

---

## Cấu trúc repo

```
.
├── common.py           # Bảng màu + font + helpers (create_fish, create_neural_net, vn, vn_markup)
├── scene0.py           # Cold open: cá chết + camera pull-back
├── scene1.py           # Câu hỏi chính: brain/body split
├── scene2.py           # 6 cards mắt sinh học + recap grid
├── scene3.py           # Sọc ngựa vằn → muỗi
├── scene4.py           # Math: design space, U(θ), pipeline, branches
├── scene5.py           # Carl Sims 1994 voxel creatures
├── scene6.py           # Pixel reduction 128 → 4 → cliffhanger
├── scene7.py           # Credits + Patreon + outro logo
└── README.md
```

**`common.py` là trái tim của repo** — tất cả scene import từ đây để chia sẻ palette, font, và helpers.

---

## Bảng màu (3Blue1Brown style)

Định nghĩa trong `common.py`:

| Tên | Hex | Dùng cho |
|-----|-----|----------|
| `BG_COLOR` | `#1C1C1C` | Nền |
| `BLUE_3B1B` | `#3B82F6` | Body, NN nodes (chủ đạo) |
| `YELLOW_3B1B` | `#FBBF24` | Highlight, công thức, accent |
| `RED_BRAIN` | `#EF4444` | Brain region, "sai", danger |
| `GREEN_3B1B` | `#10B981` | Optimal, success |
| `PURPLE_3B1B` | `#A78BFA` | Learning-based, neural |
| `ORANGE_3B1B` | `#F97316` | Predator (mèo, sư tử) |
| `PINK_3B1B` | `#EC4899` | Target, cánh bướm dưới |
| `GRAY_LIGHT` | `#E5E7EB` | Text chính, đường viền |
| `GRAY_MID` | `#9CA3AF` | Mid-tone (blur effect) |
| `GRAY_DIM` | `#6B7280` | Edges NN inactive, captions |
| `GRAY_DARKER` | `#374151` | Grid lines |

---

## Helpers tái sử dụng (trong `common.py`)

```python
# Cá schematic — không cần SVG ngoài
fish = create_fish(color=BLUE_3B1B, stroke_width=3)
# Trả về VGroup: [body, tail, eye, fin]

# Mạng nơ-ron MLP
nn_group, edges, layers = create_neural_net(
    layer_sizes=[3, 5, 5, 2],
    radius=0.13, h_buff=0.55, v_buff=0.32,
    node_color=BLUE_3B1B,
)

# Title card chuẩn
card = make_title_card("Tiêu đề", subtitle="Phụ đề", is_vietnamese=True)

# Text VN với Montserrat
label = vn("Não", font_size=24, color=RED_BRAIN, weight=BOLD)

# MarkupText VN với Montserrat
eq = vn_markup('mắt  <span foreground="#FBBF24">≈</span>  não', font_size=40)
```

---

## Production notes (khi xuất bản)

Khi làm bản thật, lưu ý vài điểm trong từng scene:

- **Scene 0** — bản schematic chỉ là stand-in. Bản hoàn thiện nên dùng stock footage cá thật và `Transform` sang phiên bản schematic.
- **Scene 2 Card 3** — vỏ sò điệp 50 dot là đại diện cho ~200 mắt thật. Tăng dot count nếu render full HD.
- **Scene 3 — sư tử/bò/muỗi** — schematic minimal. Có thể thay bằng illustration hoặc footage thật.
- **Scene 5** — voxel creatures là 2D silhouette. Bản thật của Sims là 3D, có thể thay bằng video clip gốc của Sims 1994 (xin phép trước).
- **Scene 6** — pixel reduction tối đa thực render là **64×64** (vì Manim render 128² = 16k square sẽ rất chậm). Caption ghi "~128 px" để bù.
- **Scene 7 — credits** — tên các nhà nghiên cứu (Amir Zamir, Andre Cazenave Souto, Andy Spielberg, Sönke Johnsen) là *placeholder*. **Phải kiểm tra lại tên thật từ tutorial gốc** trước khi public, và cân nhắc xin phép sử dụng tên + nội dung.

---

## Troubleshooting

**`No module named 'common'`** — đặt file scene cùng thư mục với `common.py` rồi chạy. Nếu để khác thư mục, thêm `PYTHONPATH=/đường/dẫn/đến/common manim ...`

**`No module named 'manim'`** — chưa cài hoặc cài nhầm Python environment. Chạy `which python` và `which pip` để chắc.

**`OSError: cannot load Pango` / `cairo not found`** — thiếu system library. Quay lại bước cài đặt OS tương ứng.

**Font Montserrat không hiện, ký tự tiếng Việt vỡ** — chạy `fc-list | grep -i montserrat`. Nếu không có, cài lại như mục "Font tiếng Việt" ở trên. Có thể cần chạy `fc-cache -fv` (Linux) sau khi cài font.

**Render rất chậm với Scene 2 hoặc Scene 6** — hai scene này có nhiều object cùng lúc. Dùng `-ql` thay vì `-qh` để preview, chỉ render `-qh` khi đã chắc layout.

**Scene 6 transition giữa các pixel grid trông kỳ** — đây là vấn đề `Transform` giữa 2 VGroup khác kích thước. Nếu khó chịu, đổi `Transform(view, new_view)` thành `FadeOut(view) + FadeIn(new_view)` trong vòng lặp.

**Muốn dùng `MathTex` (LaTeX) cho công thức đẹp hơn** — cài LaTeX (`texlive-full` trên Linux, MacTeX trên macOS, MiKTeX trên Windows), rồi đổi `MarkupText` thành `MathTex` với cú pháp `r"\theta_{\text{brain}}"`.

---

## Tham khảo

- Kịch bản gốc: `3blue1brown_script.md`
- [Manim Community docs](https://docs.manim.community/)
- [3Blue1Brown channel](https://www.youtube.com/@3blue1brown) — Grant Sanderson
- Tutorial gốc *"Computational Design of Diverse Morphologies and Sensors for Vision and Robotics"*

---

*Sản xuất thật cần đối chiếu lại số liệu khoa học với paper gốc và xin phép sử dụng footage từ các project được trích dẫn (xem mục Production notes ở trên).*
