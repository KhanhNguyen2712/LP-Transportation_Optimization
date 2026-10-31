# Hồ sơ thực nghiệm TransportOpt ngày 31/10/2026

Bộ chạy đã hoàn tất **45/45 lượt với trạng thái optimal**, trên **15 bộ dữ liệu**:
5 kích thước × 3 seed (17, 18, 19), mỗi bộ lặp 3 lần. Cả LP và greedy có
vi phạm lớn nhất bằng 0. Đây là dữ liệu tổng hợp, không phải số liệu logistics thực tế.

## Source và bằng chứng

- Source đo: commit `c0633868a090118a74e6daa680a04a69b0e92490`, cây làm việc sạch.
- [CSV thô, 45 lượt](../../runs/experiments.csv).
- [Metadata môi trường và SHA-256 source](../../runs/experiments.metadata.json).
- [CSV tổng hợp theo quy mô](../../runs/experiments_summary.csv).
- [Checksum bằng chứng](SHA256SUMS).
- Bảng kết quả và diễn giải: Mục 4.10–4.12 trong
  [proposal_final](../proposal/proposal_final.md).

Môi trường: Python 3.13.12, NumPy 2.5.3, SciPy 1.18.1, Pandas 3.0.5,
Streamlit 1.63.0; Linux x86_64, Intel Core i7-13620H, 16 CPU logic,
RAM hệ thống khoảng 15,32 GiB. Metadata ghi thời gian UTC.

## Chạy lại

```bash
uv sync --group dev
uv run python scripts/run_experiments.py --seeds 17 18 19 --repeats 3 \
  --output /tmp/transportopt-experiments.csv
sha256sum -c docs/experiments/SHA256SUMS
```

Lệnh checksum chạy tại thư mục gốc repository. CSV tái chạy phải có cùng
seed, kích thước, chi phí LP/greedy, saving và trạng thái; các cột thời gian,
bộ nhớ và metadata có thể khác. Không yêu cầu toàn bộ CSV tái chạy có cùng hash.

CSV bằng chứng được chuẩn hóa xuống dòng LF khi lưu Git, giữ nguyên mọi giá trị đo.

## Định nghĩa phép đo

| Cột | Ý nghĩa |
| --- | --- |
| `seed`, `repeat` | Seed dữ liệu và lần lặp, đánh số từ 1 |
| `warehouses`, `customers` | Số kho, số khách hàng; số biến bằng tích hai cột |
| `objective` | Chi phí LP tính lại từ shipment |
| `greedy_objective` | Chi phí của phương án greedy khả thi |
| `saving_ratio` | (greedy − LP) / greedy; tỷ lệ 0–1, nhân 100 khi trình bày % |
| `build_seconds` | Thời gian `build_model` |
| `solve_seconds` | Thời gian wrapper `solve`, bao gồm SciPy conversion, presolve, HiGHS |
| `runtime` | Validation + build + solve + analysis; không gồm sinh dữ liệu/greedy/UI |
| `greedy_seconds` | Validation và phân bổ greedy; không gồm tính chi phí/residual |
| `memory` | Peak byte do tracemalloc theo dõi trong pipeline LP |
| `maximum_violation` | Vi phạm lớn nhất của nghiệm LP |
| `greedy_maximum_violation` | Vi phạm lớn nhất của greedy |
| `status`, `error_message` | Trạng thái; lỗi được lưu để không loại bỏ lượt thất bại |

Bộ sinh giữ nguyên quy tắc của runner: cầu nguyên 10–100, cung cân bằng,
chi phí nguyên 1–100. Greedy duyệt khách hàng theo thứ tự đầu vào, ưu tiên kho
còn cung có chi phí thấp nhất; hoà chi phí thì ưu tiên thứ tự kho.

Tóm tắt dùng `groupby(warehouses, customers)`: 9 lượt mỗi nhóm, trung vị/min/max
thời gian, max bộ nhớ và vi phạm, min/max chi phí và saving. Chi phí/saving
không đổi giữa các lần lặp cùng seed; khoảng của chúng đại diện cho 3 dữ liệu.
Các giá trị trong CSV giữ độ chính xác số thực; chỉ làm tròn khi viết báo cáo.

## Giới hạn diễn giải

- Không warm-up riêng; chạy tuần tự theo quy mô, seed, repeat trên một máy.
- Tracemalloc bật trong phép đo LP, nên có overhead. Đây không phải thời gian
  render Streamlit hoặc benchmark production không gắn công cụ đo.
- Peak tracemalloc không phải toàn bộ RAM tiến trình/HiGHS native. Chưa đo RSS.
- Thời gian greedy và LP có phạm vi đo khác nhau; không dùng để khẳng định
  thuật toán nào nhanh hơn hoặc tính speedup giữa hai thuật toán.
- LP tiết kiệm 0–53,88% so với baseline trên dữ liệu đã chạy; không khẳng định
  cải thiện nghiêm ngặt ở mọi trường hợp, cũng không suy rộng từ 3 seed/quy mô.
- Quy mô 100×500 chạy qua script. Giao diện nhập tối đa 20×20.
- Ma trận LP hiện là dense; ở 100×500 riêng hai ma trận ràng buộc có 30 triệu
  phần tử float64. Sparse là hướng cải thiện, chưa được dùng trong kết quả này.
- Đây là baseline greedy riêng; không phải NW Corner, Least Cost toàn cục,
  Vogel hoặc MODI. App chưa có nhật ký vòng lặp của các thuật toán giải tay.
