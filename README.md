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

Trong sidebar, chọn `3 × 5 example`, bấm `Load fixture`, rồi bấm
`Validate and solve`. Case này có nghiệm tối ưu với objective **696**.

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

Runner dùng seed mặc định `17` và các kích thước cố định trong
`scripts/run_experiments.py`:

```bash
uv run python scripts/run_experiments.py
```

CSV được ghi tại `runs/experiments.csv`. Có thể đổi seed hoặc đường dẫn output:

```bash
uv run python scripts/run_experiments.py \
  --seed 17 --output runs/experiments.csv
```

## Giới hạn v1

- Chỉ giải bài toán một loại hàng, chi phí tuyến tính, cung/cầu đã biết.
- Không mô hình hóa tuyến đường, thời gian giao hàng, bản đồ, nhiều phương
  tiện, VRP, TSP hoặc MILP.
- Solver là SciPy HiGHS; các phương pháp NW Corner, Least Cost, Vogel, MODI
  và Simplex tự cài chỉ thuộc phần giải tay/báo cáo, không phải product v1.
- Dữ liệu chỉ tồn tại trong phiên Streamlit; chưa có database, backend API,
  xác thực người dùng hay phân quyền.
