# GIẢI THÍCH ĐỀ BÀI LLM INFERENCE OPTIMIZATION BẰNG NGÔN NGỮ TRẺ 3 TUỔI
## Phân tích bản chất và yêu cầu kỹ thuật dưới góc nhìn sư phạm

**Tác giả:** Nhóm nghiên cứu SpongeOs  
**Ngày:** 27/07/2026  
**Mục đích:** Cung cấp một cách tiếp cận trực quan, dễ hiểu để nắm bắt bản chất của bài toán tối ưu inference cho LLM, phù hợp cho cả người mới bắt đầu và các nhà quản lý dự án.

---

## Tóm tắt (Abstract)

Bài báo này phân tích đề thi Viettel AI Race 2026 – Đề 3: LLM Inference Optimization bằng cách sử dụng ngôn ngữ và hình ảnh quen thuộc với trẻ em 3 tuổi. Mục tiêu là làm rõ bản chất của bài toán (tối ưu hóa hệ thống đã có sẵn), các ràng buộc kỹ thuật (chỉ dùng vLLM), các khái niệm tối ưu GPU/kernel, và tiêu chí chấm điểm (TTFT, TPOT). Phương pháp này giúp các bên liên quan không chuyên về kỹ thuật có thể hiểu được cốt lõi của thách thức, từ đó hỗ trợ tốt hơn trong việc ra quyết định và đánh giá kết quả.

**Từ khóa:** LLM Inference, vLLM, Analogical Reasoning, Pedagogy, TTFT, TPOT

---

## 1. Giới thiệu (Introduction)

Trong các cuộc thi công nghệ như Viettel AI Race, việc truyền đạt yêu cầu kỹ thuật đến nhiều đối tượng (từ kỹ sư đến quản lý, từ chuyên gia đến người mới) là một thách thức. Ngôn ngữ chuyên ngành có thể gây khó hiểu và làm lu mờ bản chất của vấn đề. Bài báo này áp dụng phương pháp **suy luận tương tự (analogical reasoning)** [1] để chuyển đổi các khái niệm phức tạp của bài toán LLM Inference Optimization thành các hình ảnh và câu chuyện quen thuộc với trẻ em 3 tuổi. Cách tiếp cận này không chỉ giúp dễ hiểu mà còn làm nổi bật các yếu tố cốt lõi của bài toán.

---

## 2. Phân tích bản chất bài toán

### 2.1. Bản chất: Tối ưu hệ thống đã có sẵn

**Mô tả kỹ thuật:** Thí sinh được cung cấp một mô hình LLM đã được huấn luyện và một serving stack (vLLM) cố định. Nhiệm vụ là tối ưu hóa hiệu năng của hệ thống này mà **không được thay đổi mô hình** (cấm train, cấm fine-tune).

**Phép tương tự (cho trẻ 3 tuổi):**
> *"Mẹ đưa cho con một chiếc xe ô tô đồ chơi đã lắp ráp sẵn. Con không được tháo ra lắp lại hay độ thêm máy móc gì. Nhiệm vụ của con là làm sao để xe chạy thật nhanh và mượt, không xịt khói hay giật cục."*

**Ý nghĩa:** Điểm mấu chốt là tối ưu vận hành (operation optimization) chứ không phải cải tiến mô hình (model improvement). Điều này tập trung vào kỹ năng hệ thống (system engineering) hơn là AI/ML.

### 2.2. Ràng buộc kỹ thuật: Chỉ dùng vLLM

**Mô tả kỹ thuật:** BTC chỉ cho phép sử dụng vLLM làm framework serving duy nhất. Không được dùng TGI, llama.cpp, hay bất kỳ framework nào khác.

**Phép tương tự:**
> *"Mẹ bảo con chỉ được dùng đúng chai dầu nhớt hiệu vLLM này để tra vào xe. Dùng chai khác là mẹ phạt!"*

**Ý nghĩa:** Ràng buộc này đảm bảo tính công bằng giữa các đội và ổn định cho hệ thống chấm bài backend. Thí sinh phải thể hiện kỹ năng chuyên sâu với một công cụ cụ thể.

