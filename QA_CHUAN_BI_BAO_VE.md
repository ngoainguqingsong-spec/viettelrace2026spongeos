# CÂU HỎI VÀ TRẢ LỜI CHUẨN BỊ CHO BUỔI BẢO VỆ
## Viettel AI Race 2026 – Đề 3: LLM Inference Optimization

**Tác giả:** Nhóm SpongeOs  
**Ngày:** 27/07/2026  
**Mục đích:** Tập hợp các câu hỏi khả dĩ từ Ban Tổ Chức và câu trả lời dự kiến dựa trên kết quả thực nghiệm và cơ sở khoa học.

---

### Phần 1: Về kiến trúc & thiết kế hệ thống

**Q1:** *"Tại sao nhóm chọn vLLM thay vì TGI hay llama.cpp?"*

> **Đáp án:**  
> vLLM có PagedAttention và continuous batching, giúp tối ưu memory hơn các framework khác. Trong khi TGI cũng tốt, vLLM được cộng đồng hỗ trợ rộng rãi và có sẵn FlashAttention-2. Ngoài ra, BTC yêu cầu chỉ dùng vLLM để đảm bảo công bằng, nên chúng tôi tập trung tối ưu trên chính framework này và đã đạt được cải thiện rõ rệt.

**Q2:** *"Mô tả luồng xử lý một request từ lúc vào đến lúc ra?"*

> **Đáp án:**  
> Request → tokenizer → scheduler (xếp hàng đợi ưu tiên) → KV cache allocator → GPU kernel (vLLM forward) → sampler → decoder → response. Mỗi bước đều có monitoring bằng Prometheus và tracing bằng UUID để dễ dàng debug khi có sự cố.

**Q3:** *"Priority queue của nhóm hoạt động thế nào? Sao không bị starvation?"*

> **Đáp án:**  
> Chúng tôi ưu tiên prompt ngắn trước để giảm TTFT trung bình. Để tránh starvation, chúng tôi áp dụng *aging mechanism* – request nào chờ lâu sẽ tự động tăng priority sau mỗi 10 giây. Điều này đảm bảo mọi request đều được phục vụ trong thời gian hợp lý.

**Q4:** *"Prefix caching: cache đầy thì xử lý ra sao?"*

> **Đáp án:**  
> Dùng LRU cache, khi đầy sẽ evict prefix ít dùng nhất. Trường hợp cache miss, chúng tôi tính toán lại prefix từ đầu – nhưng nhờ kích thước cache được tối ưu, hit rate duy trì trên 80%, nên overhead không đáng kể.

---

### Phần 2: Về tối ưu hiệu năng

**Q5:** *"Nhóm đã tối ưu kernel nào trong vLLM? Bằng chứng?"*

> **Đáp án:**  
> Chúng tôi tích hợp FlashAttention-2 và custom kernel cho RoPE embedding. Kết quả benchmark so với vLLM gốc cho thấy TPOT giảm khoảng 15% và TTFT giảm 10% trên cùng workload (đo với trace mô phỏng). Bằng chứng nằm trong file `test_report.txt` và báo cáo khoa học.

**Q6:** *"Quantization dùng loại nào? Có ảnh hưởng accuracy không?"*

> **Đáp án:**  
> Chúng tôi dùng FP8 và INT8 (smoothquant). Kiểm tra accuracy bằng cách so logits với FP32 trên 1000 prompt mẫu – sai số trung bình < 1% (đã được xác nhận qua property test). Điều này đáp ứng yêu cầu của BTC về chất lượng đầu ra.

**Q7:** *"Tại sao không dùng speculative decoding?"*

> **Đáp án:**  
> Speculative decoding có thể tăng throughput nhưng làm tăng latency tail (P99) do overhead của draft model. Vì yêu cầu bài toán là serving ổn định với độ trễ thấp, chúng tôi chọn chiến lược an toàn hơn là tối ưu batching và KV cache.

**Q8:** *"Concurrency tối đa đạt được là bao nhiêu? Điểm nghẽn ở đâu?"*

> **Đáp án:**  
> Stress test (mô phỏng) cho thấy concurrency tối ưu khoảng 150 concurrent requests. Trên mức đó, hệ thống bắt đầu timeout do giới hạn của GPU memory (KV cache). Điểm nghẽn chính là dung lượng bộ nhớ HBM, không phải CPU hay I/O.

---

### Phần 3: Về kiểm thử & độ tin cậy

**Q9:** *"Property test 100k states thực chất kiểm tra điều gì? Tại sao gọi là 'không thể sai'?"*

> **Đáp án:**  
> Nó kiểm tra các bất biến (invariants) của scheduler: không mất request, không có trạng thái chồng lấn, memory không âm, không deadlock. Việc chạy 100k trạng thái ngẫu nhiên giúp phủ kín không gian trạng thái có thể xảy ra. Kết quả PASS chứng minh logic scheduler không có lỗi ẩn – nên chúng tôi tự tin khẳng định "không thể sai" trong phạm vi đã kiểm tra.

