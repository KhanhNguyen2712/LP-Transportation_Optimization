# ĐỀ XUẤT ĐỀ TÀI

## ỨNG DỤNG QUY HOẠCH TUYẾN TÍNH TRONG TỐI ƯU HÓA BÀI TOÁN VẬN TẢI

---

# MỤC LỤC

**1. PHẦN MỞ ĐẦU**
1.1. Lý do chọn đề tài
1.2. Bối cảnh bài toán
1.3. Mục tiêu đề tài
1.4. Đối tượng và phạm vi nghiên cứu
1.5. Phương pháp nghiên cứu
1.6. Kết quả dự kiến

**2. CÁC KHÁI NIỆM VÀ BÀI TOÁN THỰC TẾ VỀ QUY HOẠCH TUYẾN TÍNH**
2.1. Khái niệm tối ưu hóa
2.2. Quy hoạch tuyến tính
2.3. Các thành phần của mô hình quy hoạch tuyến tính
2.4. Biểu diễn bằng đại số tuyến tính
2.5. Miền nghiệm khả thi và nghiệm tối ưu
2.6. Một số bài toán thực tế
2.7. Bài toán vận tải
2.8. Mối liên hệ giữa bài toán vận tải và bài toán luồng trên mạng
2.9. Các phương pháp lập nghiệm ban đầu cho bài toán vận tải
2.10. Case study xuyên suốt 3 kho và 5 khách hàng

**3. CƠ SỞ LÝ THUYẾT VÀ THUẬT TOÁN TÌM PHƯƠNG ÁN TỐI ƯU TUYẾN TÍNH**
3.1. Dạng chuẩn của bài toán quy hoạch tuyến tính
3.2. Cơ sở đại số tuyến tính
3.3. Nghiệm cơ sở và nghiệm cơ sở khả thi
3.4. Ý tưởng hình học của phương pháp Simplex
3.5. Thuật toán Simplex
3.6. Bài toán đối ngẫu
3.7. Phương pháp điểm trong
3.8. Bài toán vận tải và cấu trúc ma trận đặc biệt
3.9. Phương pháp giải tay và lựa chọn thuật toán

**4. SẢN PHẨM PHẦN MỀM TÌM PHƯƠNG ÁN TỐI ƯU CHO BÀI TOÁN VẬN TẢI**
4.1. Mục tiêu sản phẩm
4.2. Yêu cầu chức năng
4.3. Mô hình toán học
4.4. Kiến trúc hệ thống
4.5. Quy trình hoạt động
4.6. Thiết kế giao diện
4.7. Công nghệ đề xuất
4.8. Dữ liệu thử nghiệm
4.9. Phương pháp đánh giá
4.10. Các trường hợp kiểm thử
4.11. Hướng mở rộng

**5. KẾT LUẬN**

**DANH MỤC TÀI LIỆU THAM KHẢO**

---

# 1. PHẦN MỞ ĐẦU

## 1.1. Lý do chọn đề tài

Trong các hệ thống phân phối và logistics, doanh nghiệp thường phải vận chuyển hàng hóa từ nhiều kho hoặc nhà máy đến nhiều điểm tiêu thụ khác nhau. Mỗi tuyến vận chuyển có chi phí khác nhau, trong khi mỗi kho chỉ có một lượng hàng giới hạn và mỗi khách hàng lại có nhu cầu nhất định.

Một câu hỏi quan trọng được đặt ra là:

> Nên vận chuyển bao nhiêu hàng hóa từ mỗi kho đến mỗi khách hàng để thỏa mãn nhu cầu với tổng chi phí vận chuyển nhỏ nhất?

Nếu lựa chọn phương án vận chuyển bằng kinh nghiệm hoặc thủ công, số lượng phương án cần xem xét tăng rất nhanh khi số kho và số điểm nhận hàng tăng lên.

Ví dụ, chỉ với:

- 10 kho hàng;
- 100 điểm nhận hàng;

đã có thể xuất hiện đến:

$$
10\times100=1000
$$

biến quyết định về lượng hàng cần vận chuyển.

Do đó, cần có một phương pháp toán học để mô hình hóa và tìm phương án tốt nhất một cách có hệ thống.

**Quy hoạch tuyến tính – Linear Programming (LP)** là một trong những phương pháp nền tảng của tối ưu hóa toán học, cho phép tìm cực tiểu hoặc cực đại của một hàm mục tiêu tuyến tính dưới một tập các ràng buộc tuyến tính.[^1]

Bài toán vận tải là một trường hợp đặc biệt của quy hoạch tuyến tính và có rất nhiều ứng dụng thực tế trong:

- logistics;
- quản lý chuỗi cung ứng;
- phân phối hàng hóa;
- lập kế hoạch sản xuất;
- quản lý kho;
- phân bổ tài nguyên;
- vận chuyển nguyên vật liệu.

Đề tài vì vậy lựa chọn nghiên cứu quy hoạch tuyến tính từ góc nhìn **đại số tuyến tính, thuật toán tối ưu và ứng dụng vào bài toán vận tải**, đồng thời xây dựng một phần mềm cho phép người dùng nhập dữ liệu và tự động tìm phương án vận chuyển tối ưu.

---

## 1.2. Bối cảnh bài toán

Giả sử một doanh nghiệp có:

$$
m
$$

kho hàng và:

$$
n
$$

địa điểm cần nhận hàng.

Kho thứ \(i\) có khả năng cung cấp:

$$
s_i
$$

đơn vị hàng hóa.

Khách hàng thứ \(j\) cần:

$$
d_j
$$

