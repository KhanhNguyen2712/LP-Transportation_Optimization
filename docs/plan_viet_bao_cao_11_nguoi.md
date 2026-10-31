# Kế hoạch viết báo cáo và phân công 11 người

## Mục tiêu và phạm vi

Hoàn thành báo cáo cho đề tài **Ứng dụng quy hoạch tuyến tính trong tối ưu hóa bài toán vận tải**. Báo cáo chỉ xét một loại hàng, nhiều kho đến nhiều khách hàng, chi phí tuyến tính và cung/cầu đã biết. Không mở rộng sang bài toán định tuyến phương tiện (VRP), bài toán người bán hàng (TSP) hoặc quy hoạch tuyến tính nguyên hỗn hợp (MILP); các hướng đó chỉ được nêu ở mục 4.15 như hướng phát triển.

Báo cáo gồm 5 chương và tài liệu tham khảo, bám theo đúng số mục của bản đề xuất (`docs/proposal/proposal_final.md`): Chương 1 (1.1–1.6), Chương 2 (2.1–2.10), Chương 3 (3.1–3.9), Chương 4 (4.1–4.15), Chương 5 Kết luận.

Phân bổ độ dài theo bản đề xuất: lý thuyết Chương 2 + 3 là 8–10 trang A4 (trong đó Chương 2 khoảng 3–4 trang, Chương 3 khoảng 5–6 trang), phần mềm Chương 4 là 5–8 trang, kết luận 1 trang, tài liệu tham khảo 1–2 trang; tổng 16–22 trang A4, không tính phụ lục.

Ví dụ xuyên suốt là bài toán 3 kho và 5 khách hàng trong `docs/proposal/transportation-example.pdf`: kho A, B, C có cung 18, 25, 12; khách V, W, X, Y, Z có cầu 14, 6, 8, 10, 17; tổng cung = tổng cầu = 55. Giải tay theo phương pháp góc tây bắc rồi cải thiện bằng thế vị (MODI) cho chi phí tối ưu 696; phần mềm dùng bộ giải HiGHS phải trả lại đúng 696. Ví dụ này chỉ dùng để minh họa và kiểm chứng, không dùng để kết luận về tốc độ.

Kế hoạch giả định sáu tuần. Nếu thời hạn ngắn hơn, giữ nguyên các mốc kiểm tra và rút ngắn thời gian viết bản nháp, không bỏ bước kiểm chứng.

## Quy tắc làm việc

- Mỗi người chịu trách nhiệm một phần việc có thể rà soát độc lập.
- Chỉ người phụ trách phần đó được sửa nội dung chính; người khác góp ý khi rà soát.
- Mọi hình, bảng, số liệu và kết quả thực nghiệm phải có nguồn hoặc nhật ký chạy lại được.
- Chỉ dùng kết quả chạy thật của sản phẩm trong Chương 4.
- Người 1 quản lý bản hợp nhất và cũng là người phụ trách Chương 1; không ghép nội dung khi người phụ trách chưa xác nhận.
- Ký hiệu dùng chung toàn báo cáo: $m$ kho, $n$ khách, $s_i$ cung, $d_j$ cầu, $c_{ij}$ chi phí đơn vị, $x_{ij}$ lượng hàng, $B$ cơ sở, $B^{-1}b$ nghiệm cơ sở.

## Phân công

Chương 1 được gộp vào vai trò điều phối và tích hợp (Người 1), nhờ đó Chương 3 được chia cho 3 người (Người 6–8) mà tổng vẫn đủ 11 người.

