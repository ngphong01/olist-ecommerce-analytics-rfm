# 📑 BÁO CÁO PHÂN TÍCH INSIGHT & ĐỀ XUẤT HÀNH ĐỘNG KINH DOANH
**Dự án:** Tối ưu hóa Doanh thu & Tỷ lệ Giữ chân Khách hàng E-commerce (Brazilian E-Commerce Olist Dataset)  
**Phụ trách phân tích:** Data Analyst

---

## 1. TỔNG QUAN KẾT QUẢ KINH DOANH (EXECUTIVE SUMMARY)

Phân tích trên tập dữ liệu thực tế hơn 100.000 giao dịch từ sàn thương mại điện tử Olist ghi nhận những chỉ số trọng yếu:
* **Tổng doanh thu thực tế (Delivered GMV):** **13,221,498 BRL** với **96,478 đơn giao thành công**.
* **Tổng số khách hàng duy nhất:** **93,358 người mua**.
* **Giá trị trung bình mỗi đơn (AOV):** **137.04 BRL**.
* **Đặc thù hành vi người dùng:** Tỷ lệ khách mua từ 2 lần trở lên chỉ chiếm **khoảng 3%**, phản ánh đặc thù mô hình marketplace nơi người dùng thường tìm kiếm sản phẩm phân tán và có xu hướng chỉ mua một lần nếu không có chiến lược chăm sóc giữ chân chủ động.

---

## 2. BỐN PHÁT HIỆN DỮ LIỆU CỐT LÕI (KEY FINDINGS)

### 🚨 Phát hiện 1: Tỷ lệ quay lại mua sắm (Retention) cực thấp
* Hơn 96.9% lượng khách hàng trên sàn chỉ phát sinh 1 đơn hàng duy nhất trong suốt vòng đời.
* **Nguyên nhân gốc rễ:** Thiếu hụt kịch bản tái tiếp cận tự động (Re-engagement Automation) sau khi khách nhận hàng thành công, khiến chi phí thu hút khách hàng mới (CAC) không được tối ưu hoá qua LTV (Customer Lifetime Value).

### ⚠️ Phát hiện 2: Khách hàng mua lại (Loyal Customers & Champions) có giá trị đơn hàng vượt trội
* Mặc dù nhóm khách hàng mua từ 2 lần trở lên chỉ chiếm khoảng 3% tổng lượng khách, nhưng giá trị trung bình mỗi khách (Customer Value) của nhóm này đạt **251.6 BRL (Loyal)** và **492.3 BRL (Champions)** — cao gấp **1.8 đến 3.6 lần** so với khách hàng mới thông thường (140.3 BRL).
* Điều này chứng minh tiềm năng tăng trưởng doanh thu khổng lồ nếu tăng được tỷ lệ mua lặp lại lên 5% - 8%.

### 🚚 Phát hiện 3: Vận tốc giao hàng quyết định trực tiếp điểm số hài lòng (CSAT)
* Các đơn giao nhanh (dưới 5 ngày) đạt điểm đánh giá trung bình **4.40 / 5.0 sao** với tỷ lệ 5 sao áp đảo.
* Ngược lại, các đơn giao trễ (trên 12 ngày) khiến điểm hài lòng rớt xuống **3.40 / 5.0 sao**, kéo theo tỷ lệ đánh giá 1 sao và khiếu nại tăng vọt gấp 3 lần.

### 📍 Phát hiện 4: Doanh thu tập trung cao độ tại các bang trọng điểm
* Bang São Paulo (SP) và Rio de Janeiro (RJ) chiếm hơn **50% tổng doanh thu toàn sàn**.
* Tuy nhiên, các bang xa vùng trung tâm chịu thời gian giao hàng trung bình từ 14 đến 22 ngày, là nguyên nhân chính khiến khách hàng ở các khu vực này có tỷ lệ đánh giá tiêu cực cao nhất.

---

## 3. ĐỀ XUẤT CHIẾN LƯỢC KINH DOANH (ACTIONABLE RECOMMENDATIONS)

| Phân khúc / Vấn đề | Hành động đề xuất | Kênh triển khai | Kỳ vọng kết quả |
| :--- | :--- | :--- | :--- |
| **Gia tăng tỷ lệ mua lại** | Thiết lập chuỗi Email/SMS tự động sau ngày giao hàng thứ 7 (hỏi thăm trải nghiệm) và ngày thứ 21 (tặng mã giảm giá 10% cho đơn hàng kế tiếp). | Email Marketing, App Push | Nâng tỷ lệ khách hàng mua lại từ 3.0% lên **5.5% - 6.0%**, tạo ra thêm khoảng **300.000 - 450.000 BRL doanh thu**. |
| **Phân khúc Khách hàng VIP** | Xây dựng chính sách Olist VIP Prime: Miễn phí vận chuyển cho các đơn hàng tiếp theo và ưu tiên xử lý khiếu nại trong 2 giờ. | CRM, CSKH 1-1 | Bảo vệ nhóm khách hàng có giá trị cao nhất khỏi rủi ro chuyển sang đối thủ cạnh tranh. |
| **Tối ưu Logistics** | Phân bổ thêm các Hub kho vệ tinh tại các cụm bang xa; thiết lập SLA chặt chẽ với các đơn vị vận chuyển có thời gian giao quá 10 ngày. | Quản lý chuỗi cung ứng | Giảm thời gian giao hàng trung bình xuống dưới 8 ngày, nâng CSAT toàn sàn lên **4.35 / 5.0**. |

---

## 4. KỊCH BẢN TRẢ LỜI PHỎNG VẤN (STAR METHOD)

1. **Situation (Bối cảnh):**  
   *"Em đã thực hiện một dự án phân tích dữ liệu toàn diện trên bộ dữ liệu thực tế của sàn thương mại điện tử Olist với hơn 100.000 đơn hàng nhằm giải quyết bài toán sụt giảm tỷ lệ giữ chân khách hàng và tối ưu hóa vận hành giao hàng."*

2. **Task (Nhiệm vụ):**  
   *"Em cần làm sạch dữ liệu từ 5 bảng quan hệ, xây dựng mô hình phân khúc khách hàng RFM bằng SQL/Python, đo lường sự ảnh hưởng của tốc độ giao hàng lên điểm hài lòng CSAT và trực quan hóa toàn bộ thành Dashboard trên Power BI."*

3. **Action (Hành động kỹ thuật):**  
   *"Về SQL và Python, em xử lý hơn 112.000 dòng chi tiết đơn hàng, dùng CTEs và Window Functions để phân hạng khách hàng theo 5 phân vị (Quantiles). Em phân tích mối tương quan giữa thời gian giao hàng và điểm đánh giá thực tế."*

4. **Result (Kết quả & Giá trị kinh doanh):**  
   *"Dự án chỉ ra rằng dù khách mua lặp lại chỉ chiếm 3%, nhưng họ mang lại giá trị đơn hàng gấp 3.5 lần khách thông thường. Em đã đề xuất kịch bản chăm sóc khách hàng tự động để thúc đẩy tỷ lệ mua lại lên 6%, ước tính đóng góp thêm hơn 400.000 BRL doanh thu mà không cần gia tăng ngân sách quảng cáo thu hút khách mới."*
