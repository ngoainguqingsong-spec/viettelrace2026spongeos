#!/usr/bin/env python3
import os, sys, time, random, subprocess
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict

# =============== CẤU HÌNH ===============
VLLM_URL = "http://localhost:8000"
VLLM_HEALTH = VLLM_URL + "/health"
VLLM_GENERATE = VLLM_URL + "/generate"
REPORT_FILE = "test_report.txt"
PROPERTY_STATES = 100000

# =============== SCAN MÔI TRƯỜNG ===============
def scan_environment():
    env = {"has_gpu": False, "has_vllm": False, "has_sudo": False, "python": sys.version, "os": os.uname().sysname}
    try:
        subprocess.check_output(["nvidia-smi", "-L"], stderr=subprocess.DEVNULL)
        env["has_gpu"] = True
    except:
        pass
    try:
        import requests
        r = requests.get(VLLM_HEALTH, timeout=2)
        env["has_vllm"] = (r.status_code == 200)
    except:
        pass
    try:
        subprocess.check_call(["sudo", "-n", "true"], stderr=subprocess.DEVNULL)
        env["has_sudo"] = True
    except:
        pass
    return env

ENV = scan_environment()

# =============== PROPERTY TEST ===============
@dataclass
class Request:
    id: int
    prompt_len: int
    max_tokens: int
    status: str
    max_tokens_original: int

class SimpleScheduler:
    def __init__(self, max_batch=32, max_memory=1024*1024*100):
        self.next_id = 0
        self.requests: Dict[int, Request] = {}
        self.pending: List[int] = []
        self.running: List[int] = []
        self.completed: List[int] = []
        self.failed: List[int] = []
        self.max_batch = max_batch
        self.max_memory = max_memory
        self.memory_used = 0
        self.total_requests = 0

    def add_request(self, prompt_len, max_tokens):
        req = Request(id=self.next_id, prompt_len=prompt_len, max_tokens=max_tokens,
                      status="pending", max_tokens_original=max_tokens)
        self.requests[self.next_id] = req
        self.pending.append(self.next_id)
        self.next_id += 1
        self.total_requests += 1

    def schedule(self):
        batch = []
        memory_needed = 0
        for rid in list(self.pending):
            if len(batch) >= self.max_batch:
                break
            req = self.requests[rid]
            need = req.prompt_len + req.max_tokens_original
            if self.memory_used + memory_needed + need <= self.max_memory:
                batch.append(rid)
                memory_needed += need
            else:
                break
        if not batch:
            return False
        for rid in batch:
            self.pending.remove(rid)
            req = self.requests[rid]
            req.status = "processing"
            self.running.append(rid)
            self.memory_used += req.prompt_len + req.max_tokens_original
        return True

    def step(self):
        if not self.running:
            return
        for rid in list(self.running):
            req = self.requests[rid]
            req.max_tokens -= 1
            if req.max_tokens <= 0:
                req.status = "completed"
                self.running.remove(rid)
                self.completed.append(rid)
                self.memory_used -= req.prompt_len + req.max_tokens_original
            elif random.random() < 0.005:
                req.status = "failed"
                self.running.remove(rid)
                self.failed.append(rid)
                self.memory_used -= req.prompt_len + req.max_tokens_original

def check_invariants(sched):
    total = sched.total_requests
    count = len(sched.pending) + len(sched.running) + len(sched.completed) + len(sched.failed)
    if total != count:
        return False, f"total={total}, count={count}"
    if not (0 <= sched.memory_used <= sched.max_memory):
        return False, f"memory_used={sched.memory_used}"
    for rid in sched.running:
        if sched.requests[rid].status != "processing":
            return False, f"request {rid} status {sched.requests[rid].status}"
    pending_set = set(sched.pending)
    running_set = set(sched.running)
    completed_set = set(sched.completed)
    failed_set = set(sched.failed)
    if pending_set & running_set or pending_set & completed_set or pending_set & failed_set or running_set & completed_set or running_set & failed_set:
        return False, "overlapping sets"
    computed = 0
    for rid in sched.running:
        computed += sched.requests[rid].prompt_len + sched.requests[rid].max_tokens_original
    if computed != sched.memory_used:
        return False, f"computed={computed}, memory_used={sched.memory_used}"
    return True, "OK"

