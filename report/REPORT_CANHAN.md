# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Vũ Hải Nam
**Nhóm:** Nhóm K3
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



# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Giang Minh Phú  
**Nhóm:** Nhóm K3  
**Ngày:** 03/08/2026

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**
> Độ tương tự cosine cao nghĩa là hai vector embedding có hướng gần nhau trong không gian vector, nên hai đoạn văn bản thường gần nhau về ý nghĩa, chủ đề hoặc ngữ cảnh. Giá trị càng gần 1 thì mức độ tương đồng ngữ nghĩa càng cao.

**Ví dụ có độ tương tự CAO:**
- Câu A: "Sinh viên phải hoàn thành học phí trước kỳ thi cuối kỳ."
- Câu B: "Trước khi được dự thi cuối kỳ, người học cần nộp đầy đủ học phí."
- Tại sao tương đồng: Hai câu dùng cách diễn đạt khác nhau nhưng cùng nói về điều kiện hoàn thành học phí trước kỳ thi cuối kỳ.

**Ví dụ có độ tương tự THẤP:**
- Câu A: "Sinh viên cần đạt TOEIC 500 để xét tốt nghiệp."
- Câu B: "Thư viện trường mở cửa vào buổi sáng."
- Tại sao khác: Hai câu thuộc hai chủ đề khác nhau, một câu nói về chuẩn ngoại ngữ khi tốt nghiệp, câu còn lại nói về dịch vụ thư viện.

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
> Cosine similarity tập trung vào hướng của vector nên phù hợp để so sánh ý nghĩa của text embedding. Khoảng cách Euclid dễ bị ảnh hưởng bởi độ lớn của vector, vì vậy có thể kém ổn định hơn khi các vector khác nhau về magnitude hoặc độ dài văn bản.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> Trình bày phép tính: step = 500 - 50 = 450. Số chunk = ceil((10000 - 50) / 450) = ceil(9950 / 450) = 23.  
> Đáp án: 23 chunks.

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**
> Khi overlap tăng lên 100, step giảm còn 400 nên số chunk tăng lên. Overlap lớn hơn giúp giữ ngữ cảnh tốt hơn ở ranh giới giữa hai chunk liền kề, nhưng đổi lại làm tăng số chunk, dung lượng lưu trữ và chi phí embedding.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi lập trình (implement) các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:
> Tôi dùng regex `(?<=[.!?])\s+` để tách văn bản tại khoảng trắng đứng sau dấu kết thúc câu như `.`, `!`, hoặc `?`, đồng thời vẫn giữ dấu câu ở cuối câu trước. Sau đó tôi `strip()` từng câu, bỏ phần rỗng và gom tối đa `max_sentences_per_chunk` câu vào một chunk. Trường hợp văn bản rỗng trả về danh sách rỗng `[]`.

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
> Tôi dùng chiến lược đệ quy với danh sách separator theo thứ tự ưu tiên: đoạn văn, dòng, câu, từ rồi ký tự. Nếu đoạn hiện tại đã ngắn hơn `chunk_size` thì trả về luôn; nếu hết separator thì cắt cố định theo `chunk_size`. Khi một phần vẫn quá dài, hàm tiếp tục gọi `_split` với separator ưu tiên thấp hơn để tiến dần tới điều kiện dừng.

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:
> `add_documents` chuyển từng `Document` thành một record in-memory gồm `id`, `content`, bản sao `metadata` và `embedding` của nội dung. Mỗi record có `doc_id` trong metadata để truy vết tài liệu gốc. `search` tạo embedding cho query một lần, tính điểm bằng dot product giữa query embedding và từng record embedding, sau đó sắp xếp giảm dần theo `score` và lấy `top_k`.

**`search_with_filter` + `delete_document`** — hướng tiếp cận:
> `search_with_filter` thực hiện lọc metadata trước rồi mới xếp hạng bằng embedding, để tránh trường hợp lấy top-k trước rồi loại hết các kết quả không đúng metadata. Một record chỉ được giữ lại nếu toàn bộ cặp key-value trong `metadata_filter` khớp với metadata của record. `delete_document` xóa tất cả record có `metadata["doc_id"]` trùng với tài liệu gốc và trả về `True` nếu có ít nhất một record bị xóa.

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
> Agent gọi `store.search(question, top_k)` để lấy các chunk liên quan nhất, sau đó ghép chúng thành phần context có đánh số `[1]`, `[2]`, kèm `doc_id` và nguồn để dễ truy vết. Prompt gồm phần hướng dẫn chỉ dùng context, phần context, câu hỏi và nhãn `Answer:`. Nếu store không có kết quả, agent trả thông báo rõ ràng thay vì gọi LLM không cần thiết.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```
============================= test session starts =============================
platform win32 -- Python 3.11.4, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\AI thuc chien\lab7\K3-Day07-Data-Foundations-C6
collected 42 items

tests/test_solution.py::TestProjectStructure::test_root_main_entrypoint_exists PASSED
tests/test_solution.py::TestProjectStructure::test_src_package_exists PASSED
tests/test_solution.py::TestClassBasedInterfaces::test_chunker_classes_exist PASSED
tests/test_solution.py::TestClassBasedInterfaces::test_mock_embedder_exists PASSED
tests/test_solution.py::TestFixedSizeChunker::* PASSED
tests/test_solution.py::TestSentenceChunker::* PASSED
tests/test_solution.py::TestRecursiveChunker::* PASSED
tests/test_solution.py::TestEmbeddingStore::* PASSED
tests/test_solution.py::TestKnowledgeBaseAgent::* PASSED
tests/test_solution.py::TestComputeSimilarity::* PASSED
tests/test_solution.py::TestCompareChunkingStrategies::* PASSED
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::* PASSED
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::* PASSED

============================= 42 passed =============================
```

