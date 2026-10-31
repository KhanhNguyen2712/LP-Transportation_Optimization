# TransportOpt

TransportOpt là ứng dụng Streamlit giải bài toán vận tải bằng quy hoạch tuyến
tính. Người dùng nhập kho, khách hàng, cung, cầu và ma trận chi phí; solver
SciPy HiGHS tìm phương án có tổng chi phí nhỏ nhất.

## Yêu cầu

- Python 3.11 trở lên
- [uv](https://docs.astral.sh/uv/)

## Cài đặt

Chạy từ thư mục gốc của repository:

```bash
uv sync --group dev
```

## Chạy ứng dụng

```bash
uv run streamlit run app.py
```

Trong sidebar, chọn `3 × 5 example`, bấm `Nạp ví dụ`, rồi bấm
`Tìm phương án tối ưu`. Case này có nghiệm tối ưu với objective **696**.

Giao diện có sơ đồ trước/sau tối ưu, diễn giải mô hình LP, bảng tính chi phí
và kiểm chứng cung/cầu. Xem [kịch bản demo và hình cho phần 4](docs/demo/README.md).

## Chạy tests

```bash
uv run pytest -q
```

## Lint và format

```bash
uv run ruff check .
uv run ruff format --check .
```

## Chạy thực nghiệm tái lập

Runner dùng seed mặc định `17` và 5 kích thước từ 2×3 đến 100×500.
Chạy bộ thực nghiệm cho báo cáo với 3 seed, mỗi seed lặp 3 lần:

```bash
uv run python scripts/run_experiments.py --seeds 17 18 19 --repeats 3
```

Kết quả thô tại `runs/experiments.csv`; môi trường, commit, SHA-256 source và
định nghĩa phép đo tại `runs/experiments.metadata.json`. Khi chạy lại để đối
chiếu mà không ghi đè bản đã lưu:

```bash
uv run python scripts/run_experiments.py --seeds 17 18 19 --repeats 3 \
  --output /tmp/transportopt-experiments.csv
```

Baseline greedy phục vụ khách hàng theo thứ tự nhập, chọn kho còn hàng có
chi phí thấp nhất; hoà chi phí thì ưu tiên thứ tự kho. `saving_ratio` là tỷ lệ
chi phí LP giảm so với greedy, để trống nếu chi phí greedy bằng 0.
`runtime` đo validation + build + solve + analysis, không gồm sinh dữ liệu và
greedy; `solve_seconds` đo lời gọi solver riêng. `memory` là peak `tracemalloc`
trong pipeline LP, không phải toàn bộ RAM tiến trình/HiGHS. Thời gian LP được
đo khi bật `tracemalloc`, không dùng để suy luận tốc độ production.

## Giới hạn v1

- Chỉ giải bài toán một loại hàng, chi phí tuyến tính, cung/cầu đã biết.
- Không mô hình hóa tuyến đường, thời gian giao hàng, bản đồ, nhiều phương
  tiện, VRP, TSP hoặc MILP.
- Solver là SciPy HiGHS; các phương pháp NW Corner, Least Cost, Vogel, MODI
  và Simplex tự cài chỉ thuộc phần giải tay/báo cáo, không phải product v1.
- Dữ liệu chỉ tồn tại trong phiên Streamlit; chưa có database, backend API,
  xác thực người dùng hay phân quyền.
