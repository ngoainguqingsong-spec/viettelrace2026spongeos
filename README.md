# 🚀 Viettel AI Race 2026 - LLM Inference Optimization

> **Đề 3:** Tối ưu hiệu năng serving cho LLM trên NVIDIA H200

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## 📌 Bài toán

Tối ưu hóa hiệu năng serving cho các mô hình ngôn ngữ lớn (LLM) trên kiến trúc NVIDIA H200, tập trung cải thiện các chỉ số:

- **TTFT** (Time to First Token) - Thời gian đến token đầu tiên
- **TPOT** (Time per Output Token) - Thời gian mỗi token đầu ra
- **Throughput** - Số request xử lý được mỗi giây

---

## 🧠 Giải pháp

### Kiến trúc hệ thống
├── bench.py # CLI với 50 lệnh (DSL cho non-technical users)
├── benchmark_with_nodes.py # Benchmark trên 4 loại node
├── property_test.py # Property test 100k states
├── test_suite.py # Test suite cơ bản
├── test_super_suite.py # Super suite 17 tests
├── generate_report.py # Sinh báo cáo từ benchmark
├── run.sh # Script chạy tự động toàn bộ pipeline
├── requirements.txt # Dependencies
├── HUONG_DAN_CLI.md # Hướng dẫn sử dụng CLI (cho người không biết lập trình)
├── BAO_CAO_BAO_VE.md # Báo cáo bảo vệ
└── benchmark_results/ # Kết quả benchmark


---

## 🚀 Cài đặt và chạy

### 1. Clone repo

```bash
git clone https://github.com/ngoainguqingsong-spec/viettelrace2026spongeos.git
cd viettelrace2026spongeos


./run.sh



# Xem tất cả lệnh
./bench.py help

# Chạy benchmark nhanh trên H200
./bench.py run-fast

# Chạy tất cả node types
./bench.py run-all

# Xem kết quả tốt nhất
./bench.py show-best

# Xuất báo cáo
./bench.py export-md


📚 Tài liệu
Hướng dẫn CLI: HUONG_DAN_CLI.md - dành cho người không biết lập trình

Báo cáo bảo vệ: BAO_CAO_BAO_VE.md

Câu hỏi bảo vệ: QA_CHUAN_BI_BAO_VE.md

👥 Tác giả
Nhà khoa học Lê Thanh Tùng - Thiết kế giải pháp và phát triển hệ thống

Đồng chí Sponge - Hỗ trợ kỹ thuật và tối ưu hóa

📄 Giấy phép
MIT License - Xem file LICENSE để biết thêm chi tiết.

⭐ Star repo nếu thấy hữu ích!