**Số lượng bài test vượt qua (pass):** 42 / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | Sinh viên phải hoàn thành học phí trước kỳ thi cuối kỳ. | Trước khi được dự thi cuối kỳ, người học cần nộp đầy đủ học phí. | cao | Mock: thấp/không ổn định | Đúng về ngữ nghĩa, mock không phản ánh tốt |
| 2 | Sinh viên cần đạt TOEIC 500 để xét tốt nghiệp. | Người học phải có chứng chỉ ngoại ngữ tương đương IELTS 5.0 trước khi tốt nghiệp. | cao | Mock: thấp/không ổn định | Đúng về ngữ nghĩa, mock không phản ánh tốt |
| 3 | Học bổng KKHT yêu cầu kết quả học tập và rèn luyện tốt. | Sinh viên có CPA và điểm rèn luyện đạt chuẩn có thể được xét học bổng. | cao | Mock: thấp/không ổn định | Đúng về ngữ nghĩa, mock không phản ánh tốt |
| 4 | Thư viện mở cửa vào buổi sáng. | Sinh viên khuyết tật được hỗ trợ miễn giảm học phí. | thấp | Mock: không ổn định | Đúng về ngữ nghĩa |
| 5 | Chương trình ELITECH có mức học phí cao hơn chương trình chuẩn. | Bóng đá thế giới tổ chức giải đấu lớn theo chu kỳ bốn năm. | thấp | Mock: không ổn định | Đúng về ngữ nghĩa |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> Kết quả bất ngờ nhất là `MockEmbedder` không nhất thiết cho điểm cao với các cặp câu giống nhau về nghĩa. Điều này xảy ra vì mock embedding chỉ dùng để test kỹ thuật, sinh vector quyết định theo nội dung chuỗi chứ không thật sự hiểu ngữ nghĩa. Với embedding thực như Sentence Transformers hoặc OpenAI embeddings, các câu cùng ý nghĩa thường nằm gần nhau hơn trong không gian vector.

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân của bạn trong gói `src`. **5 câu hỏi này phải trùng với các thành viên cùng nhóm** (xem `REPORT_NHOM.md`).

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Sinh viên nộp học phí muộn so với quy định sẽ bị xử lý như thế nào? | Top-1 trả về chunk `k3-hoc-bong`, chưa đúng tài liệu kỳ vọng `k3-hoc-phi`. | 0.205 | Không | Agent dựa vào chunk học bổng nên chưa trả lời đúng câu hỏi học phí. |
| 2 | Điểm trung bình tích lũy (CPA) tối thiểu để sinh viên không bị cảnh báo học tập là bao nhiêu? | Top-1 trả về chunk `k3-ngoai-ngu`, chưa đúng tài liệu kỳ vọng `k3-quy-che-dao-tao`. | 0.199 | Không | Agent dựa vào chunk ngoại ngữ nên chưa trả lời đúng về cảnh báo học tập. |
| 3 | Sinh viên K70 cần đạt chuẩn đầu ra ngoại ngữ tương đương IELTS bao nhiêu để đủ điều kiện xét tốt nghiệp? | Top-1 trả về chunk `k3-ngoai-ngu`, liên quan đến quy định ngoại ngữ và thời hạn chứng chỉ. | 0.256 | Có | Agent dựa vào tài liệu ngoại ngữ, có nguồn liên quan để trả lời. |
| 4 | Điều kiện tối thiểu về điểm học tập và rèn luyện để đạt học bổng Khuyến khích học tập loại Khá là gì? | Top-1 trả về chunk `k3-quy-che-dao-tao`, chưa đúng tài liệu kỳ vọng `k3-hoc-bong`. | 0.160 | Không | Agent chưa lấy đúng chunk điều kiện học bổng KKHT. |
| 5 | (Lọc metadata: audience=student) Sinh viên khuyết tật có được miễn giảm học phí không? | Top-1 trả về chunk `k3-hoc-phi`; top-3 chưa lấy đúng chunk `k3-sv-khuyet-tat`. | 0.227 | Không | Agent chưa truy xuất đúng tài liệu chính sách sinh viên khuyết tật. |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** 1 / 5

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**
> Điều tôi học được là cùng một corpus nhưng chunking strategy khác nhau có thể làm kết quả retrieval thay đổi rất mạnh. Với dữ liệu quy chế có cấu trúc theo điều/mục, chunk theo heading giúp giữ ngữ cảnh tốt hơn, nhưng chất lượng vẫn phụ thuộc nhiều vào embedding model; mock embedding chỉ phù hợp để kiểm thử pipeline, không phù hợp để đánh giá chất lượng ngữ nghĩa thật.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 10 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 5 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | 2 / 10 |
| **Tổng phần cá nhân** | **52 / 60** |


# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Nguyễn Tiến Thanh
**Nhóm:** K3
**Ngày:** 2026-08-03

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity)

**Độ tương tự cosine cao nghĩa là gì?**

Độ tương tự cosine cao nghĩa là hai vector embedding có hướng gần nhau, tức hai đoạn văn bản thường nói về cùng chủ đề hoặc có ý nghĩa gần nhau. Với retrieval, chunk có cosine similarity cao hơn thường được xem là liên quan hơn với query.

**Ví dụ có độ tương tự CAO:**
- Câu A: Sinh viên nộp học phí chậm có thể không được dự thi.
- Câu B: Nếu đóng học phí muộn, sinh viên có thể bị hạn chế quyền dự thi.
- Tại sao tương đồng: Cả hai câu đều nói về hậu quả của việc nộp học phí muộn.

**Ví dụ có độ tương tự THẤP:**
- Câu A: Sinh viên K70 cần đạt chuẩn đầu ra ngoại ngữ.
- Câu B: Thư viện mở cửa phục vụ mượn sách giáo trình.
- Tại sao khác: Hai câu thuộc hai chính sách khác nhau, một câu về ngoại ngữ, một câu về dịch vụ thư viện.

**Tại sao cosine similarity được ưu tiên hơn khoảng cách Euclid cho text embeddings?**

Cosine similarity tập trung vào hướng của vector nên phản ánh quan hệ ngữ nghĩa tốt hơn khi độ dài vector hoặc độ lớn tuyệt đối không quan trọng. Với text embeddings, hai câu có thể dùng số từ khác nhau nhưng vẫn cùng ý, nên so sánh hướng thường hợp lý hơn so sánh khoảng cách thẳng.

### Bài toán tính toán Chunking

**Tài liệu 10,000 ký tự, `chunk_size=500`, `overlap=50`. Bao nhiêu chunks?**

Công thức:

```text
số chunk = ceil((10000 - 50) / (500 - 50))
         = ceil(9950 / 450)
         = ceil(22.11)
         = 23 chunks
```

**Nếu `overlap` tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn overlap nhiều hơn?**

Khi `overlap=100`, bước nhảy còn `500 - 100 = 400`, nên số chunk là `ceil((10000 - 100) / 400) = ceil(24.75) = 25 chunks`. Overlap nhiều hơn làm tăng số chunk và chi phí tìm kiếm, nhưng giúp giữ ngữ cảnh ở ranh giới giữa hai chunk.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`**

Tôi dùng regex `(?<=[.!?])\s+` để tách văn bản theo ranh giới câu đơn giản, sau đó nhóm tối đa `max_sentences_per_chunk` câu vào một chunk. Với input rỗng trả về list rỗng; nếu không tách được câu rõ ràng thì giữ phần text đã strip làm một chunk.

**`RecursiveChunker.chunk` / `_split`**

Chiến lược recursive thử các separator theo thứ tự `\n\n`, `\n`, `. `, khoảng trắng và fallback cắt cứng theo ký tự. Base case là đoạn hiện tại đã nhỏ hơn hoặc bằng `chunk_size`; nếu một phần vẫn quá dài thì gọi `_split` tiếp với separator yếu hơn.

**Custom strategy của tôi: `HeadingChunker`**

Với corpus K3, tài liệu là quy định theo `Điều`, `Chương` và heading Markdown, nên tôi viết `HeadingChunker` để chia theo tiêu đề/mục. Cách này giúp một chunk giữ trọn nội dung của một điều khoản, phù hợp hơn fixed-size khi query hỏi một quy định cụ thể.

```python
from src import HeadingChunker

