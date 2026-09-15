# Kế hoạch viết báo cáo và phân công 11 người

## Mục tiêu và phạm vi

Hoàn thành báo cáo cho đề tài **Ứng dụng quy hoạch tuyến tính trong tối ưu hóa bài toán vận tải**. Báo cáo chỉ xét một loại hàng, nhiều kho đến nhiều khách hàng, chi phí tuyến tính và cung/cầu đã biết. Không mở rộng sang VRP, TSP hoặc MILP.

Ví dụ xuyên suốt là case study 3 kho và 5 khách hàng trong `docs/transportation-example.pdf`: giải tay theo Northwest Corner rồi MODI, sau đó kiểm chứng bằng HiGHS với chi phí tối ưu 696. Case study chỉ dùng để minh họa và kiểm chứng, không dùng để kết luận hiệu năng.

Kế hoạch giả định sáu tuần. Nếu thời hạn ngắn hơn, giữ nguyên các checkpoint và rút ngắn thời gian viết nháp, không bỏ bước kiểm chứng.

## Quy tắc làm việc

- Mỗi người chịu trách nhiệm một đầu ra có thể review độc lập.
- Chỉ người phụ trách phần đó được sửa nội dung chính; người khác góp ý qua review.
- Mọi hình, bảng, số liệu và kết quả thực nghiệm phải có nguồn hoặc log tái tạo được.
- Chỉ dùng kết quả chạy thật của sản phẩm trong Chương 4.
- Người 1 quản lý bản hợp nhất; không merge nội dung chưa được owner xác nhận.

## Phân công

| Người | Phần sở hữu | Đầu ra bàn giao |
|---|---|---|
| 1 | Điều phối và tích hợp | Outline cuối, glossary thuật ngữ, bản hợp nhất và checklist nộp bài |
| 2 | Chương 1 | Lý do chọn đề tài, bối cảnh, mục tiêu và phạm vi |
| 3 | Mục 2.1–2.4 | Khái niệm tối ưu, LP, biến/mục tiêu/ràng buộc, biểu diễn ma trận |
| 4 | Mục 2.5–2.8 | Miền khả thi, ứng dụng, transportation problem và network flow |
| 5 | Mục 2.9 | NW Corner, Least Cost, Vogel; ranh giới giữa nghiệm đầu và nghiệm tối ưu |
| 6 | Mục 3.1–3.5 | Standard form, basis/BFS, ví dụ LP nhỏ giải tay bằng Simplex |
| 7 | Mục 3.6–3.9 | Duality, interior point, MODI so với Simplex, lựa chọn HiGHS |
| 8 | Mục 2.10 | Case study 3 kho × 5 khách: dữ liệu, giải tay NW Corner → MODI, kết quả 696 |
| 9 | Mục 4.1–4.7 | Mục tiêu sản phẩm, mô hình LP, kiến trúc, chức năng và luồng xử lý |
| 10 | Mục 4.8–4.15 | Công nghệ, metrics, baseline, test cases, thực nghiệm và bảng kết quả |
| 11 | Kết luận và QA | Kết luận, tài liệu tham khảo, danh mục bảng/hình, format và slide demo |

## Tiến độ sáu tuần

### Tuần 1 — Chốt phạm vi và viết nháp nền tảng

- [ ] Người 1 chốt outline, template, thuật ngữ và quy tắc trích dẫn.
- [ ] Người 2–5 hoàn thành nháp Chương 1 và Chương 2.
- [ ] Người 8 kiểm tra lại dữ liệu case study: cung/cầu bằng 55, ma trận chi phí 3×5.
- [ ] Người 11 tạo checklist định dạng và nguồn tài liệu.

**Checkpoint tuần 1:** Mục lục không còn mục ngoài phạm vi; mọi phần lý thuyết có owner và nguồn sơ bộ.

### Tuần 2 — Thuật toán và case study

- [ ] Người 6 hoàn thành ví dụ Simplex cơ bản kích thước nhỏ.
- [ ] Người 7 hoàn thành phần duality, MODI và lý do dùng HiGHS.
- [ ] Người 8 hoàn thành đầy đủ các bước NW Corner, reduced cost, pivot và nghiệm 696.
- [ ] Người 1 review chéo Chương 2–3 để thống nhất ký hiệu $x_{ij}$, $c_{ij}$, cung và cầu.

**Checkpoint tuần 2:** Case study đạt 696 trên giấy; báo cáo không gọi NW Corner, Least Cost hoặc Vogel là phương pháp tối ưu.

### Tuần 3 — Mô tả sản phẩm

- [ ] Người 9 hoàn thành yêu cầu, kiến trúc, mô hình LP và các màn hình dự kiến.
- [ ] Người 10 chốt metrics, test cases và định dạng bảng thực nghiệm.
- [ ] Người 11 kiểm tra figure: tự vẽ lại tiếng Việt, có caption và nguồn.

**Checkpoint tuần 3:** Phần mềm được mô tả đúng phạm vi; HiGHS là solver sản phẩm, heuristic chỉ nằm trong phần học thuật.

### Tuần 4 — Lấy bằng chứng thực nghiệm

- [ ] Người 10 thu kết quả chạy thật: objective, constraint violation, runtime, memory.
- [ ] Người 9 cập nhật ảnh chụp/mô tả giao diện từ sản phẩm chạy được.
- [ ] Người 8 và 10 đối chiếu case study: HiGHS trả objective bằng 696.
- [ ] Người 1 cập nhật bảng kết quả chung.

**Checkpoint tuần 4:** Không còn placeholder cho kết quả, thời gian chạy hoặc ảnh giao diện.

### Tuần 5 — Review học thuật

- [ ] Mỗi người review một phần không thuộc mình.
- [ ] Người 11 rà citation, danh mục hình/bảng, lỗi chính tả và format.
- [ ] Người 1 giải quyết mâu thuẫn thuật ngữ, số liệu và tham chiếu chéo.

**Checkpoint tuần 5:** Toàn bộ công thức, nguồn và số liệu tái kiểm tra được.

### Tuần 6 — Hoàn tất và bảo vệ

- [ ] Render PDF, kiểm tra layout và liên kết mục lục.
- [ ] Chuẩn bị slide theo luồng: bối cảnh → mô hình → giải tay → phần mềm → thực nghiệm → kết luận.
- [ ] Chạy thử demo từ đầu với case study 696.
- [ ] Mỗi thành viên luyện phần thuyết trình do mình sở hữu.

**Definition of done:** PDF không lỗi layout; case study và sản phẩm cùng cho 696; toàn bộ hình/bảng có nguồn; demo chạy lại được theo README.

## Rủi ro và cách xử lý

| Rủi ro | Tác động | Cách xử lý |
|---|---|---|
| Các phần viết trùng hoặc lệch ký hiệu | Cao | Người 1 duy trì glossary và review hợp nhất mỗi tuần |
| Heuristic bị mô tả là solver tối ưu | Cao | Người 5 và 7 kiểm tra thuật ngữ; chỉ MODI/HiGHS được dùng cho nghiệm tối ưu |
| Bảng thực nghiệm không có dữ liệu thật | Cao | Người 10 chỉ nhận log từ runner; không điền số ước lượng |
| Figure sao chép không có nguồn | Trung bình | Tự vẽ lại, ghi nguồn dữ liệu và tác giả figure |
| Trễ phần riêng lẻ | Trung bình | Nộp nháp theo checkpoint; người 1 tái phân công trước tuần 4 |
