# 📊 VIETTEL AI RACE 2026 - BENCHMARK REPORT

**Generated:** 2026-07-27 09:42:14
**File:** benchmark_20260727_064643.json

## Best Config Overall
_No best config found (có thể dữ liệu không đầy đủ)_

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