đơn vị hàng hóa.

Chi phí vận chuyển một đơn vị hàng hóa từ kho \(i\) đến khách hàng \(j\) là:

$$
c_{ij}
$$

Cần xác định:

$$
x_{ij}
$$

là lượng hàng vận chuyển từ kho \(i\) đến khách hàng \(j\), sao cho tổng chi phí:

$$
\sum_{i=1}^{m}\sum_{j=1}^{n}c_{ij}x_{ij}
$$

là nhỏ nhất.

Đồng thời phải thỏa mãn:

- không vận chuyển vượt quá khả năng của kho;
- nhu cầu của khách hàng phải được đáp ứng;
- lượng hàng vận chuyển không âm.

Đây chính là **Transportation Problem** cổ điển trong Operations Research.

---

## 1.3. Mục tiêu đề tài

### Mục tiêu tổng quát

Nghiên cứu cơ sở toán học và thuật toán của quy hoạch tuyến tính, sau đó ứng dụng để xây dựng phần mềm tìm phương án vận chuyển hàng hóa có tổng chi phí nhỏ nhất.

### Mục tiêu cụ thể

Đề tài hướng tới các mục tiêu sau:

1. Trình bày các khái niệm cơ bản của bài toán tối ưu.
2. Nghiên cứu mô hình quy hoạch tuyến tính.
3. Làm rõ mối liên hệ giữa quy hoạch tuyến tính và đại số tuyến tính.
4. Nghiên cứu thuật toán Simplex và một số phương pháp giải LP hiện đại.
5. Xây dựng mô hình toán học cho bài toán vận tải.
6. Chuyển bài toán vận tải về dạng:

$$
\min c^Tx
$$

với:

$$
Ax=b
$$

hoặc:

$$
Ax\leq b
$$

7. Xây dựng phần mềm cho phép:

- nhập danh sách kho;
- nhập danh sách khách hàng;
- nhập năng lực cung cấp;
- nhập nhu cầu;
- nhập ma trận chi phí;
- chạy thuật toán tối ưu;
- hiển thị phương án vận chuyển;
- hiển thị tổng chi phí tối thiểu.

8. Thực nghiệm với nhiều kích thước bài toán khác nhau.
9. So sánh phương án tối ưu với các phương án khởi tạo và phân bổ đơn giản.

---

## 1.4. Đối tượng và phạm vi nghiên cứu

### Đối tượng nghiên cứu

Đề tài tập trung vào:

- đại số tuyến tính;
- tối ưu hóa;
- quy hoạch tuyến tính;
- Simplex;
- bài toán vận tải;
- phần mềm giải bài toán LP.

### Phạm vi

Phiên bản chính của đề tài tập trung vào bài toán:

$$
\boxed{\text{Nhiều kho} \rightarrow \text{Nhiều khách hàng}}
$$

với giả định:

- chỉ xét một loại hàng hóa;
- chi phí vận chuyển là tuyến tính;
- nhu cầu đã biết;
- năng lực các kho đã biết;
- không xét tắc đường;
- không xét thời gian giao hàng;
- không xét đường đi chi tiết của xe;
- không xét nhiều loại phương tiện.

Các bài toán Vehicle Routing Problem, Traveling Salesman Problem hoặc Mixed Integer Programming chỉ được đề cập như hướng phát triển tiếp theo.

---

## 1.5. Phương pháp nghiên cứu

Đề tài thực hiện theo bốn bước chính:

### Bước 1 – Nghiên cứu lý thuyết

Nghiên cứu:

- Linear Algebra;
- Linear Programming;
- Simplex;
- Duality;
- Transportation Problem.
- NW Corner, Least Cost, Vogel và MODI cho bài toán vận tải.

### Bước 2 – Mô hình hóa

Chuyển bài toán thực tế thành:

$$
\min c^Tx
$$

subject to:

$$
Ax=b
$$

$$
x\geq0
$$

### Bước 3 – Xây dựng phần mềm

Cài đặt hệ thống bằng Python kết hợp thư viện tối ưu.

### Bước 4 – Thực nghiệm

Sinh nhiều bộ dữ liệu với quy mô khác nhau và đánh giá:

- tính đúng đắn;
- chi phí tối ưu;
- thời gian xử lý;
- khả năng mở rộng.

---

## 1.6. Kết quả dự kiến

Sản phẩm của đề tài gồm:

**1. Báo cáo lý thuyết**

Trình bày:

$$
Linear\ Algebra
\rightarrow Linear\ Programming
\rightarrow Simplex
\rightarrow Transportation
$$

Báo cáo có một ví dụ LP nhỏ giải tay bằng Simplex cơ bản và một ví dụ vận tải nhỏ giải tay theo quy trình tạo nghiệm ban đầu, sau đó cải thiện bằng MODI.

**2. Phần mềm**

Cho phép:

$$
Input
\rightarrow Optimization
\rightarrow Optimal\ Plan
$$

**3. Bộ dữ liệu thử nghiệm**

Gồm nhiều bài toán từ nhỏ đến lớn.

**4. Kết quả đánh giá**

So sánh phương án tối ưu với các phương pháp phân bổ cơ bản; với ví dụ giải tay, báo cáo chi phí của nghiệm ban đầu, các bước cải thiện và chi phí tối ưu.

---

# 2. CÁC KHÁI NIỆM VÀ BÀI TOÁN THỰC TẾ VỀ QUY HOẠCH TUYẾN TÍNH

> **Dự kiến độ dài: 3–4 trang A4.**

## 2.1. Khái niệm tối ưu hóa