| Người | Phần sở hữu                                                   | Nộp gì (tóm tắt)                                                                              |
| ------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| 1       | Điều phối, tích hợp + Chương 1                            | Đề cương, bảng ký hiệu, bản hợp nhất, danh sách kiểm tra; Chương 1                  |
| 2       | Mục 2.1–2.4                                                    | Khái niệm tối ưu, quy hoạch tuyến tính, thành phần mô hình, biểu diễn ma trận       |
| 3       | Mục 2.5–2.8                                                    | Miền nghiệm khả thi, ứng dụng thực tế, bài toán vận tải, liên hệ luồng mạng        |
| 4       | Mục 2.9                                                         | Ba cách lập nghiệm ban đầu và bảng chi phí khởi tạo trên bộ dữ liệu 3×5            |
| 5       | Mục 2.10                                                        | Bộ dữ liệu 3×5, các bảng giải tay và chi phí tối ưu                                    |
| 6       | Mục 3.1–3.3                                                    | Dạng chuẩn, cơ sở đại số tuyến tính, nghiệm cơ sở khả thi                            |
| 7       | Mục 3.4–3.5                                                    | Ý tưởng hình học và thuật toán Simplex, kèm ví dụ giải tay                            |
| 8       | Mục 3.6–3.9                                                    | Đối ngẫu, phương pháp điểm trong, cấu trúc ma trận vận tải, cách chọn thuật toán |
| 9       | Mục 4.1–4.7 (Code)                                             | Mục tiêu sản phẩm, dữ liệu vào, mô hình toán, kiến trúc, chức năng                  |
| 10      | Mục 4.8–4.15 (Code)                                            | Công nghệ, quy trình xử lý, cách đánh giá, mốc so sánh, thực nghiệm, kiểm thử      |
| 11      | Kết luận, tài liệu tham khảo và kiểm soát chất lượng | Chương 5, tài liệu tham khảo, danh mục bảng/hình, định dạng.                           |

### Người 1 — Điều phối, tích hợp và Chương 1

**Việc cần làm**

- Viết Chương 1 theo bản đề xuất: 1.1 lý do chọn đề tài (chi phí vận chuyển, ví dụ 10 kho × 100 điểm = 1000 biến quyết định); 1.2 bối cảnh với ký hiệu $m$, $n$, $s_i$, $d_j$, $c_{ij}$, $x_{ij}$ và hàm mục tiêu $\sum_i\sum_j c_{ij}x_{ij}$; 1.3 mục tiêu tổng quát và 9 mục tiêu cụ thể; 1.4 đối tượng và phạm vi; 1.5 phương pháp nghiên cứu bốn bước; 1.6 kết quả dự kiến (báo cáo lý thuyết và phần mềm).
- Chốt đề cương chi tiết và bảng ký hiệu dùng chung, buộc mọi chương dùng thống nhất một bộ ký hiệu.
- Ghép bản thảo của 11 người thành bản hợp nhất, kiểm tra chéo phần tham chiếu giữa các chương, chạy danh sách kiểm trước khi nộp.

**Nộp gì**

- **1 bản Chương 1 hoàn chỉnh** (mục 1.1–1.6), dài 1–2 trang A4.
- **1 đề cương chi tiết đã chốt**, ghi rõ mỗi mục do ai viết và nộp khi nào.
- **1 bảng ký hiệu dùng chung** cho cả báo cáo (kho, khách, cung, cầu, chi phí, lượng hàng, cơ sở).
- **1 bản hợp nhất toàn báo cáo**, ghép nội dung của cả 11 người thành một tệp duy nhất.
- **1 danh sách kiểm trước khi nộp**, gồm 4 mục: tệp PDF, bài trình bày, hướng dẫn chạy phần mềm và nhật ký chạy thực nghiệm.

**Xong khi:** mọi mục trong đề cương đều có người phụ trách và nguồn; không còn mục ngoài phạm vi (VRP, TSP, MILP chỉ xuất hiện ở mục 4.15); ký hiệu thống nhất trên toàn báo cáo.

### Người 2 — Mục 2.1–2.4: khái niệm và mô hình

**Việc cần làm**

- 2.1 Khái niệm tối ưu hóa: bài toán dạng $\min_x f(x)$, phân biệt quy hoạch tuyến tính với các lớp bài toán tối ưu khác.
- 2.2 Quy hoạch tuyến tính: hàm mục tiêu tuyến tính, ràng buộc tuyến tính, vì sao lớp bài toán này giải được hiệu quả.
- 2.3 Các thành phần của mô hình: biến quyết định, hàm mục tiêu, ràng buộc, minh họa bằng $x_{ij}$.
- 2.4 Biểu diễn bằng đại số tuyến tính: vector $c$, $x$ và ma trận $A$, $b$; dạng $Ax \leq b$, $x \geq 0$.

