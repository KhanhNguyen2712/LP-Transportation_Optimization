# Kế hoạch kỹ thuật xây dựng TransportOpt

## 1. Mục tiêu và phạm vi v1

TransportOpt là ứng dụng Python giúp phân bổ một loại hàng từ nhiều kho đến nhiều khách hàng sao cho tổng chi phí vận chuyển nhỏ nhất. Người dùng nhập kho, khách hàng, cung, cầu và ma trận chi phí; hệ thống kiểm tra dữ liệu, giải Linear Programming bằng HiGHS và trình bày phương án vận chuyển.

Phạm vi được khóa theo `docs/proposal/proposal_final.md`:

- một loại hàng hóa;
- chi phí tuyến tính theo đơn vị hàng;
- cung và cầu đã biết;
- nhiều kho đến nhiều khách hàng;
- không xét đường đi xe, thời gian giao hàng, bản đồ, nhiều phương tiện, VRP, TSP hoặc MILP.

NW Corner, Least Cost, Vogel, MODI và Simplex tự cài chỉ thuộc phần giải tay trong báo cáo. Product v1 chỉ dùng HiGHS để tìm nghiệm tối ưu.

## 2. Yêu cầu sản phẩm

### 2.1. Functional requirements

| Mã | Yêu cầu | Tiêu chí chấp nhận |
|---|---|---|
| FR-01 | Quản lý kho | Thêm, sửa, xóa kho; mỗi kho có tên duy nhất và supply không âm |
| FR-02 | Quản lý khách hàng | Thêm, sửa, xóa khách hàng; mỗi khách có tên duy nhất và demand không âm |
| FR-03 | Nhập chi phí | Ma trận chi phí luôn có kích thước số kho × số khách và mọi phần tử không âm |
| FR-04 | Kiểm tra khả thi | Chặn solve nếu input sai hoặc tổng supply nhỏ hơn tổng demand |
| FR-05 | Tạo mô hình LP | Tạo đúng $c$, $A_{ub}$, $b_{ub}$, $A_{eq}$, $b_{eq}$ từ input |
| FR-06 | Tối ưu | Gọi SciPy HiGHS và phân biệt `optimal`, `infeasible` và `error` |
| FR-07 | Hiển thị kết quả | Hiển thị shipment có flow dương, tổng chi phí, supply còn lại và utilization |
| FR-08 | Case study | Nhập fixture 3 kho × 5 khách và nhận objective bằng 696 |

### 2.2. Non-functional requirements

- Kết quả phải tái tạo được từ cùng input và cùng phiên bản dependency.
- Tính đúng đắn ưu tiên hơn giao diện: nghiệm phải qua validation sau solve.
- UI không tự sửa dữ liệu người dùng khi validation lỗi.
- Test core không phụ thuộc Streamlit hay browser.
- Số liệu thực nghiệm phải xuất từ runner thành CSV, không nhập tay vào báo cáo.

## 3. Công nghệ và quyết định kiến trúc

| Thành phần | Công nghệ | Lý do |
|---|---|---|
| Runtime | Python 3.11+ | Phù hợp proposal và hệ sinh thái khoa học dữ liệu |
| Solver | SciPy `linprog(method="highs")` | LP solver chính; đơn giản và đủ cho phạm vi v1 |
| Tính toán | NumPy | Biểu diễn vector/matrix của LP |
| Bảng dữ liệu | Pandas | Hiển thị shipment, utilization và xuất kết quả thí nghiệm |
| UI | Streamlit | Ít frontend code, phù hợp demo đồ án |
| Test | pytest | Test module core độc lập và regression fixture |
| Code quality | ruff | Format/lint tối thiểu, tránh thêm tooling không cần thiết |

Không dùng OR-Tools trong v1 vì HiGHS đã đáp ứng LP hiện tại. Không cần database, backend API hay xác thực người dùng vì dữ liệu chỉ tồn tại trong phiên chạy ứng dụng.

## 4. Cấu trúc thư mục mục tiêu

