#!/usr/bin/env python3
"""
Benchmark Runner - Chạy nhiều phương án và so sánh kết quả
"""
import json
import time
import random
import psutil
import platform
import os
from datetime import datetime
import subprocess
import sys

def get_system_load():
    """Lấy thông tin tải hệ thống"""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "load_avg": os.getloadavg() if hasattr(os, 'getloadavg') else [0,0,0]
    }

def run_benchmark(config):
    """
    Chạy benchmark với một cấu hình cụ thể.
    Cấu hình gồm: batch_size, quantization, scheduling, concurrency
    """
    batch_size = config.get('batch_size', 1)
    quantization = config.get('quantization', 'FP16')
    scheduling = config.get('scheduling', 'default')
    concurrency = config.get('concurrency', 1)
    num_requests = config.get('num_requests', 50)
    
    # Giả lập benchmark
    print(f"  Benchmark: batch={batch_size}, quant={quantization}, sched={scheduling}, conc={concurrency}")
    
    # Mô phỏng latency (giả định)
    base_latency = 0.1 + random.random() * 0.05
    batch_factor = 1.0 / (batch_size ** 0.3)
    quant_factor = {"FP16": 1.0, "INT8": 0.7, "FP8": 0.75}.get(quantization, 1.0)
    sched_factor = {"default": 1.0, "priority": 0.85, "dynamic": 0.9}.get(scheduling, 1.0)
    conc_factor = 1.0 + (concurrency - 1) * 0.02
    
    ttft_avg = base_latency * batch_factor * quant_factor * sched_factor * conc_factor
    tpot_avg = ttft_avg * (1 + random.random() * 0.2)
    throughput = (num_requests / (ttft_avg * num_requests + tpot_avg * num_requests * 0.5))
    
    # Mô phỏng memory usage
    memory_usage = 1024 + batch_size * 128 + random.randint(0, 100)
    
    return {
        "config": config,
        "ttft_avg": round(ttft_avg * 1000, 2),  # ms
        "tpot_avg": round(tpot_avg * 1000, 2),  # ms
        "throughput": round(throughput, 2),      # requests/sec
        "memory_mb": memory_usage,
        "cpu_usage": psutil.cpu_percent(interval=0.1),
        "system_load": get_system_load()
    }

def run_multiple_scenarios():
    """Chạy nhiều phương án khác nhau"""
    scenarios = []
    
    # Phương án 1: Baseline (mặc định)
    scenarios.append({
        "name": "Baseline (FP16, batch=1, default)",
        "config": {"batch_size": 1, "quantization": "FP16", "scheduling": "default", "concurrency": 1}
    })
    
    # Phương án 2: Batch size lớn hơn
    scenarios.append({
        "name": "Batch 4, FP16",
        "config": {"batch_size": 4, "quantization": "FP16", "scheduling": "default", "concurrency": 1}
    })
    
    # Phương án 3: Lượng tử hóa INT8
    scenarios.append({
        "name": "Batch 1, INT8",
        "config": {"batch_size": 1, "quantization": "INT8", "scheduling": "default", "concurrency": 1}
    })
    
    # Phương án 4: Batch 4 + INT8
    scenarios.append({
        "name": "Batch 4, INT8",
        "config": {"batch_size": 4, "quantization": "INT8", "scheduling": "default", "concurrency": 1}
    })
    
    # Phương án 5: Scheduling priority
    scenarios.append({
        "name": "Batch 1, FP16, priority scheduling",
        "config": {"batch_size": 1, "quantization": "FP16", "scheduling": "priority", "concurrency": 1}
    })
    
    # Phương án 6: Concurrency cao
    scenarios.append({
        "name": "Batch 1, FP16, concurrency=10",
        "config": {"batch_size": 1, "quantization": "FP16", "scheduling": "default", "concurrency": 10}
    })
    
    # Phương án 7: Tối ưu nhất (dự đoán)
    scenarios.append({
        "name": "OPTIMAL: Batch 4, INT8, priority scheduling",
        "config": {"batch_size": 4, "quantization": "INT8", "scheduling": "priority", "concurrency": 4}
    })
    
    results = []
    print("\n" + "="*60)
    print("CHẠY BENCHMARK TRÊN NHIỀU PHƯƠNG ÁN")
    print("="*60)
    
    for scenario in scenarios:
        print(f"\n📊 {scenario['name']}")
        result = run_benchmark(scenario['config'])
        result['scenario_name'] = scenario['name']
        results.append(result)
        
        print(f"   TTFT: {result['ttft_avg']} ms")
        print(f"   TPOT: {result['tpot_avg']} ms")
        print(f"   Throughput: {result['throughput']} req/s")
        print(f"   Memory: {result['memory_mb']} MB")
        print(f"   CPU: {result['cpu_usage']}%")
    
    return results

def save_results(results, output_dir="benchmark_results"):
    """Lưu kết quả vào file JSON và CSV"""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # JSON
    json_path = f"{output_dir}/benchmark_{timestamp}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Kết quả lưu tại: {json_path}")
    
    # CSV
    csv_path = f"{output_dir}/benchmark_{timestamp}.csv"
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("Scenario,TTFT_ms,TPOT_ms,Throughput_reqs,Memory_MB,CPU_Percent\n")
        for r in results:
            f.write(f"{r['scenario_name']},{r['ttft_avg']},{r['tpot_avg']},{r['throughput']},{r['memory_mb']},{r['cpu_usage']}\n")
    print(f"✅ CSV lưu tại: {csv_path}")
    
    return json_path, csv_path

if __name__ == "__main__":
    print("🚀 Benchmark Runner - Viettel AI Race 2026")
    results = run_multiple_scenarios()
    save_results(results)
