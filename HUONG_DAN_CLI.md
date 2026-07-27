## 📘 HƯỚNG DẪN SỬ DỤNG 50 LỆNH - CHO NGƯỜI KHÔNG BIẾT LẬP TRÌNH

> **Tác giả:** Nhà khoa học Lê Thanh Tùng  
> **Đối tượng:** Các đồng chí không biết lập trình

---

### Trước khi bắt đầu

- Mở terminal (cửa sổ đen) trên máy tính.
- Gõ lệnh sau để vào thư mục chứa công cụ:
```bash
cd ~/viettelrace2026spongeos
```
- Mỗi lệnh bắt đầu bằng chữ `bench`. Nhà khoa học chỉ cần copy nguyên dòng lệnh, dán vào terminal, rồi nhấn Enter.

---

### 1️⃣ NHÓM LỆNH CHẠY THỬ (RUN) - 15 lệnh

**Mục đích:** Chạy thử hệ thống với các cấu hình khác nhau để xem nó chạy nhanh hay chậm.

| Lệnh | Nó làm gì? | Giải thích cho trẻ em |
|------|------------|----------------------|
| `bench run` | Chạy thử với cấu hình mặc định | "Chạy thử bình thường, máy tự chọn cách chạy." |
| `bench run-fast` | Chạy thử để được nhanh nhất có thể | "Chạy thử để được nhanh nhất, nhưng tốn điện." |
| `bench run-cheap` | Chạy thử để tốn ít tài nguyên nhất | "Chạy thử để tiết kiệm pin, nhưng chậm hơn." |
| `bench run-balanced` | Chạy thử cân bằng giữa nhanh và tiết kiệm | "Chạy thử vừa đủ, không nhanh quá cũng không chậm quá." |
| `bench run-h200` | Chạy thử trên máy tính mạnh nhất (giả lập H200) | "Giả vờ máy tính là siêu máy tính, xem nó chạy nhanh cỡ nào." |
| `bench run-edge` | Chạy thử trên máy tính yếu nhất (giả lập Edge) | "Giả vờ máy tính là máy tính bàn cũ, xem nó có chạy được không." |
| `bench run-all` | Chạy thử trên tất cả các loại máy tính (4 loại) | "Chạy thử trên cả 4 loại máy tính, so sánh xem loại nào nhanh nhất." |
| `bench run-comparison edge h200` | So sánh 2 loại máy tính (ví dụ: Edge và H200) | "Chạy thử trên máy yếu và máy mạnh, rồi so sánh." |
| `bench run-batch-sweep` | Chạy thử với các kích thước lô khác nhau | "Thử gửi 1, 2, 4, 8,... câu hỏi cùng lúc, xem cái nào nhanh nhất." |
| `bench run-quant-sweep` | Chạy thử với các kiểu nén số khác nhau | "Thử nén số theo 3 kiểu, xem kiểu nào vừa nhanh vừa ít tốn bộ nhớ." |
| `bench run-sched-sweep` | Chạy thử với các cách sắp xếp câu hỏi khác nhau | "Thử 3 cách sắp xếp thứ tự câu hỏi, xem cách nào xử lý nhanh nhất." |
| `bench run-concurrency-sweep` | Chạy thử với số người dùng cùng lúc khác nhau | "Thử có 1, 2, 4, 8, 16 người hỏi cùng lúc, xem máy chịu được bao nhiêu." |
| `bench run-stress` | Chạy thử với áp lực cao (nhiều câu hỏi cùng lúc) | "Bắn 100 câu hỏi cùng lúc để xem máy có bị đơ không." |
| `bench run-soak` | Chạy thử trong thời gian dài (5 phút) | "Cho máy chạy liên tục 5 phút để xem có bị nóng hay chậm dần không." |
| `bench run-chaos` | Chạy thử với các lỗi giả định (mất điện, nghẽn mạng) | "Giả vờ mất điện, nghẽn mạng, xem máy có tự cứu được không." |

---

### 2️⃣ NHÓM LỆNH KIỂM TRA (TEST) - 6 lệnh

**Mục đích:** Kiểm tra xem hệ thống có bị lỗi không.

