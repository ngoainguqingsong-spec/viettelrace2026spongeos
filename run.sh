#!/bin/bash
echo "🔍 Quét môi trường hệ thống..."
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "❌ Không tìm thấy Python. Hãy cài đặt Python 3."
    exit 1
fi
echo "✅ Dùng Python: $($PYTHON --version)"
$PYTHON -c "import requests" 2>/dev/null || {
    echo "⚠️  Thư viện 'requests' chưa có, đang cài pip..."
    $PYTHON -m pip install requests --user --quiet
}
echo "🚀 Chạy test suite..."
$PYTHON test_suite.py
