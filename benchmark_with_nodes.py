#!/usr/bin/env python3
"""
benchmark_with_nodes.py - Chạy benchmark với các kiểu node khác nhau
Usage: python3 benchmark_with_nodes.py --node-type [edge|standard|high-end|h200]
"""

import json
import time
import random
import psutil
import os
import argparse
import sys
from datetime import datetime

def get_node_config(node_type):
    """Cấu hình cho từng loại node"""
    configs = {
        "edge": {
            "name": "Edge (CPU-only, 2 cores, 4GB RAM)",
            "cpu_limit": 2,
            "ram_limit_mb": 4096,
            "gpu": False,
            "batch_sizes": [1, 2],
            "concurrency_levels": [1, 2],
            "quantizations": ["FP16", "INT8"],
            "schedulings": ["default", "priority"]
        },
        "standard": {
            "name": "Standard (Single GPU, 8 cores, 16GB RAM)",
            "cpu_limit": 8,
            "ram_limit_mb": 16384,
            "gpu": True,
            "batch_sizes": [1, 4, 8],
            "concurrency_levels": [1, 4, 8],
            "quantizations": ["FP16", "INT8"],
            "schedulings": ["default", "priority", "dynamic"]
        },
        "high-end": {
            "name": "High-End (Multi-GPU, 32 cores, 64GB RAM)",
            "cpu_limit": 32,
            "ram_limit_mb": 65536,
            "gpu": True,
            "batch_sizes": [1, 4, 8, 16],
            "concurrency_levels": [1, 4, 8, 16],
            "quantizations": ["FP16", "INT8", "FP8"],
            "schedulings": ["default", "priority", "dynamic"]
        },
        "h200": {
            "name": "NVIDIA H200 (141GB HBM3, 168 cores)",
            "cpu_limit": 168,
            "ram_limit_mb": 141000,
            "gpu": True,
            "batch_sizes": [1, 4, 8, 16, 32],
            "concurrency_levels": [1, 4, 8, 16, 32],
            "quantizations": ["FP16", "INT8", "FP8"],
            "schedulings": ["default", "priority", "dynamic"]
        }
    }
    return configs.get(node_type, configs["standard"])

def run_single_benchmark(batch, quant, sched, conc, node_cfg):
    """Chạy một cấu hình cụ thể, mô phỏng theo loại node"""
    base_latency = 0.08 + random.random() * 0.04
    
    # Điều chỉnh theo node
    node_factor = {
        "edge": 3.0,
        "standard": 1.5,
        "high-end": 1.0,
        "h200": 0.7
    }.get(node_cfg.get("node_key", "standard"), 1.0)
    
    # Công thức ước lượng
    batch_factor = 1.0 / (batch ** 0.35)
    quant_factor = {"FP16": 1.0, "INT8": 0.7, "FP8": 0.65}.get(quant, 1.0)
    sched_factor = {"default": 1.0, "priority": 0.85, "dynamic": 0.82}.get(sched, 1.0)
    conc_factor = 1.0 + (conc - 1) * 0.015
    
    ttft = base_latency * node_factor * batch_factor * quant_factor * sched_factor * conc_factor
    tpot = ttft * (1.1 + random.random() * 0.15)
    throughput = 50 / (ttft * 50 + tpot * 25)
    memory = 1024 + batch * 128 + (256 if quant in ["INT8", "FP8"] else 0) + random.randint(0, 200)
    
    return {
        "ttft_ms": round(ttft * 1000, 2),
        "tpot_ms": round(tpot * 1000, 2),
        "throughput": round(throughput, 2),
        "memory_mb": memory,
        "cpu_usage": psutil.cpu_percent(interval=0.1)
    }

def run_benchmark_for_node(node_type):
    print(f"\n{'='*70}")
    print(f"🚀 BENCHMARK ON: {node_type.upper()}")
    node_cfg = get_node_config(node_type)
    node_cfg["node_key"] = node_type
    print(f"📋 Config: {node_cfg['name']}")
    print(f"   CPU Limit: {node_cfg['cpu_limit']}, RAM Limit: {node_cfg['ram_limit_mb']}MB")
    print(f"{'='*70}\n")
    
    results = []
    
    for batch in node_cfg["batch_sizes"]:
        for quant in node_cfg["quantizations"]:
            for sched in node_cfg["schedulings"]:
                for conc in node_cfg["concurrency_levels"][:2]:  # Lấy 2 mức conc đầu để không tràn log
                    config_name = f"B{batch}_{quant}_{sched}_C{conc}"
                    print(f"⏳ Testing: {config_name}...", end=" ", flush=True)
                    
                    result = run_single_benchmark(batch, quant, sched, conc, node_cfg)
                    result["config"] = {
                        "batch_size": batch,
                        "quantization": quant,
                        "scheduling": sched,
                        "concurrency": conc
                    }
                    result["config_name"] = config_name
                    results.append(result)
                    
                    print(f"TTFT={result['ttft_ms']}ms, TPOT={result['tpot_ms']}ms, TPS={result['throughput']}")
    
    return results

def main():
    parser = argparse.ArgumentParser(description="Benchmark LLM serving with different node types")
    parser.add_argument("--node-type", "-n", 
                        choices=["edge", "standard", "high-end", "h200"],
                        default="standard",
                        help="Loại node muốn benchmark")
    parser.add_argument("--output", "-o", default="benchmark_results.json",
                        help="File output JSON")
    parser.add_argument("--all", action="store_true",
                        help="Chạy tất cả các loại node")
    
    args = parser.parse_args()
    
    all_results = {}
    
    if args.all:
        node_list = ["edge", "standard", "high-end", "h200"]
        for node in node_list:
            all_results[node] = run_benchmark_for_node(node)
    else:
        all_results[args.node_type] = run_benchmark_for_node(args.node_type)
    
    # Lưu JSON
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Kết quả lưu tại: {args.output}")
    
    # In bảng tổng hợp best config cho từng node
    print("\n" + "="*70)
    print("🏆 BEST CONFIG PER NODE")
    print("="*70)
    for node, results in all_results.items():
        if not results:
            continue
        best = min(results, key=lambda x: x["ttft_ms"])
        print(f"   {node.upper()}: {best['config_name']} -> TTFT={best['ttft_ms']}ms, TPS={best['throughput']}")

if __name__ == "__main__":
    main()
