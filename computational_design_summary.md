# Computational Design of Diverse Morphologies and Sensors for Vision and Robotics

> Bản tổng hợp nội dung chi tiết của tutorial gốc (~3 giờ, 4 diễn giả). Mục đích: tài liệu tham khảo để hiểu sâu chủ đề trước khi sản xuất video. Đọc xong file này bạn sẽ có đủ context để nói chuyện về co-design như một người trong ngành.

---

## Mục lục

- [0. Tổng quan](#0-tổng-quan)
- [1. Khung khái niệm cốt lõi](#1-khung-khái-niệm-cốt-lõi)
- [2. Sự đa dạng của hệ thị giác sinh học](#2-sự-đa-dạng-của-hệ-thị-giác-sinh-học)
- [3. Case study 1: Photoreceptor agents](#3-case-study-1-photoreceptor-agents)
- [4. Case study 2: Underwater vision](#4-case-study-2-underwater-vision)
- [5. Robot mechanical morphology & codesign](#5-robot-mechanical-morphology--codesign)
- [6. Câu hỏi mở và hướng tương lai](#6-câu-hỏi-mở-và-hướng-tương-lai)
- [7. Glossary thuật ngữ](#7-glossary-thuật-ngữ)
- [8. Tài liệu đọc thêm](#8-tài-liệu-đọc-thêm)

---

## 0. Tổng quan

### 0.1. Tutorial gốc nói về cái gì?

Đây là một tutorial chuyên sâu (workshop/tutorial tại một hội nghị về computer vision/robotics), trình bày lĩnh vực **computational design** — cụ thể là dùng thuật toán để tự động thiết kế **hình thái (morphology)** và **hệ cảm biến (sensors)** cho các tác tử (agents) — bao gồm cả robot vật lý và cả các sinh vật sinh học mà ta đang cố hiểu.

Câu hỏi trung tâm: thay vì để con người thiết kế cơ thể robot bằng trực giác rồi gắn AI vào điều khiển, **liệu ta có thể đồng thời tối ưu cả thân và não?**

### 0.2. Bốn diễn giả, bốn góc nhìn

| Diễn giả (theo nội dung) | Phần | Trọng tâm |
|---|---|---|
| **Amir** (CV/AI) | Mở đầu | Khung khái niệm + sự đa dạng thị giác sinh học |
| **Andre** (CV) | Case study 1 | Tối ưu thiết kế photoreceptor cho navigation tasks |
| **Sönke Johnsen** (Biology, Duke) | Case study 2 | Mô hình trade-off sensitivity vs resolution dưới biển sâu |
| **Andy** (Robotics) | Phần lớn nửa sau | Co-design thân robot bằng differentiable simulation và generative AI |

### 0.3. Vì sao chủ đề này quan trọng

Lý do thực dụng: thiết kế robot đang là cổ chai. Mỗi prototype mất hàng tháng. Sai lầm phải quay lại từ đầu. Nếu máy tính có thể đề xuất thiết kế thay con người, ta tăng tốc được toàn bộ vòng lặp R&D.

Lý do khoa học: sinh học cho thấy không có "một thiết kế cơ thể duy nhất tốt nhất". Mỗi loài là một trường hợp tối ưu hoá riêng cho ngách sinh thái của nó. Hiểu được nguyên lý đằng sau giúp ta hiểu cả quá trình tiến hoá lẫn cách xây hệ thống AI tổng quát.

Lý do triết học: đặt câu hỏi "trí tuệ nằm ở đâu" — mở rộng định nghĩa AI từ chỉ-mạng-nơ-ron sang cả vật lý cơ thể.

---

## 1. Khung khái niệm cốt lõi

### 1.1. Con cá chết — nơi trí tuệ ẩn náu

Tutorial mở đầu bằng một thí nghiệm tư duy nổi tiếng. Người ta gắn dây vào đầu một **con cá đã chết**, đặt nó vào dòng nước chảy ngược chiều. Cơ thể con cá uốn lượn, đuôi quẫy — trông y hệt một con cá đang bơi. Não đã chết. Vậy thì "kiến thức bơi" nằm ở đâu?

**Câu trả lời:** kiến thức được mã hoá trong **chính cấu trúc vật lý** của cơ thể — độ đàn hồi của thịt, tỉ lệ chiều dài đuôi, độ dẻo của xương sống. Tương tác giữa cấu trúc đó với dòng nước **tự nhiên tạo ra hành vi bơi** mà không cần tính toán nào.

### 1.2. Hai loại tham số: brain và body

Mọi tác tử thông minh có thể được mô tả bằng hai tập tham số:

```
agent = (θ_brain, θ_body)
```

| | θ_brain | θ_body |
|---|---|---|
| Bản chất | Trọng số mạng nơ-ron, policy, perception model | Hình học, vật liệu, vị trí cảm biến, độ cứng khớp |
| Tốc độ thay đổi | Nhanh — học được trong vài phút | Chậm — qua tiến hoá hoặc fabrication |
| Tính linh hoạt | Cao — có thể fine-tune liên tục | Thấp — gần như cố định sau khi chế tạo |
| Truyền thống AI | Trọng tâm chính | Bị bỏ qua hoặc thiết kế bằng tay |

Quan điểm xuyên suốt tutorial: **cả hai đều là tham số có thể học được**. Cộng đồng AI chỉ mới khai thác bên trái.

### 1.3. Morphology = cơ học + tri giác

"Morphology" trong tutorial không chỉ nghĩa là hình dạng cơ học. Nó bao gồm:

- **Mechanical morphology**: kích thước, hình dạng, vật liệu, sơ đồ khớp, cấu trúc đàn hồi.
- **Perceptual morphology**: số lượng và loại sensor, vị trí đặt, trường nhìn, độ phân giải, độ nhạy.

Cả hai đều "ở phía cơ thể" của agent và đều có thể tối ưu được.

### 1.4. Vì sao đa dạng sinh học là điểm tựa

Tutorial liên tục quay lại sinh học vì sinh học đã giải bài toán này 4 tỉ năm rồi. Mỗi loài là một thiết kế tối ưu cho ngách sinh thái cụ thể. Quan điểm Gibson: **tính chất của hệ tri giác phản ánh môi trường nó sống**.

Hệ quả: không tồn tại "một thiết kế cơ thể đa năng tốt nhất". Đây là phiên bản sinh học của **No Free Lunch theorem** trong machine learning — agent tổng quát hoá tốt mọi nơi sẽ không xuất sắc ở đâu.

### 1.5. Khi nào computational design đáng dùng?

Câu trả lời: khi **trực giác con người không đáng tin**. Có ba dấu hiệu:

1. **Domain quá xa lạ** — không có analog trong kinh nghiệm con người (vd: thiết kế "pill cam" — camera nhỏ uống vào để chẩn đoán nội soi).
2. **Tham số tương tác phức tạp** — thay đổi một thứ ảnh hưởng khắp nơi.
3. **Trực giác có thể sai** — đây là điểm quan trọng nhất.

#### Ví dụ kinh điển: vì sao ngựa vằn có sọc?

Trực giác ai cũng đoán: **ngụy trang**. Hợp lý — sọc làm sư tử khó nhắm khi đàn chạy. Hoặc giả thuyết nâng cao hơn: làm cả đàn trông như một sinh vật to lớn.

Cả hai đều **sai**.

Sự thật:

- Sư tử có thị giác kém hơn người. Từ khoảng cách săn, sư tử **không phân biệt được ngựa vằn với lừa** — sọc bị blur.
- Sọc thực ra là **biện pháp đuổi muỗi**. Mắt kép của muỗi không xử lý được hoa văn tương phản cao → muỗi không hạ cánh được.
- Bằng chứng thực tiễn: nông dân ở vài nước **sơn sọc lên bò** để giảm bệnh do muỗi truyền — và nó hiệu quả.

**Bài học**: khi ta thiết kế bằng trực giác con người ("trông phải thế này"), ta áp đặt human-centric prior lên một bài toán không thuộc về con người. Computational design không có bias đó.

### 1.6. Khung toán học chung

Tổng quát hoá toàn bộ tutorial vào một công thức:

$$
\theta^* = \arg\max_{\theta \in \Theta} \; U(\theta)
$$

Trong đó:

- $\theta$ là **design parameters** — toạ độ trong không gian thiết kế (cao chiều, có thể là vị trí voxel, trọng số sensor, ...).
- $U(\theta)$ là **utility function** — đánh giá thiết kế đó tốt thế nào trên nhiệm vụ.
- $\Theta$ là **design space** — tập hợp các thiết kế khả dĩ.

Vấn đề: $U(\theta)$ thường **không có công thức đóng**. Để tính nó, ta phải:

1. Lấy thiết kế $\theta$,
2. Mô phỏng cơ thể đó trong môi trường,
3. Gắn một controller (có thể cũng cần học),
4. Cho chạy nhiệm vụ,
5. Đo phần thưởng cuối cùng.

Đây chính là chỗ phân nhánh thành hai trường phái phương pháp.

### 1.7. Hai trường phái phương pháp

#### Physics-based

- **Khi dùng**: ta có mô hình toán học cho domain (ví dụ: Newtonian mechanics cho cơ học cứng, Navier-Stokes cho fluid).
- **Cách làm**: viết simulator giải các phương trình vật lý. Tối ưu trên simulator đó bằng các kỹ thuật cổ điển (gradient descent, sequential quadratic programming, ...).
- **Ví dụ trong tutorial**: thiết kế cơ học robot với differentiable simulation (Andy).

#### Learning-based

- **Khi dùng**: domain thiếu mô hình giải tích — ví dụ "mắt → tri giác → hành vi" không có phương trình.
- **Cách làm**: học một mô hình thay thế từ dữ liệu, dùng nó để tối ưu thiết kế.
- **Ví dụ trong tutorial**: photoreceptor optimization (Andre) — không có công thức cho "tín hiệu sensor → điều hướng thành công", phải học cả policy và sensor design qua reinforcement learning.

Cả hai trường phái đều là **specialization của cùng một meta-pipeline**: drug discovery, material discovery, AlphaGo — đều đi theo công thức "học mô hình đầu vào → đầu ra, rồi tối ưu ngược lại không gian đầu vào".

---

## 2. Sự đa dạng của hệ thị giác sinh học

Phần này (Amir trình bày) đi qua các tham số thiết kế của mắt mà tiến hoá đã khai thác. Mỗi tham số là một "trục" của design space mà ta có thể bắt chước trong computational design.

### 2.1. Field of view và placement

Quy tắc tổng quát:

- **Predator** (hổ, đại bàng): mắt đặt phía trước → trường nhìn hai mắt chồng lấp → có depth perception → tốt cho ngắm bắn.
- **Prey** (hươu, thỏ): mắt đặt hai bên → trường nhìn rộng (gần 360°) → phát hiện kẻ thù từ mọi hướng → đánh đổi mất depth perception ở phía trước.

Đây không phải quy tắc tuyệt đối — luôn có ngoại lệ — nhưng là pattern dominant.

### 2.2. Hình dạng đồng tử

- **Đồng tử dọc** (mèo, cáo): predator phục kích, ưu tiên depth perception khi rình.
- **Đồng tử ngang** (dê, ngựa): prey, mở rộng field of view ngang.
- **Đồng tử tròn** (người, chó): generalist.

Hình dạng đồng tử ảnh hưởng đến cả **bokeh tự nhiên** của mắt — quan trọng cho depth-from-defocus.

### 2.3. Adaptation to darkness

Vài chiến lược tiến hoá đã thử:

#### (a) Mắt to bất thường

**Tarsier** — loài linh trưởng nhỏ — có **mắt to gần bằng não**. Aperture lớn → thu nhiều photon hơn → nhìn được trong đêm.

#### (b) Reflective coating (tapetum lucidum)

Mèo, hươu, nhiều động vật có vú khác có một lớp **gương sau retina**. Khi ánh sáng đi qua retina mà chưa được hấp thụ hết, lớp gương phản xạ nó về để retina có cơ hội hấp thụ lần hai. Đây là lý do mắt mèo "phát sáng" khi rọi đèn pin.

#### (c) Pooling photoreceptors

**Sweat bees** (một loài ong) trong điều kiện ánh sáng yếu sẽ **gộp nhiều photoreceptor lại thành một "siêu pixel"** — đánh đổi resolution để tăng sensitivity. Trong CV, đây tương đương với spatial pooling.

#### (d) Bỏ mắt hoàn toàn

**Mexican tetra** (cá hang động) là minh hoạ kinh điển. Tổ tiên của nó sống ở mặt nước, có mắt bình thường. Khi một nhánh di cư vào hang tối, mắt trở thành "thiết bị tốn năng lượng vô ích" — não tiêu thụ rất nhiều glucose cho hệ thị giác. Tiến hoá đã **xoá mắt** khỏi cơ thể chúng. Anh em họ trên mặt đất vẫn có mắt nguyên vẹn.

Bài học: **không có gì nói rằng càng nhiều sensor càng tốt**. Đôi khi tối ưu là **giảm**.

### 2.4. Số lượng fovea

Fovea = vùng retina có mật độ photoreceptor cao nhất → nơi tạo ra ảnh sắc nét nhất. Người có **một** fovea, rộng cỡ ngón tay cái khi đưa cánh tay duỗi thẳng. Mọi thứ ngoài fovea đều mờ — ta chỉ không nhận ra vì mắt chuyển động liên tục để "quét" fovea qua các vùng quan trọng.

**Đại bàng và chim ưng có hai fovea**: một nhìn thẳng, một nhìn nghiêng ~45°. Hệ quả hành vi: chúng săn theo **đường xoắn ốc logarit** — vì đường này cho phép giữ một trong hai fovea luôn khoá vào con mồi trong khi cơ thể vẫn tiếp cận nó.

### 2.5. Phân tán vs tập trung

**Sò điệp (scallop)** có **200-300 con mắt** rải khắp viền vỏ. Mỗi mắt cá nhân nhỏ, độ phân giải thấp. Thay vì tập trung photoreceptor vào một retina dày đặc kiểu người, sò điệp **phân tán** chúng.

Một chi tiết kỹ thuật thú vị: mắt sò điệp dùng **gương lõm** (concave mirror) thay vì thấu kính để hội tụ ánh sáng. Đây là một trong số rất ít sinh vật dùng quang học phản xạ thay vì khúc xạ.

### 2.6. Resolution: ai sắc nét, ai không?

Đo bằng **cycles per degree** — số chu kỳ đen-trắng có thể phân biệt trong một độ góc nhìn.

| Loài | Acuity (cycles/degree) |
|---|---|
| Đại bàng | ~140 |
| Người | ~60-100 |
| Mèo | ~5-10 |
| Chuột | ~1 |
| Bướm | ~0.1 |
| Côn trùng nói chung | 0.05-0.5 |

Khoảng cách hơn **3 bậc độ lớn** giữa người và bướm. Hầu hết động vật **mù theo tiêu chuẩn pháp lý của con người** — nhưng vẫn xử lý tốt môi trường của chúng.

Hệ quả thực tế cho computational design: **đừng giả định cần camera 4K để giải bài toán thị giác**. Resolution thấp có thể đã đủ.

#### Trường hợp con bướm

Một con bướm map butterfly nhìn một con bướm cùng loài cách 2m chỉ thấy **một đốm mờ không phân biệt nổi**. Trớ trêu hơn: hoa văn rực rỡ trên cánh chúng — chúng **không thấy được lẫn nhau**. Giả thuyết cũ cho rằng đó là tín hiệu courtship để giao phối → giả thuyết này sai vì độ phân giải không đủ.

Sự thật: hoa văn dành cho **chim** — kẻ săn mồi có thị giác tốt hơn. Một số bướm có hoa văn giả mạo loài độc → chim né → tránh được predation. Lại một lần nữa: trực giác con người ("hoa văn để giao tiếp") đã sai.

### 2.7. Multimodality

Không sinh vật nào chỉ dùng một giác quan. Vài ví dụ "thiết kế khứu giác":

- **Mũi chó**: có khe hở bên (lateral slits) đảm bảo luôn hút phân tử mùi vào, kể cả khi thở ra. Đây là một thiết kế **morphology cảm biến** thực sự.
- **Lưỡi rắn xẻ đôi**: hai đầu sample mùi ở hai điểm không gian → tính được **gradient mùi** → mùi có hướng. Đây là **stereo olfaction**, tương đương với stereo vision.
- **Kền kền (turkey vulture)**: vốn có thị giác tốt (bay cao), nhưng còn có khứu giác cực mạnh — phát hiện xác chết từ ~13km. Có công ty dùng kền kền làm "đội tuần tra phát hiện rò rỉ đường ống khí gas": bơm hoá chất hấp dẫn kền kền vào khí, hễ thấy đàn kền kền tụ lại đoạn nào → biết có rò rỉ.

Bài học cho design: cảm biến đa dạng **bù trừ lẫn nhau**. Một sensor vision tệ có thể được cứu bởi một sensor proprioception tốt.

---

## 3. Case study 1: Photoreceptor agents

(Andre trình bày — project về việc thay camera bằng vài photoreceptor đơn giản và để máy tính tìm cách đặt chúng.)

### 3.1. Câu hỏi nghiên cứu

CV truyền thống: lấy camera 128×128 pixel hoặc cao hơn, đặt ở vị trí "trực giác" trên agent (thường là phía trước, ngang tầm mắt người), rồi train CNN/Transformer để giải task.

Câu hỏi: **giảm resolution xuống cực thấp — 1, 2, 4 pixel — và để máy tự tìm vị trí đặt — liệu có còn giải được không?**

Hai inspiration sinh học:

- Côn trùng có "mắt" cực thô sơ nhưng hành vi cực phức tạp.
- Tiến hoá tối ưu hoá vị trí và hướng mắt rất khác nhau giữa các loài.

### 3.2. Mô hình hoá photoreceptor trong simulator

Cách triển khai đơn giản:

1. Render một camera view bình thường (128×128 chẳng hạn) tại vị trí và hướng của photoreceptor.
2. **Average toàn bộ ảnh** thành 3 con số RGB → đó là tín hiệu của **một** photoreceptor.

Khi tăng số photoreceptor:

- **Spawn nhiều sensor riêng biệt** ở các vị trí khác nhau, hoặc
- **Chia ảnh camera thành lưới** (2×2, 4×4, 8×8) và average mỗi ô → hiệu quả tương đương camera độ phân giải cực thấp.

Tham số thiết kế cho mỗi photoreceptor:

- Vị trí (x, y, z) trên cơ thể agent.
- Hướng (yaw, pitch).
- Field of view (góc mở của cone).

Tổng cộng: nếu agent có $N$ photoreceptor, design space là $\theta \in \mathbb{R}^{6N}$.

### 3.3. Tasks

Hai task điều hướng tiêu chuẩn (lấy từ Habitat / Matterport datasets — quét 3D thật của các căn nhà):

1. **Point-goal navigation**: agent biết toạ độ (x, y) tương đối của mục tiêu. Việc cần làm là né tường và đi tới đó nhanh nhất.
2. **Object-goal navigation**: mục tiêu là một quả bóng xanh đặt trong scene; agent **không biết toạ độ** — phải khám phá scene để tìm bóng.

Cộng thêm: ba task continuous control từ DeepMind Control suite (Reacher, Walker, Finger) — giải hoàn toàn bằng tín hiệu visual.

### 3.4. Baseline đối chứng

Để đặt kết quả vào bối cảnh:

- **Blind agent**: không có visual input. Học từ structural bias của dataset (ví dụ: nhà thường có hành lang dẫn đến các phòng). → cận dưới của hiệu suất.
- **Camera agent**: 128×128, kiến trúc Transformer thông thường. → baseline tiêu chuẩn.
- **Camera + ResNet-50**: kiến trúc mạnh hơn. → upper baseline.

### 3.5. Kết quả với thiết kế ngẫu nhiên

Thông điệp #1: **vài photoreceptor (4-8) đã đủ để vượt xa blind agent** và đạt hiệu suất tương đương camera ở Transformer baseline.

Thông điệp #2: **với cùng số lượng photoreceptor, hiệu suất biến thiên rất lớn theo cách đặt**. Một vài thiết kế ngẫu nhiên đạt gần camera, một vài thiết kế khác tệ ngang blind agent.

→ **Vị trí đặt sensor mới là yếu tố quyết định**, không phải số lượng sensor. Đây là động lực cho design optimization.

### 3.6. Thuật toán design optimization

#### Vấn đề với cách tiếp cận naive

Setup tự nhiên là **bi-level optimization**:

```
outer loop: cập nhật thiết kế θ
    inner loop: train policy φ tối ưu cho θ
    đánh giá U(θ, φ*)
```

Mỗi lần thay θ, phải train lại policy từ đầu — tốn 1-2 ngày cho một thiết kế. Nếu cần đánh giá hàng nghìn thiết kế (Bayesian optimization, evolutionary search) → không khả thi.

#### Trick chính: gộp design vào single rollout

Thay vì hai vòng lặp tách biệt, **xem design như một "action ban đầu"** cùng namespace với control actions:

1. Đầu episode: policy "phát ra" một thiết kế θ (ví dụ: vị trí 4 photoreceptor).
2. Renderer dùng θ này để render observations cho phần còn lại của episode.
3. Policy điều khiển agent dựa trên observations đó.
4. Reward cuối episode được dùng để **đồng thời cập nhật cả θ và φ trong cùng một backward pass**.

Hệ quả:

- Reward giờ phụ thuộc cả thiết kế lẫn policy: $R(\theta, \phi)$.
- Policy được conditioned trên θ → cùng một policy có thể ứng xử khác nhau cho các thiết kế khác nhau, nên không phải retrain mỗi khi đổi thiết kế.

#### Pseudocode

```python
for iteration in range(N):
    # Sample design + execute trajectory
    theta = policy.propose_design()  # one-shot at episode start
    obs_seq = []
    for t in range(T):
        obs = render(env_state, theta)  # design enters here
        action = policy(obs, theta)     # policy conditioned on theta
        env_state = simulate(env_state, action)
        obs_seq.append(obs)
    reward = task_reward(env_state)

    # Update both theta and phi from same reward signal
    grad_theta, grad_phi = backprop(reward, theta, phi)
    theta -= lr * grad_theta
    phi -= lr * grad_phi
```

### 3.7. Kết quả tối ưu hoá — và một bất ngờ

Sau optimization:

- Hiệu suất gần tiệm cận camera baseline (đôi khi **vượt** ResNet-50 baseline).
- Thiết kế thu được trông **không trực giác** với người.

#### Kết quả gây sốc nhất

Cho **point-goal navigation**, một trong các photoreceptor tối ưu **thường chĩa xuống đất** (góc pitch ~ -60° đến -80°).

**Vì sao?** Hồi quy lại bản chất task: agent **đã biết** toạ độ mục tiêu. Việc duy nhất còn lại là **tránh va chạm**. Sensor nhìn thẳng xuống mặt sàn là cách hiệu quả nhất để phát hiện vật cản gần (chân tường, đồ đạc trên đường) trước khi đâm vào.

Đây là loại insight mà con người **không tự nghĩ ra** — không kỹ sư nào tự nguyện gắn camera chĩa xuống chân robot. Nhưng khi tối ưu kỹ, đó lại là vị trí tốt nhất.

Tương tự cho object-goal navigation: target là quả bóng cao ngang giữa thân agent → camera tối ưu hội tụ về độ cao đó.

#### So sánh với thiết kế của con người

Tiến hành human survey: cho người tham gia thiết kế vị trí 4 photoreceptor cho một task cụ thể.

- Hiệu suất thiết kế của con người **biến thiên rất lớn**.
- Thiết kế tối ưu của thuật toán **luôn nằm ở top**.
- Intuition của người: chọn vị trí "trông hợp lý" — nhưng những vị trí đó không tối ưu cho động lực học cụ thể của agent.

### 3.8. Sim-to-real

Triển khai policy lên TurtleBot thật:

- Sensor: 8×8 = 64 photoreceptor (tương đương camera 8×8).
- Mục tiêu: tìm và tới gần một quả bóng hồng đặt trên hộp.
- Train hoàn toàn trong simulator. **Zero real-world fine-tuning.**

Kết quả: hoạt động — không phải lúc nào cũng thành công, nhưng pattern hành vi đúng (khám phá → phát hiện → tiếp cận). Cho thấy thiết kế perceptual morphology tối ưu trong sim **chuyển được sang thật** mà không cần điều chỉnh.

### 3.9. Ý nghĩa rộng hơn

- **Resolution không phải tất cả**: một agent với 4 pixel có thể giải được task mà CV cộng đồng mặc định cần 128×128.
- **Vị trí > số lượng**: dùng ít sensor đặt đúng còn tốt hơn nhiều sensor đặt sai.
- **Co-design > sequential design**: nếu thiết kế body trước, train brain sau, ta không bao giờ tìm được local optimum tốt nhất.

---

## 4. Case study 2: Underwater vision

(Sönke Johnsen — biologist tại Duke. Phần này khoa học cơ bản hơn, trình bày một mô hình toán học cho mắt động vật biển sâu.)

### 4.1. Color vs spatial vision

Trực giác phổ biến: màu sắc là kênh thông tin giàu. Các bài báo sinh học hay đào sâu về "secret color channels" — UV, polarization, ...

**Sự thật**: không gian màu thị giác **rất hẹp**. Ánh sáng "nhìn được" chỉ trải dài từ ~350nm đến ~630nm — chưa đến một bậc độ lớn về bước sóng.

Bài kiểm tra: lấy một ảnh, chia làm hai kênh — luminance (độ sáng) và chrominance (sắc độ).

- **Chỉ luminance** (đen trắng): vẫn nhận diện được hầu hết thông tin trong ảnh. Đây là lý do TV đen trắng hoạt động tốt nhiều thập kỷ.
- **Chỉ chrominance** (mất luminance): gần như không phân biệt được hình dạng 3D nào.

Hệ quả: **spatial vision quan trọng hơn color** cho hầu hết task perceptual. Đây là lý do nhóm Sönke tập trung vào acuity (độ phân giải không gian) thay vì colour vision.

### 4.2. Trade-off cốt lõi: sensitivity vs resolution

Trong mắt (cũng như trong camera), hai thuộc tính cạnh tranh nhau:

- **Resolution** cao = pixel nhỏ = ít photon trên mỗi pixel = ảnh nhiễu trong điều kiện thiếu sáng.
- **Sensitivity** cao = pixel lớn (gộp nhiều photon) = ảnh sáng nhưng mờ.

Trong CV, đây là lý do iPhone đời đầu chụp ngày tốt, chụp đêm tệ: pixel quá nhỏ, không gom đủ photon trong điều kiện ánh sáng yếu.

Có thể tăng cả hai bằng cách **làm mắt to hơn** (aperture lớn hơn → nhiều photon, vẫn giữ pixel nhỏ). Đây là lý do tarsier có mắt to bằng não. Nhưng mắt to là một khoản đầu tư khổng lồ về năng lượng và không gian.

### 4.3. Hai chế độ ánh sáng dưới biển

Càng xuống sâu, ánh sáng càng giảm. Có hai regime hoàn toàn khác nhau:

#### (a) Ambient light (≤ 500m)

Ánh sáng mặt trời còn xuyên xuống được (dù đã giảm vài bậc độ lớn). Sinh vật nhìn cảnh vật như "ảnh chụp": rặng san hô, đàn cá, các vật thể trải rộng trong không gian.

Nhiệm vụ thị giác: phân biệt **extended objects** — cần resolution + sensitivity cân bằng để nhận ra hình thù.

#### (b) Bioluminescent (> 500m)

Ánh sáng mặt trời gần như tắt hẳn. Hầu hết tín hiệu thị giác đến từ **bioluminescence** — sinh vật tự phát sáng. Đặc biệt là loài **ostracod** — phát sáng theo chuỗi điểm theo các pattern không gian-thời gian (xoắn ốc, đường thẳng, đổi hướng) như một loại "Morse code" để gọi bạn tình.

Nhiệm vụ thị giác: phát hiện **point sources** — cần định vị flash sáng chính xác.

### 4.4. Mô hình toán cho optimal acuity

Mục tiêu: tính độ acuity tối ưu cho mắt một con mực nhìn vào con cá có sọc.

#### Bước 1: Modulation Transfer Function (MTF) của mắt

MTF mô tả cách contrast của ảnh giảm khi target xa hơn. Có thể đo cả morphology (qua giải phẫu retina) lẫn behavior. MTF của mắt thường gần với gaussian:

$$
\text{MTF}_{\text{eye}}(f) = \exp\left(-\left(\frac{f}{f_c}\right)^2\right)
$$

trong đó $f$ là tần số không gian (cycles per degree), $f_c$ là cutoff phụ thuộc vào $\Delta\rho$ (resolution của mắt).

#### Bước 2: Contrast threshold phụ thuộc photon noise

Số photon đến mỗi pixel tuân theo phân phối Poisson — std bằng $\sqrt{n}$. Khi ánh sáng yếu, signal-to-noise ratio (SNR) giảm:

$$
\text{SNR} = \frac{n}{\sqrt{n}} = \sqrt{n}
$$

Contrast threshold tối thiểu để phát hiện vật:

$$
C_{\min} \propto \frac{1}{\sqrt{n}}
$$

trong đó $n$ là số photon trên mỗi pixel mỗi đơn vị thời gian, phụ thuộc vào ambient light, aperture, integration time, và pixel size.

#### Bước 3: Sighting distance

Khoảng cách tối đa thấy được tính bằng cách kết hợp MTF của mắt với contrast threshold. Trong vacuum (chưa tính nước):

$$
\text{Sighting distance} = f(\Delta\rho, \text{light level}, \text{target contrast})
$$

Hàm này có **một cực đại** ở giữa: mắt 1 pixel vô dụng, mắt vô số pixel cũng vô dụng (ánh sáng chia quá nhỏ → noise át tín hiệu).

#### Bước 4: Cộng thêm ảnh hưởng của nước

Đây là phần làm bài toán không giải được analytically nữa.

- **Veiling light**: ánh sáng tán xạ từ các hướng khác làm "che mờ" cảnh — frequency-independent.
- **Multiple scattering**: tán xạ nhiều lần — frequency-dependent — đã được mô hình hoá bởi Zaneveld và Pegau.

Phải giải số học. Tham số đầu vào:

- Beam attenuation coefficient của nước (~0.005 cho biển khơi sạch).
- Depth.
- Time of day.
- Eye pupil size, integration time.
- Target size, target contrast.

### 4.5. So sánh với động vật thật — và kết quả gây sốc

Lấy dữ liệu acuity của hàng chục loài cá và mực ở các độ sâu khác nhau, plot lên đồ thị "depth vs acuity". So sánh với prediction của mô hình.

#### Kết quả ở < 500m

Mô hình khớp với thực tế **trong vòng factor of 2-3** — đây là độ chính xác cực tốt cho biology (vốn quen làm việc với "một chữ số có nghĩa"). Mô hình ambient-light regime **đúng**.

#### Kết quả ở > 500m

**Mô hình sai hẳn**: prediction nói acuity nên giảm mạnh (vì ánh sáng yếu → cần gộp pixel để có sensitivity). Nhưng thực tế: **động vật biển sâu có acuity cao hơn nhiều so với prediction** — lên tới một bậc độ lớn.

#### Giải thích

Mô hình giả định task là "phân biệt extended objects under ambient light". Ở > 500m, task đã đổi sang **"localize bioluminescent point sources"**.

Với point sources:

- F-number của hệ quang không quan trọng (tất cả ánh sáng từ một điểm rơi vào ~1 photoreceptor bất kể aperture).
- Thứ duy nhất quan trọng là **biết flash xuất hiện ở đâu** — cần acuity cao.

Bài học: **mô hình "trade-off chuẩn"** chỉ đúng trong regime mà nó được rút ra. Khi distribution của tín hiệu thay đổi (extended → point), trade-off đổi hoàn toàn. Đây là một điểm gặp tự nhiên với CV: thuật toán và sensor design phụ thuộc rất mạnh vào prior về **dạng tín hiệu** ta đang xử lý.

### 4.6. Các yếu tố underwater bổ sung

Bonus complications mà thị giác trên cạn không có:

- **Light spectrum thay đổi theo viewing angle**: nhìn lên thấy ánh sáng trắng (mặt trời), nhìn ngang thấy xanh (lọc qua nước), nhìn xuống thấy tím (upwelling). Một số loài có **mắt khác nhau cho hướng nhìn khác nhau**.
- **Caustics**: sóng mặt nước hoạt động như chuỗi thấu kính dương âm liên tục → ánh sáng tới mắt thay đổi vài bậc độ lớn trong ~1/30 giây.
- **Water clarity dependent on location**: dòng chảy ngọt từ sông đổ ra → phytoplankton bloom → optical properties thay đổi đột ngột.

Tutorial gợi ý: nên có **VR experience** để con người thấy được "thế giới của tôm cá" — radiative transfer simulators đã có sẵn cho việc này.

---

## 5. Robot mechanical morphology & codesign

(Andy — phần dài nhất, ~90 phút. Đây là where the toán học nặng nhất.)

### 5.1. Tại sao codesign?

#### Quy trình thiết kế truyền thống

```
Spec → Concept → Components → Build → Program → Test
                                                  ↓
                                  (lỗi → quay lại bước nào?)
```

Vấn đề:

- **Không có chứng chỉ ở bất kỳ bước nào**: không ai dám đảm bảo concept ban đầu sẽ work.
- **Mỗi prototype tốn tháng**: build + program + test cycle dài.
- **Trial-and-error** + **intuition** = pipeline không scale.

#### Specification-driven codesign

Mục tiêu: từ task spec, **đồng thời** sinh ra:

- Topology của body (nơi nào có khớp, nơi nào không).
- Material distribution (chỗ nào cứng, chỗ nào mềm).
- Sensor placement.
- Controller (policy).

Tất cả trong **một** vòng tối ưu hoá duy nhất.

### 5.2. Khung toán học cho codesign

Từ control theory, dynamical system:

$$
\dot{x} = f(x, u, \theta_{\text{body}})
$$

trong đó $x$ là state, $u$ là control input, $\theta_{\text{body}}$ là design parameters của thân.

Loss function:

$$
L = \int_0^T \ell(x(t), u(t)) \, dt
$$

Codesign minimization:

$$
\min_{\theta_{\text{body}}, \, \pi} \; L \quad \text{s.t.} \; \dot{x} = f(x, \pi(x), \theta_{\text{body}})
$$

trong đó $\pi$ là policy (controller).

### 5.3. Triple nested inverse problem

Trong thực tế, design parameters không tự do — chúng phải:

1. Tối ưu cho objective (inverse problem #1).
2. **Có thể fabricate**: nhiều thiết kế ảo không in 3D được (inverse problem #2).
3. **Translate trung thực sang thật**: kể cả fabricate được thì sim-to-real gap có thể giết design (inverse problem #3).

Tutorial nhấn mạnh: hầu hết research hiện tại chỉ giải tốt #1, một số ít chạm vào #2, gần như chưa ai giải đồng thời cả ba.

### 5.4. Phân loại robot

#### Rigid

- Skeleton + joints. Vài độ tự do (DoF).
- Pros: dễ điều khiển, state nhỏ gọn (toạ độ joint).
- Cons: không grasp được vật mềm tốt, không có compliance.

#### Soft

- Continuum mechanics. Vô số DoF (về lý thuyết).
- Pros: grasp tự nhiên, an toàn khi tương tác với người, tự cân bằng tốt.
- Cons: cực khó mô hình hoá, sim chậm, control phức tạp.

#### Hybrid

- Rigid skeleton + soft "skin" hoặc compliant joints.
- Phổ biến trong sinh học: con người là hybrid (xương cứng, cơ mềm).

### 5.5. Các loại simulation

| Simulator type | Use case | Tốc độ |
|---|---|---|
| Rigid body | Robot công nghiệp, articulated arms | Rất nhanh trên GPU |
| Soft body / FEM | Soft robots, manipulation | Chậm |
| Fluid dynamics | Bơi, bay | Rất chậm |
| Multiphysics | Coupling (ví dụ thân robot tương tác với nước) | Cực chậm |

Trade-offs khi chọn simulator:

- Loại media (rigid/soft/fluid).
- Yêu cầu accuracy.
- Dimensionality của state.
- Stiffness của hệ — hệ "stiff" cần time step cực nhỏ hoặc implicit integration.
- Hỗ trợ GPU.
- **Differentiability** — có tính được gradient hay không.

### 5.6. Differentiable simulation

Đây là trung tâm của phần mechanical codesign hiện đại.

#### Ý tưởng

Coi simulator như một **mạng nơ-ron rất dài**: mỗi step là một layer, mỗi state là một activation. Nếu mỗi step được viết bằng các phép toán differentiable (matmul, dot, sigmoid, …), thì cả simulator differentiable.

Hệ quả: với bất kỳ output nào (reward, final position, ...) ta tính được gradient với respect to bất kỳ input nào (initial state, physics params, design params).

#### ChainQueen — ví dụ chính trong tutorial

Một differentiable simulator cho soft body. Scene mẫu:

- Robot soft 4 chân.
- Goal: chạy về phía trước càng xa càng tốt trong T giây.
- Design variables (initial): trọng số neural network điều khiển.
- Forward pass: simulator chạy T bước, output cuối là khoảng cách.
- Backward pass: gradient của khoảng cách với respect to weights → cập nhật bằng Adam.

**Kết quả**: robot học đi trong **6 giây wall-clock**, sau ~12 iterations (mỗi iteration ~0.5s).

So sánh với reinforcement learning (PPO, SAC): cùng task này, RL tốn hàng giờ vì mỗi rollout phải explore ngẫu nhiên. Differentiable simulation cho gradient *trực tiếp* về policy parameters → cập nhật mỗi step có hướng chính xác.

#### Caveats

- **Không phải lúc nào cũng tốt hơn RL**: gradient-based là **greedy** — kẹt ở local minima nếu landscape có nhiều ngách. Với task cần exploration nhiều (ví dụ: navigate trong môi trường thưa reward), RL vẫn hơn.
- **Memory cực kỳ tốn kém**: backprop qua hàng triệu time step → phải lưu activation ở mỗi bước. Soft robot với time step ~7μs → 1 triệu bước cho 1 giây sim. Không server nào đủ RAM cho điều này.

#### Giải pháp: implicit integration

- **Explicit integration** (Forward Euler, RK4): cập nhật state theo derivative hiện tại. Phải dùng time step cực nhỏ cho hệ stiff để tránh numerical explosion.
- **Implicit integration** (Backward Euler): giải hệ phương trình ngầm tại mỗi step. Time step lớn hơn, ổn định hơn — đánh đổi accuracy.

Trong codesign, **độ chính xác sub-percent thường không quan trọng** — vì sim-to-real gap đã sai lớn hơn nhiều rồi. Implicit integration là sweet spot thực tế.

#### Tools để bắt đầu

- **Taichi** (DSL Python-like, GPU-friendly) — domain specific language cho differentiable physics.
- **NVIDIA Warp** — tương tự, do NVIDIA phát triển.
- **MuJoCo MJX** (port sang JAX của MuJoCo) — gần đây có gradient.

### 5.7. Ba phương pháp codesign

#### (a) Evolutionary search

- Karl Sims (1994) là kinh điển: voxel creatures được encode bằng chromosome string, mutate và crossover qua các thế hệ.
- Pros: không cần gradient → áp dụng được cho non-differentiable systems.
- Cons: chậm, không scale lên design space cao chiều.
- Modern instantiation: **EvoGym** (sandbox 2D voxel-based, khá vui để prototype).

#### (b) Gradient-based codesign

Mở rộng ChainQueen: gradient không chỉ về policy weights mà cả về **physical design parameters**:

$$
\theta^* = \arg\min_{\theta_{\text{body}}, \theta_{\text{ctrl}}} L\bigl(\text{sim}(\theta_{\text{body}}, \theta_{\text{ctrl}})\bigr)
$$

Cập nhật cùng lúc:

$$
\theta_{\text{body}} \leftarrow \theta_{\text{body}} - \alpha \nabla_{\theta_{\text{body}}} L
$$
$$
\theta_{\text{ctrl}} \leftarrow \theta_{\text{ctrl}} - \alpha \nabla_{\theta_{\text{ctrl}}} L
$$

**Quan sát quan trọng**: thêm design dimension (stiffness, density, Poisson ratio, geometry) **luôn cải thiện performance**. Curse of dimensionality không xuất hiện ở đây — vì gradient chỉ hướng đi đúng đắn ngay cả trong high-D space.

Một ví dụ ấn tượng: optimize cả material distribution của một quadruped (~100,000 design variables — stiffness của mỗi voxel). Robot tự "thiết kế" ra:

- Chân có vùng cứng ở điểm push-off.
- Vùng mềm ở chỗ tiếp đất (như đệm hấp thụ shock).
- Thân chính cứng trung bình.

Thiết kế **trông biomimetic** — gần với cấu trúc xương + cơ + dây chằng của động vật thật. Tự nhiên đã giải bài này, ChainQueen tìm lại được pattern.

#### (c) Generative-based codesign

Vấn đề với gradient-based: vẫn greedy, vẫn local. Generative methods cho exploration tốt hơn.

##### Vì sao không hỏi ChatGPT?

Tutorial có đoạn humor: **thử yêu cầu ChatGPT thiết kế "soft robot hái dâu"**. Kết quả:

- Cánh tay với khớp khoá cứng (không cử động được).
- Robot lơ lửng trong không khí (không có support structure).
- Một con "spider strawberry" — nightmare fuel.

Trong study lớn hơn (yêu cầu thiết kế xe, bàn ghế, robot khác): xe có bánh nằm ngang — đừng leo lên xe đó.

**Vì sao LLM thất bại?** Hai thiếu sót:

1. **Visual intelligence**: không có 3D understanding.
2. **Physical intelligence**: không biết simulate. Không có "certificate of performance" — không cách nào tự kiểm tra xem thiết kế có chạy được không.

Bài học: **simulation là không thể thiếu** trong design pipeline. Cho dù dùng LLM/diffusion để propose, vẫn phải có simulator để verify.

##### DiffuseBot

Đây là contribution mới nhất Andy giới thiệu. Pipeline:

1. **Text spec**: "soft robot có thể grasp strawberry".
2. **Diffusion model proposes geometry**: dùng Point-E (off-the-shelf 3D point cloud diffusion từ OpenAI).
3. **K-means clustering** trên geometry → quyết định nơi đặt actuators.
4. **Robotization**: dense-ify point cloud thành mesh có thể simulate (differentiable).
5. **Simulation evaluates**: chạy task, tính reward.
6. **Gradient từ simulation** được dùng để **bias diffusion process** ở iteration tiếp theo.
7. Lặp lại — diffusion dần "dịch chuyển" embedding về vùng generate ra robots high-performance.

Điểm mới về kỹ thuật: thay vì conditioning diffusion bằng text embedding hoặc CLIP image embedding, **conditioning bằng simulation gradient**. Đây là cầu nối giữa generative AI và physics-based optimization.

Kết quả: robots **đẹp + functional + có thể fabricate**. Có thể trade off bằng cách thêm CLIP loss cho aesthetics: "tôi muốn nó tròn hơn" hoặc "rộng hơn".

### 5.8. Sensor placement codesign

Project riêng nhưng cùng paradigm: thay vì gắn sensor "ở chỗ trông hợp lý", để thuật toán tìm ra.

#### Setup

- Robot soft, dạng gripper.
- Task: **classify** vật đang grasp (tròn, tam giác, hình thoi, hoặc rỗng).
- Design space: vị trí đặt strain sensors trên gripper.

#### Trick: sparse mask trong neural network

Mỗi điểm trên gripper có một weight $w_i \in [0, 1]$ trong input layer của classifier. Loss:

$$
L = L_{\text{classify}} + \lambda \|w\|_1
$$

Phần $\|w\|_1$ ép hầu hết $w_i$ về 0 — chỉ giữ lại vài sensor "quan trọng nhất". Sau training, đọc các $w_i \neq 0$ → đó là vị trí đặt sensor.

#### Kết quả

- **5 sensor đặt đúng** đủ để classify với accuracy cao.
- **Sensor đặt ngẫu nhiên** thường tệ.
- **Sensor đặt bởi human** thường rơi vào các vùng "trông geometrically đặc biệt" (góc cạnh, đầu finger), nhưng **không phải** vùng có chuyển động lớn nhất.
- Thuật toán hội tụ về các vùng có **deformation cao** khi grasp — đó là nơi tín hiệu strain mang nhiều thông tin nhất.

Lại một lần nữa: trực giác con người ưu tiên "geometry interesting", thuật toán ưu tiên "thông tin về task". Hai tiêu chí khác nhau.

### 5.9. Fabrication: từ ảo sang thật

Đây là chỗ chưa được giải tốt.

#### Vấn đề

Optimal soft robot có thể có **gradient vật liệu liên tục** — mỗi voxel một độ cứng khác nhau. Không quy trình fabrication nào hiện tại in được điều này.

#### Giải pháp đang thử: machine knitting

- Dùng máy dệt kim với vài loại sợi (elastic, conductive, thường).
- Mỗi loại stitch tạo ra micro-structure có stiffness khác nhau.
- Bằng cách **patch các stitches khác nhau** trên cùng tấm vải, tạo ra "regions" với property khác nhau — xấp xỉ gradient liên tục.
- Vải dẫn điện tích hợp luôn strain sensors.

Đây là một ví dụ về **abstraction layer** giữa virtual design và fabrication: thay vì thiết kế ở mức voxel, thiết kế ở mức "patch của stitch type" — discrete và fabricable.

### 5.10. Sim-to-real gap

Vấn đề muôn thuở. Hierarchy giải pháp:

1. **Better modeling**: simulator chính xác hơn — luôn đánh đổi với speed.
2. **System identification**: dùng video real-world để fit lại parameters của simulator.
3. **Domain randomization**: train trên ensemble simulator với parameters ngẫu nhiên → policy robust với mismatch.
4. **Online adaptation**: fine-tune controller sau khi deploy. Dễ hơn fine-tune body (đã built).
5. **Hybrid simulation**: kết hợp simulator analytical + neural residual model học từ real data.
6. **Real-world feedback loop**: fabricate fast, test, dùng dữ liệu cập nhật simulator → đề xuất design tiếp theo. Đây là tương lai mà tutorial gợi ý.

Friction là điểm sticking point thường gặp nhất — gần như mọi sim-to-real story đều đổ vỡ vì friction.

---

## 6. Câu hỏi mở và hướng tương lai

### 6.1. Foundation models cho design?

Hiện tại các thuật toán codesign vẫn task-specific: mỗi task train từ đầu. Liệu có một "foundation model cho thiết kế cơ thể" — pretrained trên hàng triệu (task, body) pair — có thể few-shot cho task mới?

Diễn giả Andy: "Tôi không biết, nhưng sẽ không ngạc nhiên nếu kết hợp các generative technologies (vision, physics, text) lại sẽ cho ra điều đó."

### 6.2. Cross-robot transfer

Hiện tại sim-to-real research thường về **một** robot cụ thể. Liệu có phương pháp giúp **bất kỳ** thiết kế nào do thuật toán đề xuất đều transfer được?

### 6.3. Spec-change adaptation

Khi yêu cầu task thay đổi sau khi đã build robot — robot có tự thích nghi không? Hiện tại chỉ controller có thể (qua online RL); body thì cố định.

### 6.4. Joint reasoning over all axes

Tutorial cho thấy từng project xử lý 1-2 trục thiết kế: chỉ vision (Andre), chỉ material + geometry (ChainQueen), chỉ sensor placement, chỉ generative geometry (DiffuseBot). **Chưa có phương pháp nào đồng thời lý luận về tất cả**: actuator + planning + topology + materials + sensing.

Tự nhiên làm điều đó — nhưng chậm khủng khiếp (4 tỉ năm). Câu hỏi là: liệu có meta-architecture nào cho phép thuật toán giải đồng thời mà không sụp đổ vì curse of dimensionality?

### 6.5. Democratization

Lý do thực tế khiến field này quan trọng: **giúp người không phải kỹ sư cơ khí thiết kế được robot**. Nếu thuật toán có thể nhận spec ngôn ngữ tự nhiên + sandbox simulator → output bản vẽ fabricable, thì rào cản nhập ngành giảm mạnh.

---

## 7. Glossary thuật ngữ

| Thuật ngữ | Nghĩa |
|---|---|
| **Acuity** | Độ phân giải thị giác, đo bằng cycles per degree |
| **Aperture** | Đường kính lỗ thu sáng của mắt/camera |
| **Backprop / Back-propagation** | Thuật toán tính gradient bằng chain rule, ngược từ output |
| **Bi-level optimization** | Tối ưu hai vòng lặp lồng nhau (outer = design, inner = controller) |
| **Bioluminescence** | Phát sáng sinh học (đom đóm, sinh vật biển sâu) |
| **Codesign / Co-design** | Đồng thời tối ưu body và brain |
| **Differentiable simulation** | Simulator mà mọi output có thể tính gradient với respect to mọi input |
| **Fovea** | Vùng retina có mật độ photoreceptor cao nhất |
| **Implicit integration** | Phương pháp tích phân số ổn định cho hệ stiff (Backward Euler...) |
| **Modulation Transfer Function (MTF)** | Hàm mô tả contrast giảm theo tần số không gian |
| **Morphology** | Cấu trúc cơ thể + cảm biến của agent |
| **MuJoCo / Taichi / NVIDIA Warp** | Differentiable physics frameworks |
| **No Free Lunch theorem** | Không có thuật toán tốt cho mọi task |
| **Photoreceptor** | Tế bào cảm thụ ánh sáng — đơn vị cơ bản của mắt |
| **Point-goal navigation** | Task điều hướng khi biết toạ độ mục tiêu |
| **Object-goal navigation** | Task điều hướng khi chỉ biết hình ảnh mục tiêu |
| **Sim-to-real gap** | Khoảng cách giữa hành vi trong simulator và trên robot thật |
| **Strange attractor** | Tập hấp dẫn fractal trong hệ động lực hỗn loạn (Lorenz...) |
| **Trajectory optimization** | Tối ưu hoá quỹ đạo dưới ràng buộc động lực học |
| **Voxel** | Pixel 3D — đơn vị thể tích cơ bản trong simulation |

---

## 8. Tài liệu đọc thêm

### 8.1. Papers / projects được nhắc trong tutorial

- **Karl Sims**, *Evolving Virtual Creatures* (1994) — paper kinh điển khởi đầu computational creature design.
- **ChainQueen** (Hu et al., 2019) — differentiable simulator cho soft robotics.
- **DiffuseBot** (Wang et al., 2023) — diffusion-based soft robot generation với simulation feedback.
- **EvoGym** — sandbox để chơi với evolutionary algorithms cho voxel robots.
- **Habitat** (Meta AI) — simulator cho indoor navigation, là nền tảng cho photoreceptor agent paper.
- **Matterport3D** — dataset 3D scans của các căn nhà thật.
- **Underactuated Robotics** (MIT, Russ Tedrake) — textbook online cho trajectory optimization và RL trong robotics.

### 8.2. Frameworks để thử ngay

| Tool | Use case |
|---|---|
| **Taichi** | Differentiable physics, dễ học nhất |
| **NVIDIA Warp** | Differentiable physics, tích hợp với PyTorch |
| **MuJoCo MJX** | Rigid body sim trên JAX, gradient available |
| **PyBullet / Gazebo** | Rigid body sim truyền thống (không differentiable) |
| **Genesis** (mới ra 2024) | Multi-physics, GPU-native, differentiable |

### 8.3. Đọc nền tảng

- **Russ Tedrake** *Underactuated Robotics* — chương về trajectory optimization và LQR.
- **Sutton & Barto**, *Reinforcement Learning: An Introduction* — cho phần policy learning.
- **Goodfellow, Bengio, Courville**, *Deep Learning* — chương 6-9 cho backprop.
- **Sönke Johnsen** *The Optics of Life: A Biologist's Guide to Light in Nature* — sách của chính diễn giả về optics sinh học, dễ đọc.

---

## Phụ lục — Một số insight cốt lõi cô đọng

Nếu chỉ giữ lại vài câu, đây là những điều quan trọng nhất:

1. **Trí tuệ không chỉ trong não.** Cá chết vẫn bơi vì cơ thể đã encode sẵn cách bơi. AI hiện tại bỏ qua điều này.

2. **Trực giác con người là source of bias.** Sọc ngựa vằn không phải để ngụy trang; sensor tối ưu chĩa xuống đất, không thẳng phía trước. Khi domain xa lạ, hãy để thuật toán quyết định.

3. **Số chiều của input không quyết định khả năng giải task.** 4 photoreceptor có thể navigate tốt như camera 128×128. Quan trọng là **đặt ở đâu**.

4. **Bi-level optimization có thể gập thành single rollout.** Đây là trick kỹ thuật quan trọng nhất của Andre — biến intractable thành tractable.

5. **Differentiable simulation là vũ khí mới.** Backprop xuyên qua vật lý cho phép tối ưu thân + não cùng lúc với hiệu quả mà evolutionary search không thể.

6. **Generative AI không thay được simulation.** ChatGPT đề xuất robot xe có bánh nằm ngang. Phải có simulator để verify — nhưng dùng cùng simulator để **bias** generative model là pipeline thắng cuộc (DiffuseBot).

7. **Sim-to-real vẫn là open problem.** Mọi thứ đẹp trong sim không đảm bảo work thật. Friction giết nhiều dự án nhất.

8. **Tự nhiên là benchmark.** Mỗi loài sinh vật là một thiết kế tối ưu cho ngách của nó. Hiểu được tự nhiên làm điều đó cho ta kim chỉ nam thiết kế thuật toán.

---

*Tài liệu này là tổng hợp và diễn giải nội dung từ tutorial gốc. Để chắc chắn về số liệu cụ thể (số mắt sò điệp, tỉ lệ phần trăm trong các paper benchmark, v.v.), nên đối chiếu với paper gốc hoặc liên hệ trực tiếp các tác giả.*