```text
.
├── app.py                         # Entry point Streamlit
├── pyproject.toml                 # Dependencies và cấu hình tool
├── README.md                      # Cài đặt, chạy app, test, demo
├── src/
│   └── transportopt/
│       ├── __init__.py
│       ├── domain.py              # Input/output data models, solver status
│       ├── validation.py          # Kiểm tra input trước solve
│       ├── model_builder.py       # TransportationInput → LP matrices
│       ├── solver.py              # Gọi HiGHS và map kết quả solver
│       ├── results.py             # Tính cost, residual, utilization, routes
│       ├── fixtures.py            # Đọc fixture dùng chung
│       └── ui/
│           ├── input_form.py      # Form kho, khách và cost matrix
│           └── result_view.py     # Shipment table và metrics
├── tests/
│   ├── fixtures/
│   │   ├── case_2x3.json          # Expected objective: 620
│   │   ├── case_3x5.json          # Expected objective: 696
│   │   ├── surplus_supply.json
│   │   ├── insufficient_supply.json
│   │   └── multiple_optima.json
│   ├── test_validation.py
│   ├── test_model_builder.py
│   ├── test_solver.py
│   ├── test_results.py
│   └── test_regression_cases.py
├── scripts/
│   └── run_experiments.py         # Sinh data, chạy solver, xuất CSV
└── runs/
    └── .gitkeep                   # Chỉ chứa artifact thí nghiệm sinh ra
```

Thư mục `runs/` chỉ chứa kết quả tái tạo được; không commit CSV lớn nếu chưa có nhu cầu báo cáo cụ thể.

## 5. Kiến trúc hệ thống và luồng dữ liệu

```text
Streamlit UI
  │ TransportationInput
  ▼
validation.py
  │ validated TransportationInput
  ▼
model_builder.py
  │ LinearProgram(c, A_ub, b_ub, A_eq, b_eq)
  ▼
solver.py  ── SciPy HiGHS ──► SolveResult
  │
  ▼
results.py
  │ TransportationResult(routes, cost, residuals, utilization)
  ▼
result_view.py
```

Nguyên tắc biên module:

- UI chỉ thu thập/hiển thị dữ liệu; không tự tạo ma trận LP hoặc gọi SciPy trực tiếp.
- `validation.py` là cổng duy nhất trước solve.
- `model_builder.py` không biết Streamlit hoặc DataFrame.
- `solver.py` chỉ map mô hình LP sang HiGHS và không tự tính lại objective.
- `results.py` là nơi duy nhất tính lại objective và feasibility từ shipment; đây là lớp chống sai lệch giữa solver và UI.

## 6. Data contract và mô hình LP

### 6.1. Data contract

`TransportationInput` gồm:

- `warehouse_names: list[str]`
- `customer_names: list[str]`
- `supply: ndarray[float]`, dài $m$
- `demand: ndarray[float]`, dài $n$
- `costs: ndarray[float]`, shape $(m, n)$

`TransportationResult` gồm shipment matrix shape $(m, n)$, objective, `unused_supply`, `customer_residual`, `warehouse_utilization`, solver status và solver message.

### 6.2. LP mapping

Với biến được flatten theo chỉ số `k = i * n + j`:

$$
\min c^T x
$$

với ràng buộc cung:

$$
\sum_j x_{ij}\leq s_i,
$$

và ràng buộc cầu:

$$
\sum_i x_{ij}=d_j,
$$

cùng điều kiện $x_{ij}\geq0$. Khi supply dư, không thêm dummy customer trong product; HiGHS trả phần supply chưa sử dụng. Dummy customer chỉ cần cho các phương pháp giải tay cân bằng trong báo cáo.

## 7. Kế hoạch hiện thực theo module

### Phase 0 — Khởi tạo project và contract

#### Task 0.1: Scaffold và dependency tối thiểu

**Files:** `pyproject.toml`, `src/transportopt/__init__.py`, `app.py`, `README.md`  
**Dependencies:** Không có

**Acceptance criteria:**

- [ ] Cài được dependency của app, solver và test từ một lệnh đã ghi trong README.
- [ ] `app.py` khởi động Streamlit với trang trống có tiêu đề TransportOpt.
- [ ] Package import được trong test.

**Verification:** Chạy import package, chạy test rỗng và mở Streamlit local.

#### Task 0.2: Domain models và fixture loader

**Files:** `domain.py`, `fixtures.py`, `tests/fixtures/*.json`, `tests/test_fixtures.py`  
**Dependencies:** Task 0.1

**Acceptance criteria:**

