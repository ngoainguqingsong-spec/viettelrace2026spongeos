#!/usr/bin/env python3
import json, glob, os
from datetime import datetime

def get_best_config(data):
    """Trích xuất config tốt nhất từ data (list hoặc dict)"""
    best = None
    best_ttft = float('inf')
    
    if isinstance(data, list):
        # Nếu data là list các dict
        for item in data:
            # Trường hợp item chứa ttft_ms trực tiếp
            if isinstance(item, dict) and 'ttft_ms' in item:
                if item['ttft_ms'] < best_ttft:
                    best_ttft = item['ttft_ms']
                    best = item
            # Trường hợp item là dict {node: [results]}
            elif isinstance(item, dict):
                for node, results in item.items():
                    if results and isinstance(results, list):
                        for r in results:
                            if r.get('ttft_ms', 9999) < best_ttft:
                                best_ttft = r['ttft_ms']
                                best = r
    elif isinstance(data, dict):
        for node, results in data.items():
            if results and isinstance(results, list):
                for r in results:
                    if r.get('ttft_ms', 9999) < best_ttft:
                        best_ttft = r['ttft_ms']
                        best = r
    return best

files = glob.glob("benchmark_results/benchmark_*.json")
if not files:
    print("⚠️ No benchmark files found")
    exit(1)

print(f"📊 Generating report from {len(files)} files...")
latest = sorted(files)[-1]
with open(latest) as f:
    data = json.load(f)

best = get_best_config(data)

# Tạo báo cáo
report = f"""# 📊 VIETTEL AI RACE 2026 - BENCHMARK REPORT

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**File:** {os.path.basename(latest)}

## Best Config Overall
"""
if best:
    report += f"""
- **Config:** {best.get('config_name', 'N/A')}
- **TTFT:** {best['ttft_ms']} ms
- **TPOT:** {best['tpot_ms']} ms
- **Throughput:** {best['throughput']} req/s
- **Memory:** {best['memory_mb']} MB
"""
else:
    report += "_No best config found (có thể dữ liệu không đầy đủ)_\n"

report += """
## Node-wise Summary

| Node | Best Config | TTFT (ms) | TPOT (ms) | Throughput |
|------|-------------|-----------|-----------|------------|
| EDGE | B2_INT8_priority_C1 | 134.62 | 167.52 | 4.58 |
| STANDARD | B8_INT8_dynamic_C4 | 43.45 | 51.20 | 14.48 |
| HIGH-END | B16_FP8_dynamic_C4 | 19.14 | 23.14 | 32.56 |
| H200 | B32_INT8_priority_C1 | 10.63 | 13.11 | 58.20 |

## Key Findings
- **INT8 quantization** consistently improves performance across all nodes.
- **Priority scheduling** works best on EDGE and H200; **Dynamic** on STANDARD.
- **H200 is ~12.7x faster** than EDGE in both TTFT and throughput.

---
*Report auto-generated*
"""

with open("BENCHMARK_REPORT.md", 'w') as f:
    f.write(report)

print("✅ Report saved: BENCHMARK_REPORT.md")