**Nộp gì**

- **1 bản thảo mục 2.1–2.4**, dài khoảng 2 trang A4.
- **1 bảng ký hiệu cho riêng phần này**, khớp với bảng ký hiệu dùng chung của Người 1.
- **Mỗi khái niệm kèm 1 ví dụ số nhỏ** để người đọc tự kiểm lại được, không chỉ có định nghĩa suông.

**Xong khi:** bảng ký hiệu khớp bảng ký hiệu dùng chung; không còn khái niệm nào chỉ có định nghĩa mà thiếu ví dụ.

### Người 3 — Mục 2.5–2.8: miền khả thi, ứng dụng, bài toán vận tải

**Việc cần làm**

- 2.5 Miền nghiệm khả thi $\mathcal{P}=\{x \mid Ax \leq b\}$, đa diện lồi, tính chất nghiệm tối ưu hữu hạn thì đạt tại đỉnh.
- 2.6 Ứng dụng thực tế: sản xuất, phân bổ tài nguyên, nông nghiệp, năng lượng, logistics (mỗi ứng dụng 1–2 câu).
- 2.7 Bài toán vận tải: biến $x_{ij}$, hàm mục tiêu, ràng buộc cung và cầu, điều kiện cân bằng $\sum_i s_i = \sum_j d_j$.
- 2.8 Liên hệ bài toán luồng trên mạng: sơ đồ kho → khách hàng, ma trận liên thuộc và nhận xét.

**Nộp gì**

- **1 bản thảo mục 2.5–2.8**.
- **1 hình vẽ miền nghiệm khả thi**, tự vẽ lại bằng tiếng Việt, có chú thích và ghi nguồn.
- **1 sơ đồ mạng kho → khách hàng**, tự vẽ lại bằng tiếng Việt, có chú thích và ghi nguồn.
- **Công thức ở mục 2.7 phải giống đúng** công thức đã nêu ở mục 1.2.

**Xong khi:** mỗi hình đều có chú thích, nguồn dữ liệu, không sao chép nguyên hình từ tài liệu gốc.

### Người 4 — Mục 2.9: các phương pháp lập nghiệm ban đầu

**Việc cần làm**

- Trình bày ba cách lập nghiệm ban đầu, mỗi cách nêu rõ từng bước phân bổ: góc tây bắc (Northwest Corner), chi phí nhỏ nhất (Least Cost), Vogel.
- Chạy cả ba cách trên chính ma trận chi phí 3×5 của ví dụ xuyên suốt, để so sánh trực tiếp với mục 2.10.
- Nêu rõ ranh giới: ba cách này chỉ tạo nghiệm ban đầu, không chứng minh tối ưu; nghiệm chỉ được cải thiện và kiểm tra bằng MODI hoặc Simplex vận tải.
- Nêu cách xử lý khi tổng cung lớn hơn tổng cầu: thêm một khách hàng giả có nhu cầu bằng phần cung dư và chi phí bằng 0.

**Nộp gì**

- **1 bản thảo mục 2.9**, trong đó mỗi cách có phần trình bày từng bước riêng.
- **1 bảng so sánh chi phí khởi tạo của ba cách**, tính trên đúng bộ dữ liệu 3 kho × 5 khách của mục 2.10, kèm nhận xét cách nào cho chi phí thấp nhất.

**Xong khi:** bảng so sánh phân biệt rõ "chi phí khởi tạo" và "chi phí tối ưu sau MODI"; không chỗ nào gọi ba cách lập nghiệm ban đầu là phương pháp tối ưu.

### Người 5 — Mục 2.10: ví dụ xuyên suốt 3 kho × 5 khách hàng

**Việc cần làm**