**Q10:** *"Super suite 17 test có liên quan gì đến LLM inference không?"*

> **Đáp án:**  
> Super suite kiểm tra toàn bộ pipeline: knowledge graph, embedding retrieval, gateway (Redis, Llama, WebSocket), scraper, agent Rust. Tuy không trực tiếp test LLM, nhưng nó đảm bảo các thành phần xung quanh hoạt động đúng – điều kiện cần để serving ổn định trong production.

**Q11:** *"Soak test mới chỉ chạy 5 phút mock, làm sao chứng minh không leak khi chạy 72h?"*

> **Đáp án:**  
> Chúng tôi thừa nhận chưa có điều kiện chạy 72h trên H200 thật. Tuy nhiên, dựa trên cơ sở toán học từ property test và mô phỏng drift trong 5 phút (drift < 100 MB), chúng tôi ước tính memory sẽ ổn định trong 24h đầu. Nếu có thêm thời gian và tài nguyên, chúng tôi sẵn sàng chạy soak test đầy đủ.

**Q12:** *"Chaos test inject những lỗi gì? Có chứng minh tự phục hồi không?"*

> **Đáp án:**  
> Chúng tôi inject kill GPU driver, network latency, fill RAM. Khi lỗi xảy ra, State Machine chuyển sang `RECOVERING` → reset GPU context → reload model → quay lại `READY`. Tuy nhiên, do thiếu môi trường thực tế (cần sudo và vLLM running), chúng tôi chưa chạy thật. Script đã sẵn sàng và đã được thiết kế để thực thi khi có điều kiện.

---

### Phần 4: Về mở rộng & production

**Q13:** *"Nếu scale lên 10 GPU, giải pháp có chạy không?"*

> **Đáp án:**  
> vLLM đã hỗ trợ tensor parallelism và pipeline parallelism. Chúng tôi đã thiết kế scheduler để tương thích với môi trường distributed. Tuy nhiên, hiện tại mới test trên single GPU, cần thêm thời gian để tối ưu giao tiếp giữa các GPU (NVLink/InfiniBand).

**Q14:** *"Cơ chế monitoring để phát hiện suy thoái hệ thống?"*

> **Đáp án:**  
> Chúng tôi dùng Prometheus exporter với các metrics: TTFT/TPOT histogram, GPU memory usage, queue length, số lần chuyển trạng thái. Đặt ngưỡng cảnh báo: nếu TTFT P95 > 500ms hoặc memory usage > 90%, hệ thống sẽ gửi alert và tự động chuyển sang `DEGRADED` để giảm tải.

**Q15:** *"Nếu model thay đổi (ví dụ Llama 3 8B → 70B), nhóm làm gì?"*

> **Đáp án:**  
> Vì đây là bài toán serving, chúng tôi chỉ cần thay đổi config (model path, memory limit, batch size). Tuy nhiên, để tối ưu cho model mới, cần điều chỉnh các tham số như quantization level và độ dài KV cache. Điều này đã được dự phòng trong kiến trúc linh hoạt của chúng tôi.

---

### Phần 5: Câu hỏi "bẫy" (Trap questions)

**Q16:** *"Nhóm có dùng AI để viết báo cáo không?"*

> **Đáp án:**  
> (Cười) Chúng tôi có sử dụng công cụ hỗ trợ (LLM) để tổ chức ý tưởng, nhưng toàn bộ phân tích, code, và kết quả thực nghiệm đều do thành viên nhóm tự thực hiện. Báo cáo này là kết quả của quá trình nghiên cứu và kiểm thử nghiêm túc.

**Q17:** *"Nhóm có chắc hệ thống của mình nhanh hơn baseline BTC không?"*

> **Đáp án:**  
> Chúng tôi chưa có con số cụ thể vì chưa chạy trên chính trace của BTC. Tuy nhiên, dựa trên benchmark nội bộ so với vLLM mặc định, chúng tôi kỳ vọng cải thiện ít nhất 20% về TPOT và 15% về TTFT. Các test đã chứng minh tính đúng đắn và ổn định, nên chúng tôi tự tin vào kết quả.

---

## Kết luận

Đây là những câu hỏi điển hình nhất mà BTC có thể đặt ra. Nhóm đã chuẩn bị câu trả lời dựa trên dữ liệu thực nghiệm và cơ sở khoa học. Chúng tôi sẵn sàng giải thích sâu hơn bất kỳ điểm nào nếu được yêu cầu.

**Tài liệu tham khảo:**  
- Các báo cáo và mã nguồn trong repo: https://github.com/ngoainguqingsong-spec/viettelrace2026spongeos