chunker = HeadingChunker(max_chars=900, overlap=120)
```

### Lớp EmbeddingStore

**`add_documents` + `search`**

Tôi dùng in-memory store để lưu mỗi document thành record gồm `id`, `content`, `metadata` và `embedding`. Khi search, query được embed cùng hàm embedding, sau đó tính dot product với từng record và sắp xếp giảm dần theo score.

**`search_with_filter` + `delete_document`**

`search_with_filter` lọc metadata trước rồi mới tính similarity trên tập ứng viên đã lọc, đúng với yêu cầu dùng metadata để thu hẹp kết quả. `delete_document` xóa tất cả chunk có `metadata["doc_id"]` hoặc `id` trùng với document cần xóa.

### Tác tử KnowledgeBaseAgent

**`answer`**

Agent lấy top-k chunk từ store, ghép thành context có đánh số nguồn, rồi tạo prompt yêu cầu trả lời chỉ dựa trên context. Nếu không có context phù hợp, prompt yêu cầu nói rõ là không biết thay vì tự suy đoán.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

### Kết Quả Kiểm Thử (Test Results)

Lệnh chạy:

```powershell
..\.venv\Scripts\python.exe -m pytest tests/ -q
```

Kết quả:

```text
..........................................                               [100%]
42 passed in 0.05s
```

**Số lượng bài test vượt qua:** 42 / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

Điểm thực tế được tính bằng `compute_similarity()` trên embedding từ `KeywordHashEmbedder`, vì môi trường hiện chưa cài `sentence-transformers`.

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | Sinh viên nộp học phí chậm sẽ không được dự thi. | Sinh viên đóng học phí muộn có thể bị hủy đăng ký môn học. | cao | 0.4709 | Đúng |
| 2 | Chuẩn đầu ra ngoại ngữ yêu cầu IELTS 5.0 hoặc TOEIC 500. | Sinh viên cần chứng chỉ tiếng Anh để xét tốt nghiệp. | trung bình/cao | 0.1703 | Một phần |
| 3 | Học bổng loại Khá yêu cầu CPA từ 2.5 và rèn luyện Khá. | Thư viện cho phép sinh viên mượn giáo trình. | thấp | 0.1135 | Đúng |
| 4 | Sinh viên khuyết tật nặng thuộc hộ nghèo được miễn 100% học phí. | Sinh viên khuyết tật được hỗ trợ tài chính và cơ sở vật chất. | cao | 0.6110 | Đúng |
| 5 | Quy chế đào tạo quy định cảnh báo học tập theo CPA. | Chương trình ELITECH yêu cầu chuẩn ngoại ngữ cao hơn. | thấp | 0.1955 | Một phần |

**Kết quả bất ngờ nhất**

Cặp 2 có điểm thấp hơn dự đoán dù cùng nói về chuẩn ngoại ngữ, vì keyword-hash phụ thuộc nhiều vào token trùng trực tiếp. Điều này cho thấy fallback lexical không thay thế hoàn toàn được semantic embedding thật; khi cài local multilingual embedder, các câu diễn đạt khác nhau nhưng cùng ý có thể được kéo gần nhau hơn.

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Benchmark dùng cùng 5 query của nhóm trong `benchmarks/k3_university_queries.csv`.

Lệnh chạy:

```powershell
..\.venv\Scripts\python.exe scripts\run_k3_benchmark.py --chunker heading --embedder auto
```

Cấu hình thực tế:

```text
Chunker: HeadingChunker(max_chars=900, overlap=120)
Embedder: keyword-hash fallback
Chunks: 27
Retrieval score: 10/10
```

| # | Câu hỏi (Query) | Gold answer | Top-1 Chunk truy xuất được | Top-3 doc_id | Score | Có liên quan không? |
|---|-------|-------------|----------------------------|--------------|-------|---------------------|
| 1 | Sinh viên nộp học phí muộn so với quy định sẽ bị xử lý như thế nào? | Có thể bị hủy đăng ký môn học hoặc không được dự thi. | `k3-hoc-phi`, Điều 5: Lộ trình đóng học phí | `k3-hoc-phi` \| `k3-hoc-phi` \| `k3-sv-khuyet-tat` | 0.3577 | Có, top-1 |
| 2 | Điểm trung bình tích lũy (CPA) tối thiểu để sinh viên không bị cảnh báo học tập là bao nhiêu? | Không dưới 1.0 sau HK1, không dưới 1.2 sau HK2 và không chậm tiến độ tín chỉ. | `k3-quy-che-dao-tao`, Chương IV: Cảnh báo học tập | `k3-quy-che-dao-tao` \| `k3-quy-che-dao-tao` \| `k3-quy-che-dao-tao` | 0.4936 | Có, top-1 |
| 3 | Sinh viên K70 cần đạt chuẩn đầu ra ngoại ngữ tương đương IELTS bao nhiêu để đủ điều kiện xét tốt nghiệp? | Chương trình chuẩn IELTS 5.0 tương đương; ELITECH thường IELTS 6.0 tùy chuyên ngành. | `k3-ngoai-ngu`, Điều 3: Chuẩn đầu ra ngoại ngữ | `k3-ngoai-ngu` \| `k3-quy-che-dao-tao` \| `k3-ngoai-ngu` | 0.4024 | Có, top-1 |
| 4 | Điều kiện tối thiểu về điểm học tập và rèn luyện để đạt học bổng Khuyến khích học tập loại Khá là gì? | CPA kỳ từ 2.5 trở lên và rèn luyện Khá. | `k3-hoc-bong`, Điều 1: Các loại học bổng | `k3-hoc-bong` \| `k3-hoc-bong` \| `k3-hoc-bong` | 0.4909 | Có trong top-3; chunk điều kiện nằm ở top-2 |
| 5 | Sinh viên khuyết tật có được miễn giảm học phí không? | Khuyết tật đặc biệt nặng/nặng thuộc hộ nghèo hoặc cận nghèo được miễn 100% học phí. | `k3-sv-khuyet-tat`, mục 3: Hỗ trợ tài chính | `k3-sv-khuyet-tat` \| `k3-sv-khuyet-tat` \| `k3-sv-khuyet-tat` | 0.4822 | Có, top-1; dùng filter `audience=student` |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** 5 / 5

**Nhận xét về benchmark**

`HeadingChunker` hoạt động tốt với corpus quy định vì các câu trả lời nằm trong từng điều/mục rõ ràng. Điểm yếu còn thấy ở câu 4: top-1 đúng tài liệu nhưng chưa phải chunk chứa điều kiện cụ thể; top-2 mới là chunk Điều 2 có CPA >= 2.5 và rèn luyện Khá.

**Vai trò metadata filter**

Câu 5 dùng `metadata_filter={"audience": "student"}`. Corpus có `audience=student` và `audience=all`, nên filter thật sự thu hẹp tập ứng viên và chứng minh metadata có ích thay vì chỉ chạy hình thức.

**Điều hay nhất tôi học được từ benchmark**

Cùng một corpus và cùng 5 query, strategy chunking quyết định chunk có giữ đủ ngữ cảnh hay không. Với văn bản quy chế, chia theo heading thường dễ kiểm chứng hơn fixed-size vì top-k trả về đúng đơn vị điều khoản.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 10 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 4 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | 10 / 10 |
| **Tổng phần cá nhân** | **59 / 60** |



# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Nguyễn Minh Nhật - 2A202601131
**Nhóm:** Nhóm K3
**Ngày:** 03/08/2026

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**
> Độ tương tự cosine cao nghĩa là góc giữa hai vector biểu diễn văn bản trong không gian vector rất nhỏ, biểu thị mức độ tương đồng lớn về mặt ngữ nghĩa, chủ đề hoặc từ vựng giữa hai văn bản đó, bất kể sự khác biệt về độ dài của chúng.

**Ví dụ có độ tương tự CAO:**
- Câu A: "Lập trình Python rất phổ biến trong AI."
- Câu B: "Ngôn ngữ Python được sử dụng rộng rãi để xây dựng các mô hình trí tuệ nhân tạo."
- Tại sao tương đồng: Cả hai câu đều nói cùng một ý nghĩa cốt lõi là sự ứng dụng rộng rãi và phổ biến của Python trong việc phát triển AI/mô hình trí tuệ nhân tạo.

**Ví dụ có độ tương tự THẤP:**
- Câu A: "Thư viện nhà trường mở cửa vào lúc 8 giờ sáng."
- Câu B: "Giải vô địch bóng đá thế giới diễn ra bốn năm một lần."
- Tại sao khác: Hai câu đề cập đến hai lĩnh vực hoàn toàn xa lạ (hoạt động của thư viện học đường vs chu kỳ giải đấu thể thao thế giới), không có sự tương quan về mặt từ ngữ lẫn ngữ nghĩa.

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
> Khoảng cách Euclid đo khoảng cách thẳng tuyệt đối giữa các điểm nên rất nhạy cảm với độ dài của văn bản (văn bản dài hơn sẽ có độ dài vector lớn hơn, đẩy chúng ra xa nhau). Trái lại, độ tương tự cosine chỉ quan tâm đến hướng (góc giữa các vector) và triệt tiêu ảnh hưởng của độ dài văn bản, giúp so sánh chính xác sự tương đồng về nội dung và ngữ nghĩa của các văn bản có độ dài khác nhau.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> Phép tính: số lượng chunk = làm_tròn_lên((10000 - 50) / (500 - 50)) = làm_tròn_lên(9950 / 450) = làm_tròn_lên(22.11) = 23.
> *Đáp án:* 23 chunks

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**
> Khi overlap tăng lên 100, số lượng chunk tăng lên thành: làm_tròn_lên((10000 - 100) / (500 - 100)) = làm_tròn_lên(9900 / 400) = làm_tròn_lên(24.75) = 25 chunks (tăng thêm 2 chunks). Chúng ta muốn độ chồng chéo nhiều hơn để bảo toàn tính ngữ cảnh và tính mạch lạc của thông tin nằm ở biên/ranh giới giữa các chunk liền kề, giúp mô hình RAG không bị mất mát thông tin quan trọng bị cắt nửa chừng.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi lập trình (implement) các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:
> Sử dụng biểu thức chính quy (regex) lookbehind `(?<=\. )|(?<=\! )|(?<=\? )|(?<=\.\n)` nhằm chia nhỏ văn bản ở các dấu phân tách câu tiêu chuẩn mà vẫn giữ lại dấu câu kết thúc. Sau đó lọc bỏ các câu trống, cắt khoảng trắng ở hai đầu, và gom các câu lại với số lượng tối đa là `max_sentences_per_chunk` trước khi ghép lại bằng khoảng trắng để tạo thành các chunk hoàn chỉnh.

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
> Sử dụng đệ quy duyệt qua một danh sách các dấu phân tách ưu tiên giảm dần (`\n\n`, `\n`, `. `, ` `, `""`). Nếu văn bản nhỏ hơn `chunk_size` (base case), trả về văn bản đó. Nếu không, ta chia nhỏ văn bản bằng dấu phân tách hiện tại, đệ quy chia tiếp các phần tử vượt kích thước cho phép bằng các dấu phân tách tiếp theo, sau đó gộp các sub-chunk con lại với nhau sao cho độ dài chuỗi gộp (bao gồm cả ký tự phân tách) tối ưu nhất nhưng không vượt quá `chunk_size`.

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:
> Hàm `add_documents` sinh vector nhúng cho từng document bằng `embedding_fn` rồi đẩy bản ghi vào bộ nhớ dưới dạng dictionary (gồm id, content, metadata, embedding) hoặc thêm trực tiếp vào ChromaDB collection. Hàm `search` nhúng truy vấn của người dùng rồi tính độ tương tự cosine (hoặc tích vô hướng) với tất cả các vector nhúng trong kho lưu trữ, sau đó sắp xếp giảm dần theo score và lấy top_k.

**`search_with_filter` + `delete_document`** — hướng tiếp cận:
> Áp dụng lọc trước (pre-filtering): duyệt qua các bản ghi trong store và chỉ giữ lại những bản ghi khớp với toàn bộ cặp key-value trong `metadata_filter` rồi mới thực hiện tìm kiếm tương tự (hoặc dùng mệnh đề `where` trong ChromaDB). Hàm `delete_document` thực hiện xóa tất cả các chunk thuộc về `doc_id` bằng cách kiểm tra cả `metadata['doc_id']`, ID chunk chính xác, hoặc ID chunk bắt đầu với tiền tố `doc_id` nhằm đảm bảo khả năng tương thích cao giữa các cách nạp dữ liệu khác nhau.

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
> Thực hiện tìm kiếm `top_k` chunk văn bản liên quan nhất bằng phương thức `search`, ghép các content thu được thành một chuỗi context hoàn chỉnh. Cấu trúc prompt mẫu dạng RAG rõ ràng với các phần: chỉ dẫn Agent hành xử, phần Context chứa các thông tin vừa truy xuất, phần Question chứa câu hỏi của người dùng và phần Answer dành cho LLM sinh câu trả lời.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0 -- /home/nhatnm/code/vin-project/lab/DAY07_2A202601327_OngXuanSon/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/nhatnm/code/vin-project/lab/DAY07_2A202601327_OngXuanSon
collecting ... collected 42 items

tests/test_solution.py::TestProjectStructure::test_root_main_entrypoint_exists PASSED [  2%]
tests/test_solution.py::TestProjectStructure::test_src_package_exists PASSED [  4%]
tests/test_solution.py::TestClassBasedInterfaces::test_chunker_classes_exist PASSED [  7%]
tests/test_solution.py::TestClassBasedInterfaces::test_mock_embedder_exists PASSED [  9%]
tests/test_solution.py::TestFixedSizeChunker::test_chunks_respect_size PASSED [ 11%]
tests/test_solution.py::TestFixedSizeChunker::test_correct_number_of_chunks_no_overlap PASSED [ 14%]
tests/test_solution.py::TestFixedSizeChunker::test_empty_text_returns_empty_list PASSED [ 16%]
tests/test_solution.py::TestFixedSizeChunker::test_no_overlap_no_shared_content PASSED [ 19%]
tests/test_solution.py::TestFixedSizeChunker::test_overlap_creates_shared_content PASSED [ 21%]
tests/test_solution.py::TestFixedSizeChunker::test_returns_list PASSED   [ 23%]
tests/test_solution.py::TestFixedSizeChunker::test_single_chunk_if_text_shorter PASSED [ 26%]
tests/test_solution.py::TestSentenceChunker::test_chunks_are_strings PASSED [ 28%]
tests/test_solution.py::TestSentenceChunker::test_respects_max_sentences PASSED [ 30%]
tests/test_solution.py::TestSentenceChunker::test_returns_list PASSED    [ 33%]
tests/test_solution.py::TestSentenceChunker::test_single_sentence_max_gives_many_chunks PASSED [ 35%]
tests/test_solution.py::TestRecursiveChunker::test_chunks_within_size_when_possible PASSED [ 38%]
tests/test_solution.py::TestRecursiveChunker::test_empty_separators_falls_back_gracefully PASSED [ 40%]
tests/test_solution.py::TestRecursiveChunker::test_handles_double_newline_separator PASSED [ 42%]
tests/test_solution.py::TestRecursiveChunker::test_returns_list PASSED   [ 45%]
tests/test_solution.py::TestEmbeddingStore::test_add_documents_increases_size PASSED [ 47%]
tests/test_solution.py::TestEmbeddingStore::test_add_more_increases_further PASSED [ 50%]
tests/test_solution.py::TestEmbeddingStore::test_initial_size_is_zero PASSED [ 52%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_content_key PASSED [ 54%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_score_key PASSED [ 57%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_sorted_by_score_descending PASSED [ 59%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_at_most_top_k PASSED [ 61%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_list PASSED [ 64%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_non_empty PASSED [ 66%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_returns_string PASSED [ 69%]
tests/test_solution.py::TestComputeSimilarity::test_identical_vectors_return_1 PASSED [ 71%]
tests/test_solution.py::TestComputeSimilarity::test_opposite_vectors_return_minus_1 PASSED [ 73%]
tests/test_solution.py::TestComputeSimilarity::test_orthogonal_vectors_return_0 PASSED [ 76%]
tests/test_solution.py::TestComputeSimilarity::test_zero_vector_returns_0 PASSED [ 78%]
tests/test_solution.py::TestCompareChunkingStrategies::test_counts_are_positive PASSED [ 80%]
tests/test_solution.py::TestCompareChunkingStrategies::test_each_strategy_has_count_and_avg_length PASSED [ 83%]
tests/test_solution.py::TestCompareChunkingStrategies::test_returns_three_strategies PASSED [ 85%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_filter_by_department PASSED [ 88%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_no_filter_returns_all_candidates PASSED [ 90%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_returns_at_most_top_k PASSED [ 92%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_reduces_collection_size PASSED [ 95%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_false_for_nonexistent_doc PASSED [ 97%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_true_for_existing_doc PASSED [100%]

============================== 42 passed in 0.03s ==============================
```

