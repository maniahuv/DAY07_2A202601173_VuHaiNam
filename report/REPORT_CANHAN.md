# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Vũ Hải Nam
**Nhóm:** sixtuat
**Ngày:** 03/08/2026

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**
> *Viết 1-2 câu:* Nghĩa là góc giữa hai vector embedding rất nhỏ (gần 0 độ), thể hiện hai đoạn văn bản có ý nghĩa ngữ nghĩa rất gần gũi và tương đồng với nhau.

**Ví dụ có độ tương tự CAO:**
- Câu A: "Sinh viên nộp học phí muộn sẽ không được thi cuối kỳ."
- Câu B: "Nếu đóng học phí trễ hạn, sinh viên bị cấm thi học kỳ."
- Tại sao tương đồng: Hai câu dùng từ vựng khác nhau (đóng/nộp, trễ hạn/muộn) nhưng cùng chung một ngữ nghĩa cốt lõi về hình phạt khi nộp tiền học muộn.

**Ví dụ có độ tương tự THẤP:**
- Câu A: "Sinh viên nộp học phí muộn sẽ không được thi cuối kỳ."
- Câu B: "Thư viện mở cửa từ 8h sáng đến 5h chiều hàng ngày."
- Tại sao khác: Hai câu nói về hai chủ đề hoàn toàn độc lập (học phí vs thời gian mở cửa thư viện), không có điểm chung về ngữ nghĩa.

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
> *Viết 1-2 câu:* Vì cosine similarity tập trung vào hướng của vector (ngữ nghĩa) thay vì độ dài của vector (độ dài văn bản), giúp so sánh được hai đoạn text có độ dài ngắn khác nhau nhưng cùng chung ý nghĩa.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> *Trình bày phép tính:* Mỗi chunk tiếp theo sẽ nhích tới một khoảng là: stride = chunk_size - overlap = 500 - 50 = 450. Số lượng chunk = ceil((10000 - 50) / 450) = 23 chunks (hoặc tính nhanh: 10000 / 450 làm tròn lên).
> *Đáp án:* Khoảng 23 chunks.

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**
> *Viết 1-2 câu:* Số lượng chunk sẽ tăng lên (khoảng 25 chunks) vì bước nhảy (stride) giảm xuống còn 400. Cần độ chồng chéo nhiều hơn để đảm bảo không bị cắt đứt ngữ cảnh quan trọng giữa hai đoạn văn, giúp truy xuất thông tin đầy đủ hơn.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi lập trình (implement) các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:
> *Viết 2-3 câu: dùng biểu thức chính quy (regex) gì để phát hiện câu? Xử lý trường hợp ngoại lệ (edge case) nào?* Sử dụng regex `[^.!?]+[.!?]*` hoặc `re.split` theo dấu câu để tách câu. Trường hợp ngoại lệ được xử lý là ghép các câu quá ngắn hoặc xử lý dấu câu bị thừa.

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
> *Viết 2-3 câu: thuật toán hoạt động thế nào? Base case (trường hợp cơ sở) là gì?* Thuật toán sẽ đệ quy cắt văn bản theo các dấu phân cách (như `\n\n`, `\n`, ` `). Base case là khi đoạn văn bản hiện tại có độ dài nhỏ hơn `chunk_size` thì sẽ trả về đoạn đó luôn.

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:
> *Viết 2-3 câu: lưu trữ thế nào? Tính độ tương tự ra sao?* Các chunk sau khi được mô hình mã hóa sẽ được lưu trữ vào bộ nhớ in-memory (hoặc ChromaDB). Khi search, hệ thống mã hóa câu query và tính Cosine Similarity giữa nó với toàn bộ các chunk trong kho để chọn ra Top-K.

**`search_with_filter` + `delete_document`** — hướng tiếp cận:
> *Viết 2-3 câu: lọc (filter) trước hay sau? Xóa bằng cách nào?* Lọc (filter) bằng metadata được thực hiện trước khi tính similarity (pre-filtering) để tối ưu tốc độ tính toán. Xóa tài liệu bằng cách duyệt mảng và loại bỏ các chunk có chung `doc_id`.

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
> *Viết 2-3 câu: cấu trúc prompt? Cách đưa ngữ cảnh (inject context) vào thế nào?* Hệ thống tìm top-k chunks liên quan, nối nội dung lại và nhúng vào prompt mẫu dưới dạng `Context: ...`. Sau đó truyền prompt (gồm Context và Query) cho LLM để tổng hợp câu trả lời sát thực tế nhất.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```text
============================= test session starts ==============================
collected 42 items

tests/test_solution.py::TestSentenceChunker::test_basic_sentence_splitting PASSED [ 2%]
...
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_true_for_existing PASSED [100%]

============================== 42 passed in 0.10s ==============================
```