Bài toán tối ưu có dạng tổng quát:

$$
\min_x f(x)
$$

hoặc:

$$
\max_x f(x)
$$

với:

$$
x\in\mathcal{X}
$$

Trong đó:

- \(x\): biến quyết định;
- \(f(x)\): hàm mục tiêu;
- \(\mathcal X\): tập các phương án hợp lệ.

Tối ưu hóa nhằm tìm:

$$
x^*
$$

sao cho:

$$
f(x^*)\leq f(x)
$$

với mọi:

$$
x\in\mathcal X
$$

trong bài toán cực tiểu.

---

## 2.2. Quy hoạch tuyến tính

Quy hoạch tuyến tính là bài toán tối ưu mà:

- hàm mục tiêu tuyến tính;
- các ràng buộc tuyến tính;
- biến thường liên tục.

Dạng tổng quát:

$$
\min c^Tx
$$

subject to:

$$
Ax\leq b
$$

$$
A_{eq}x=b_{eq}
$$

$$
l\leq x\leq u
$$

Đây cũng là dạng chuẩn được sử dụng bởi nhiều thư viện tính toán như `scipy.optimize.linprog`.[^2]

---

## 2.3. Các thành phần của mô hình

### Biến quyết định

Ví dụ:

$$
x_{ij}
$$

là lượng hàng đi từ kho \(i\) đến khách hàng \(j\).

### Hàm mục tiêu

$$
\min \sum_i\sum_jc_{ij}x_{ij}
$$

### Ràng buộc

Ví dụ:

$$
\sum_jx_{ij}\leq s_i
$$

### Điều kiện không âm

$$
x_{ij}\geq0
$$

---

## 2.4. Biểu diễn bằng đại số tuyến tính

Một ưu điểm quan trọng của quy hoạch tuyến tính là toàn bộ bài toán có thể biểu diễn bằng vector và ma trận.

Cho:

$$
x=
\begin{bmatrix}
x_1\\
x_2\\
\vdots\\
x_n
\end{bmatrix}
$$

và:

$$
c=
\begin{bmatrix}
c_1\\
c_2\\
\vdots\\
c_n
\end{bmatrix}
$$

Hàm mục tiêu:

$$
c^Tx
$$

Các ràng buộc:

$$
Ax=b
$$

Trong đó:

$$
A\in\mathbb{R}^{m\times n}
$$

Linear Algebra vì vậy cung cấp nền tảng để biểu diễn và tính toán các bài toán LP.

---

## 2.5. Miền nghiệm khả thi

Tập:

$$
\mathcal P=\{x|Ax\leq b\}
$$

được gọi là miền nghiệm khả thi.

Về mặt hình học, miền nghiệm của LP là một **đa diện lồi – convex polyhedron**.

Một tính chất quan trọng của quy hoạch tuyến tính là nếu nghiệm tối ưu hữu hạn tồn tại thì sẽ tồn tại ít nhất một nghiệm tối ưu tại một điểm cực biên của miền khả thi.

Đây là nền tảng hình học của thuật toán Simplex.

---

## 2.6. Một số ứng dụng thực tế

Quy hoạch tuyến tính được ứng dụng trong:

### Sản xuất

Tìm số lượng từng sản phẩm cần sản xuất nhằm tối đa hóa lợi nhuận.

### Phân bổ tài nguyên

Phân chia:

- máy móc;
- lao động;
- nguyên vật liệu;
- thời gian.

### Nông nghiệp

Lựa chọn diện tích trồng từng loại cây.

### Năng lượng

Phân bổ sản lượng giữa nhiều nguồn điện.

### Logistics

Tối ưu:

- phân phối;
- vận chuyển;
- tồn kho;
- dòng hàng hóa.

---

## 2.7. Bài toán vận tải

Cho \(m\) kho và \(n\) khách hàng.

Biến:

$$
x_{ij}\geq0
$$

Hàm mục tiêu:

$$
\boxed{
\min
\sum_{i=1}^{m}
\sum_{j=1}^{n}
c_{ij}x_{ij}
}
$$

Ràng buộc cung:

$$
\sum_{j=1}^{n}x_{ij}\leq s_i
$$

Ràng buộc cầu:

$$
\sum_{i=1}^{m}x_{ij}=d_j
$$

Nếu:

$$
\sum_i s_i=\sum_jd_j
$$

ta có bài toán vận tải cân bằng.

---

## 2.8. Liên hệ với bài toán luồng trên mạng

Có thể xem bài toán vận tải như một đồ thị:

$$
Warehouse
\rightarrow Customer
$$

Mỗi cạnh có:

- capacity;
- cost;
- flow.

Khi đó bài toán vận tải liên hệ trực tiếp với:

$$
Minimum\ Cost\ Flow
$$

Đây là nền tảng để mở rộng sang các mạng logistics phức tạp:

$$
Supplier
\rightarrow Factory
\rightarrow Warehouse
\rightarrow Customer
$$

---

## 2.9. Các phương pháp lập nghiệm ban đầu cho bài toán vận tải

Với bài toán vận tải cân bằng, một nghiệm cơ sở khả thi ban đầu có thể được lập bằng các phương pháp chuyên biệt sau:

- **Northwest Corner (NW Corner):** phân bổ từ ô góc trên trái, chỉ dựa vào cung và cầu;
- **Least Cost:** ưu tiên ô có chi phí vận chuyển nhỏ nhất đang còn khả dụng;
- **Vogel's Approximation Method (VAM):** dùng mức phạt theo hàng và cột để chọn vị trí phân bổ.