**Số lượng bài test vượt qua (pass):** 42 / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế (Mock / Local) | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | Lập trình Python rất phổ biến trong AI. | Ngôn ngữ Python được sử dụng rộng rãi để xây dựng các mô hình trí tuệ nhân tạo. | Cao | -0.0565 / 0.8620 | Đúng (với Local) |
| 2 | Hôm nay trời nắng đẹp. | Thời tiết hôm nay có nắng và rất đẹp. | Cao | 0.0716 / 0.9549 | Đúng (với Local) |
| 3 | Tôi thích ăn phở bò. | Món ăn yêu thích của tôi là phở bò. | Cao | 0.1480 / 0.8769 | Đúng (với Local) |
| 4 | Học phí học kỳ này tăng nhẹ. | Thư viện trường mở cửa đến 9 giờ tối. | Thấp | 0.0928 / 0.2022 | Đúng (với Local) |
| 5 | Chú chó đang đuổi theo quả bóng. | Công nghệ blockchain đang thay đổi ngành tài chính. | Thấp | -0.2433 / -0.0245 | Đúng (với Local) |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> Kết quả bất ngờ nhất là các câu tương đồng về mặt ngữ nghĩa (như Cặp 1, 2, 3) có điểm similarity gần như bằng 0 (hoặc âm) khi dùng `MockEmbedder`. Điều này hoàn toàn dễ hiểu vì MockEmbedder sinh vector dựa trên MD5 hash của chuỗi văn bản (mang tính ngẫu nhiên), không đại diện cho ý nghĩa từ vựng. Trái lại, khi chuyển sang dùng `LocalEmbedder` (Sentence Transformers), điểm số của các cặp câu tương đồng về ngữ nghĩa tăng vọt lên trên 0.85, trong khi các câu không liên quan thì rất thấp (~0.20 hoặc dưới 0). Điều này chỉ ra rằng text embeddings thực sự lưu giữ thông tin ngữ nghĩa sâu sắc bằng cách ánh xạ các từ ngữ có liên quan vào các vùng gần nhau trong không gian vector đa chiều.

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân của bạn trong gói `src`. **5 câu hỏi này phải trùng với các thành viên cùng nhóm** (xem `REPORT_NHOM.md`).

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** __ / 5

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**
> *Viết 2-3 câu:*

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 10 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 5 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | 0 / 10 |
| **Tổng phần cá nhân** | **50 / 60** |


# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Nguyễn Duy Dũng  
**Nhóm:** Nhóm K3  
**Ngày:** 03/08/2026

> **Nộp 1 bản / sinh viên.** Phần nhóm nộp chung trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**  
Độ tương tự cosine cao nghĩa là hai vector biểu diễn hai văn bản có hướng gần giống nhau trong không gian embedding. Với text embeddings, điều này thường cho thấy hai đoạn văn có nội dung hoặc ý nghĩa gần nhau, dù có thể dùng từ ngữ khác nhau.

**Ví dụ có độ tương tự CAO:**
- Câu A: Sinh viên cần hoàn thành học phí trước hạn.
- Câu B: Người học phải nộp học phí đúng thời hạn quy định.
- Tại sao tương đồng: Hai câu cùng nói về nghĩa vụ nộp học phí đúng hạn.

**Ví dụ có độ tương tự THẤP:**
- Câu A: Sinh viên cần chứng chỉ ngoại ngữ để xét tốt nghiệp.
- Câu B: Thời tiết hôm nay có mưa lớn.
- Tại sao khác: Hai câu thuộc hai chủ đề hoàn toàn khác nhau, một câu nói về quy định học tập còn câu kia nói về thời tiết.

**Tại sao độ tương tự cosine được ưu tiên hơn khoảng cách Euclid cho text embeddings?**  
Cosine similarity tập trung vào hướng của vector, tức là quan hệ ngữ nghĩa, thay vì độ lớn tuyệt đối của vector. Điều này phù hợp với text embeddings vì hai văn bản có thể khác độ dài nhưng vẫn cùng ý nghĩa.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**  
Phép tính:

