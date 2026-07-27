#!/bin/bash
# run.sh - Chạy toàn bộ pipeline tự động

set -e

echo "🚀 VIETTEL AI RACE 2026 - PIPELINE"
echo "========================================"

# 1. Cài đặt dependencies
echo "📦 Cài đặt dependencies..."
pip install -r requirements.txt -q

# 2. Chạy property test
echo "🧪 Chạy property test (100k states)..."
python3 property_test.py

# 3. Chạy benchmark
echo "📊 Chạy benchmark trên H200..."
python3 bench.py run-fast

# 4. Tạo báo cáo
echo "📄 Tạo báo cáo..."
python3 generate_report.py

echo "✅ HOÀN TẤT!"
echo "📁 Kết quả: benchmark_results/"
echo "📄 Báo cáo: BENCHMARK_REPORT.md"