| Lệnh | Nó làm gì? | Giải thích cho trẻ em |
|------|------------|----------------------|
| `bench test` | Chạy tất cả các bài kiểm tra | "Kiểm tra toàn bộ hệ thống một lượt." |
| `bench test-property` | Kiểm tra tính ổn định với 100.000 tình huống | "Kiểm tra 100.000 tình huống ngẫu nhiên, xem có tình huống nào làm máy lỗi không." |
| `bench test-suite` | Kiểm tra các chức năng cơ bản | "Kiểm tra các chức năng chính của máy." |
| `bench test-super` | Kiểm tra 17 chức năng nâng cao | "Kiểm tra 17 chức năng phức tạp hơn." |
| `bench test-all` | Chạy tất cả các bài kiểm tra (full) | "Kiểm tra mọi thứ từ đầu đến cuối." |
| `bench test-quick` | Kiểm tra nhanh (chỉ 10.000 tình huống) | "Kiểm tra nhanh trong 1 phút, chỉ 10.000 tình huống." |

---

### 3️⃣ NHÓM LỆNH SO SÁNH (COMPARE) - 4 lệnh

**Mục đích:** So sánh các kết quả chạy thử với nhau.

| Lệnh | Nó làm gì? | Giải thích cho trẻ em |
|------|------------|----------------------|
| `bench compare` | So sánh 2 kết quả chạy thử gần nhất | "So sánh lần chạy vừa rồi với lần trước đó." |
| `bench compare-best` | Tìm ra cấu hình chạy nhanh nhất trong tất cả các lần chạy | "Xem trong tất cả các lần chạy, lần nào nhanh nhất và dùng cấu hình gì." |
| `bench compare-table` | Hiển thị bảng so sánh các lần chạy | "Hiện bảng so sánh các lần chạy gần đây, nhìn rõ từng cái." |
| `bench compare-latest` | So sánh 2 kết quả mới nhất (giống `compare`) | "Giống lệnh `compare`." |

---

### 4️⃣ NHÓM LỆNH XEM KẾT QUẢ (SHOW) - 5 lệnh

**Mục đích:** Xem kết quả chạy thử.

| Lệnh | Nó làm gì? | Giải thích cho trẻ em |
|------|------------|----------------------|
| `bench show` | Hiển thị kết quả chạy thử gần nhất | "Cho xem kết quả của lần chạy thử cuối cùng." |
| `bench show-best` | Hiển thị cấu hình nhanh nhất | "Cho biết cấu hình nào nhanh nhất." |
| `bench show-history` | Hiển thị danh sách các lần chạy trước đó | "Liệt kê các lần chạy thử đã làm trước đây." |
| `bench show-summary` | Hiển thị tóm tắt tất cả các lần chạy | "Tóm tắt tất cả các lần chạy, xem cái nào tốt nhất." |
| `bench show-latest` | Giống `show` | "Giống lệnh `show`." |

---

### 5️⃣ NHÓM LỆNH XUẤT BÁO CÁO (EXPORT) - 4 lệnh

**Mục đích:** Tạo file báo cáo để gửi cho người khác.

| Lệnh | Nó làm gì? | Giải thích cho trẻ em |
|------|------------|----------------------|
| `bench export` | Xuất báo cáo dạng Markdown (đẹp) | "Tạo một file báo cáo có định dạng đẹp, ai cũng đọc được." |
| `bench export-md` | Giống `export` | "Giống lệnh `export`." |
| `bench export-csv` | Xuất báo cáo dạng CSV (bảng tính) | "Tạo một file bảng tính (Excel) để xem số liệu." |
| `bench export-json` | Xuất kết quả thô dạng JSON (dành cho kỹ thuật) | "Tạo file dữ liệu thô, dành cho người biết lập trình." |

---

### 6️⃣ NHÓM LỆNH THEO DÕI (MONITOR) - 4 lệnh

**Mục đích:** Xem máy tính đang hoạt động thế nào.

| Lệnh | Nó làm gì? | Giải thích cho trẻ em |
|------|------------|----------------------|
| `bench monitor` | Xem CPU và bộ nhớ đang dùng bao nhiêu | "Cho biết máy tính đang mệt hay khỏe (CPU và RAM)." |
| `bench monitor-gpu` | Xem card đồ họa đang làm gì | "Cho biết card đồ họa (GPU) đang chạy thế nào." |
| `bench monitor-memory` | Xem bộ nhớ đang dùng bao nhiêu | "Cho biết máy tính còn bao nhiêu bộ nhớ trống." |
| `bench monitor-realtime` | Theo dõi liên tục, cập nhật mỗi giây | "Cứ mỗi giây lại cập nhật tình trạng máy tính một lần." |

---