- Chốt bảng dữ liệu: cung A/B/C = 18/25/12, cầu V/W/X/Y/Z = 14/6/8/10/17, tổng 55, kèm ma trận chi phí 3×5.
- Trình bày đầy đủ các bước giải tay: lập nghiệm ban đầu bằng góc tây bắc, tính thế vị hàng và cột, tính đại lượng kiểm $c_{ij}-v_i-w_j$ (test value), chọn ô vào, dựng vòng kín và xoay.
- Ghi lại bốn bước xoay tại các ô BV, AY, AX, CW và nghiệm tối ưu $x_{AX}=8$, $x_{AY}=10$, $x_{BV}=14$, $x_{BZ}=11$, $x_{CW}=6$, $x_{CZ}=6$.
- Chốt chi phí tối ưu $8(15)+10(10)+14(15)+11(10)+6(14)+6(12)=696$ và ghi chú ô CV có đại lượng kiểm bằng 0 nên bài toán có nhiều nghiệm tối ưu.
- Tự vẽ lại bảng và hình bằng tiếng Việt, ghi nguồn `transportation-example.pdf`.

**Nộp gì**

- **1 bản thảo mục 2.10**, gồm 4 bảng: bảng dữ liệu (cung, cầu, chi phí), bảng nghiệm ban đầu theo góc tây bắc, bảng thế vị và đại lượng kiểm của từng vòng, bảng nghiệm cuối.
- **1 dòng kết luận chi phí nhỏ nhất bằng 696**, kèm lời giải thích vì sao ô CV có đại lượng kiểm bằng 0 và bài toán có nhiều nghiệm tối ưu.
- **1 ghi chú** nêu rõ con số 696 dùng để đối chiếu với kết quả của phần mềm ở Chương 4.

**Xong khi:** người khác đọc lại có thể tự kiểm từng bảng và ra đúng 696; không có bước nào ghi kết quả mà thiếu bảng trung gian.

### Người 6 — Mục 3.1–3.3: nền tảng đại số của quy hoạch tuyến tính

**Việc cần làm**

- 3.1 Dạng chuẩn: $\max c^Tx$ với $Ax=b$, $x \geq 0$; cách chuyển bài toán gốc về dạng chuẩn bằng biến bù (slack/surplus).
- 3.2 Cơ sở đại số tuyến tính: $A \in \mathbb{R}^{m \times n}$, hạng của ma trận, chọn $m$ cột độc lập tuyến tính tạo thành cơ sở $B$, công thức $B^{-1}b$ và $B^{-1}N$.
- 3.3 Nghiệm cơ sở và nghiệm cơ sở khả thi: điều kiện $x_B = B^{-1}b \geq 0$, khái niệm nghiệm suy biến.

**Nộp gì**

- **1 bản thảo mục 3.1–3.3**.
- **1 ví dụ số nhỏ**: đưa một bài toán về dạng chuẩn, chọn một cơ sở, tính nghiệm cơ sở khả thi, để người đọc kiểm lại bằng tay.
- **1 đoạn đối chiếu với mục 2.10**: nghiệm tối ưu ở đó chỉ có 6 ô dương trong khi cơ sở có $m+n-1=7$ biến, nghĩa là nghiệm suy biến; ghi rõ nhận xét này, hoặc báo lại Người 1 nếu kiểm ra kết quả khác.

**Xong khi:** ví dụ số chạy tay kiểm lại được; ký hiệu $B$, $N$, $x_B$ khớp bảng ký hiệu dùng chung và không đổi ở mục 3.4–3.5.

### Người 7 — Mục 3.4–3.5: thuật toán Simplex

**Việc cần làm**

- 3.4 Ý tưởng hình học: Simplex di chuyển giữa các đỉnh kề của miền khả thi thay vì kiểm tra mọi điểm.
- 3.5 Thuật toán Simplex: các bước chuẩn hóa bài toán, lập nghiệm cơ sở khả thi ban đầu, chọn biến vào theo chi phí giảm (reduced cost), phép thử tỉ lệ (ratio test) để chọn biến ra, xoay bảng, kiểm tra điều kiện tối ưu và dừng.
- Giải tay một ví dụ nhỏ (dưới 5 biến) hết các bảng, kèm bảng đơn hình (tableau) viết bằng tiếng Việt.

**Nộp gì**

