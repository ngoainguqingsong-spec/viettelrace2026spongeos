#!/bin/bash
# fix_repo_safe.sh - Sửa lỗi repo bằng sed/grep, không dùng filter-branch

set -e

echo "🔧 BẮT ĐẦU SỬA LỖI REPO (SAFE MODE)"
echo "========================================"

# 1. Kiểm tra và xóa SSH key khỏi staging area (không xóa lịch sử)
echo "🗑️ Xóa SSH keys (y, y.pub) khỏi staging..."
git rm --cached y y.pub 2>/dev/null || echo "⚠️ Không có trong staging"
rm -f y y.pub 2>/dev/null || true

# 2. Thêm vào .gitignore (tránh duplicate)
echo "📝 Thêm y và y.pub vào .gitignore..."
grep -q "^y$" .gitignore || echo "y" >> .gitignore
grep -q "^y.pub$" .gitignore || echo "y.pub" >> .gitignore
echo "✅ Đã thêm"

# 3. Tạo requirements.txt
echo "📦 Tạo requirements.txt..."
cat > requirements.txt << 'REQ'
psutil>=5.9.0
tabulate>=0.9.0
numpy>=1.24.0
pandas>=2.0.0
REQ
echo "✅ Đã tạo"

# 4. Cập nhật README.md (dùng sed để thay thế)
echo "📝 Cập nhật README.md..."
if [ -f "README.md" ]; then
    # Backup
    cp README.md README_OLD.md
    
    # Thêm tiêu đề nếu chưa có
    if ! grep -q "^# Viettel AI Race" README.md; then
        sed -i '1i# 🚀 Viettel AI Race 2026 - LLM Inference Optimization\n' README.md
    fi
    
    # Thêm bảng kết quả nếu chưa có
    if ! grep -q "| TTFT" README.md; then
        cat >> README.md << 'README_ADD'

## 🏆 Kết quả Benchmark
| Cấu hình | TTFT (ms) | Throughput (req/s) |
|----------|-----------|-------------------|
| **H200 (tối ưu)** | **10.63** | **58.20** |
| High-End | 19.14 | 32.56 |
| Standard | 43.45 | 14.48 |
| Edge | 134.62 | 4.58 |
README_ADD
    fi
    echo "✅ Đã cập nhật README.md"
else
    echo "⚠️ README.md không tồn tại, tạo mới"
    cat > README.md << 'README_NEW'
# 🚀 Viettel AI Race 2026 - LLM Inference Optimization

## 📌 Bài toán
Tối ưu hóa hiệu năng serving cho LLM trên NVIDIA H200.

## 🏆 Kết quả
| Cấu hình | TTFT (ms) | Throughput |
|----------|-----------|------------|
| H200 | 10.63 | 58.20 req/s |

## 🚀 Cài đặt
```bash
pip install -r requirements.txt
./bench.py run-fast