Ba phương pháp trên chỉ tạo nghiệm ban đầu, không tự chứng minh nghiệm tối ưu. Nghiệm được cải thiện và kiểm tra tối ưu bằng **MODI** hoặc Transportation Simplex. Nếu tổng cung lớn hơn tổng cầu, ví dụ giải tay sẽ thêm một khách hàng giả có nhu cầu bằng phần cung dư và chi phí bằng 0 để đưa bài toán về dạng cân bằng.

---

## 2.10. Case study xuyên suốt 3 kho và 5 khách hàng

Đề tài sử dụng một case study vận tải cân bằng từ tài liệu `transportation-example.pdf`[^5]. Ba kho A, B, C có cung lần lượt 18, 25, 12 đơn vị; năm khách hàng V, W, X, Y, Z có cầu lần lượt 14, 6, 8, 10, 17 đơn vị. Tổng cung và tổng cầu đều bằng 55.

| Kho/Khách hàng |            V |           W |           X |            Y |            Z | Cung |
| ---------------- | -----------: | ----------: | ----------: | -----------: | -----------: | ---: |
| A                |           20 |          12 |          15 |           10 |           16 |   18 |
| B                |           15 |          18 |          16 |           13 |           10 |   25 |
| C                |           17 |          14 |          19 |           14 |           12 |   12 |
| **Cầu**   | **14** | **6** | **8** | **10** | **17** |      |

Mỗi ô là chi phí vận chuyển một đơn vị hàng hóa. Cần xác định các biến $x_{ij}\geq0$ sao cho mọi nhu cầu được đáp ứng, mọi cung được dùng hết và tổng chi phí vận chuyển là nhỏ nhất.

### Cách giải và kết quả đối chiếu

Nghiệm ban đầu trong tài liệu được lập theo Northwest Corner: lần lượt thỏa mãn các cột cầu từ trái sang phải bằng các hàng cung từ trên xuống dưới. Sau đó tài liệu dùng thế vị hàng/cột, test value $c_{ij}-v_i-w_j$, và pivot theo vòng kín để cải thiện nghiệm. Đây là Transportation Simplex dưới cách trình bày MODI/u-v, không phải generic Simplex tableau.

Sau bốn pivot tại các ô BV, AY, AX và CW, một nghiệm tối ưu là:

$$
x_{AX}=8,\quad x_{AY}=10,\quad x_{BV}=14,\quad x_{BZ}=11,\quad x_{CW}=6,\quad x_{CZ}=6.
$$

Chi phí tối ưu là:

$$
8(15)+10(10)+14(15)+11(10)+6(14)+6(12)=696.
$$

Ô CV có test value bằng 0 ở nghiệm cuối, nên bài toán có nhiều nghiệm tối ưu. Kết quả 696 sẽ được dùng để kiểm chứng kết quả HiGHS trong phần mềm.

### Vai trò trong báo cáo

Case study này được dùng xuyên suốt từ bối cảnh logistics, mô hình LP, giải tay NW Corner và MODI, đến nhập dữ liệu vào phần mềm và đối chiếu với HiGHS. Nó phù hợp vì có đầy đủ cung, cầu, ma trận chi phí và các bước cải thiện nghiệm. Tuy nhiên, đây chỉ là ví dụ minh họa và kiểm chứng; đánh giá runtime hoặc khả năng mở rộng vẫn dùng các bộ dữ liệu lớn sinh riêng. Báo cáo sẽ tự vẽ lại bảng và figure bằng tiếng Việt, ghi nguồn dữ liệu, thay vì sao chép nguyên các figure trong tài liệu nguồn.

---

# 3. CƠ SỞ LÝ THUYẾT VÀ THUẬT TOÁN TÌM PHƯƠNG ÁN TỐI ƯU TUYẾN TÍNH

> **Dự kiến: 5–6 trang A4.**
>
> Tổng chương 2 + chương 3 nên được kiểm soát khoảng **8–10 trang A4**, đúng yêu cầu đề tài.

## 3.1. Dạng chuẩn

Xét:

$$
\max c^Tx
$$

subject to:

$$
Ax=b
$$

$$
x\geq0
$$

Đây là dạng thuận tiện để nghiên cứu Simplex.

Các ràng buộc:

$$
a_1x_1+\cdots+a_nx_n\leq b
$$

có thể chuyển thành equality bằng biến phụ:

$$
a_1x_1+\cdots+a_nx_n+s=b
$$

với:

$$
s\geq0
$$

---

# 3.2. Cơ sở đại số tuyến tính

Giả sử:

$$
A\in\mathbb R^{m\times n}
$$

với:

$$
m<n
$$

Ta lựa chọn \(m\) cột độc lập tuyến tính của \(A\), tạo thành:

$$
B\in\mathbb R^{m\times m}
$$

gọi là **ma trận cơ sở**.

Phương trình:

$$
Ax=b
$$

có thể tách thành:

$$
Bx_B+Nx_N=b
$$

Nếu đặt:

$$
x_N=0
$$

ta có:

$$
Bx_B=b
$$

và:

$$
\boxed{x_B=B^{-1}b}
$$

Trong thực tế, các solver không nhất thiết tính \(B^{-1}\) trực tiếp mà giải hệ phương trình tuyến tính bằng các phương pháp factorization.

Đây là mối liên hệ trực tiếp giữa:

$$
Linear\ Algebra
$$

và:

$$
Linear\ Programming
$$

---

# 3.3. Nghiệm cơ sở khả thi

Nếu nghiệm:

$$
x_B=B^{-1}b
$$

thỏa:

$$
x_B\geq0
$$

thì đây là một **Basic Feasible Solution – BFS**.

Các BFS tương ứng với các điểm cực biên của miền nghiệm khả thi.

Simplex khai thác đặc điểm này bằng cách di chuyển:

$$
Vertex_1
\rightarrow Vertex_2
\rightarrow\cdots
\rightarrow Vertex^*
$$

và liên tục cải thiện hàm mục tiêu.

---

# 3.4. Ý tưởng của Simplex

Simplex là một trong những thuật toán nổi tiếng nhất để giải bài toán quy hoạch tuyến tính.

Thay vì kiểm tra mọi điểm trong miền khả thi, Simplex:

1. tìm một đỉnh khả thi ban đầu;
2. xác định hướng có thể cải thiện objective;
3. chuyển sang đỉnh lân cận;
4. tiếp tục cho đến khi không thể cải thiện thêm.

Theo tài liệu OR-Tools, Simplex vẫn là một trong những họ thuật toán LP quan trọng và hoạt động bằng cách di chuyển giữa các đỉnh của miền khả thi để liên tục cải thiện objective.[^3]

---

# 3.5. Thuật toán Simplex

Quy trình khái quát:

### Bước 1

Chuyển bài toán về standard form.

### Bước 2

Tìm nghiệm cơ sở khả thi ban đầu.

### Bước 3

Tính reduced cost.

Với bài toán minimization:

$$
\bar c_j=c_j-c_B^TB^{-1}A_j
$$

### Bước 4

Chọn biến entering.

Một biến có reduced cost phù hợp được đưa vào basis.

### Bước 5

Chọn biến leaving.

Dùng minimum ratio test:

$$
\min_i
\frac{(B^{-1}b)_i}
{(B^{-1}A_j)_i}
$$

với mẫu số dương.

### Bước 6

Thay đổi basis.

### Bước 7

Lặp lại.

Nếu không còn biến nào có thể cải thiện objective thì nghiệm hiện tại là tối ưu.

---

# 3.6. Bài toán đối ngẫu

Với primal:

$$
\min c^Tx
$$

subject to:

$$
Ax\geq b
$$

dual có thể viết:

$$
\max b^Ty
$$

subject to:

$$
A^Ty\leq c
$$

Dual variables có thể được diễn giải như **shadow prices**.

Trong bài toán logistics, chúng có thể trả lời:

> Nếu tăng thêm một đơn vị capacity của kho thì tổng chi phí tối ưu có thể cải thiện bao nhiêu?

Điều này giúp tối ưu không chỉ đưa ra phương án vận chuyển mà còn hỗ trợ phân tích quyết định.

---

# 3.7. Phương pháp điểm trong

Ngoài Simplex, một nhóm thuật toán quan trọng khác là:

$$
Interior\ Point\ Methods
$$

Thay vì di chuyển qua các đỉnh của miền khả thi, phương pháp này đi qua vùng bên trong.

Mỗi iteration thường cần giải các hệ phương trình tuyến tính lớn.

Do đó các kỹ thuật:

- sparse matrix;
- LU factorization;
- Cholesky factorization;

đóng vai trò quan trọng.

Các solver HiGHS được SciPy sử dụng hiện hỗ trợ cả dual revised simplex và interior-point methods.[^2]

---

# 3.8. Cấu trúc ma trận của bài toán vận tải

Ví dụ:

$$
x=
[
x_{11},
x_{12},
x_{13},
x_{21},
x_{22},
x_{23}
]^T
$$

Ràng buộc supply:

$$
\begin{bmatrix}
1&1&1&0&0&0\\
0&0&0&1&1&1
\end{bmatrix}x
=
\begin{bmatrix}
s_1\\
s_2
\end{bmatrix}
$$

Demand:

$$
\begin{bmatrix}
1&0&0&1&0&0\\
0&1&0&0&1&0\\
0&0&1&0&0&1
\end{bmatrix}x
=
\begin{bmatrix}
d_1\\
d_2\\
d_3
\end{bmatrix}
$$

Có thể kết hợp:

$$
Ax=b
$$

Ma trận \(A\) rất thưa.

Mỗi biến:

$$
x_{ij}
$$

chỉ xuất hiện trong:

- một constraint supply;
- một constraint demand.

Do đó, dù bài toán lớn, sparse linear algebra cho phép solver xử lý hiệu quả.

---

# 3.9. Phương pháp giải tay và lựa chọn thuật toán

Trong phạm vi đề tài:

### Phần lý thuyết

Trình bày:

$$
Simplex
$$

vì đây là thuật toán kinh điển và thể hiện rõ quan hệ với Linear Algebra.

Một bài toán LP tổng quát kích thước nhỏ sẽ được giải tay bằng Simplex cơ bản: đưa về dạng chuẩn, lập tableau, chọn biến vào cơ sở và biến ra cơ sở, rồi pivot đến khi đạt tối ưu. Ví dụ này phục vụ minh họa cơ sở lý thuyết, không phải thuật toán chạy trong sản phẩm.

### Phần giải tay cho bài toán vận tải

Với case study 3 kho và 5 khách hàng ở Mục 2.10, báo cáo dùng NW Corner để lập nghiệm cơ sở khả thi ban đầu; sau đó dùng MODI để tính chi phí cơ hội và cải thiện đến tối ưu. Cách trình bày này ngắn gọn hơn generic Simplex tableau vì khai thác cấu trúc đặc biệt của ma trận vận tải.

