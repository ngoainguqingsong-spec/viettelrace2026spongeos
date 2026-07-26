#!/usr/bin/env python3
import sys, random
from dataclasses import dataclass
from typing import List, Dict

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

def run_test(num_states):
    sched = SimpleScheduler()
    print(f"🔄 Property test với {num_states} trạng thái...")
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
            print(f"❌ Lỗi tại state {i}: {msg}")
            return False
        if (i+1) % max(1, num_states//10) == 0:
            print(f"  ✅ Đã qua {i+1} states")
    print(f"✅ PASSED: {num_states} states, mọi bất biến đều đúng.")
    print("💪 Kết luận: hệ thống 'không thể sai' (trong không gian đã kiểm tra).")
    return True

if __name__ == "__main__":
    num = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    run_test(num)