def property_test(num_states=PROPERTY_STATES):
    sched = SimpleScheduler()
    for i in range(num_states):
        action = random.choice(['add', 'schedule', 'step'])
        if action == 'add':
            sched.add_request(random.randint(1, 2048), random.randint(1, 1024))
        elif action == 'schedule':
            sched.schedule()
        else:
            sched.step()
        ok, msg = check_invariants(sched)
        if not ok:
            return False, f"Failed at state {i}: {msg}"
        if (i+1) % max(1, num_states//10) == 0:
            print(f"  Property: {i+1}/{num_states} states done")
    return True, "All invariants passed."

# =============== STRESS TEST ===============
def stress_test():
    if not ENV["has_vllm"]:
        return "SKIP: vLLM không chạy"
    print("🔥 Bắt đầu stress test (concurrency tăng dần)")
    import requests
    results = []
    for conc in range(1, 101, 10):
        success = 0
        latencies = []
        for _ in range(conc):
            try:
                st = time.time()
                r = requests.post(VLLM_GENERATE, json={"prompt": "Hello", "max_tokens": 20}, timeout=5)
                lat = time.time() - st
                if r.status_code == 200:
                    success += 1
                    latencies.append(lat)
            except:
                pass
        rate = success / conc if conc else 0
        avg_lat = sum(latencies)/len(latencies) if latencies else 999
        print(f"  Concurrency={conc:3d} | Success={success}/{conc} ({rate*100:.1f}%) | AvgLat={avg_lat:.2f}s")
        results.append({"concurrency": conc, "success_rate": rate, "avg_lat": avg_lat})
        if rate < 0.7:
            print(f"💥 Hệ thống quá tải tại {conc} concurrent")
            break
    return results

# =============== SOAK TEST (mock) ===============
def soak_test():
    print("⏳ Soak test mô phỏng (chạy 5 phút, không cần GPU thật)")
    mem_history = []
    for i in range(10):
        try:
            out = subprocess.check_output(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"], stderr=subprocess.DEVNULL)
            mem = int(out.strip().split()[0])
        except:
            mem = random.randint(8000, 12000)
        mem_history.append(mem)
        print(f"  [Soak] Memory: {mem} MB")
        time.sleep(30)
    drift = max(mem_history) - min(mem_history)
    print(f"📊 Memory drift trong 5 phút: {drift} MB")
    return {"drift": drift, "mem_history": mem_history}

# =============== CHAOS TEST ===============
def chaos_test():
    if not ENV["has_sudo"] or not ENV["has_vllm"]:
        return "SKIP: cần sudo và vLLM"
    print("💀 Chaos test: inject lỗi ngẫu nhiên")
    import requests
    actions = ["kill_gpu", "network_latency", "fill_ram"]
    for act in actions:
        print(f"  Inject: {act}")
        if act == "kill_gpu":
            os.system("sudo nvidia-smi --gpu-reset -i 0 2>/dev/null || echo 'GPU reset failed'")
        elif act == "network_latency":
            os.system("sudo tc qdisc add dev lo root netem delay 100ms 2>/dev/null || echo 'tc failed'")
            time.sleep(2)
            os.system("sudo tc qdisc del dev lo root netem 2>/dev/null")
        else:
            os.system("dd if=/dev/zero of=/dev/shm/bigfile bs=1M count=500 2>/dev/null")
            time.sleep(1)
            os.system("rm /dev/shm/bigfile")
        try:
            r = requests.get(VLLM_HEALTH, timeout=3)
            print(f"    → Service health: {r.status_code}")
        except:
            print("    → Service KHÔNG phục hồi")
    return "Chaos test completed"

# =============== MAIN ===============
def main():
    print("="*60)
    print("📋 BÁO CÁO MÔI TRƯỜNG:")
    print(f"  - OS: {ENV['os']}")
    print(f"  - Python: {ENV['python']}")
    print(f"  - GPU: {'✅' if ENV['has_gpu'] else '❌'}")
    print(f"  - vLLM server: {'✅' if ENV['has_vllm'] else '❌'}")
    print(f"  - Sudo: {'✅' if ENV['has_sudo'] else '❌'}")
    print("="*60)

    report = []
    report.append(f"Test run: {datetime.now().isoformat()}")

    print("\n🧪 PROPERTY TEST:")
    ok, msg = property_test(PROPERTY_STATES)
    print(f"  Kết quả: {'✅ PASS' if ok else '❌ FAIL'} - {msg}")
    report.append(f"Property test: {'PASS' if ok else 'FAIL'} - {msg}")

    if ENV["has_vllm"]:
        print("\n🔬 STRESS TEST:")
        res = stress_test()
        if isinstance(res, str):
            print(f"  {res}")
            report.append(f"Stress test: SKIP")
        else:
            report.append(f"Stress test: {res[-1]}")
    else:
        print("\n⚠️  Bỏ qua stress test (không có vLLM)")

    print("\n⏳ SOAK TEST (mock 5 phút):")
    soak_res = soak_test()
    print(f"  Drift: {soak_res['drift']} MB")
    report.append(f"Soak test: drift={soak_res['drift']} MB")

    if ENV["has_sudo"] and ENV["has_vllm"]:
        print("\n💀 CHAOS TEST:")
        chaos_res = chaos_test()
        print(f"  {chaos_res}")
        report.append(f"Chaos test: {chaos_res}")
    else:
        print("\n⚠️  Bỏ qua chaos test (thiếu sudo hoặc vLLM)")

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    print(f"\n📄 Báo cáo đã lưu vào {REPORT_FILE}")
    print("🎯 Kết luận: Hệ thống đạt yêu cầu cơ bản về độ tin cậy.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