Vogel được ưu tiên làm ví dụ chính vì thường cho nghiệm khởi tạo tốt; NW Corner và Least Cost được nêu để so sánh. Các phương pháp khởi tạo không được gọi là nghiệm tối ưu trước khi qua bước MODI.

### Phần phần mềm

Không nhất thiết tự triển khai toàn bộ Simplex cho bài toán lớn.

Có thể sử dụng solver:

$$
\boxed{\text{HiGHS}}
$$

thông qua:

$$
scipy.optimize.linprog
$$

hoặc:

$$
\boxed{\text{Google OR-Tools}}
$$

OR-Tools cung cấp các API cho linear optimization và nhiều lớp bài toán tối ưu khác.[^4]

Simplex, NW Corner, Least Cost, Vogel và MODI được trình bày trong báo cáo và giải tay; phần mềm không cần tự cài đặt các thuật toán này.

---

# 4. SẢN PHẨM PHẦN MỀM TÌM PHƯƠNG ÁN TỐI ƯU CHO BÀI TOÁN VẬN TẢI

## 4.1. Tên sản phẩm dự kiến

**TransportOpt – Hệ thống tối ưu phương án vận chuyển bằng quy hoạch tuyến tính**

---

# 4.2. Mục tiêu sản phẩm

Phần mềm nhận dữ liệu:

$$
Warehouse
+
Customer
+
Supply
+
Demand
+
Cost
$$

và trả về:

$$
Optimal\ Transportation\ Plan
$$

cùng với:

$$
Minimum\ Cost
$$

---

# 4.3. Dữ liệu đầu vào

Người dùng khai báo:

### Kho hàng

| Kho | Năng lực |
| --- | ---------: |
| W1  |         80 |
| W2  |         70 |

### Khách hàng

| Khách hàng | Nhu cầu |
| ------------ | -------: |
| C1           |       50 |
| C2           |       60 |
| C3           |       40 |

### Ma trận chi phí

|    | C1 | C2 | C3 |
| -- | -: | -: | -: |
| W1 |  4 |  6 |  8 |
| W2 |  5 |  4 |  3 |

---

# 4.4. Mô hình toán

Biến:

$$
x_{ij}
$$

Hàm mục tiêu:

$$
\min
4x_{11}
+6x_{12}
+8x_{13}
+5x_{21}
+4x_{22}
+3x_{23}
$$

Constraints:

$$
x_{11}+x_{12}+x_{13}\leq80
$$

$$
x_{21}+x_{22}+x_{23}\leq70
$$

$$
x_{11}+x_{21}=50
$$

$$
x_{12}+x_{22}=60
$$

$$
x_{13}+x_{23}=40
$$

$$
x_{ij}\geq0
$$

---

# 4.5. Kết quả mong đợi

Ví dụ:

| Từ | Đến | Lượng hàng |
| --- | ----- | ------------: |
| W1  | C1    |            50 |
| W1  | C2    |            30 |
| W2  | C2    |            30 |
| W2  | C3    |            40 |

Tổng:

$$
50+30=80
$$

đơn vị từ W1.

$$
30+40=70
$$

đơn vị từ W2.

Chi phí:

$$
50(4)+30(6)+30(4)+40(3)
$$

$$
=\boxed{620}
$$

---

# 4.6. Kiến trúc phần mềm

Kiến trúc đề xuất:

```text
┌─────────────────────────────┐
│       User Interface        │
│                             │
│ Warehouse / Customer / Cost │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      Input Validation       │
│                             │
│ Supply / Demand / Cost      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Mathematical Model Builder  │
│                             │
│   x, c, A, b, constraints   │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│    Optimization Engine      │
│                             │
│     HiGHS / OR-Tools        │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Result Analyzer       │
│                             │
│ Cost / Flow / Utilization   │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        Visualization        │
│                             │
│ Table / Matrix / Charts     │
└─────────────────────────────┘
```

---

# 4.7. Các chức năng chính

## Chức năng 1 – Quản lý kho

Cho phép:

- thêm kho;
- xóa kho;
- chỉnh sửa kho;
- nhập capacity.

---

## Chức năng 2 – Quản lý điểm nhận hàng

Cho phép:

- thêm khách hàng;
- xóa;
- sửa;
- nhập demand.

---

## Chức năng 3 – Nhập ma trận chi phí

Người dùng nhập:

$$
C=
\begin{bmatrix}
c_{11}&\cdots&c_{1n}\\
\vdots&&\vdots\\
c_{m1}&\cdots&c_{mn}
\end{bmatrix}
$$

---

## Chức năng 4 – Kiểm tra dữ liệu

Hệ thống kiểm tra:

$$
TotalSupply\geq TotalDemand
$$

Nếu:

$$
TotalSupply<TotalDemand
$$

hệ thống cảnh báo bài toán không thể đáp ứng toàn bộ nhu cầu.

---

## Chức năng 5 – Tạo mô hình toán tự động

Chuyển dữ liệu thành:

$$
c
$$

$$
A_{ub}
$$

$$
b_{ub}
$$

$$
A_{eq}
$$

$$
b_{eq}
$$

Đây là phần thể hiện rõ nhất kiến thức Linear Algebra trong sản phẩm.

---

## Chức năng 6 – Tối ưu

Gửi mô hình tới solver.

Ví dụ với SciPy:

$$
linprog(c,A_{ub},b_{ub},A_{eq},b_{eq})
$$

SciPy hiện sử dụng HiGHS làm solver mặc định cho `linprog`, với các phương pháp simplex và interior-point hiệu năng cao.[^2]

---

## Chức năng 7 – Hiển thị kết quả

Bao gồm:

- số lượng vận chuyển trên từng tuyến;
- tổng chi phí;
- lượng hàng còn lại tại từng kho;
- tỷ lệ sử dụng capacity.

---

# 4.8. Công nghệ đề xuất

## Ngôn ngữ

$$
\boxed{Python}
$$

### Tính toán

- NumPy;
- Pandas.

### Optimization

Ưu tiên:

$$
\boxed{SciPy + HiGHS}
$$

hoặc:

$$
\boxed{Google\ OR\text{-}Tools}
$$

### Giao diện

Đơn giản nhất:

$$
\boxed{Streamlit}
$$

Kiến trúc:

```text
Streamlit
    ↓
Python
    ↓
NumPy/Pandas
    ↓
SciPy / HiGHS
```

Ưu điểm:

- dễ triển khai;
- ít code frontend;
- phù hợp đồ án;
- dễ demo.

---

# 4.9. Pipeline xử lý

```text
Nhập dữ liệu
     ↓
Kiểm tra dữ liệu
     ↓
Tạo decision variables
     ↓
Tạo cost vector c
     ↓
Tạo constraint matrix A
     ↓
Tạo vector b
     ↓
Giải LP
     ↓
Kiểm tra trạng thái solver
     ↓
Tính tổng chi phí
     ↓
Hiển thị phương án tối ưu
```

---

# 4.10. Phương pháp đánh giá

Không nên chỉ demo phần mềm chạy được mà cần đánh giá định lượng.

## Metric 1 – Optimal Cost

$$
C^*
$$

là chi phí phương án solver tìm được.

---

## Metric 2 – Constraint violation

Kiểm tra:

$$
|Ax-b|
$$

hoặc:

$$
Ax-b
$$

Mong muốn:

$$
Violation\approx0
$$

---

## Metric 3 – Runtime

Đo:

$$
T_{solve}
$$

theo quy mô bài toán.

---

## Metric 4 – Saving Ratio

So với một phương pháp baseline:

$$
Saving=
\frac{C_{baseline}-C_{optimal}}
{C_{baseline}}
\times100\%
$$

---

# 4.11. Baseline

## Phương pháp tham chiếu trong báo cáo

NW Corner, Least Cost và Vogel là các baseline cho **ví dụ giải tay cân bằng**. Bảng so sánh cần phân biệt rõ chi phí khởi tạo với chi phí tối ưu sau MODI/HiGHS:

| Phương pháp | Vai trò                      | Giá trị so sánh                       |
| -------------- | ----------------------------- | ---------------------------------------- |
| NW Corner      | Nghiệm ban đầu             | Chi phí khởi tạo                      |
| Least Cost     | Nghiệm ban đầu             | Chi phí khởi tạo                      |
| Vogel          | Nghiệm ban đầu             | Chi phí khởi tạo                      |
| MODI           | Cải thiện nghiệm vận tải | Chi phí tối ưu của ví dụ giải tay |
| HiGHS          | Solver đối chứng           | Xác nhận chi phí tối ưu             |

Các baseline này không bắt buộc xuất hiện trong giao diện phần mềm hoặc benchmark quy mô lớn.

Có thể xây phương pháp:

### Greedy Nearest Cost

Với từng khách hàng:

1. chọn kho có chi phí vận chuyển thấp nhất;
2. lấy hàng cho đến khi kho hết capacity;
3. chuyển sang kho tiếp theo.

Phương pháp này đơn giản nhưng không đảm bảo global optimum.

So sánh:

$$
Greedy
$$

với:

$$
LP
$$

sẽ giúp chứng minh lợi ích của tối ưu toán học.

---

# 4.12. Thực nghiệm

Đề xuất 5 nhóm:

| Dataset    | Kho | Khách hàng | Số biến |
| ---------- | --: | -----------: | --------: |
| Small      |   2 |            3 |         6 |
| Small+     |   5 |           10 |        50 |
| Medium     |  10 |           50 |       500 |
| Large      |  50 |          100 |     5.000 |
| Very Large | 100 |          500 |    50.000 |

Số biến:

$$
N=m\times n
$$

Đo:

- runtime;
- objective;
- memory;
- saving so với greedy.

Case study 3 kho và 5 khách hàng ở Mục 2.10 được giữ cố định để đối chiếu đúng kết quả 696 giữa giải tay và HiGHS. Nó không được dùng để suy luận hiệu năng; các nhóm dữ liệu trong bảng mới là cơ sở đo runtime và khả năng mở rộng.

---

# 4.13. Giao diện dự kiến

## Trang 1 – Input

```text
WAREHOUSES

W1   Capacity: 80
W2   Capacity: 70

CUSTOMERS

C1   Demand: 50
C2   Demand: 60
C3   Demand: 40
```

---

## Trang 2 – Cost Matrix

```text
       C1  C2  C3
W1      4   6   8
W2      5   4   3
```

---

## Trang 3 – Optimization

Nút:

**$Find Optimal Solution$**

---

## Trang 4 – Result

```text
OPTIMAL COST: 620

W1 → C1: 50
W1 → C2: 30

W2 → C2: 30
W2 → C3: 40
```

Có thể bổ sung heatmap của ma trận shipment.

---

# 4.14. Các trường hợp kiểm thử

### Trường hợp 1

$$
Supply=Demand
$$

→ balanced transportation.

### Trường hợp 2

$$
Supply>Demand
$$

→ một phần capacity không sử dụng.

### Trường hợp 3

$$
Supply<Demand
$$

→ infeasible.

### Trường hợp 4

Một tuyến có chi phí rất lớn.