**Số lượng bài test vượt qua (pass):** 42 / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | Mức học phí HUST là bao nhiêu? | Chi phí học tập tại Bách Khoa như thế nào? | cao | ~0.85 | Có |
| 2 | Quy định học bổng KKHT. | Sinh viên nộp học phí muộn bị kỷ luật. | thấp | ~0.12 | Có |
| 3 | Sinh viên khuyết tật được miễn học phí. | Chính sách hỗ trợ học phí cho người khuyết tật. | cao | ~0.91 | Có |
| 4 | Điểm CPA tối thiểu để không bị cảnh báo là bao nhiêu? | Chuẩn đầu ra tiếng Anh K70. | thấp | ~0.08 | Có |
| 5 | Điều kiện nhận học bổng Trần Đại Nghĩa. | Mức điểm xét học bổng Khuyến khích học tập. | cao | ~0.65 | Có |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> *Viết 2-3 câu:* Cặp số 5 khá bất ngờ vì cùng chủ đề "học bổng" nhưng điểm tương đồng không quá cao tuyệt đối, do chúng nhắm đến 2 loại học bổng khác nhau (học lực vs khó khăn). Điều này cho thấy Embeddings biểu diễn ý nghĩa không chỉ dựa trên từ khóa chung mà còn bắt được chi tiết ngữ cảnh cốt lõi.

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân của bạn trong gói `src`. **5 câu hỏi này phải trùng với các thành viên cùng nhóm** (xem `REPORT_NHOM.md`).

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Sinh viên nộp học phí muộn so với quy định sẽ bị xử lý như thế nào? | ...Trường hợp nộp chậm sẽ bị xử lý theo quy chế công tác sinh viên... | 0.89 | Có | Bị hủy đăng ký môn học và không được dự thi cuối kỳ. |
| 2 | Điểm trung bình tích lũy (CPA) tối thiểu để sinh viên không bị cảnh báo học tập là bao nhiêu? | ...Sinh viên bị cảnh báo học tập nếu CPA < 1.0 (sau HK1)... | 0.85 | Có | Phụ thuộc vào học kỳ, ví dụ HK1 là < 1.0, HK2 là < 1.2... |
| 3 | Sinh viên K70 cần đạt chuẩn đầu ra ngoại ngữ tương đương IELTS bao nhiêu để xét tốt nghiệp? | ...hoặc TOEIC quốc tế đạt từ 500 điểm trở lên (hoặc IELTS 5.0...)... | 0.88 | Có | Cần TOEIC 500 hoặc chứng chỉ quốc tế IELTS 5.0 - 5.5 trở lên. |
| 4 | Điều kiện tối thiểu về điểm học tập và rèn luyện để đạt học bổng Khuyến khích học tập loại Khá là gì? | ...Loại C (Khá): Học lực Khá (CPA kỳ >= 2.5), Rèn luyện Khá... | 0.90 | Có | Cần đạt CPA kỳ >= 2.5 và Điểm rèn luyện từ Khá trở lên. |
| 5 | (Lọc audience=student) Sinh viên khuyết tật có được miễn giảm học phí không? | ...Sinh viên khuyết tật đặc biệt nặng và khuyết tật nặng được miễn... | 0.92 | Có | Có, được miễn 100% học phí nếu thuộc diện hộ nghèo/cận nghèo. |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** 5 / 5

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**
> *Viết 2-3 câu:* Việc thay đổi kích thước Chunk (Chunk Size) và ngắt đoạn theo Header ảnh hưởng rất lớn đến độ chuẩn xác của ngữ cảnh. Nếu cắt giữa chừng một đoạn Điều khoản, Bot có thể bị thiếu vế điều kiện và dẫn tới trả lời sai lệch.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 10 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 5 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | 10 / 10 |
| **Tổng phần cá nhân** | **60 / 60** |