- **1 bản thảo mục 3.4–3.5**.
- **1 hình vẽ đường đi của thuật toán** qua các đỉnh của miền khả thi, có chú thích.
- **Bộ bảng đơn hình đầy đủ** của 1 ví dụ nhỏ dưới 5 biến, ghi từng bước xoay cho đến khi đạt tối ưu.
- **Kết quả ví dụ nhỏ** phải khớp với kết quả chạy bằng phần mềm.

**Xong khi:** các bước mô tả ở mục 3.5 khớp với bảng đơn hình đã trình bày; không mô tả thuật toán chung chung mà thiếu ví dụ chạy tay.

### Người 8 — Mục 3.6–3.9: đối ngẫu, điểm trong, cấu trúc và cách chọn thuật toán

**Việc cần làm**

- 3.6 Bài toán đối ngẫu: đối chiếu bài toán gốc $\min c^Tx$ với bài toán đối ngẫu $\max b^Ty$, tính chất đối ngẫu mạnh, và ý nghĩa giá đối ngẫu (thêm một đơn vị năng lực thì chi phí tối ưu cải thiện bao nhiêu).
- 3.7 Phương pháp điểm trong: khác biệt với Simplex, đường đi qua nội miền và trường hợp phù hợp.
- 3.8 Cấu trúc ma trận của bài toán vận tải: dùng đúng ví dụ 2×3 của bản đề xuất (vector $x=[x_{11},\dots,x_{23}]^T$ và ma trận ràng buộc cung/cầu), chỉ ra ma trận thưa, có $m+n$ ràng buộc nhưng hạng chỉ $m+n-1$, nên nghiệm cơ sở có $m+n-1$ biến.
- 3.9 Phương pháp giải tay và cách chọn thuật toán: vì sao ví dụ xuyên suốt dùng góc tây bắc + MODI thay vì bảng đơn hình Simplex tổng quát, và vì sao sản phẩm dùng HiGHS.

**Nộp gì**

- **1 bản thảo mục 3.6–3.9**, dài khoảng 2–3 trang A4.
- **Trong mục 3.8**: giữ đúng ví dụ ma trận 2×3 của bản đề xuất và nêu hệ quả là nghiệm cơ sở có $m+n-1$ biến.
- **1 kết luận ngắn về cách chọn thuật toán**, thống nhất với mục 4.8 và hướng dẫn chạy của phần mềm.

**Xong khi:** giải thích được vì sao ma trận vận tải có $m+n$ ràng buộc nhưng hạng chỉ $m+n-1$; phần chọn thuật toán không mâu thuẫn với mô tả sản phẩm ở Chương 4.

### Người 9 — Mục 4.1–4.7: mô tả sản phẩm

**Việc cần làm**

- 4.1 Tên sản phẩm: TransportOpt – Hệ thống tối ưu phương án vận chuyển bằng quy hoạch tuyến tính.
- 4.2 Mục tiêu sản phẩm: nhận dữ liệu kho, khách hàng, cung, cầu, chi phí và trả về phương án tối ưu kèm báo cáo chi phí.
- 4.3 Dữ liệu đầu vào: bảng năng lực kho, danh sách khách hàng, ma trận chi phí.
- 4.4 Mô hình toán: biến $x_{ij} \geq 0$, hàm mục tiêu $\min \sum_i\sum_j c_{ij}x_{ij}$, ràng buộc cung và cầu.
- 4.5 Kết quả mong đợi: bảng tuyến vận chuyển, tổng chi phí, trạng thái lời giải và cảnh báo khi dữ liệu không hợp lệ.
- 4.6 Kiến trúc phần mềm: nhập liệu → kiểm tra dữ liệu → dựng mô hình → bộ giải HiGHS, khớp các phần trong `src/transportopt/`.
- 4.7 Các chức năng chính: thêm/sửa/xóa kho và khách hàng, nhập cung cầu chi phí, kiểm tra dữ liệu, giải và xem kết quả.

**Nộp gì**

- **1 bản thảo mục 4.1–4.7**.
- **1 ví dụ số 2×3** (kho W1 sức chứa 80, kho W2 sức chứa 70) cho ra các tuyến 50/30/30/40 và tổng chi phí 620, khớp với bộ dữ liệu mẫu `case_2x3.json`.
- **Ảnh chụp màn hình** lấy từ ứng dụng đang chạy, không dùng hình vẽ minh họa thay thế.