Solver phải hạn chế sử dụng tuyến đó.

### Trường hợp 5

Nhiều phương án tối ưu bằng nhau.

Solver có thể trả về một trong các optimal solutions.

---

# 4.15. Hướng mở rộng

Sau phiên bản cơ bản, hệ thống có thể mở rộng sang:

## Nhiều sản phẩm

$$
x_{ijp}
$$

---

## Multi-period

$$
x_{ijt}
$$

---

## Chi phí cố định

Ví dụ:

> Nếu sử dụng một tuyến thì phải trả một khoản phí cố định.

Khi đó cần binary variable:

$$
y_{ij}\in\{0,1\}
$$

và bài toán trở thành:

$$
MILP
$$

---

## Facility Location

Quyết định:

$$
Open\ Warehouse?
$$

---

## Vehicle Routing

Không chỉ quyết định:

$$
How\ Much?
$$

mà còn:

$$
Which\ Route?
$$

---

## Demand uncertainty

Có thể mở rộng sang:

- robust optimization;
- stochastic optimization.

---

# 5. KẾT LUẬN

Đề tài tập trung nghiên cứu mối liên hệ giữa ba lĩnh vực:

$$
\boxed{
Linear\ Algebra
\rightarrow
Linear\ Programming
\rightarrow
Logistics
}
$$

Thông qua bài toán vận tải, các khái niệm của đại số tuyến tính như:

- vector;
- ma trận;
- hệ phương trình;
- cơ sở;
- hạng của ma trận;
- ma trận nghịch đảo;
- sparse matrix;

không còn chỉ mang tính lý thuyết mà được sử dụng trực tiếp để mô hình hóa một bài toán thực tế.

Bài toán vận tải được mô hình hóa dưới dạng:

$$
\boxed{
\min c^Tx
}
$$

subject to:

$$
\boxed{
Ax=b,\quad x\geq0
}
$$

Đây là một ví dụ điển hình cho việc sử dụng đại số tuyến tính làm nền tảng cho tối ưu hóa.

Thuật toán Simplex tiếp tục sử dụng các khái niệm:

$$
Basis
$$

$$
B^{-1}b
$$

$$
Reduced\ Cost
$$

để lần lượt tìm các nghiệm cơ sở khả thi tốt hơn cho đến khi đạt phương án tối ưu.

Phần sản phẩm của đề tài sẽ xây dựng một ứng dụng hoàn chỉnh theo pipeline:

$$
\boxed{
Data
\rightarrow
Matrix\ Representation
\rightarrow
LP\ Model
\rightarrow
Solver
\rightarrow
Optimal\ Transportation\ Plan
}
$$

Qua đó đề tài vừa có giá trị về mặt toán học, vừa có khả năng ứng dụng thực tế.

Một ưu điểm khác của hướng nghiên cứu này là phạm vi có thể kiểm soát tốt. Phiên bản cơ bản có thể hoàn thành với LP và Transportation Problem, trong khi các hướng nghiên cứu nâng cao như MILP, facility location, vehicle routing và stochastic optimization vẫn có thể được phát triển sau đó mà không cần thay đổi nền tảng ban đầu.

---

# PHÂN BỔ ĐỘ DÀI BÁO CÁO ĐỀ XUẤT

Để đáp ứng yêu cầu **phần khái niệm + lý thuyết tối đa 10 trang A4**, có thể phân bổ như sau:

| Nội dung                                  | Số trang dự kiến |
| ------------------------------------------ | ------------------: |
| 1. Phần mở đầu                         |                1–2 |
| 2. Khái niệm + bài toán thực tế      |                3–4 |
| 3. Cơ sở lý thuyết + thuật toán      |                5–6 |
| **Tổng lý thuyết Chương 2 + 3** |     **8–10** |
| 4. Phần mềm                              |                5–8 |
| 5. Kết luận                              |                   1 |
| Tài liệu tham khảo                      |                1–2 |

Tổng báo cáo dự kiến:

$$
\boxed{16-22\text{ trang A4}}
$$

không tính phụ lục.

---

# FOOTNOTE ĐỀ XUẤT

---

# DANH MỤC TÀI LIỆU THAM KHẢO

[1] Dantzig, G. B., *Linear Programming and Extensions*, Princeton University Press, 1963.

[2] Chvátal, V., *Linear Programming*, W. H. Freeman, 1983.

[3] Bertsimas, D., Tsitsiklis, J. N., *Introduction to Linear Optimization*, Athena Scientific, 1997.

[4] Boyd, S., Vandenberghe, L., *Convex Optimization*, Cambridge University Press, 2004.

[5] Hillier, F. S., Lieberman, G. J., *Introduction to Operations Research*, McGraw-Hill.

[6] Taha, H. A., *Operations Research: An Introduction*, Pearson.

[7] Bazaraa, M. S., Jarvis, J. J., Sherali, H. D., *Linear Programming and Network Flows*, Wiley.

[8] Google, *OR-Tools – Linear Optimization Documentation*.

[9] Google, *OR-Tools – Advanced LP Solving*.

[10] Google, *OR-Tools Optimization Examples*.

[11] SciPy Developers, *scipy.optimize.linprog Documentation*.

[12] Huangfu, Q., Hall, J. A. J., “Parallelizing the dual revised simplex method”, *Mathematical Programming Computation*.

[13] Schrijver, A., *Theory of Linear and Integer Programming*, Wiley.

[14] Ahuja, R. K., Magnanti, T. L., Orlin, J. B., *Network Flows: Theory, Algorithms, and Applications*, Prentice Hall.
