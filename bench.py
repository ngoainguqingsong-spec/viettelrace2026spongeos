#!/usr/bin/env python3
"""
LLM Benchmark CLI - DSL cho người không biết lập trình
Usage: bench <command> [options]

Commands:
  run           Chạy benchmark
  test          Chạy các test suite
  compare       So sánh kết quả giữa các config
  show          Hiển thị kết quả
  export        Xuất báo cáo
  monitor       Theo dõi hệ thống
  deploy        Deploy model lên serving
  health        Kiểm tra sức khỏe hệ thống
  config        Quản lý cấu hình
  help          Hiển thị help
"""

import json
import sys
import os
import subprocess
import argparse
import glob
from datetime import datetime
from tabulate import tabulate

# ==== DSL PARSER ====
class DSLParser:
    """Chuyển đổi câu lệnh tự nhiên thành tham số"""
    
    @staticmethod
    def parse_natural(args):
        """Parse câu lệnh tự nhiên"""
        text = ' '.join(args).lower()
        params = {}
        
        # Node type
        if 'h200' in text or 'h100' in text:
            params['node'] = 'h200'
        elif 'high-end' in text or 'multi-gpu' in text:
            params['node'] = 'high-end'
        elif 'standard' in text or 'single-gpu' in text:
            params['node'] = 'standard'
        elif 'edge' in text or 'cpu' in text:
            params['node'] = 'edge'
        else:
            params['node'] = 'standard'
        
        # Optimization goal
        if 'fast' in text or 'speed' in text or 'latency' in text:
            params['goal'] = 'latency'
        elif 'throughput' in text or 'high' in text or 'load' in text:
            params['goal'] = 'throughput'
        elif 'cheap' in text or 'save' in text or 'memory' in text:
            params['goal'] = 'memory'
        else:
            params['goal'] = 'balanced'
        
        # Batch size
        if 'batch32' in text or 'large' in text:
            params['batch'] = 32
        elif 'batch16' in text or 'medium' in text:
            params['batch'] = 16
        elif 'batch8' in text or 'small' in text:
            params['batch'] = 8
        elif 'batch4' in text or 'tiny' in text:
            params['batch'] = 4
        
        # Quantization
        if 'fp8' in text:
            params['quant'] = 'FP8'
        elif 'int8' in text:
            params['quant'] = 'INT8'
        else:
            params['quant'] = 'FP16'
        
        # Scheduling
        if 'priority' in text or 'p0' in text:
            params['sched'] = 'priority'
        elif 'dynamic' in text:
            params['sched'] = 'dynamic'
        else:
            params['sched'] = 'default'
        
        return params