- [ ] Fixture 2×3 và 3×5 đọc thành `TransportationInput` hợp lệ.
- [ ] Fixture 2×3 ghi expected objective 620; fixture 3×5 ghi 696.
- [ ] Contract tách rõ invalid input khỏi solver infeasible.

**Verification:** Fixture 3×5 có tổng supply = tổng demand = 55 và ma trận 3×5.

### Phase 1 — Core solver không có UI

#### Task 1.1: Validation

**Files:** `validation.py`, `tests/test_validation.py`  
**Dependencies:** Task 0.2

**Acceptance criteria:**

- [ ] Từ chối tên trống/trùng, mảng sai kích thước, NaN/Infinity và số âm.
- [ ] Từ chối tổng supply nhỏ hơn tổng demand với message dễ hiểu.
- [ ] Chấp nhận bài toán supply dư và chi phí bằng 0.

**Verification:** Test valid, negative cost, malformed matrix, supply thiếu và supply dư.

#### Task 1.2: LP model builder

**Files:** `model_builder.py`, `tests/test_model_builder.py`  
**Dependencies:** Task 1.1

**Acceptance criteria:**

- [ ] Vector $c$ có độ dài $m\times n$ và theo đúng thứ tự flatten đã chốt.
- [ ] $A_{ub}$ có $m$ hàng; $A_{eq}$ có $n$ hàng.
- [ ] Mỗi hàng/cột của shipment ánh xạ đúng một ràng buộc cung/cầu.

**Verification:** Với fixture 2×3, assert shapes là `(2, 6)` và `(3, 6)`; kiểm tra vài hệ số cụ thể.

#### Task 1.3: HiGHS solver wrapper

**Files:** `solver.py`, `tests/test_solver.py`  
**Dependencies:** Task 1.2

**Acceptance criteria:**

- [ ] Gọi `linprog(..., method="highs")` với non-negative bounds.
- [ ] Map status solver sang `optimal`, `infeasible` hoặc `error`.
- [ ] Không trả shipment khi solver không optimal.

**Verification:** Fixture 2×3 trả 620 và fixture 3×5 trả 696 trong tolerance $10^{-8}$.

#### Task 1.4: Result analyzer

**Files:** `results.py`, `tests/test_results.py`  
**Dependencies:** Task 1.3

**Acceptance criteria:**

- [ ] Tính lại objective từ `costs * shipment`.
- [ ] Kiểm tra demand residual, supply violation và non-negativity.
- [ ] Tạo routes có flow dương, unused supply và utilization theo kho.

**Verification:** Objective tự tính lại khớp solver; residual tối đa không vượt tolerance; supply dư hiển thị đúng.

### Checkpoint 1 — Core correctness

- [ ] `pytest` pass cho validation, model builder, solver và result analyzer.
- [ ] Case 2×3 trả 620; case 3×5 trả 696.
- [ ] Không có module core import Streamlit.

### Phase 2 — Vertical slice giao diện

#### Task 2.1: Form nhập dữ liệu

**Files:** `ui/input_form.py`, `app.py`  
**Dependencies:** Tasks 0.2, 1.1

**Acceptance criteria:**

- [ ] Người dùng thêm/xóa kho và khách; cost matrix cập nhật theo kích thước mới.
- [ ] Form giữ lại giá trị hợp lệ khi validation lỗi.
- [ ] Có nút nạp case 2×3 và case 3×5 để demo.

**Verification:** Nhập được hai fixture không cần sửa code; lỗi matrix hiển thị trước khi solve.

#### Task 2.2: Connect solve flow

**Files:** `app.py`, `ui/input_form.py`  
**Dependencies:** Tasks 1.2–1.4, 2.1

**Acceptance criteria:**

- [ ] Nút Solve chỉ gọi core sau validation thành công.
- [ ] Solver message hiển thị khi input không khả thi hoặc solver lỗi.
- [ ] UI không nuốt exception hoặc hiển thị traceback cho người dùng cuối.

**Verification:** Case supply thiếu không gọi solve; hai fixture chuẩn nhận status optimal.

#### Task 2.3: Result view

**Files:** `ui/result_view.py`, `app.py`  
**Dependencies:** Tasks 1.4, 2.2

**Acceptance criteria:**