```text
số chunk = ceil((10000 - 50) / (500 - 50))
          = ceil(9950 / 450)
          = 23
```

Đáp án: **23 chunks**.

**Nếu overlap tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn overlap nhiều hơn?**  
Khi overlap = 100:

```text
số chunk = ceil((10000 - 100) / (500 - 100))
          = ceil(9900 / 400)
          = 25
```

Số chunk tăng từ 23 lên 25 vì bước nhảy giữa hai chunk nhỏ hơn. Overlap lớn hơn giúp giữ thêm ngữ cảnh ở ranh giới giữa các chunk, nhưng cũng làm tăng số lượng chunk và chi phí lưu trữ/tìm kiếm.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của tôi khi lập trình các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:  
Tôi dùng regex `(?<=[.!?])\s+` để tách câu tại khoảng trắng đứng sau dấu `.`, `!`, hoặc `?`, nhờ vậy vẫn giữ lại dấu câu trong nội dung. Sau khi tách, tôi loại bỏ câu rỗng và gom mỗi nhóm tối đa `max_sentences_per_chunk` câu thành một chunk. Trường hợp văn bản rỗng được xử lý bằng cách trả về danh sách rỗng.

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:  
Tôi triển khai chia đệ quy theo thứ tự separator `\n\n`, `\n`, `. `, `" "`, rồi cuối cùng là cắt cứng theo ký tự. Nếu đoạn hiện tại đã ngắn hơn hoặc bằng `chunk_size`, hàm trả về ngay đoạn đó làm một chunk. Nếu một phần sau khi tách vẫn quá dài, thuật toán tiếp tục gọi `_split` với separator kế tiếp để chia nhỏ hơn.

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:  
Tôi lưu mỗi `Document` thành một record trong bộ nhớ, gồm `id`, `content`, `metadata`, `embedding` và thứ tự thêm vào. Khi search, truy vấn được embed bằng cùng `embedding_fn`, sau đó tính điểm bằng dot product giữa query embedding và document embedding. Kết quả được sắp xếp giảm dần theo score và chỉ lấy tối đa `top_k`.

**`search_with_filter` + `delete_document`** — hướng tiếp cận:  
Với `search_with_filter`, tôi lọc metadata trước rồi mới chạy similarity search trên tập record đã lọc, giúp tránh trả về tài liệu sai đối tượng. Với `delete_document`, tôi xóa các record có `metadata["doc_id"]` hoặc `id` trùng với `doc_id` cần xóa, sau đó trả về `True` nếu số lượng record giảm.

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:  
Agent nhận câu hỏi, truy xuất top-k chunk liên quan từ `EmbeddingStore`, rồi ghép các chunk đó thành phần `Context` trong prompt. Prompt yêu cầu mô hình trả lời dựa trên context và nói không biết nếu context không đủ. Cuối cùng agent gọi `llm_fn(prompt)` để tạo câu trả lời.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```text
pytest tests/ -v
collected 42 items

tests/test_solution.py::TestProjectStructure::* PASSED
tests/test_solution.py::TestClassBasedInterfaces::* PASSED
tests/test_solution.py::TestFixedSizeChunker::* PASSED
tests/test_solution.py::TestSentenceChunker::* PASSED
tests/test_solution.py::TestRecursiveChunker::* PASSED
tests/test_solution.py::TestEmbeddingStore::* PASSED
tests/test_solution.py::TestKnowledgeBaseAgent::* PASSED
tests/test_solution.py::TestComputeSimilarity::* PASSED
tests/test_solution.py::TestCompareChunkingStrategies::* PASSED
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::* PASSED
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::* PASSED

42 passed
```

**Số lượng bài test vượt qua (pass):** 42 / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

Kết quả thực tế dưới đây được chạy bằng `_mock_embed`, nên điểm số chỉ dùng để kiểm tra hàm `compute_similarity`, không phản ánh đầy đủ quan hệ ngữ nghĩa tiếng Việt. Vì vậy cột "Đúng?" được hiểu theo hai lớp: đúng với trực giác ngữ nghĩa của tôi hay đúng với điểm mock thực tế.

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | Sinh viên nộp học phí đúng hạn. | Sinh viên phải hoàn thành học phí theo thông báo. | cao | 0.0556 | Đúng về ngữ nghĩa, mock cho điểm thấp |
| 2 | CPA thấp có thể bị cảnh báo học tập. | Điểm trung bình tích lũy dưới ngưỡng sẽ bị cảnh báo. | cao | 0.0553 | Đúng về ngữ nghĩa, mock cho điểm thấp |
| 3 | Sinh viên cần chứng chỉ ngoại ngữ để xét tốt nghiệp. | IELTS hoặc TOEIC có thể dùng cho chuẩn đầu ra. | cao | -0.0904 | Đúng về ngữ nghĩa, mock không phản ánh tốt |
| 4 | Học bổng yêu cầu kết quả học tập và rèn luyện tốt. | Sinh viên khuyết tật có thể được hỗ trợ học phí. | trung bình/thấp | 0.1756 | Sai theo mock, vì mock cho điểm cao nhất |
| 5 | Thư viện cho mượn tài liệu. | Trời hôm nay có mưa lớn. | thấp | -0.0768 | Đúng |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**  
Kết quả bất ngờ nhất là cặp 4 có điểm cao nhất dù hai câu không cùng nội dung chính. Điều này cho thấy mock embedding không thật sự hiểu nghĩa, mà chỉ tạo vector xác định để kiểm thử code. Vì vậy phần dự đoán của tôi hợp lý về mặt ngữ nghĩa, nhưng kết quả số từ mock có thể lệch; khi đánh giá retrieval nghiêm túc, cần dùng local multilingual embedder hoặc một embedding model thật.

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Tôi chạy benchmark trên corpus `data/quy_che_dao_tao_hust` với strategy cá nhân:

```text
RecursiveChunker(chunk_size=400)
Embedding backend: mock embeddings fallback
Số chunk đã nạp: 27
```

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Sinh viên nộp học phí muộn so với quy định sẽ bị xử lý như thế nào? | `k3-ngoai-ngu`, chunk 2: nội dung về phân lớp tiếng Anh và miễn học ngoại ngữ cơ bản. | 0.2799 | Không | Agent dựa vào context sai nên chưa trả lời đúng trọng tâm học phí nộp muộn. |
| 2 | CPA tối thiểu để sinh viên không bị cảnh báo học tập là bao nhiêu? | `k3-ngoai-ngu`, chunk 1: nội dung về chuẩn đầu vào ngoại ngữ. | 0.2164 | Không | Agent nhận context ngoại ngữ nên không trả lời đúng ngưỡng CPA cảnh báo học tập. |
| 3 | Sinh viên K70 cần đạt chuẩn đầu ra ngoại ngữ tương đương IELTS bao nhiêu để đủ điều kiện xét tốt nghiệp? | `k3-sv-khuyet-tat`, chunk 5: nội dung về quy trình nộp hồ sơ hỗ trợ sinh viên khuyết tật. | 0.2678 | Không | Agent bị cung cấp context sai, không nêu đúng IELTS 5.0 hoặc yêu cầu ELITECH cao hơn. |
| 4 | Điều kiện tối thiểu về điểm học tập và rèn luyện để đạt học bổng Khuyến khích học tập loại Khá là gì? | `k3-ngoai-ngu`, chunk 1: nội dung về chuẩn đầu vào ngoại ngữ. | 0.2088 | Không ở top-1; top-3 có chunk liên quan | Agent chưa trả lời đúng điều kiện CPA và rèn luyện vì chunk học bổng chỉ xuất hiện ở hạng 3. |
| 5 | Sinh viên khuyết tật có được miễn giảm học phí không? | `k3-hoc-phi`, chunk 0: nội dung chung về quy định học phí 2025-2026. | 0.2640 | Không | Agent lấy context học phí chung; top-3 không chứa đúng chunk về miễn 100% học phí cho sinh viên khuyết tật nặng thuộc hộ nghèo/cận nghèo. |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** 1 / 5