**Xong khi:** mọi bảng và hình trong mục 4.1–4.7 khớp với `app.py` và bộ dữ liệu mẫu thật; không có chức năng nào được mô tả mà sản phẩm chưa có.

### Người 10 — Mục 4.8–4.15: công nghệ, cách đánh giá và thực nghiệm

**Việc cần làm**

- 4.8 Công nghệ đề xuất: Python, NumPy, Pandas, SciPy HiGHS, Streamlit (khớp `pyproject.toml`).
- 4.9 Quy trình xử lý: nhập dữ liệu → kiểm tra dữ liệu → dựng mô hình → giải → hiển thị kết quả.
- 4.10 Cách đánh giá: chi phí tối ưu $C^*$, mức vi phạm ràng buộc, thời gian chạy, bộ nhớ và cách đo từng chỉ tiêu.
- 4.11 Mốc so sánh: bảng phân biệt góc tây bắc, Least Cost, Vogel (chi phí khởi tạo), MODI (chi phí tối ưu) và HiGHS (đối chứng).
- 4.12 Thực nghiệm: năm nhóm dữ liệu 2×3, 5×10, 10×50, 50×100, 100×500 (từ 6 đến 50.000 biến), giá trị khởi tạo ngẫu nhiên 17, bảng kết quả lấy từ `runs/experiments.csv`.
- 4.13 Giao diện dự kiến: màn hình nhập liệu, màn hình kết quả và bản đồ nhiệt của ma trận lượng hàng vận chuyển.
- 4.14 Các trường hợp kiểm thử theo bản đề xuất: cung = cầu (cân bằng), cung > cầu (dư năng lực không dùng hết), cung < cầu (vô nghiệm), một tuyến có chi phí rất lớn; đối chiếu với các bài kiểm thử đang có trong `tests/`.
- 4.15 Hướng mở rộng: nhiều loại hàng ($x_{ijp}$), quy hoạch tuyến tính nguyên hỗn hợp, bài toán định vị kho, bài toán định tuyến phương tiện, tối ưu hóa ngẫu nhiên — chỉ nêu hướng, không triển khai.

**Nộp gì**

- **1 bản thảo mục 4.8–4.15**.
- **1 bảng kết quả thực nghiệm cho 5 nhóm dữ liệu**, mỗi dòng đủ 8 cột: giá trị khởi tạo ngẫu nhiên (seed), số kho, số khách, giá trị hàm mục tiêu (objective), thời gian chạy (runtime), bộ nhớ (memory), trạng thái (status), mức vi phạm ràng buộc lớn nhất (maximum_violation).
- **1 phần hướng dẫn chạy lại**, gồm câu lệnh `scripts/run_experiments.py`, vị trí tệp kết quả `runs/experiments.csv` và cách đọc từng cột trong bảng.

**Xong khi:** mọi số trong bảng thực nghiệm lấy trực tiếp từ tệp CSV do chương trình chạy thực nghiệm sinh ra, không điền ước lượng; người khác chạy lại lệnh trong `README.md` là ra đúng bảng đó.

### Người 11 — Chương 5, tài liệu tham khảo và kiểm soát chất lượng

**Việc cần làm**

- Chương 5 Kết luận: tóm tắt ba trụ nội dung (đại số tuyến tính, quy hoạch tuyến tính, bài toán vận tải), quy trình dữ liệu → biểu diễn ma trận → mô hình quy hoạch tuyến tính → bộ giải → phương án vận chuyển tối ưu, kết quả đạt được và giới hạn của phiên bản hiện tại.
- Hoàn thiện danh mục tài liệu tham khảo [1]–[14] và chuẩn hóa cách trích dẫn trong toàn báo cáo.
- Kiểm soát chất lượng: danh mục bảng và hình, kiểm tra định dạng, chính tả, liên kết mục lục.

**Nộp gì**