- [ ] Hiển thị total cost, shipment routes, unused supply và utilization.
- [ ] Chỉ hiển thị routes có flow lớn hơn tolerance.
- [ ] Bảng shipment có tên kho/khách đúng input.

**Verification:** Kiểm tra visual với case 2×3 và 3×5; cost hiển thị lần lượt 620 và 696.

### Checkpoint 2 — End-to-end app

- [ ] Nhập fixture → validate → solve → thấy kết quả trong một phiên Streamlit.
- [ ] Kết quả UI khớp `TransportationResult`; không tái tính logic ở UI.

### Phase 3 — Regression và thực nghiệm

#### Task 3.1: Regression suite

**Files:** `tests/test_regression_cases.py`, `tests/fixtures/*.json`  
**Dependencies:** Checkpoint 1

**Acceptance criteria:**

- [ ] Có case balanced, supply dư, supply thiếu, cost lớn và nhiều nghiệm tối ưu.
- [ ] Case nhiều nghiệm tối ưu kiểm tra objective/feasibility, không ép một shipment duy nhất.
- [ ] Test case 3×5 kiểm tra objective 696 và residual.

**Verification:** Một lệnh `pytest` chạy toàn bộ tests không cần UI.

#### Task 3.2: Experiment runner

**Files:** `scripts/run_experiments.py`, `runs/`, `tests/test_experiments.py`  
**Dependencies:** Checkpoint 1

**Acceptance criteria:**

- [ ] Sinh dữ liệu theo seed cố định cho 2×3, 5×10, 10×50, 50×100 và 100×500.
- [ ] Ghi `seed`, dimensions, objective, runtime, memory, status và maximum violation vào CSV.
- [ ] Không dùng fixture 3×5 để kết luận runtime hay scale.

**Verification:** Hai lần chạy cùng seed tạo cùng input; CSV có đủ trường và các status được ghi lại.

### Checkpoint 3 — Evidence cho báo cáo

- [ ] Regression suite pass.
- [ ] CSV thí nghiệm được tạo lại bằng một lệnh documented.
- [ ] Chương 4 chỉ lấy bảng/figure từ artifact này.

### Phase 4 — Bàn giao

#### Task 4.1: README và demo script

**Files:** `README.md`, `scripts/`  
**Dependencies:** Checkpoints 2–3

**Acceptance criteria:**

- [ ] Hướng dẫn cài đặt, chạy app, test và experiment ngắn gọn, chạy được.
- [ ] Demo nêu case 3×5 và expected objective 696.
- [ ] Nêu rõ giới hạn product v1.

**Verification:** Một người chưa từng chạy project có thể tái tạo demo theo README.

#### Task 4.2: Release verification

**Files:** Không thêm code trừ khi phát hiện lỗi  
**Dependencies:** Task 4.1

**Acceptance criteria:**

- [ ] Tests pass, app khởi động, fixture 2×3/3×5 trả 620/696.
- [ ] Input invalid và infeasible có thông báo rõ.
- [ ] Không có kết quả benchmark không tái tạo được.

**Verification:** Chạy full flow từ README trên môi trường sạch.

## 8. Rủi ro và xử lý

| Rủi ro | Tác động | Xử lý |
|---|---|---|
| Sai thứ tự flatten giữa model và shipment | Cao | Ghi một quy ước trong `model_builder.py`; test exact coefficient và reshape |
| Solver thành công nhưng UI hiển thị sai | Cao | `results.py` tính lại cost/residual; UI chỉ render result object |
| Supply dư bị mô hình hóa như demand bằng | Cao | Giữ cung là `<=`; test fixture supply dư riêng |
| Ràng buộc số thực có residual nhỏ | Trung bình | Chốt tolerance, không so sánh float bằng tuyệt đối 0 |
| Scope creep sang routing hoặc heuristic | Trung bình | Không thêm dependency/route module ngoài danh sách ở Mục 4 |

## 9. Definition of done

- [ ] Code được tổ chức đúng cấu trúc ở Mục 4 và core không phụ thuộc Streamlit.
- [ ] HiGHS giải đúng case 2×3 với objective 620 và case 3×5 với objective 696.
- [ ] Validation, regression tests và experiment runner có thể chạy lại.
- [ ] UI hiển thị shipment, total cost, unused supply, utilization và lỗi rõ ràng.
- [ ] README đủ để tái tạo app, test và artifact cho báo cáo.