### 7️⃣ NHÓM LỆNH TRIỂN KHAI (DEPLOY) - 4 lệnh

**Mục đích:** Cài đặt và chạy mô hình lên máy chủ.

| Lệnh | Nó làm gì? | Giải thích cho trẻ em |
|------|------------|----------------------|
| `bench deploy` | Triển khai mô hình (mặc định) | "Cài đặt mô hình lên máy chủ và chạy." |
| `bench deploy-vllm` | Triển khai với vLLM (công cụ chuyên dụng) | "Cài đặt bằng công cụ vLLM, thường là nhanh nhất." |
| `bench deploy-tgi` | Triển khai với TGI (công cụ khác) | "Cài đặt bằng công cụ TGI, một lựa chọn khác." |
| `bench deploy-clean` | Xóa hết các bản cài đặt cũ | "Dọn dẹp sạch sẽ, xóa các bản triển khai trước đó." |

---

### 8️⃣ NHÓM LỆNH KIỂM TRA SỨC KHỎE (HEALTH) - 3 lệnh

**Mục đích:** Kiểm tra máy tính có ổn không.

| Lệnh | Nó làm gì? | Giải thích cho trẻ em |
|------|------------|----------------------|
| `bench health` | Kiểm tra sức khỏe tổng thể | "Xem máy tính có đang khỏe mạnh không." |
| `bench health-check` | Giống `health` | "Kiểm tra CPU, bộ nhớ, card đồ họa xem có vấn đề gì không." |
| `bench health-report` | Tạo báo cáo sức khỏe | "Tạo một file báo cáo tình trạng máy tính." |

---

### 9️⃣ NHÓM LỆNH CẤU HÌNH (CONFIG) - 5 lệnh

**Mục đích:** Xem và thay đổi cài đặt.

| Lệnh | Nó làm gì? | Giải thích cho trẻ em |
|------|------------|----------------------|
| `bench config` | Xem cấu hình hiện tại | "Cho xem các cài đặt hiện tại của máy." |
| `bench config-show` | Giống `config` | "Xem cấu hình." |
| `bench config-set batch=32` | Đặt lại tham số (ví dụ: batch=32) | "Thay đổi một cài đặt, ví dụ số lượng câu hỏi gửi cùng lúc." |
| `bench config-reset` | Đặt lại cấu hình về mặc định | "Trở về cài đặt gốc ban đầu." |
| `bench config-recommend` | Tự động đề xuất cấu hình phù hợp với máy | "Máy sẽ tự khuyên dùng cấu hình nào cho phù hợp." |

---

### 🔟 NHÓM LỆNH TIỆN ÍCH (MISC) - 4 lệnh

**Mục đích:** Lệnh phụ trợ.

| Lệnh | Nó làm gì? | Giải thích cho trẻ em |
|------|------------|----------------------|
| `bench help` | Hiển thị tất cả các lệnh | "Hiện ra danh sách các lệnh có thể dùng." |
| `bench info` | Hiển thị thông tin máy tính | "Cho biết máy tính đang dùng hệ điều hành gì, CPU bao nhiêu nhân, RAM bao nhiêu GB." |
| `bench clean` | Xóa hết các file log và kết quả cũ | "Dọn dẹp sạch sẽ, xóa các file tạm." |
| `bench version` | Hiển thị phiên bản công cụ | "Cho biết công cụ đang ở phiên bản nào." |

---

## 📌 LƯU Ý QUAN TRỌNG

- **Khi chạy lệnh**, hãy đảm bảo Nhà khoa học đang đứng trong thư mục `~/viettelrace2026spongeos` (gõ `cd ~/viettelrace2026spongeos` trước).
- **Kết quả** sẽ được lưu vào thư mục `benchmark_results/` và `benchmark_logs/`. Các đồng chí có thể xem file báo cáo mới nhất tên `BENCHMARK_REPORT.md` hoặc `report_YYYYMMDD_HHMMSS.md`.
- **Lệnh `bench clean`** sẽ xóa hết dữ liệu cũ, cẩn thận khi dùng.

---

## 📖 CÁCH DÙNG NHANH CHO NGƯỜI MỚI

1. Mở terminal.
2. `cd ~/viettelrace2026spongeos`
3. `bench run-fast` → chạy thử nhanh.
4. `bench show-best` → xem kết quả tốt nhất.
5. `bench export-md` → tạo báo cáo để gửi.

---

**Chúc các đồng chí thành công!** 🚀