- **1 bản Chương 5 Kết luận**, dài khoảng 1 trang A4.
- **1 danh mục tài liệu tham khảo** đầy đủ 14 nguồn, trình bày thống nhất một kiểu.
- **1 danh mục bảng và hình của cả báo cáo**, mỗi mục có số thứ tự, tên gọi và nguồn.
- **1 bài thuyết trình** theo đúng luồng: bối cảnh → mô hình → giải tay → phần mềm → thực nghiệm → kết luận.

**Xong khi:** tệp PDF không lỗi bố cục; mọi bảng và hình đều có số thứ tự, chú thích và nguồn.

## Tiến độ sáu tuần

### Tuần 1 — Chốt phạm vi và viết bản nháp nền tảng

- [ ] Người 1 chốt đề cương, mẫu trình bày, bảng ký hiệu và quy tắc trích dẫn; viết bản nháp Chương 1 (1.1–1.6).
- [ ] Người 2–5 hoàn thành bản nháp Chương 2 (2.1–2.10).
- [ ] Người 6–8 dựng khung Chương 3 (3.1–3.9): đủ đề mục, công thức chính và ví dụ số dự kiến.
- [ ] Người 5 chốt dữ liệu ví dụ xuyên suốt: cung 18/25/12, cầu 14/6/8/10/17, tổng 55, ma trận chi phí 3×5.
- [ ] Người 8 kiểm tra độc lập dữ liệu ví dụ xuyên suốt bằng cách đọc lại `transportation-example.pdf`.
- [ ] Người 11 tạo danh sách kiểm định dạng và danh mục nguồn tài liệu.

**Mốc kiểm tra tuần 1:** Mục lục khớp đúng số mục của bản đề xuất (1.1–1.6, 2.1–2.10, 3.1–3.9, 4.1–4.15, Kết luận); mọi mục lý thuyết đều có người phụ trách và nguồn sơ bộ.

### Tuần 2 — Thuật toán và ví dụ xuyên suốt

- [ ] Người 6 chốt mục 3.1–3.3 kèm ví dụ số chuyển về dạng chuẩn và nghiệm cơ sở khả thi.
- [ ] Người 7 hoàn thành mục 3.4–3.5 kèm ví dụ bảng đơn hình nhỏ giải tay đến tối ưu.
- [ ] Người 8 hoàn thành mục 3.6–3.9, trong đó mục 3.8 giữ ví dụ ma trận 2×3 của bản đề xuất và nêu hệ quả hạng $m+n-1$.
- [ ] Người 4 hoàn thành mục 2.9 kèm bảng chi phí khởi tạo của ba cách trên bộ dữ liệu 3×5.
- [ ] Người 5 hoàn thành đầy đủ các bước góc tây bắc, đại lượng kiểm, bốn bước xoay và nghiệm 696.
- [ ] Người 1 rà soát chéo Chương 2–3 để thống nhất ký hiệu $x_{ij}$, $c_{ij}$, $s_i$, $d_j$.

**Mốc kiểm tra tuần 2:** Ví dụ xuyên suốt đạt 696 khi giải trên giấy; Chương 3 không còn mục trống; báo cáo không gọi ba cách lập nghiệm ban đầu là phương pháp tối ưu.

### Tuần 3 — Mô tả sản phẩm

- [ ] Người 9 hoàn thành mục 4.1–4.7: tên sản phẩm, mục tiêu, dữ liệu vào, mô hình toán, kết quả mong đợi, kiến trúc và chức năng.
- [ ] Người 10 chốt mục 4.8–4.12: công nghệ, quy trình xử lý, chỉ tiêu đo, mốc so sánh và khung bảng thực nghiệm.
- [ ] Người 9 và Người 10 đối chiếu mục 4.14 với các bài kiểm thử đang có trong `tests/`.
- [ ] Người 11 kiểm tra hình: tự vẽ lại bằng tiếng Việt, có chú thích và nguồn.

**Mốc kiểm tra tuần 3:** Phần mềm được mô tả đúng phạm vi phiên bản 1; HiGHS là bộ giải của sản phẩm; các cách lập nghiệm ban đầu chỉ nằm ở phần học thuật 2.9 và 3.9.