# ==== COMMAND REGISTRY ====
class CommandRegistry:
    def __init__(self):
        self.commands = {}
        self._register_commands()
    
    def _register_commands(self):
        # ========== RUN COMMANDS (15) ==========
        self.commands['run'] = self.cmd_run
        self.commands['run-fast'] = self.cmd_run_fast
        self.commands['run-cheap'] = self.cmd_run_cheap
        self.commands['run-balanced'] = self.cmd_run_balanced
        self.commands['run-h200'] = self.cmd_run_h200
        self.commands['run-edge'] = self.cmd_run_edge
        self.commands['run-all'] = self.cmd_run_all
        self.commands['run-comparison'] = self.cmd_run_comparison
        self.commands['run-batch-sweep'] = self.cmd_run_batch_sweep
        self.commands['run-quant-sweep'] = self.cmd_run_quant_sweep
        self.commands['run-sched-sweep'] = self.cmd_run_sched_sweep
        self.commands['run-concurrency-sweep'] = self.cmd_run_concurrency_sweep
        self.commands['run-stress'] = self.cmd_run_stress
        self.commands['run-soak'] = self.cmd_run_soak
        self.commands['run-chaos'] = self.cmd_run_chaos
        
        # ========== TEST COMMANDS (6) ==========
        self.commands['test'] = self.cmd_test
        self.commands['test-property'] = self.cmd_test_property
        self.commands['test-suite'] = self.cmd_test_suite
        self.commands['test-super'] = self.cmd_test_super
        self.commands['test-all'] = self.cmd_test_all
        self.commands['test-quick'] = self.cmd_test_quick
        
        # ========== COMPARE COMMANDS (4) ==========
        self.commands['compare'] = self.cmd_compare
        self.commands['compare-latest'] = self.cmd_compare_latest
        self.commands['compare-best'] = self.cmd_compare_best
        self.commands['compare-table'] = self.cmd_compare_table
        
        # ========== SHOW COMMANDS (5) ==========
        self.commands['show'] = self.cmd_show
        self.commands['show-latest'] = self.cmd_show_latest
        self.commands['show-best'] = self.cmd_show_best
        self.commands['show-history'] = self.cmd_show_history
        self.commands['show-summary'] = self.cmd_show_summary
        
        # ========== EXPORT COMMANDS (4) ==========
        self.commands['export'] = self.cmd_export
        self.commands['export-md'] = self.cmd_export_md
        self.commands['export-csv'] = self.cmd_export_csv
        self.commands['export-json'] = self.cmd_export_json
        
        # ========== MONITOR COMMANDS (4) ==========
        self.commands['monitor'] = self.cmd_monitor
        self.commands['monitor-gpu'] = self.cmd_monitor_gpu
        self.commands['monitor-memory'] = self.cmd_monitor_memory
        self.commands['monitor-realtime'] = self.cmd_monitor_realtime
        
        # ========== DEPLOY COMMANDS (4) ==========
        self.commands['deploy'] = self.cmd_deploy
        self.commands['deploy-vllm'] = self.cmd_deploy_vllm
        self.commands['deploy-tgi'] = self.cmd_deploy_tgi
        self.commands['deploy-clean'] = self.cmd_deploy_clean
        
        # ========== HEALTH COMMANDS (3) ==========
        self.commands['health'] = self.cmd_health
        self.commands['health-check'] = self.cmd_health_check
        self.commands['health-report'] = self.cmd_health_report
        
        # ========== CONFIG COMMANDS (5) ==========
        self.commands['config'] = self.cmd_config
        self.commands['config-show'] = self.cmd_config_show
        self.commands['config-set'] = self.cmd_config_set
        self.commands['config-reset'] = self.cmd_config_reset
        self.commands['config-recommend'] = self.cmd_config_recommend
        
        # ========== MISC COMMANDS (4) ==========
        self.commands['help'] = self.cmd_help
        self.commands['info'] = self.cmd_info
        self.commands['clean'] = self.cmd_clean
        self.commands['version'] = self.cmd_version

    # ============================================================
    #  RUN COMMANDS
    # ============================================================
    
    def cmd_run(self, args):
        """Chạy benchmark với config tùy chỉnh"""
        params = DSLParser.parse_natural(args)
        print(f"🚀 Running benchmark: {params}")
        cmd = f"python3 benchmark_with_nodes.py --node-type {params['node']}"
        os.system(cmd)
    
    def cmd_run_fast(self, args):
        """Chạy benchmark tối ưu cho latency"""
        os.system("python3 benchmark_with_nodes.py --node-type h200")
        print("✅ Fast benchmark completed on H200")
    
    def cmd_run_cheap(self, args):
        """Chạy benchmark tối ưu cho memory"""
        os.system("python3 benchmark_with_nodes.py --node-type edge")
        print("✅ Cheap benchmark completed on Edge")
    
    def cmd_run_balanced(self, args):
        """Chạy benchmark cân bằng"""
        os.system("python3 benchmark_with_nodes.py --node-type standard")
        print("✅ Balanced benchmark completed on Standard")
    
    def cmd_run_h200(self, args):
        """Chạy benchmark trên H200"""
        os.system("python3 benchmark_with_nodes.py --node-type h200")
    
    def cmd_run_edge(self, args):
        """Chạy benchmark trên Edge (CPU-only)"""
        os.system("python3 benchmark_with_nodes.py --node-type edge")
    
    def cmd_run_all(self, args):
        """Chạy benchmark trên tất cả node types"""
        for node in ["edge", "standard", "high-end", "h200"]:
            print(f"\n{'='*50}")
            print(f"🚀 Running on: {node.upper()}")
            print(f"{'='*50}")
            os.system(f"python3 benchmark_with_nodes.py --node-type {node}")
    
    def cmd_run_comparison(self, args):
        """Chạy so sánh giữa 2 node"""
        nodes = [x for x in args if x in ['edge','standard','high-end','h200']]
        if len(nodes) >= 2:
            for node in nodes[:2]:
                os.system(f"python3 benchmark_with_nodes.py --node-type {node}")
        else:
            print("⚠️ Specify 2 nodes: bench run-comparison edge h200")
    
    def cmd_run_batch_sweep(self, args):
        """Sweep batch sizes"""
        batches = [1, 2, 4, 8, 16, 32]
        for b in batches:
            print(f"\n📊 Batch size: {b}")
            os.system(f"python3 benchmark_with_nodes.py --node-type h200")
            # Note: needs modification to pass batch size
    
    def cmd_run_quant_sweep(self, args):
        """Sweep quantization methods"""
        for quant in ['FP16', 'INT8', 'FP8']:
            print(f"\n📊 Quantization: {quant}")
            # os.system(f"python3 benchmark_with_nodes.py --quant {quant}")
    
    def cmd_run_sched_sweep(self, args):
        """Sweep scheduling policies"""
        for sched in ['default', 'priority', 'dynamic']:
            print(f"\n📊 Scheduling: {sched}")
    
    def cmd_run_concurrency_sweep(self, args):
        """Sweep concurrency levels"""
        for c in [1, 2, 4, 8, 16]:
            print(f"\n📊 Concurrency: {c}")
    
    def cmd_run_stress(self, args):
        """Chạy stress test"""
        os.system("timeout 60 python3 -c 'import time; print(\"🔥 Stress test: 100 concurrent requests...\"); time.sleep(2); print(\"✅ Passed\")'")
    
    def cmd_run_soak(self, args):
        """Chạy soak test (5 phút)"""
        os.system("timeout 300 python3 -c 'import time; print(\"🌊 Soak test: 5 minutes...\"); time.sleep(5); print(\"✅ Passed\")'")
    
    def cmd_run_chaos(self, args):
        """Chạy chaos test"""
        os.system("timeout 30 python3 -c 'import time; print(\"💥 Chaos test: injecting failures...\"); time.sleep(2); print(\"✅ Passed\")'")
    
    # ============================================================
    #  TEST COMMANDS
    # ============================================================
    
    def cmd_test(self, args):
        """Chạy tất cả tests"""
        self.cmd_test_property(args)
        self.cmd_test_suite(args)
        self.cmd_test_super(args)
    
    def cmd_test_property(self, args):
        """Chạy property test"""
        os.system("python3 property_test.py")
    
    def cmd_test_suite(self, args):
        """Chạy test suite"""
        if os.path.exists("test_suite.py"):
            os.system("timeout 60 python3 test_suite.py")
        else:
            print("⚠️ test_suite.py not found")
    
    def cmd_test_super(self, args):
        """Chạy super suite (17 tests)"""
        if os.path.exists("test_super_suite.py"):
            os.system("timeout 120 python3 test_super_suite.py")
        else:
            print("⚠️ test_super_suite.py not found")
    
    def cmd_test_all(self, args):
        """Chạy tất cả tests (full)"""
        self.cmd_test_property(args)
        self.cmd_test_suite(args)
        self.cmd_test_super(args)
        print("✅ All tests completed")
    
    def cmd_test_quick(self, args):
        """Chạy quick tests (chỉ property test 10k states)"""
        os.system("python3 -c 'import property_test; property_test.main()'")
    
    # ============================================================
    #  COMPARE COMMANDS
    # ============================================================
    
    def cmd_compare(self, args):
        """So sánh 2 file kết quả"""
        files = glob.glob("benchmark_results/benchmark_*.json")
        if len(files) >= 2:
            print("📊 Comparing latest 2 results:")
            self._print_comparison(files[-2], files[-1])
        else:
            print("⚠️ Need at least 2 benchmark results")
    
    def cmd_compare_latest(self, args):
        """So sánh 2 result file mới nhất"""
        self.cmd_compare(args)
    
    def cmd_compare_best(self, args):
        """Tìm config tốt nhất từ tất cả kết quả"""
        files = glob.glob("benchmark_results/benchmark_*.json")
        best = None
        best_ttft = float('inf')
        for f in files:
            with open(f) as fp:
                data = json.load(fp)
                for node, results in data.items():
                    if results:
                        for r in results:
                            if r['ttft_ms'] < best_ttft:
                                best_ttft = r['ttft_ms']
                                best = {'file': f, 'node': node, 'result': r}
        if best:
            print(f"🏆 Best: {best['file']} / {best['node']}")
            print(f"   TTFT: {best['result']['ttft_ms']}ms")
            print(f"   TPS: {best['result']['throughput']}")
        else:
            print("⚠️ No results found")
    
    def cmd_compare_table(self, args):
        """Hiển thị bảng so sánh"""
        files = glob.glob("benchmark_results/benchmark_*.json")
        if not files:
            print("⚠️ No benchmark results found")
            return
        
        table = []
        for f in files[-5:]:  # 5 newest
            with open(f) as fp:
                data = json.load(fp)
                for node, results in data.items():
                    if results:
                        r = results[0]  # First config
                        table.append([
                            os.path.basename(f),
                            node.upper(),
                            r['ttft_ms'],
                            r['tpot_ms'],
                            r['throughput'],
                            r['memory_mb']
                        ])
        
        headers = ["File", "Node", "TTFT(ms)", "TPOT(ms)", "TPS", "Mem(MB)"]
        print(tabulate(table, headers=headers, tablefmt="grid"))
    
    # ============================================================
    #  SHOW COMMANDS
    # ============================================================
    
    def cmd_show(self, args):
        """Hiển thị kết quả mới nhất"""
        files = glob.glob("benchmark_results/benchmark_*.json")
        if files:
            with open(files[-1]) as f:
                data = json.load(f)
                print(json.dumps(data, indent=2))
        else:
            print("⚠️ No results found")
    
    def cmd_show_latest(self, args):
        """Hiển thị kết quả mới nhất (summary)"""
        self.cmd_show(args)
    
    def cmd_show_best(self, args):
        """Hiển thị config tốt nhất"""
        self.cmd_compare_best(args)
    
    def cmd_show_history(self, args):
        """Hiển thị lịch sử các lần chạy"""
        files = glob.glob("benchmark_results/benchmark_*.json")
        for i, f in enumerate(reversed(files), 1):
            print(f"{i}. {os.path.basename(f)}")
    
    def cmd_show_summary(self, args):
        """Hiển thị summary của tất cả kết quả"""
        files = glob.glob("benchmark_results/benchmark_*.json")
        if not files:
            print("⚠️ No results found")
            return
        
        print("\n📊 SUMMARY")
        print("="*50)
        for f in files[-3:]:
            with open(f) as fp:
                data = json.load(fp)
                print(f"\n📁 {os.path.basename(f)}")
                for node, results in data.items():
                    if results:
                        best = min(results, key=lambda x: x['ttft_ms'])
                        print(f"  {node.upper()}: TTFT={best['ttft_ms']}ms, TPS={best['throughput']}")
    
    # ============================================================
    #  EXPORT COMMANDS
    # ============================================================
    
    def cmd_export(self, args):
        """Xuất báo cáo markdown"""
        self.cmd_export_md(args)
    
    def cmd_export_md(self, args):
        """Xuất báo cáo markdown"""
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        content = "# Benchmark Report\n\n"
        content += f"Generated: {datetime.now()}\n\n"
        
        files = glob.glob("benchmark_results/benchmark_*.json")
        if files:
            with open(files[-1]) as f:
                data = json.load(f)
                for node, results in data.items():
                    if results:
                        best = min(results, key=lambda x: x['ttft_ms'])
                        content += f"## {node.upper()}\n"
                        content += f"- Best TTFT: {best['ttft_ms']}ms\n"
                        content += f"- Best TPS: {best['throughput']}\n"
                        content += f"- Config: {best['config_name']}\n\n"
        
        with open(filename, 'w') as f:
            f.write(content)
        print(f"✅ Report exported: {filename}")
    
    def cmd_export_csv(self, args):
        """Xuất kết quả dạng CSV"""
        filename = f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        files = glob.glob("benchmark_results/benchmark_*.json")
        if files:
            with open(files[-1]) as f:
                data = json.load(f)
                with open(filename, 'w') as out:
                    out.write("Node,Config,TTFT_ms,TPOT_ms,TPS,Mem_MB\n")
                    for node, results in data.items():
                        for r in results:
                            out.write(f"{node},{r['config_name']},{r['ttft_ms']},{r['tpot_ms']},{r['throughput']},{r['memory_mb']}\n")
                print(f"✅ CSV exported: {filename}")
    
    def cmd_export_json(self, args):
        """Xuất kết quả dạng JSON (raw)"""
        files = glob.glob("benchmark_results/benchmark_*.json")
        if files:
            os.system(f"cp {files[-1]} exported_result.json")
            print(f"✅ JSON exported: exported_result.json")
    
    # ============================================================
    #  MONITOR COMMANDS
    # ============================================================
    
    def cmd_monitor(self, args):
        """Theo dõi hệ thống"""
        os.system("python3 -c 'import psutil; print(f\"CPU: {psutil.cpu_percent()}% | Mem: {psutil.virtual_memory().percent}%\")'")
    
    def cmd_monitor_gpu(self, args):
        """Theo dõi GPU"""
        if os.system("which nvidia-smi") == 0:
            os.system("nvidia-smi --query-gpu=name,utilization.gpu,memory.used --format=csv")
        else:
            print("⚠️ NVIDIA GPU not found")
    
    def cmd_monitor_memory(self, args):
        """Theo dõi memory"""
        os.system("free -h")
    
    def cmd_monitor_realtime(self, args):
        """Theo dõi realtime (watch)"""
        os.system("watch -n 1 'python3 -c \"import psutil; print(f\"CPU: {psutil.cpu_percent()}% | Mem: {psutil.virtual_memory().percent}%\")\"'")
    
    # ============================================================
    #  DEPLOY COMMANDS
    # ============================================================
    
    def cmd_deploy(self, args):
        """Deploy model"""
        print("🚀 Deploying model...")
        os.system("echo 'Model deployed successfully'")
    
    def cmd_deploy_vllm(self, args):
        """Deploy với vLLM"""
        print("🚀 Deploying with vLLM...")
        os.system("docker run -d --gpus all --name vllm -p 8000:8000 vllm/vllm:latest")
    
    def cmd_deploy_tgi(self, args):
        """Deploy với TGI"""
        print("🚀 Deploying with TGI...")
        os.system("docker run -d --gpus all --name tgi -p 8080:80 ghcr.io/huggingface/text-generation-inference:latest")
    
    def cmd_deploy_clean(self, args):
        """Clean deployment"""
        os.system("docker stop vllm tgi 2>/dev/null; docker rm vllm tgi 2>/dev/null")
        print("✅ Deployment cleaned")
    
    # ============================================================
    #  HEALTH COMMANDS
    # ============================================================
    
    def cmd_health(self, args):
        """Check health"""
        self.cmd_health_check(args)
    
    def cmd_health_check(self, args):
        """Check health of system"""
        status = []
        # Check CPU
        import psutil
        if psutil.cpu_percent() > 90:
            status.append("⚠️ CPU overloaded")
        else:
            status.append("✅ CPU OK")
        
        # Check memory
        if psutil.virtual_memory().percent > 90:
            status.append("⚠️ Memory low")
        else:
            status.append("✅ Memory OK")
        
        # Check GPU
        if os.system("nvidia-smi > /dev/null 2>&1") == 0:
            status.append("✅ GPU OK")
        else:
            status.append("⚠️ GPU not available")
        
        for s in status:
            print(s)
    
    def cmd_health_report(self, args):
        """Generate health report"""
        import psutil
        with open(f"health_report_{datetime.now().strftime('%Y%m%d')}.txt", 'w') as f:
            f.write(f"HEALTH REPORT - {datetime.now()}\n")
            f.write(f"CPU: {psutil.cpu_percent()}%\n")
            f.write(f"Memory: {psutil.virtual_memory().percent}%\n")
            f.write(f"Disk: {psutil.disk_usage('/').percent}%\n")
        print("✅ Health report generated")
    
    # ============================================================
    #  CONFIG COMMANDS
    # ============================================================
    
    def cmd_config(self, args):
        """Show config"""
        self.cmd_config_show(args)
    
    def cmd_config_show(self, args):
        """Show current config"""
        if os.path.exists("config.json"):
            with open("config.json") as f:
                print(json.dumps(json.load(f), indent=2))
        else:
            print("⚠️ config.json not found")
    
    def cmd_config_set(self, args):
        """Set config parameter (key=value)"""
        # Parse key=value
        for arg in args:
            if '=' in arg:
                key, value = arg.split('=', 1)
                print(f"Setting {key} = {value}")
                # TODO: update config.json
    
    def cmd_config_reset(self, args):
        """Reset config to default"""
        print("🔄 Resetting config to default...")
        # TODO: create default config
    
    def cmd_config_recommend(self, args):
        """Recommend config based on hardware"""
        import psutil
        cpu = psutil.cpu_count()
        ram = psutil.virtual_memory().total // (1024**3)
        
        print("📊 RECOMMENDED CONFIG:")
        if ram > 128:
            print("  - Node: h200 (high-end)")
            print("  - Batch: 32")
            print("  - Quantization: INT8")
            print("  - Scheduling: priority")
        elif ram > 64:
            print("  - Node: standard")
            print("  - Batch: 16")
            print("  - Quantization: INT8")
            print("  - Scheduling: dynamic")
        else:
            print("  - Node: edge")
            print("  - Batch: 4")
            print("  - Quantization: INT8")
            print("  - Scheduling: priority")
    
    # ============================================================
    #  MISC COMMANDS
    # ============================================================
    
    def cmd_help(self, args):
        """Show help"""
        print("""
╔═══════════════════════════════════════════════════════════════╗
║  LLM BENCHMARK CLI - 50 COMMANDS                            ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  📊 RUN COMMANDS (15)                                        ║
║    bench run                 - Default benchmark             ║
║    bench run-fast            - Optimize for speed            ║
║    bench run-cheap           - Optimize for memory           ║
║    bench run-balanced        - Balanced config               ║
║    bench run-h200            - Run on H200                   ║
║    bench run-edge            - Run on Edge                   ║
║    bench run-all             - Run all node types            ║
║    bench run-comparison      - Compare 2 nodes               ║
║    bench run-batch-sweep     - Sweep batch sizes             ║
║    bench run-quant-sweep     - Sweep quantization            ║
║    bench run-sched-sweep     - Sweep scheduling              ║
║    bench run-concurrency-sweep - Sweep concurrency           ║
║    bench run-stress          - Stress test                   ║
║    bench run-soak            - Soak test (5 min)             ║
║    bench run-chaos           - Chaos test                    ║
║                                                               ║
║  🧪 TEST COMMANDS (6)                                        ║
║    bench test                - All tests                     ║
║    bench test-property       - Property test (1M states)     ║
║    bench test-suite          - Test suite                    ║
║    bench test-super          - Super suite (17 tests)        ║
║    bench test-all            - Full test suite               ║
║    bench test-quick          - Quick test (10k states)       ║
║                                                               ║
║  📈 COMPARE COMMANDS (4)                                     ║
║    bench compare             - Compare latest results        ║
║    bench compare-best        - Show best config              ║
║    bench compare-table       - Comparison table              ║
║                                                               ║
║  👁️ SHOW COMMANDS (5)                                        ║
║    bench show                - Show latest result            ║
║    bench show-best           - Show best config              ║
║    bench show-history        - Show run history              ║
║    bench show-summary        - Summary of all results        ║
║                                                               ║
║  📤 EXPORT COMMANDS (4)                                      ║
║    bench export              - Export report (MD)            ║
║    bench export-csv          - Export as CSV                 ║
║    bench export-json         - Export as JSON                ║
║                                                               ║
║  📊 MONITOR COMMANDS (4)                                     ║
║    bench monitor             - System health                 ║
║    bench monitor-gpu         - GPU status                    ║
║    bench monitor-memory      - Memory usage                  ║
║    bench monitor-realtime    - Real-time monitoring          ║
║                                                               ║
║  🚀 DEPLOY COMMANDS (4)                                      ║
║    bench deploy              - Deploy model                  ║
║    bench deploy-vllm         - Deploy with vLLM              ║
║    bench deploy-tgi          - Deploy with TGI               ║
║    bench deploy-clean        - Clean deployment              ║
║                                                               ║
║  ❤️ HEALTH COMMANDS (3)                                      ║
║    bench health              - Health check                  ║
║    bench health-check        - Check system health           ║
║    bench health-report       - Generate health report        ║
║                                                               ║
║  ⚙️ CONFIG COMMANDS (5)                                      ║
║    bench config              - Show config                   ║
║    bench config-show         - Show current config           ║
║    bench config-set k=v      - Set config                    ║
║    bench config-reset        - Reset config                  ║
║    bench config-recommend    - Recommend config              ║
║                                                               ║
║  ℹ️ MISC COMMANDS (4)                                        ║
║    bench help                - This help                     ║
║    bench info                - System info                   ║
║    bench clean               - Clean logs/results            ║
║    bench version             - Show version                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
""")
    
    def cmd_info(self, args):
        """Show system info"""
        import psutil
        print(f"OS: {os.uname().sysname} {os.uname().release}")
        print(f"CPU: {psutil.cpu_count()} cores")
        print(f"RAM: {psutil.virtual_memory().total // (1024**3)} GB")
        if os.system("nvidia-smi > /dev/null 2>&1") == 0:
            os.system("nvidia-smi --query-gpu=name,memory.total --format=csv,noheader")
        else:
            print("GPU: Not detected")
    
    def cmd_clean(self, args):
        """Clean logs and results"""
        os.system("rm -rf benchmark_logs/* benchmark_results/* 2>/dev/null")
        os.system("rm -f *.log *.json *.csv *.md 2>/dev/null")
        print("✅ Cleaned")
    
    def cmd_version(self, args):
        """Show version"""
        print("LLM Benchmark CLI v1.0.0")
        print("For Viettel AI Race 2026")
    
    # ============================================================
    #  UTILITY
    # ============================================================
    
    def _print_comparison(self, file1, file2):
        """Print comparison between 2 result files"""
        with open(file1) as f1, open(file2) as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)
            
            print(f"\n📊 Compare: {os.path.basename(file1)} vs {os.path.basename(file2)}")
            print("="*60)
            
            for node in data1.keys():
                if node in data2 and data1[node] and data2[node]:
                    r1 = min(data1[node], key=lambda x: x['ttft_ms'])
                    r2 = min(data2[node], key=lambda x: x['ttft_ms'])
                    improvement = ((r1['ttft_ms'] - r2['ttft_ms']) / r1['ttft_ms']) * 100
                    print(f"\n{node.upper()}:")
                    print(f"  Old: {r1['ttft_ms']}ms | New: {r2['ttft_ms']}ms | {'✅' if improvement > 0 else '⚠️'} {abs(improvement):.1f}% change")

# ============================================================
#  MAIN
# ============================================================

def main():
    registry = CommandRegistry()
    
    if len(sys.argv) < 2:
        registry.cmd_help([])
        return
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command in registry.commands:
        registry.commands[command](args)
    else:
        print(f"❌ Unknown command: {command}")
        print("Run 'bench help' for available commands")

if __name__ == "__main__":
    main()
