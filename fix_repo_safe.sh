#!/bin/bash
# fix_repo_safe.sh - Sửa lỗi repo cho người không chuyên

set -e

echo "🔧 BẮT ĐẦU SỬA LỖI REPO"
echo "========================================"

# 1. Xóa SSH keys khỏi staging và thư mục
echo "🗑️ Xóa SSH keys (y, y.pub)..."
git rm --cached y y.pub 2>/dev/null || echo "⚠️ Không tìm thấy trong staging"
rm -f y y.pub 2>/dev/null || true
echo "✅ Đã xóa"

# 2. Thêm vào .gitignore nếu chưa có
echo "📝 Cập nhật .gitignore..."
grep -q "^y$" .gitignore || echo "y" >> .gitignore
grep -q "^y.pub$" .gitignore || echo "y.pub" >> .gitignore
echo "✅ Đã cập nhật"

# 3. Tạo requirements.txt
echo "📦 Tạo requirements.txt..."
cat > requirements.txt << 'REQ'
psutil>=5.9.0
tabulate>=0.9.0
numpy>=1.24.0
pandas>=2.0.0
REQ
echo "✅ Đã tạo"

# 4. Xóa file báo cáo trùng
echo "🗑️ Xóa file báo cáo trùng..."
rm -f BENCHMARK_REPORT.md FINAL_REPORT.md
echo "✅ Đã xóa"

# 5. Cấp quyền cho bench.py
echo "🔑 Cấp quyền cho bench.py..."
chmod +x bench.py
echo "✅ Đã cấp quyền"

# 6. Commit và push
echo "📤 Push lên GitHub..."
git add .
git commit -m "Fix: Xóa SSH keys, thêm requirements.txt, cập nhật .gitignore, xóa báo cáo trùng, cấp quyền bench.py"
git push origin main

echo "✅ HOÀN TẤT!"