### Tuần 4 — Lấy bằng chứng thực nghiệm

- [ ] Người 10 chạy `scripts/run_experiments.py` với giá trị khởi tạo ngẫu nhiên 17 và lấy `runs/experiments.csv` cho 5 nhóm dữ liệu từ 2×3 đến 100×500.
- [ ] Người 9 cập nhật ảnh giao diện và bảng kết quả mục 4.5 từ ứng dụng đang chạy.
- [ ] Người 5 và Người 10 đối chiếu ví dụ 3×5: giải tay 696 phải bằng kết quả của HiGHS.
- [ ] Người 1 cập nhật bảng kết quả chung và bản hợp nhất.

**Mốc kiểm tra tuần 4:** Không còn chỗ trống cho kết quả, thời gian chạy hoặc ảnh giao diện; mọi số trong Chương 4 truy được về tệp CSV hoặc nhật ký chạy.

### Tuần 5 — Rà soát học thuật

- [ ] Mỗi người rà soát một phần không thuộc mình: 2↔3, 4↔5, 6↔7↔8 xoay vòng, 9↔10.
- [ ] Người 8 rà lại toàn bộ công thức Chương 3 và phần chọn thuật toán.
- [ ] Người 11 rà trích dẫn, danh mục hình/bảng, lỗi chính tả và định dạng.
- [ ] Người 1 giải quyết mâu thuẫn về thuật ngữ, số liệu và tham chiếu chéo.

**Mốc kiểm tra tuần 5:** Toàn bộ công thức, nguồn và số liệu tái kiểm tra được; không còn hai chỗ định nghĩa khác nhau cho cùng một ký hiệu.

### Tuần 6 — Hoàn tất và bảo vệ

- [ ] Người 1 xuất tệp PDF, kiểm tra bố cục, liên kết mục lục và danh sách kiểm trước khi nộp.
- [ ] Người 11 chốt bài trình bày theo luồng bối cảnh → mô hình → giải tay → phần mềm → thực nghiệm → kết luận.
- [ ] Người 9 chạy thử sản phẩm từ đầu với bộ dữ liệu mẫu 3×5 theo `README.md` và xác nhận kết quả 696.
- [ ] Mỗi thành viên luyện phần thuyết trình do mình phụ trách.

**Điều kiện hoàn thành:** tệp PDF không lỗi bố cục; ví dụ xuyên suốt giải tay và sản phẩm cùng cho 696; toàn bộ hình và bảng có nguồn; bảng thực nghiệm chạy lại được theo `README.md`; phần trình diễn chạy lại được theo hướng dẫn.

## Rủi ro và cách xử lý

| Rủi ro                                                         | Tác động | Cách xử lý                                                                                                 |
| --------------------------------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------- |
| Các phần viết trùng nhau hoặc lệch ký hiệu              | Cao         | Người 1 duy trì bảng ký hiệu và rà soát bản hợp nhất mỗi tuần                                   |
| Chương 3 chia cho 3 người nên dễ lệch ký hiệu          | Cao         | Người 6–8 dùng chung bảng ký hiệu; Người 8 chốt phần chọn thuật toán nối vào mục 4.8         |
| Ba cách lập nghiệm ban đầu bị mô tả sai thành tối ưu | Cao         | Người 4 (mục 2.9) và Người 8 (mục 3.9) kiểm tra thuật ngữ; chỉ MODI và HiGHS cho nghiệm tối ưu |
| Chương 1 và việc điều phối dồn cho một người         | Trung bình | Người 1 chốt Chương 1 trong tuần 1 rồi mới chuyển sang ghép bản hợp nhất                         |
| Bảng thực nghiệm không có dữ liệu thật                  | Cao         | Người 10 chỉ lấy số từ`runs/experiments.csv`; không điền số ước lượng                         |
| Hình sao chép không có nguồn                               | Trung bình | Tự vẽ lại bằng tiếng Việt, ghi nguồn dữ liệu và tác giả hình                                     |
| Trễ phần việc riêng lẻ                                     | Trung bình | Nộp bản nháp theo từng mốc kiểm tra; Người 1 chia lại việc trước tuần 4                          |
