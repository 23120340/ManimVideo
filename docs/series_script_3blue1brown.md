# Trí tuệ nằm trong cơ thể

> Kịch bản video phong cách **3Blue1Brown**, tổng hợp từ tutorial *"Computational Design of Diverse Morphologies and Sensors for Vision and Robotics"* và workflow Manim của Grant Sanderson.

---

## Mục lục

- [0. Tổng quan & chiến lược biên kịch](#0-tổng-quan--chiến-lược-biên-kịch)
- [1. Tập 1 — "Cá chết vẫn biết bơi" (kịch bản chi tiết)](#1-tập-1--cá-chết-vẫn-biết-bơi-kịch-bản-chi-tiết)
- [2. Tập 2 — "Thấy thế giới bằng 4 pixel" (dàn ý)](#2-tập-2--thấy-thế-giới-bằng-4-pixel-dàn-ý)
- [3. Tập 3 — "Thiết kế cơ thể bằng gradient descent" (dàn ý)](#3-tập-3--thiết-kế-cơ-thể-bằng-gradient-descent-dàn-ý)
- [4. Sổ tay Manim cho series này](#4-sổ-tay-manim-cho-series-này)
- [5. Visual asset checklist](#5-visual-asset-checklist)

---

## 0. Tổng quan & chiến lược biên kịch

### 0.1. Vấn đề: tài liệu gốc dài 3 tiếng, có 4 diễn giả

Talk gốc bao trùm hai mảng lớn:

- **Vision / Perception** (Amir, Andre, Sönke): hình thái và sensor cho thị giác — sự đa dạng của mắt sinh học, photoreceptor tối giản, thị giác dưới biển sâu.
- **Robotics / Co-design** (Andy): differentiable simulation, evolutionary search, generative design (DiffuseBot), fabrication.

Nén tất cả vào 1 video sẽ làm mất đi cái mà 3Blue1Brown hay làm nhất: **đào sâu một ý tưởng đến chỗ "aha"**. Vì vậy mình tách thành 3 tập, mỗi tập có một câu hỏi trung tâm và một khoảnh khắc bất ngờ riêng.

### 0.2. Sợi chỉ xuyên suốt cả series

Một câu hỏi duy nhất, kéo dài 3 tập:

> *"Trong một sinh vật thông minh, trí tuệ nằm ở đâu — trong não, hay trong cả cơ thể?"*

| Tập | Câu hỏi | Khoảnh khắc "aha" |
|-----|---------|---------------------|
| 1 | Trí tuệ có thật sự nằm trong não không? | Sọc ngựa vằn KHÔNG phải để ngụy trang — nó giúp ruồi hút máu khó hạ cánh. |
| 2 | Cần bao nhiêu pixel để "thấy"? | Một robot 4 pixel có thể điều hướng tốt như camera 128×128, và sensor tối ưu lại nhìn xuống đất. |
| 3 | Có thể "đào tạo" cơ thể như đào tạo não không? | Đạo hàm chạy xuyên qua mô phỏng vật lý — và một con robot "tiến hoá" trong 6 giây. |

### 0.3. Quy ước phong cách 3Blue1Brown

Series cần tuân thủ:

- **Bảng đen xanh đậm** (`#1C1C1C` background, `#3B82F6` blue, `#FBBF24` yellow cho highlight).
- **Font:** CMU Serif cho công thức, Inter / Helvetica cho text.
- **Không nói "let's", "we'll".** Voiceover ở thì hiện tại, kiểu kể chuyện.
- **Mỗi đoạn dài ~30-90 giây kết thúc bằng một câu hỏi mở** dẫn sang đoạn tiếp.
- **Hình ảnh đi trước lời nói.** Khi chuyển ý, để hình động chạy 1-2 giây trước khi voiceover vào.
- **Easing mặc định là `smooth` (cubic bezier).** Chỉ dùng `linear` khi muốn nhấn cảm giác máy móc / không sống.

---

## 1. Tập 1 — "Cá chết vẫn biết bơi" (kịch bản chi tiết)

**Thời lượng dự kiến:** 18-22 phút.
**Mục tiêu nhận thức:** Khán giả hiểu rằng "morphology" (cấu trúc cơ thể và bộ phận cảm thụ) là một dạng tham số có thể tối ưu được, ngang hàng với tham số mạng nơ-ron.

---

### Scene 0 — Cold open: Con cá chết (0:00 – 0:35)

**Visual:**
- Mở đầu: clip thật / phỏng theo, một con cá đang "bơi" trong dòng nước chảy. Cảnh quay từ bên hông.
- Sau 5 giây, camera lùi ra. Lộ ra một sợi dây kéo chiếc đầu cá về phía trước, và dòng nước chảy ngược. **Con cá đã chết.**
- Cú zoom out này nên dùng `self.play(self.frame.animate.scale(2.5), run_time=2)` để mượt.

**Voiceover (VO):**
> Đây là một con cá đang bơi.
> *(2 giây pause, để khán giả quan sát)*
> Nhưng có một chi tiết khiến đoạn video này trở nên kỳ lạ:
> *(camera lùi)*
> Con cá đã chết. Một sợi dây giữ đầu nó cố định, và dòng nước đang chảy. Tất cả những gì bạn thấy — cái đuôi quẫy, cơ thể uốn lượn — chỉ là tương tác giữa một xác cá và dòng nước.
> Vậy mà nó vẫn bơi.

**Manim note:**
- Cảnh thật khó tái hiện 100% bằng Manim. Đề xuất: dùng `ImageMobject` cho video thật ở cold open, sau đó *Transform* sang phiên bản schematic (đường viền cá + spline cho dây + trường vector dòng nước).
- Cú lộ "dây" có thể làm bằng `Create(rope)` với `rate_func=rush_into`.

---

### Scene 1 — Câu hỏi chính (0:35 – 2:00)

**Visual:**
- Schematic cá chia làm hai phần: **đầu** highlight đỏ (gắn nhãn "BRAIN"), **thân** highlight xanh ("BODY").
- Phần đầu mờ dần đi (`FadeOut(brain_glow)`) — não đã chết, không còn hoạt động.
- Phần thân vẫn quẫy theo dòng nước.

**VO:**
> Khi nói về trí tuệ nhân tạo, ta thường mặc định: trí tuệ nằm trong "não" — trong mạng nơ-ron, trong các tham số được học. Cơ thể chỉ là phần cứng để chạy nó.
> Nhưng con cá này không có não nữa. Nếu nó vẫn "biết" bơi, thì phần kiến thức đó đang nằm ở đâu?

**Visual transition:**
- Hai pane song song xuất hiện. Trái: `θ_brain` — một mạng nơ-ron nhỏ với các trọng số nhấp nháy (animation: thay đổi nhanh). Phải: `θ_body` — đường viền cơ thể cá với các điểm vật lý (độ cứng, độ đàn hồi, hình dạng).
- Trên `θ_brain`: nhãn "fast, flexible".
- Trên `θ_body`: nhãn "slow, rigid".

**VO (tiếp):**
> Cả hai bên đều là **tham số**. Nhưng chúng khác nhau ở tốc độ thay đổi.
> Não thay đổi mỗi giây — nó học từ phản hồi của môi trường. Cơ thể thay đổi qua hàng triệu năm tiến hoá. Một bên mềm dẻo, một bên cứng nhắc.
> Và lâu nay, hầu hết công sức nghiên cứu AI dồn vào bên trái.

**Manim:**
```python
brain = NeuralNetwork(layer_sizes=[4, 6, 6, 2])
body = SVGMobject("fish_outline.svg").set_color(BLUE)
# Cùng dùng VGroup để ghép thành "agent"
agent = VGroup(brain, body).arrange(RIGHT, buff=2)
```

---

### Scene 2 — Sự đa dạng kinh ngạc của mắt sinh học (2:00 – 5:30)

Đây là phần "wonder" — để khán giả ngạc nhiên trước khi vào toán học.

**Visual structure:** 6 thẻ (cards) lần lượt trượt vào, mỗi thẻ ~25 giây. Layout dạng grid 2×3 cuối cùng.

**Card 1 — Mắt mèo vs mắt dê**
- Hai mắt cận cảnh side-by-side.
- Mèo: đồng tử dọc.
- Dê / cừu: đồng tử ngang, kéo dài tới gần 180°.
- Animation: vẽ field of view như hai cánh quạt mở rộng. Mèo có cánh quạt hẹp + sâu (depth perception). Dê có cánh quạt cực rộng (cảnh giác).

> VO: "Hình dạng đồng tử không phải ngẫu nhiên. Đồng tử dọc cho phép mèo — kẻ săn mồi phục kích — định vị độ sâu chính xác. Đồng tử ngang cho phép con mồi quan sát gần hết 360 độ."

**Card 2 — Đại bàng có 2 fovea**
- Vẽ võng mạc người (1 hố vàng) → võng mạc đại bàng (2 hố vàng).
- Animation: hai tia "high-res" chiếu ra từ mắt đại bàng, một nhìn thẳng, một nhìn 45°.
- Hệ quả hành vi: đại bàng săn theo đường xoắn ốc — `ParametricFunction` vẽ quỹ đạo logarithmic spiral.
> VO: "Mắt người có một điểm nhìn sắc nét nhất — gọi là hố vàng. Đại bàng có **hai**. Một nhìn thẳng phía trước. Một nhìn chếch 45 độ sang bên. Điều đó có nghĩa là gì trong thực tế? Khi săn mồi, đại bàng bay theo đường xoắn ốc — không phải vì ngẫu nhiên, mà vì đường đó giữ con mồi cố định trên hố vàng thứ hai trong suốt quá trình lao xuống. Cơ thể đã **mã hoá chiến thuật săn mồi** vào chính cấu trúc của mắt."

**Card 3 — Sò điệp có 200 con mắt**
- Vẽ vỏ sò với chấm xanh nhỏ rải khắp viền.
- Zoom vào một chấm: lộ ra một con mắt nhỏ với *gương* bên trong (không phải thấu kính!).
- Cú twist: "Thay vì gom photoreceptor lại thành một retina dày đặc, sò điệp **phân tán** chúng thành 200 con mắt độc lập."

> VO: "Sò điệp có khoảng 200 con mắt, rải dọc viền vỏ. Nếu bạn nghĩ đó là 200 con mắt 'bình thường' — sai. Bên trong mỗi con mắt không phải thấu kính, mà là **gương**. Một gương parabol hội tụ ánh sáng về phía sau, ngược hoàn toàn với cách mắt người hoạt động. Và thay vì dồn toàn bộ độ phân giải vào một điểm, sò điệp phân tán nó ra 200 sensor độc lập. Mỗi sensor tệ hơn mắt người nhiều lần — nhưng tổng thể, chúng bao phủ một trường nhìn mà không có con mắt đơn lẻ nào đạt được."

**Card 4 — Cá hang động (cave fish)**
- Animation tiến hoá: con cá ban đầu có mắt to, qua các thế hệ mắt teo dần đi rồi biến mất, da phủ kín.
- VO: "Tại sao? Vì trong hang tối, mắt là một thứ tốn năng lượng vô ích. Tiến hoá đã 'xoá' nó — nhưng anh em họ trên mặt đất của nó vẫn có mắt."

**Card 5 — Tarsier**
- So sánh tỉ lệ: mắt tarsier vs não tarsier vs mắt người vs não người.
- VO: "Mắt của con tarsier này lớn bằng cả não nó. Đó là cái giá phải trả để săn mồi trong đêm."

**Card 6 — Bướm**
- Cảnh: hai con bướm bay cách nhau 2m.
- Hiển thị "góc nhìn của con bướm": ảnh blur thê thảm, đối phương chỉ là một đốm mờ.
- VO: "Con bướm này không thể thấy được con bướm kia. Hoa văn rực rỡ trên cánh nó — nó cũng không thấy được luôn. Hoa văn ấy không dành cho đồng loại. Nó dành cho **chim**, kẻ săn mồi nhìn rõ hơn nó nhiều."

**VO chốt scene:**
> Sáu loài. Sáu chiến lược thị giác hoàn toàn khác nhau. Và đây mới là phần dễ thấy — phần cấu trúc cơ học bên ngoài.

**Manim note:**
Dùng `Transform` để chuyển từ card này sang card kia, không `FadeOut + FadeIn`. Mỗi card cuối nên có một con số highlight to (200 mắt, 2 fovea, v.v.) để dễ ghi nhớ.

---

### Scene 3 — Cú twist: Sọc ngựa vằn (5:30 – 7:30)

Đây là khoảnh khắc "aha" của tập này.

**Visual:**
- Hình con ngựa vằn đứng giữa thảo nguyên.
- Pop-up câu hỏi: "Vì sao ngựa vằn có sọc?"
- Hiện hai đáp án phổ biến với icon: 🦁 ("Camouflage cho sư tử") và 🐎 ("Trông như đàn lớn hơn").

**VO:**
> Câu trả lời "trực giác" gần như ai cũng đoán được: sọc để ngụy trang khỏi sư tử, hoặc để cả đàn nhìn lớn hơn. Hợp lý, đúng không?

**Visual:**
- Animation: chuyển sang góc nhìn của sư tử. Hiển thị độ phân giải thị giác sư tử so với người (~1/4). Ngựa vằn từ xa **không hề nhìn ra sọc** — nó chỉ là một khối xám nhập nhoè.

**VO:**
> Trừ một chi tiết. Sư tử không có thị giác đủ tốt để thấy được sọc từ khoảng cách săn. Với chúng, một con ngựa vằn và một con lừa nhìn giống hệt nhau.

**Visual:**
- Zoom vào một con ruồi hút máu / mòng cố đậu trên da ngựa vằn. Khi nó gặp vùng có sọc, nó *trượt đi* (mất định hướng do tương phản cao).
- Cú lật bài: cảnh nông dân sơn hoạ tiết sọc lên... bò.

**VO:**
> Câu trả lời thật: sọc giúp **ruồi hút máu khó hạ cánh**. Các thí nghiệm với ngựa, ngựa vằn và bò sơn sọc cho thấy hoa văn tương phản cao làm giảm số lần côn trùng hút máu hạ cánh.

**VO chốt:**
> Bài học: khi ta đoán "trí tuệ thiết kế" theo trực giác con người, ta sai. Bởi cơ thể không tiến hoá để **chúng ta** thấy đẹp — nó tiến hoá để giải bài toán mà nó đang đối mặt.

**Manim:**
- Cú "trượt" của côn trùng trên sọc: dùng `UpdateFromAlphaFunc` với hàm noise để mô phỏng disorientation.
- Title card "ANSWER: BITING FLIES" xuất hiện với `Write` animation, giữ 2 giây, fade.

---

### Scene 4 — Định nghĩa toán học của bài toán (7:30 – 11:00)

Bây giờ chuyển từ wonder sang math. Đây là phần trung tâm 3Blue1Brown.

**Visual:**
- Hai không gian chiếu side-by-side.
- Trái: **Design space** — mỗi điểm là một thiết kế cơ thể (parametrized: kích thước mắt, vị trí, trường nhìn, ...).
- Phải: **Performance space** — mỗi điểm là một số (utility, ví dụ: "tỉ lệ sống sót").

**VO:**
> Ở góc nhìn toán học, mọi thứ có thể được gói gọn như sau. Tồn tại một **không gian thiết kế** θ — mỗi điểm trong đó là một cách dựng cơ thể. Tồn tại một **hàm utility** U(θ) — đo xem thiết kế đó "tốt" tới đâu cho một nhiệm vụ.

**Visual:**
- Vẽ một đường cong U(θ) trên không gian 1D (cho dễ hình dung). Đỉnh = thiết kế tối ưu.
- Animation: con trỏ trượt trên không gian θ, đường cong U trượt theo, sáng lên ở đỉnh.

**VO:**
> Câu hỏi tối ưu hoá quen thuộc:
> $$\theta^* = \arg\max_\theta \; U(\theta)$$
> Nhưng có một vấn đề. Để biết U(θ), ta phải **mô phỏng** cơ thể đó trong môi trường, gắn vào nó một controller, để nó chạy nhiệm vụ. U không có công thức đóng.

**Visual:**
- Vẽ pipeline: θ (design) → simulator/world → controller → reward → U(θ).
- Mỗi node nhấp nháy khi giá trị "chảy" qua.

**VO:**
> Đây là chỗ phân nhánh thành hai trường phái:

**Visual:** Chia màn hình.
- Trái: Phương trình Newton, sơ đồ cơ thể cứng + lò xo. Nhãn: **"Physics-based"**.
  > "Dùng tri thức vật lý để viết một mô hình hành vi, rồi tối ưu trên đó."
- Phải: Một mạng nơ-ron mô phỏng não → behavior. Nhãn: **"Learning-based"**.
  > "Khi ta không có công thức cho 'tri giác → hành vi', học từ dữ liệu."

**VO:**
> Tutorial mà tập video này dựa trên có một quan sát thú vị: phần thiết kế cơ học của robot thường đi theo nhánh trái — vì ta hiểu vật lý. Còn phần thiết kế **hệ thị giác** thường đi theo nhánh phải — vì 'mắt → hành vi' không có công thức gọn gàng.

---

### Scene 5 — Carl Sims: 30 năm trước (11:00 – 13:00)

**Visual:**
- Title card: "1994" — chữ kiểu retro.
- Clip evolved virtual creatures kiểu Carl Sims (có thể tự render bằng Manim với các "voxel creatures" đơn giản).
- Quần thể 8 "sinh vật" boxel thử bơi / nhảy / leo. Một số ngã, một số tiến lên.

**VO:**
> Năm 1994, Karl Sims đã làm điều này: cho một thuật toán tiến hoá tự lắp ráp các khối hộp thành sinh vật. Mục tiêu: đi xa nhất. Không có thiết kế thủ công. Chỉ có voxels và một utility function.
> Kết quả ra những "sinh vật" lạ lùng — đôi khi vô lý — nhưng rõ ràng đang **giải bài toán** mà ta đặt ra.

**Visual transition:**
- Một con sinh vật của Sims biến hình mượt thành con cá chết ban đầu (Transform).

**VO:**
> Cùng một ý tưởng: **để máy tính thiết kế cơ thể.** Khác biệt giờ là 30 năm sau — ta có nhiều compute hơn, nhiều dữ liệu hơn, và những công cụ toán học mới. Đó là lý do ý tưởng này đang sống lại.

**Manim:**
- Voxel creatures: dựng bằng `Cube` lồng vào `VGroup`. Mỗi update step, ngẫu nhiên thêm/xoá block + áp gravity bằng physics đơn giản.
- Hoặc đơn giản hoá: chỉ vẽ silhouette 2D, dùng `Wiggle` cho animation.

---

### Scene 6 — Setup cho Tập 2 (13:00 – 17:00)

**Visual:**
- Quay lại sơ đồ θ_brain | θ_body từ Scene 1.
- θ_body từ một khối duy nhất → tách thành nhiều thành phần: **shape**, **eye position**, **eye resolution**, **field of view**, **sensor count**.

**VO:**
> Vậy ta tối ưu cái gì? Câu hỏi đầu tiên là: **mắt**.
> Ngày nay, hầu hết hệ thống thị giác máy tính dùng cùng một công thức: một camera có độ phân giải cao đặt ở vị trí "hợp lý theo trực giác con người". Nhưng tự nhiên không làm vậy. Tự nhiên có sò điệp với 200 con mắt. Có cá hang động không mắt. Có bướm thấy mọi thứ mờ tịt.
> Nếu **trực giác** đã sai trong vụ ngựa vằn, thì có lẽ trực giác của ta về camera cũng đang sai.

**Visual cliffhanger:**
- Một con robot nhỏ, ban đầu có camera 128×128 pixel.
- Hạ pixel xuống: 64×64, 32×32, 16×16, 8×8, 4×4, **2×2**, **1**.
- Mỗi bước, hỏi ở dưới: "Liệu nó còn thấy được mục tiêu không?"
- Dừng ở 4 pixel. Câu hỏi cuối cùng floating trên màn:

> **"Một robot 4 pixel có thể điều hướng trong nhà không?"**

**VO:**
> Đây là chủ đề của tập tiếp theo. Hẹn gặp lại.

**End card:** logo channel + "Ep. 2: Seeing the world with 4 pixels" lờ mờ hiện ra.

**Manim:**
- Pixel reduction: dùng `pixel_array_dtype` hoặc đơn giản là `ImageMobject` rồi `apply_function` để pixelate dần.

---

### Scene 7 — Outro & ghi chú nhân vật (17:00 – cuối)

**Visual:**
- Ảnh slide cuối kiểu 3b1b: chữ "Thanks to" + danh sách nguồn gốc tutorial (Amir Zamir, Andre, Sönke Johnsen, Andy Spielberg — kiểm tra lại tên).
- Support note / link tutorial gốc.

---

## 2. Tập 2 — "Thấy thế giới bằng 4 pixel" (dàn ý)

**Mục tiêu nhận thức:** Khán giả hiểu bi-level optimization, và tin được rằng số chiều của input không phải là yếu tố quyết định khả năng.

### Cấu trúc 6 phần

**Phần 1: Recap & câu hỏi (0:00 – 1:30)**
- Hiển thị lại "robot 4 pixel" cliffhanger.
- Câu hỏi: với 4 con số RGB cập nhật mỗi 1/30 giây, có đủ thông tin để né va chạm và tìm mục tiêu không?

**Phần 2: Photoreceptor là gì? (1:30 – 4:00)**
- Vẽ một photoreceptor như "trung bình theo không gian" của một mảng pixel.
- Visual: lấy một frame từ camera, chia ô 8×8, mỗi ô tính trung bình → đó là tín hiệu của 64 photoreceptor.
- Tham số thiết kế: vị trí, hướng, field of view (3 spheres + 1 cone).

**Phần 3: Bài toán điều hướng (4:00 – 7:00)**
- Giới thiệu point-goal navigation và target navigation.
- Animation: top-down map, robot xuất phát từ pin, mục tiêu là sao.
- Đường đi của 3 agent overlay: blind (loạn xạ quanh start), camera (đường thẳng), photoreceptor (gần camera).

**Phần 4: Bi-level optimization (7:00 – 11:00)**

Đây là phần "math heart" của tập này.

- Vẽ vòng lặp ngoài: cập nhật θ (design) — vòng lặp trong: cập nhật φ (policy).
- Naive: outer = Bayesian opt, mỗi iteration tốn 1-2 ngày. Quá chậm.
- Trick mà Andre dùng: gộp design action vào cùng một rollout với control action. Giờ chỉ cần 1 vòng lặp.
- Công thức:
  $$\nabla_\theta \mathbb{E}_\tau[R(\tau; \theta, \phi)] \quad \text{và} \quad \nabla_\phi \mathbb{E}_\tau[R(\tau; \theta, \phi)] \quad \text{cùng một backward pass.}$$

**Phần 5: Khoảnh khắc bất ngờ (11:00 – 14:00)**
- Vẽ thiết kế tối ưu cho point-goal navigation.
- Một photoreceptor chĩa **xuống đất**. Pause. Voiceover: "Vì sao?"
- Giải thích: agent đã biết toạ độ mục tiêu. Việc duy nhất nó cần là né tường. Sensor nhìn xuống là cách hiệu quả nhất.
- Khán giả: "À, hợp lý — nhưng tôi sẽ không bao giờ tự nghĩ ra."
- Dẫn câu khảo sát: con người chọn thiết kế trực giác → kết quả tệ một cách đáng ngạc nhiên.

**Phần 6: Sim-to-real (14:00 – 17:00)**
- Clip TurtleBot thật trong phòng, cố tìm bóng hồng.
- Voiceover: tất cả train trong simulator. Zero real-world fine-tuning. Vẫn chạy.

**Phần 7: Cliffhanger (17:00 – 18:00)**
- "Nếu mắt có thể tối ưu được, thì cơ thể thì sao? Lò xo, khớp, độ cứng vật liệu? Đó là tập sau."

---

## 3. Tập 3 — "Thiết kế cơ thể bằng gradient descent" (dàn ý)

**Mục tiêu nhận thức:** Differentiable simulation là gì, vì sao nó cho phép "gradient descent qua vật lý", và DiffuseBot dùng diffusion model để khám phá không gian thiết kế.

### Cấu trúc 5 phần

**Phần 1: Hook — robot tự học đi trong 6 giây (0:00 – 1:00)**
- Mở đầu: clip "soft robot" tự học đi trong 12 iterations, mỗi iteration ~0.5s.
- Voiceover: "RL cần hàng chục nghìn rollouts. Cái này: 12. Vì sao?"

**Phần 2: Differentiable simulation (1:00 – 6:00)**
- Coi simulator như một mạng nơ-ron khổng lồ.
- Visual: pipeline forward — state₀ → physics step → state₁ → ... → state_T → reward.
- Backward: gradient chạy ngược qua chính các bước vật lý.
- Đề cập đến giá phải trả: bộ nhớ. Cần checkpoint mỗi step. Soft robot cần time step ~7μs → 1 triệu bước/giây mô phỏng.
- Implicit integration giảm bộ nhớ, đổi lại mất chính xác.

**Phần 3: Co-design (6:00 – 11:00)**
- Mở rộng: gradient không chỉ chảy về controller (φ), mà cả về **design parameters** (θ).
- Cùng một backward pass cập nhật cả "não" và "cơ thể".
- Visual: robot 4 chân tự tìm độ cứng của vật liệu ở từng vùng cơ thể. Vùng đỏ = cứng (chân đẩy), vùng xanh = mềm (vùng tiếp đất).
- Ý sâu sắc: số lượng tham số tăng nhưng performance không giảm — "lời nguyền chiều cao" không xảy ra ở đây.

**Phần 4: Generative design (11:00 – 16:00)**
- "Cứ hỏi ChatGPT thiết kế robot hái dâu đi" → kết quả buồn cười (cánh tay khoá cứng, xe có bánh nằm ngang).
- Bài học: LLM thiếu **physical intelligence** — không có simulator để kiểm tra.
- DiffuseBot: dùng diffusion model đề xuất hình học, nhưng **conditioning** không phải bằng text hay image — mà bằng **gradient từ simulator**.
- Visual: noise → robot. Mỗi denoising step được "đẩy" bởi simulation gradient.

**Phần 5: Ngõ ra & câu hỏi mở (16:00 – 19:00)**
- Sim-to-real gap là vấn đề lớn nhất còn lại.
- Tương lai: foundation model cho design? Có thể, nhưng cần dữ liệu fabrication thực tế.
- Quay lại con cá chết. "Tự nhiên đã làm điều này 4 tỉ năm. Ta vừa mới bắt đầu."
- End: "Trí tuệ không nằm trong não. Nó nằm trong **toàn bộ vòng lặp** — não, cơ thể, và môi trường tương tác."

---

## 4. Sổ tay Manim cho series này

> Phần này tổng hợp các kỹ thuật Grant Sanderson chia sẻ trong file thứ hai, áp dụng vào series.

### 4.1. Workflow đề xuất (theo Grant)

1. **Một file Python = một scene dài** (4-5 phút final), không tách subroutine quá nhỏ — chia sẻ context giúp iterate nhanh hơn.
2. **Sublime + Terminus + Python REPL** chạy song song. Highlight code → `cmd+R` → Manim render đoạn vừa highlight.
3. **`checkpoint_paste`**: comment `# section_name` ở đầu mỗi block. Manim cache state — paste lại block đó sẽ revert state về đầu block, như Jupyter notebook nhưng ở dạng plain text.
4. **Render cuối ở 4K**, có flag `--prerun` để estimate thời gian render và bắt lỗi sớm.

### 4.2. Animation primitives sẽ dùng nhiều nhất

```python
from manim import *

class ChapterOneScene(Scene):
    def construct(self):
        # 1. Write — animate vẽ chữ/đường viền dần dần
        title = Text("Trí tuệ nằm trong cơ thể", font_size=48)
        self.play(Write(title), run_time=2)

        # 2. Transform — biến A thành B (KHÔNG phải FadeOut + FadeIn)
        fish = SVGMobject("fish_alive.svg")
        fish_dead = SVGMobject("fish_dead.svg")
        self.play(Transform(fish, fish_dead), run_time=3)

        # 3. Rate function — easing
        # Mặc định: smooth (cubic bezier). Linear chỉ khi muốn cảm giác máy móc.
        self.play(
            square.animate.shift(RIGHT * 3),
            run_time=2,
            rate_func=smooth,  # hoặc linear, rush_into, there_and_back
        )

        # 4. Highlight subset — quan trọng cho text → equation
        eq = MathTex(r"\theta^* = \arg\max_\theta U(\theta)")
        # eq[0] là cả công thức, eq[0][2:4] là subset character
        self.play(Indicate(eq[0][2:4]))  # nhấp nháy "θ*"
```

### 4.3. Lorenz Attractor làm ẩn dụ cho "design space"

Đây là cú "hôi của" hay nhất từ video Grant. Lorenz Attractor là chaos — quỹ đạo phân kỳ — **nhưng** vẫn bị hút về một strange attractor. Đây là ẩn dụ hoàn hảo cho **optimization landscape của design space**: nhiều cực trị địa phương, nhưng có cấu trúc.

Dùng nó ở Tập 3, Phần 3, khi nói về co-optimization:

```python
class DesignAttractor(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()

        # Lorenz parameters
        sigma, rho, beta = 10, 28, 8/3
        def lorenz_step(state, dt=0.005):
            x, y, z = state
            return np.array([
                x + sigma*(y-x)*dt,
                y + (x*(rho-z) - y)*dt,
                z + (x*y - beta*z)*dt,
            ])

        # 10 starting points cực gần nhau
        epsilon = 1e-5
        starts = [np.array([1+i*epsilon, 1, 1]) for i in range(10)]

        # Tạo curves và dots
        curves = VGroup()
        dots = VGroup()
        for s in starts:
            traj = [s.copy()]
            state = s.copy()
            for _ in range(3000):
                state = lorenz_step(state)
                traj.append(state.copy())
            curve = VMobject().set_points_smoothly([axes.c2p(*p) for p in traj])
            curve.set_stroke(width=1, opacity=0.5)
            curves.add(curve)
            dots.add(Dot3D(axes.c2p(*s), radius=0.05))

        # Animate vẽ curves
        self.play(*[Create(c) for c in curves], run_time=10)

        # TracingTail effect cho dots — kỹ thuật Grant chỉ trong file
        # (xem implementation cụ thể trong manim community: TracedPath)
        for dot, s in zip(dots, starts):
            tail = TracedPath(dot.get_center, dissipating_time=2.0,
                              stroke_opacity=[0, 1])
            self.add(tail)
        # ...
```

**Voiceover khi cảnh này chạy** (ở Tập 3):
> "Đây không phải Lorenz attractor. Đây là quỹ đạo của 10 thiết kế robot khởi đầu gần như giống nhau, được tối ưu hoá đồng thời. Chúng phân kỳ — chaos — nhưng đều bị hút về cùng một vùng trong không gian thiết kế. Đó chính là 'strange attractor' của co-design."

### 4.4. Lưu ý kỹ thuật

- **3D scene cần 30-60s/giây render ở 4K.** Pre-cache trajectory trước, đừng tính lúc render.
- **TracedPath** với `dissipating_time` tạo hiệu ứng đuôi mờ — mô tả rất tốt cho "trajectory trong design space".
- **Group highlighting:** khi cần highlight 1 chữ trong một text, lấy ra subset (`text[0]` → group ký tự) rồi `[i]` từng ký tự.
- **Manim Community Edition** được khuyến nghị cho người mới (test, doc tốt hơn). Phiên bản riêng của Grant (`3b1b/manim`) có nhiều feature mới hơn nhưng không stable.

---

## 5. Visual asset checklist

Để dựng được series này cần chuẩn bị trước:

### 5.1. Footage thật / external clip

- [ ] Clip cá chết "bơi" trong dòng nước (cho cold open Tập 1) — có thể tự quay hoặc license stock footage.
- [ ] Clip TurtleBot điều hướng thật (Tập 2) — xin từ project gốc của Andre, hoặc tái dựng clip phỏng theo.
- [ ] Clip soft robot tự học đi (Tập 3) — từ ChainQueen demo của MIT.

### 5.2. SVG cần vẽ thủ công

- [ ] Cá: hai phiên bản (sống + chết).
- [ ] Mắt 6 loài: mèo, dê, đại bàng (võng mạc), sò điệp, cá hang động, bướm.
- [ ] Robot 4 chân (Tập 3 hero shot).
- [ ] Pipeline schematic: design → simulator → controller → reward.

### 5.3. Animation cần dựng riêng

- [ ] Pixel reduction từ 128×128 xuống 1 pixel (Tập 1 cliffhanger, Tập 2 intro).
- [ ] Bi-level optimization loop (Tập 2 Phần 4).
- [ ] Differentiable simulation forward + backward pass (Tập 3 Phần 2).
- [ ] Lorenz attractor như metaphor cho design space (Tập 3 Phần 3).
- [ ] Diffusion process: noise → robot, conditioned by simulation gradient (Tập 3 Phần 4).

### 5.4. Title cards / typography

- [ ] Logo channel.
- [ ] Episode title cards (3 variants).
- [ ] End screen với "next episode preview".
- [ ] Citation panel cuối mỗi tập (link tutorial gốc, link papers cụ thể: ChainQueen, DiffuseBot, photoreceptor agent).

---

## Phụ lục — Một số quote / data point cần fact-check trước khi quay

- Tỉ lệ acuity người vs đại bàng vs côn trùng: ~100 cycles/degree vs ~140 vs ~0.1 (Sönke).
- Sò điệp có **200-300** con mắt (Amir).
- Time step soft robot ~7μs → 1 triệu steps cho 1 giây mô phỏng (Andy).
- Chain Queen: gradient computation ≤15s cho mọi system trong demo (Andy).
- DiffuseBot beats baselines ở "almost all" examples (Andy) — kiểm tra paper để có con số cụ thể.
- Karl Sims paper: 1994 (Amir).
- Cave fish: Mexican tetra (Astyanax mexicanus) — không nêu tên trong talk nhưng đây là ví dụ kinh điển.

---

*Kịch bản này tổng hợp từ tutorial gốc và workflow Manim của Grant Sanderson, viết theo phong cách 3Blue1Brown để tham khảo. Khi sản xuất thật, cần đối chiếu lại số liệu với paper gốc và xin phép sử dụng footage từ các project được trích dẫn.*