Chỉ câu 4 có chunk chứa thông tin gold answer trong top-3, nhưng chunk đó đứng hạng 3 chứ không phải top-1. Các câu còn lại trả về chunk đúng chủ đề rất yếu hoặc sai chủ đề, nên agent không có đủ context để trả lời chính xác.

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**  
Tôi thấy việc giữ nguyên corpus, query và embedding backend là rất quan trọng để so sánh chunking strategy công bằng. Ngoài ra, metadata filter giúp kiểm soát đối tượng tài liệu tốt hơn, nhưng filter chỉ hiệu quả khi corpus có metadata đủ phân biệt và embedding/ranking đủ tốt để đưa chunk đúng lên cao.

**Phân tích lỗi ngắn:**  
Failure case rõ nhất là câu hỏi về chuẩn đầu ra ngoại ngữ nhưng top-1 lại là chunk quy trình hỗ trợ sinh viên khuyết tật. Nguyên nhân chính là benchmark hiện dùng mock embedding, không hiểu quan hệ ngữ nghĩa tiếng Việt, nên score gần như không phản ánh đúng nội dung. Nếu làm tiếp, tôi sẽ chạy lại bằng `EMBEDDING_PROVIDER=local`, thử chunk theo heading/điều khoản để giữ tiêu đề trong từng chunk, và so sánh với `RecursiveChunker(chunk_size=400)`.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 10 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 5 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | 2 / 10 |
| **Tổng phần cá nhân** | **52 / 60** |


# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Ong Xuân Sơn
**Nhóm:** 6 Tuất
**Ngày:** 03/08/2026

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**
> Độ tương tự cosine cao nghĩa là hai vector embedding có hướng gần giống nhau, tức là hai đoạn văn bản có nội dung hoặc ý nghĩa gần nhau. Trong bài toán retrieval, câu hỏi và chunk có cosine similarity cao thường là dấu hiệu chunk đó có khả năng chứa thông tin liên quan.

**Ví dụ có độ tương tự CAO:**
- Câu A: Sinh viên phải hoàn thành học phí trước thời hạn do nhà trường thông báo.
- Câu B: Người học cần nộp học phí đúng hạn theo thông báo của trường.
- Tại sao tương đồng: Hai câu dùng từ khác nhau nhưng cùng nói về nghĩa vụ đóng học phí đúng hạn của sinh viên.

**Ví dụ có độ tương tự THẤP:**
- Câu A: Sinh viên được xét học bổng dựa trên kết quả học tập và rèn luyện.
- Câu B: Thư viện mở cửa từ thứ Hai đến thứ Sáu hằng tuần.
- Tại sao khác: Hai câu thuộc hai chủ đề khác nhau: một câu nói về học bổng, câu còn lại nói về lịch hoạt động thư viện.

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
> Cosine si/milarity tập trung vào hướng của vector thay vì độ lớn tuyệt đối, nên phù hợp để so sánh mức độ giống nhau về ng/ữ nghĩa giữa các văn bản. Với text embeddings, hai câu có thể có độ dài hoặc độ lớn vector khác nhau nhưng vẫn cùng ý nghĩa, vì vậy cosine thường ổn định hơn Euclidean distance.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> *Trình bày phép tính:* Bước nhảy giữa hai chunk là `chunk_size - overlap = 500 - 50 = 450`. Số lượng chunk được tính theo công thức `ceil((10000 - 50) / (500 - 50)) = ceil(9950 / 450) = ceil(22.11)`.
> *Đáp án:* Cần khoảng **23 chunks**.

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**
> Khi `overlap=100`, bước nhảy là `500 - 100 = 400`, nên số chunk là `ceil((10000 - 100) / (500 - 100)) = ceil(9900 / 400) = 25 chunks`. Overlap lớn hơn làm tăng số chunk nhưng giúp giữ ngữ cảnh giữa hai chunk liền kề, giảm nguy cơ cắt mất ý quan trọng ở ranh giới chunk.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi lập trình (implement) các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:
> Tôi dùng regex `(?<=[.!?])\s+` để tách văn bản tại khoảng trắng đứng sau các dấu kết thúc câu như `.`, `!`, `?`. Sau khi tách, tôi loại bỏ khoảng trắng thừa và bỏ các câu rỗng, rồi gom tối đa `max_sentences_per_chunk` câu vào một chunk. Trường hợp văn bản rỗng hoặc chỉ có khoảng trắng được xử lý bằng cách trả về danh sách rỗng.

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
> Tôi triển khai chia đệ quy theo thứ tự separator từ lớn đến nhỏ: đoạn văn `\n\n`, dòng `\n`, câu `. `, từ `" "`, rồi cuối cùng là cắt cứng theo ký tự. Base case là khi đoạn hiện tại đã ngắn hơn hoặc bằng `chunk_size`, hàm trả về đoạn đó sau khi `strip()`. Nếu một separator không xuất hiện trong văn bản hoặc một phần sau khi cắt vẫn quá dài, hàm tiếp tục gọi `_split()` với separator tiếp theo.

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:
> Tôi lưu dữ liệu bằng in-memory store, mỗi record gồm `id`, `content`, `metadata` và `embedding` được sinh từ `embedding_fn`. Khi thêm tài liệu, tôi chuẩn hóa metadata và tự gắn `doc_id` nếu chưa có để tiện truy vết. Khi tìm kiếm, query được embed rồi so sánh với từng embedding trong store bằng cosine similarity, sau đó sắp xếp giảm dần theo `score` và lấy `top_k`.

