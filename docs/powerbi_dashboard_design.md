# 🎨 Hướng Dẫn Thiết Kế Dashboard Power BI (Data Modeling & DAX)

Tài liệu này cung cấp toàn bộ kiến trúc mô hình dữ liệu (Data Model), các công thức đo lường DAX chuẩn, và bố cục giao diện 3 trang Dashboard chuyên nghiệp cho dự án **E-Commerce Customer Retention & RFM Segmentation**.

---

## 1. Mô Hình Dữ Liệu (Star Schema)

Khi nạp dữ liệu từ thư mục `data/raw/` và `data/processed/` vào Power BI Desktop:

* **Bảng FACT (Bảng Sự kiện):**
  * `orders`: Lưu mã đơn, ngày mua, ngày giao, trạng thái.
  * `order_items`: Lưu chi tiết từng món hàng, giá tiền (`price`), phí ship (`freight_value`).

* **Bảng DIMENSION (Bảng Chiều phân tích):**
  * `customers`: Thông tin khách hàng (`customer_id`, `customer_unique_id`, `customer_city`, `customer_region`).
  * `products`: Thông tin sản phẩm (`product_id`, `product_category`, `cost_price`).
  * `rfm_customer_segments`: Bảng phân khúc RFM (`customer_unique_id`, `Recency`, `Frequency`, `Monetary`, `Customer_Segment`).
  * `order_reviews`: Đánh giá của khách (`order_id`, `review_score`).
  * `Dim_Date`: Tạo bảng lịch tự động trong Power BI bằng DAX để lọc thời gian chuẩn.

### Thiết lập quan hệ (Relationships):
* `orders[order_id]` **(1) ── (N)** `order_items[order_id]`
* `customers[customer_id]` **(1) ── (N)** `orders[customer_id]`
* `products[product_id]` **(1) ── (N)** `order_items[product_id]`
* `customers[customer_unique_id]` **(N) ── (1)** `rfm_customer_segments[customer_unique_id]`
* `orders[order_id]` **(1) ── (1)** `order_reviews[order_id]`
* `Dim_Date[Date]` **(1) ── (N)** `orders[order_purchase_timestamp]`

---

## 2. Bảng Lịch Chuẩn (Calendar Table) trong Power BI

```dax
Dim_Date = 
VAR MinYear = YEAR(MIN(orders[order_purchase_timestamp]))
VAR MaxYear = YEAR(MAX(orders[order_purchase_timestamp]))
RETURN
ADDCOLUMNS(
    CALENDAR(DATE(MinYear, 1, 1), DATE(MaxYear, 12, 31)),
    "Year", YEAR([Date]),
    "Month_Num", MONTH([Date]),
    "Month_Name", FORMAT([Date], "MMM"),
    "Year_Month", FORMAT([Date], "YYYY-MM"),
    "Quarter", "Q" & FORMAT([Date], "Q"),
    "Day_of_Week", FORMAT([Date], "dddd")
)
```

---

## 3. Các Công Thức Đo Lường DAX Cốt Lõi (Core Measures)

### 3.1. Các chỉ số Tài chính & Bán hàng (Sales KPIs)
```dax
Total Revenue = SUM(order_items[price])
```

```dax
Total Delivered Orders = 
CALCULATE(
    DISTINCTCOUNT(orders[order_id]),
    orders[order_status] = "delivered"
)
```

```dax
Average Order Value = 
DIVIDE([Total Revenue], [Total Delivered Orders], 0)
```

```dax
Revenue Last Month = 
CALCULATE(
    [Total Revenue],
    DATEADD(Dim_Date[Date], -1, MONTH)
)
```

```dax
MoM Revenue Growth % = 
DIVIDE([Total Revenue] - [Revenue Last Month], [Revenue Last Month], 0)
```

### 3.2. Chỉ số Khách hàng & Vận hành (Customer & Operational KPIs)
```dax
Unique Customers = DISTINCTCOUNT(customers[customer_unique_id])
```

```dax
Avg Review Score = AVERAGE(order_reviews[review_score])
```

```dax
Late Delivery Rate % = 
VAR TotalDelivered = CALCULATE(COUNTROWS(orders), orders[order_status] = "delivered")
VAR LateOrders = 
    CALCULATE(
        COUNTROWS(orders),
        orders[order_status] = "delivered",
        orders[order_delivered_customer_date] > orders[order_estimated_delivery_date]
    )
RETURN
DIVIDE(LateOrders, TotalDelivered, 0)
```

---

## 4. Thiết Kế Bố Cục 3 Trang Dashboard (Dashboard Architecture)

### 📌 Trang 1: Executive KPI & Sales Overview
* **Hàng trên cùng (Card Visuals):** Total Revenue | Total Orders | AOV | Avg CSAT | Late Delivery %
* **Biểu đồ chính (Bên trái):** `Area Chart / Line Chart` Doanh thu theo tháng so sánh cùng kỳ
* **Biểu đồ phụ (Bên phải):** `Clustered Bar Chart` Doanh thu theo danh mục | `Bar Chart` Doanh thu theo vùng miền
* **Góc dưới:** `Scatter Plot` Tương quan thời gian giao hàng và điểm review

### 📌 Trang 2: Cohort Retention Analysis
* **Visual Trọng tâm:** `Matrix Visual (Heatmap)` với Rows là Cohort Month, Columns là Cohort Index, Values là Retention Rate %
* **Card tóm tắt:** Tỷ lệ quay lại tháng thứ 1 (Month 1 Retention Rate) | Tỷ lệ khách mua từ 2 lần trở lên (Repeat Customer Rate)

### 📌 Trang 3: RFM Customer Segmentation & Action Matrix
* **Hàng trên (KPI):** Số lượng khách VIP | % Doanh thu từ VIP | Số lượng khách At Risk
* **Biểu đồ Donut Chart:** Cơ cấu doanh thu theo phân khúc RFM
* **Biểu đồ Treemap / Scatter Plot:** Trục X Recency, Trục Y Monetary, Kích thước Frequency, Màu sắc Customer Segment
* **Bảng chi tiết (Customer Action List):** Cột Customer ID, Segment, Recency, Total Spent, Region kèm nút Export