### 2.3. Tối ưu GPU và Kernel

**Mô tả kỹ thuật:** Tối ưu hóa cách sử dụng phần cứng GPU, bao gồm việc khai thác các kernel tính toán (CUDA kernels), quản lý bộ nhớ, và tinh chỉnh pipeline xử lý của vLLM.

**Phép tương tự:**
> *"Con không được thay máy mới, nhưng con có thể xỏ tay vào bánh xe, tra thêm mỡ, bơm hơi lốp, chỉnh lại thắng để xe dùng hết sức mạnh của pin, phóng vèo vèo."*

**Ý nghĩa:** Tối ưu GPU là yếu tố then chốt để cải thiện hiệu năng mà không cần thay đổi phần cứng. Điều này đòi hỏi hiểu biết sâu về kiến trúc GPU và các kỹ thuật lập trình hiệu năng cao.

### 2.4. Tiêu chí chấm điểm: Chính xác và Tốc độ

**Mô tả kỹ thuật:** 
- **Vòng gác cổng:** Đảm bảo độ chính xác (quality/accuracy) của đầu ra. Nếu sai, bị loại.
- **Vòng xếp hạng:** So sánh hiệu năng tốc độ qua hai chỉ số: TTFT (thời gian đến token đầu tiên) và TPOT (thời gian sinh mỗi token tiếp theo). TTFT càng thấp, TPOT càng thấp, điểm càng cao.

**Phép tương tự:**
> *"Cô giáo bảo con lái xe qua vạch kẻ. Nếu xe đi lệch đường (sai) là bị loại. Nếu đi đúng, cô bấm giờ xem con xuất phát nhanh bao nhiêu (TTFT) và chạy liên tục nhanh bao nhiêu (TPOT)."*

**Ý nghĩa:** Đây là bài toán tối ưu đa mục tiêu (multi-objective): vừa phải đảm bảo chất lượng (ràng buộc cứng), vừa phải tối ưu tốc độ (mục tiêu mềm). Hai chỉ số TTFT và TPOT đo lường các khía cạnh khác nhau của trải nghiệm người dùng: độ phản hồi ban đầu và độ mượt mà khi sinh nội dung dài.

---

## 3. Tóm tắt kết luận

Dưới dạng một câu ngắn gọn cho trẻ 3 tuổi:

> *"Họ đưa cho con một cỗ máy đã lắp sẵn. Con chỉ được dùng một loại dầu duy nhất, nhưng con phải khéo léo vặn hết công suất cho nó chạy. Phải chạy đúng đường trước, sau đó phải chạy nhanh hơn tất cả các bạn khác từ lúc xuất phát cho đến lúc về đích!"*

---

## 4. Ứng dụng trong chiến lược phát triển

Hiểu bản chất bài toán theo cách này giúp định hướng chiến lược tối ưu:
- **Giai đoạn 1 (Ưu tiên cao nhất):** Đảm bảo độ chính xác (model verification test). Nếu không qua cổng, mọi nỗ lực tối ưu tốc độ đều vô nghĩa.
- **Giai đoạn 2:** Tối ưu TTFT bằng cách tập trung vào prefetching, cache, và scheduling cho các prompt ngắn.
- **Giai đoạn 3:** Tối ưu TPOT bằng cách cải thiện kernel, batching, và quantization để tăng throughput cho các prompt dài.
- **Xuyên suốt:** Áp dụng bộ kiểm thử đa tầng (property, stress, soak, chaos) để đảm bảo các tối ưu không làm giảm độ ổn định của hệ thống.

---

## 5. Tài liệu tham khảo

[1] Gentner, D. (1983). Structure-mapping: A theoretical framework for analogy. Cognitive Science, 7(2), 155-170.  
[2] Bài viết gốc của Lê Thanh Tùng (SpongeOs), 2026.

---

**Phụ lục:** Mã nguồn và các bài viết liên quan tại repo:  
https://github.com/ngoainguqingsong-spec/viettelrace2026spongeos