**`search_with_filter` + `delete_document`** — hướng tiếp cận:
> Với `search_with_filter`, tôi lọc metadata trước để chỉ giữ lại các record thỏa mãn toàn bộ điều kiện, rồi mới chạy similarity search trên tập đã lọc. Cách này giúp giảm nhiễu khi câu hỏi cần giới hạn theo phòng ban, ngôn ngữ hoặc loại tài liệu. Với `delete_document`, tôi tạo lại danh sách store bằng cách loại bỏ mọi record có `metadata["doc_id"]` hoặc `id` trùng với `doc_id` cần xóa, rồi trả về `True` nếu số lượng record giảm.

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
> Tôi triển khai `KnowledgeBaseAgent.answer` theo mẫu RAG: đầu tiên gọi `store.search()` để lấy top-k chunk liên quan nhất, sau đó ghép các chunk này thành phần `Context` trong prompt. Prompt gồm hướng dẫn trả lời dựa trên context, danh sách chunk được đánh số, câu hỏi của người dùng và nhãn `Answer:`. Cuối cùng agent gọi `llm_fn(prompt)` để sinh câu trả lời dựa trên ngữ cảnh đã truy xuất.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```
pytest tests/ -v
==================================================== test session starts =====================================================
platform win32 -- Python 3.13.9, pytest-9.1.1, pluggy-1.5.0 -- C:\Users\Admin\miniconda3\python.exe
rootdir: C:\Users\Admin\Desktop\AITHUCCHIEN\LABS\DAY07_2A202601327_OngXuanSon
collected 42 items

tests/test_solution.py::TestProjectStructure::test_root_main_entrypoint_exists PASSED
tests/test_solution.py::TestProjectStructure::test_src_package_exists PASSED
tests/test_solution.py::TestClassBasedInterfaces::test_chunker_classes_exist PASSED
tests/test_solution.py::TestClassBasedInterfaces::test_mock_embedder_exists PASSED
tests/test_solution.py::TestFixedSizeChunker::* PASSED
tests/test_solution.py::TestSentenceChunker::* PASSED
tests/test_solution.py::TestRecursiveChunker::* PASSED
tests/test_solution.py::TestEmbeddingStore::* PASSED
tests/test_solution.py::TestKnowledgeBaseAgent::* PASSED
tests/test_solution.py::TestComputeSimilarity::* PASSED
tests/test_solution.py::TestCompareChunkingStrategies::* PASSED
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::* PASSED
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::* PASSED

===================================================== 42 passed in 0.13s =====================================================
```

**Số lượng bài test vượt qua (pass):** 42 / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | Sinh viên phải nộp học phí đúng hạn. | Người học cần hoàn thành học phí theo thông báo của trường. | cao | 0.2241 | Đúng |
| 2 | Sinh viên cần đạt chuẩn ngoại ngữ để xét tốt nghiệp. | Người học phải có chứng chỉ tiếng Anh phù hợp trước khi tốt nghiệp. | cao | 0.1478 | Đúng |
| 3 | Học bổng được xét dựa trên kết quả học tập và rèn luyện. | Sinh viên có thành tích tốt có thể được nhận học bổng. | cao | 0.1102 | Đúng |
| 4 | Thư viện mở cửa từ thứ Hai đến thứ Sáu. | Sinh viên bị cảnh báo học tập nếu CPA quá thấp. | thấp | -0.1217 | Đúng |
| 5 | Sinh viên khuyết tật có thể được hỗ trợ học phí. | Chương trình đào tạo kỹ sư thường kéo dài 5 năm. | thấp | 0.0301 | Sai |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> Kết quả bất ngờ nhất là cặp 5: tôi dự đoán thấp vì hai câu nói về hai chủ đề khác nhau, nhưng điểm thực tế lại dương nhẹ. Điều này cho thấy với mock embedding, điểm similarity chỉ có tính xác định để phục vụ test chứ chưa phản ánh tốt quan hệ ngữ nghĩa thật của tiếng Việt. Khi đánh giá retrieval nghiêm túc, nên dùng local multilingual embedder thay vì mock embedding.

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân của bạn trong gói `src`. **5 câu hỏi này phải trùng với các thành viên cùng nhóm** (xem `REPORT_NHOM.md`).

Chiến lược tôi dùng: `FixedSizeChunker(chunk_size=400, overlap=50)` kết hợp `search_with_filter()` theo metadata phù hợp (`department` hoặc `audience`). Embedder dùng trong lần chạy này là `_mock_embed`, nên score có tính tham khảo và tôi đánh giá chất lượng chủ yếu dựa trên việc top-3 có chứa chunk đúng nguồn hay không.

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Sinh viên nộp học phí muộn so với quy định sẽ bị xử lý như thế nào? | `k3-hoc-phi::chunk_1` - nội dung về mức học phí và cách tính học phí theo tín chỉ. | 0.3080 | Có | Sinh viên nộp muộn có thể bị hạn chế quyền lợi học tập, không được dự thi cuối kỳ hoặc bị xử lý theo quy chế công tác sinh viên. |
| 2 | Điểm trung bình tích lũy CPA tối thiểu để sinh viên không bị cảnh báo học tập là bao nhiêu? | `k3-hoc-phi::chunk_4` - nội dung về thời hạn đóng học phí và xử lý nộp chậm. | 0.2866 | Không | Câu trả lời đúng nằm trong top-3: sinh viên bị cảnh báo nếu CPA dưới 1.0 sau HK1 hoặc dưới 1.2 sau HK2; vì vậy cần đạt ít nhất các ngưỡng này theo giai đoạn. |
| 3 | Sinh viên K70 cần đạt chuẩn đầu ra ngoại ngữ tương đương IELTS bao nhiêu để đủ điều kiện xét tốt nghiệp? | `k3-ngoai-ngu::chunk_1` - nội dung về TOEIC 500/IELTS 5.0 và quy đổi học phần ngoại ngữ. | 0.1447 | Có | Chương trình chuẩn yêu cầu TOEIC 500 hoặc tương đương IELTS 5.0; một số chương trình ELITECH yêu cầu cao hơn, khoảng IELTS 6.0. |
| 4 | Điều kiện tối thiểu về điểm học tập và rèn luyện để đạt học bổng Khuyến khích học tập loại Khá là gì? | `k3-sv-khuyet-tat::chunk_1` - nội dung về đối tượng sinh viên khuyết tật và hỗ trợ tài chính. | 0.0988 | Không | Câu trả lời đúng nằm trong top-3: học bổng loại Khá yêu cầu CPA kỳ từ 2.5 trở lên, rèn luyện Khá, không có môn điểm F và không bị kỷ luật. |
| 5 | (Lọc metadata: `audience=student`) Sinh viên khuyết tật có được miễn giảm học phí không? | `k3-hoc-phi::chunk_3` - nội dung về học phí chương trình liên kết quốc tế. | 0.1263 | Không | Câu trả lời đúng nằm trong top-3: sinh viên khuyết tật nặng hoặc đặc biệt nặng thuộc hộ nghèo/cận nghèo được miễn 100% học phí và có thể được hỗ trợ học tập khác. |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** 5 / 5

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**
> Tôi thấy metadata filtering giúp cải thiện đáng kể độ chính xác top-3, đặc biệt khi corpus có nhiều tài liệu cùng nhắc đến các từ như "học phí", "sinh viên", "điều kiện". Tuy nhiên, top-1 vẫn có thể sai khi dùng mock embedding, nên khi so sánh nghiêm túc cần dùng local multilingual embedder và thử nhiều cấu hình chunking khác nhau.

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
