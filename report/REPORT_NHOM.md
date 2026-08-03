# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store

**Nhóm:** sixtuat

**Thành viên:** 
- Vũ Hải Nam - 2A202601173
- Giang Minh Phú - 2A202601729
- Nguyễn Tiến Thành - 2A202601539
- Nguyễn Minh Nhật - 2A202601131
- Nguyễn Duy Dũng - 2A202601505
- Ong Xuân Sơn - 2A202601327

**Ngày:** 03/08/2026

> **Nộp 1 bản / nhóm.** Phần cá nhân (hướng tiếp cận, kết quả riêng, dự đoán…) mỗi thành viên nộp riêng trong `REPORT_CANHAN.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần nhóm: 40** = Lựa chọn tài liệu (10) + Thiết kế chiến lược (15) + Chất lượng truy xuất (10) + Thuyết trình (5).

---

## 1. Lựa chọn tài liệu (Document Set Quality) — Nhóm (10 điểm)

### Phạm vi bộ tài liệu (Scope)

**Chủ đề (cố định theo lớp K3):** Dịch vụ / quy định đại học (đăng ký môn, học phí, học bổng, thư viện, ký túc xá…).

**Phạm vi cụ thể nhóm tập trung:**
> Tập trung vào các quy chế học vụ (đào tạo, ngoại ngữ), chính sách tài chính (học phí, học bổng) và hỗ trợ sinh viên khuyết tật tại ĐH Bách Khoa Hà Nội.

### Danh sách tài liệu (Data Inventory)

| # | Tên tài liệu | Nguồn (Source URL) | Ngày lấy / Phiên bản | Số ký tự | Metadata đã gán |
|---|--------------|------------|--------------------|----------|-----------------|
| 1 | Quy định học phí 2025-2026 | https://ctt.hust.edu.vn/.../QD%20HOC%20PHI%20-%202025-2026-final.pdf | 2026-08-03 | ~3500 | audience: student, department: academic-affairs |
| 2 | Quy chế đào tạo đại học | https://ctt.hust.edu.vn/.../QCDT_2025_5445_QD-DHBK.pdf | 2026-08-03 | ~5000 | audience: faculty, department: academic-affairs |
| 3 | Quy định học bổng | https://husteduvn-my.sharepoint.com/.../ESCBPVQlzNFOlglsvRwxAZYBqxdZc6QR_f9Y2TuGC2IiSA?e=Pszv9k | 2026-08-03 | ~4200 | audience: student, department: student-affairs |
| 4 | Quy định ngoại ngữ từ K70 | https://ctt.hust.edu.vn/.../06_%20Quy%20%C4%91%E1%BB%8Bnh%20ngo%E1%BA%A1i%20ng%E1%BB%AF%20t%E1%BB%AB%20K70_ch%C3%ADnh%20quy_final.pdf | 2026-08-03 | ~3000 | audience: student, department: academic-affairs |
| 5 | Chính sách hỗ trợ sinh viên khuyết tật | https://drive.google.com/file/d/1oALudWB-XEWPjGe6ynKZ2Zi-SldikVSt/view?usp=sharing | 2026-08-03 | ~2500 | audience: student, department: student-affairs |

**Danh sách kiểm tra quản trị dữ liệu (Data governance checklist):**
- [x] Tập tài liệu (Corpus) chỉ chứa nguồn công khai/được phép dùng và không chứa dữ liệu cá nhân, thông tin đăng nhập hoặc tài liệu nội bộ.
- [x] Mỗi tài liệu có `source_url`, `retrieved_at`, `document_version` (hoặc ngày hiệu lực) trong metadata.

### Cấu trúc Metadata (Metadata Schema)

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho truy xuất (retrieval)? |
|----------------|------|---------------|-------------------------------|
| audience | string | student | Giúp phân biệt tài liệu dành cho sinh viên so với giảng viên (VD: học phí, học bổng). |
| department | string | academic-affairs | Giúp lọc nhanh tài liệu theo phòng ban (Phòng Đào tạo, Phòng CTSV...). |

---

## 2. Thiết kế chiến lược (Strategy Design) — Nhóm (15 điểm)

### Phân tích đường cơ sở (Baseline Analysis)

| Tài liệu | Chiến lược (Strategy) | Số lượng Chunk | Độ dài trung bình | Giữ được ngữ cảnh không? |
|-----------|----------|-------------|------------|-------------------|
| k3-ngoai-ngu.md | FixedSizeChunker (`fixed_size`) | 16 | 200.5 | Kém (Hay bị cắt đứt giữa câu hoặc bảng biểu) |
| k3-ngoai-ngu.md | SentenceChunker (`by_sentences`) | 8 | 420.2 | Tốt hơn (Giữ trọn câu), nhưng dễ gom nhầm nếu câu ngắn |
| k3-ngoai-ngu.md | RecursiveChunker (`recursive`) | 12 | 260.4 | Khá tốt (Cắt theo đoạn `\n\n` tự nhiên) |
| k3-ngoai-ngu.md | HeadingChunker (`heading`) | 5 | 850.0 | Tốt nhất (Giữ nguyên vẹn cấu trúc logic của Điều/Khoản) |

### Chiến lược của từng thành viên

**Thành viên 1 — Vũ Hải Nam**
- **Loại chiến lược:** SentenceChunker (max_sentences_per_chunk=3)
- **Mô tả & lý do chọn:** Văn bản quy định thường có câu dài chứa nhiều điều kiện. Cắt theo câu giúp trọn vẹn ý nghĩa ngữ pháp của điều khoản.
- **Code snippet:** regex `[^.!?]+[.!?]*` tách theo câu.

**Thành viên 2 — Nguyễn Tiến Thành**
- **Loại chiến lược:** HeadingChunker (max_chars=900, overlap=120)
- **Mô tả & lý do chọn:** Quy định Bách Khoa thường cấu trúc chặt chẽ theo từng Điều, Mục. Việc tách bằng regex dựa trên Heading Markdown đảm bảo một đoạn điều khoản không bao giờ bị xé lẻ.
- **Code snippet:** Tùy biến `HeadingChunker` cắt theo tiêu đề markdown `##`.

**Thành viên 3 — Nguyễn Duy Dũng**
- **Loại chiến lược:** RecursiveChunker (chunk_size=400)
- **Mô tả & lý do chọn:** Tách đệ quy tự nhiên theo cấu trúc xuống dòng `\n\n`, `\n`, tránh cắt ngang đoạn và duy trì sự liền mạch tốt hơn cắt chữ cố định.

**Thành viên 4 — Ong Xuân Sơn**
- **Loại chiến lược:** FixedSizeChunker (chunk_size=400, overlap=50)
- **Mô tả & lý do chọn:** Cách tiếp cận cơ bản nhưng đảm bảo độ dài chunk đồng đều để test độ nhạy của Mock Embedder.
- **Code snippet:** Trượt cửa sổ văn bản với bước nhảy `chunk_size - overlap`.

**Thành viên 5 & 6 — Giang Minh Phú, Nguyễn Minh Nhật**
- **Loại chiến lược:** RecursiveChunker & SentenceChunker
- **Mô tả & lý do chọn:** Phối hợp thử nghiệm đệ quy và tách câu linh hoạt để theo dõi độ biến thiên của Mock Embedder.

### So Sánh Giữa Các Thành Viên

| Thành viên | Chiến lược (Strategy) | Điểm truy xuất (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| Tiến Thanh | HeadingChunker | 10/10 | Giữ chuẩn cấu trúc Điều/Khoản của HUST, truy xuất thông tin rất đầy đủ. | Phải code regex phức tạp để bắt chính xác heading, tốn kém tài nguyên. |
| Hải Nam | SentenceChunker | 10/10 | Không bị đứt gãy câu chữ giữa chừng. | Câu quá dài sẽ vượt quá token LLM, câu ngắn bị nhiễu. |
| Xuân Sơn | FixedSizeChunker | 10/10 | Kích thước đều đặn, dễ tính toán số lượng. | Hay cắt ngang câu và bảng biểu khiến LLM bị mất ngữ cảnh (ảo giác). |
| Duy Dũng | RecursiveChunker | 2/10 | Linh hoạt cắt theo cấu trúc đoạn văn. | Mock Embedder đôi khi vẫn chấm điểm thấp cho đoạn liên quan. |

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**
> Đối với văn bản hành chính HUST (như quy chế), chiến lược **Heading/Section-based Chunker** (của Nguyễn Tiến Thanh) là tốt nhất. Lý do là mỗi "Điều" hay "Khoản" đều mang một khối ngữ nghĩa trọn vẹn. Cắt theo các ranh giới này giúp Agent luôn đọc được đầy đủ vế điều kiện "Nếu... thì..." mà không bị mất mát do bị chặt đôi giữa chừng.

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### Câu hỏi đánh giá & Câu trả lời chuẩn (nhóm thống nhất)

| # | Câu hỏi (Query) | Câu trả lời chuẩn (Gold Answer) | Chunk nào chứa thông tin? |
|---|-------|-------------------------------|--------------------------|
| 1 | Sinh viên nộp học phí muộn so với quy định sẽ bị xử lý như thế nào? | Có thể bị hủy đăng ký môn học hoặc không được dự thi. | k3-hoc-phi |
| 2 | Điểm trung bình tích lũy (CPA) tối thiểu để sinh viên không bị cảnh báo học tập là bao nhiêu? | Phụ thuộc vào số tín chỉ hoặc số học kỳ, VD: không dưới 1.0 cho HK1, <1.2 cho HK2. | k3-quy-che-dao-tao |
| 3 | Sinh viên K70 cần đạt chuẩn đầu ra ngoại ngữ tương đương IELTS bao nhiêu để đủ điều kiện xét tốt nghiệp? | TOEIC 500 hoặc IELTS 5.0 - 5.5 tùy hệ. ELITECH có thể yêu cầu IELTS 6.0. | k3-ngoai-ngu |
| 4 | Điều kiện tối thiểu về điểm học tập và rèn luyện để đạt học bổng Khuyến khích học tập loại Khá là gì? | CPA kỳ từ 2.5 trở lên và ĐRL từ Khá trở lên. | k3-hoc-bong |
| 5 | (Lọc metadata: audience=student) Sinh viên khuyết tật có được miễn giảm học phí không? | Khuyết tật nặng/đặc biệt nặng thuộc hộ nghèo/cận nghèo được miễn 100% học phí. | k3-sv-khuyet-tat |

### Tổng hợp chất lượng truy xuất của nhóm

| # | Câu hỏi | Chiến lược tốt nhất cho câu này | Có chunk liên quan trong top-3? | Ghi chú |
|---|---------|-------------------------------|-------------------------------|---------|
| 1 | Học phí nộp muộn | SentenceChunker (Hải Nam) | Có (Top 1) | Điểm cosine cao (0.89), câu trả lời đi thẳng vào vấn đề hủy đăng ký môn học. |
| 2 | CPA cảnh báo | HeadingChunker (Tiến Thanh) | Có (Top 1) | Lấy được trọn vẹn Chương IV về Cảnh báo học tập (Score: 0.49). |
| 3 | IELTS K70 | SentenceChunker (Hải Nam) | Có (Top 1) | Bắt trúng câu có chứa "TOEIC 500" và "IELTS 5.0" (Score: 0.88). |
| 4 | Học bổng Khá | HeadingChunker (Tiến Thanh) | Có (Top 2) | Chunk điều kiện nằm ở top 2, nhưng ngữ cảnh rất nguyên vẹn do lấy theo Điều 1. |
| 5 | SV Khuyết tật | Mọi chiến lược | Có (Top 1) | Với việc áp dụng filter, kết quả được focus chuẩn xác vào file chính sách (Score ~ 0.92). |

**Lọc bằng metadata có giúp ích không? Ở câu hỏi nào?**
> Bộ lọc cực kỳ hữu ích ở Câu 5 (Sinh viên khuyết tật). Bằng cách dùng filter `{"audience": "student"}`, hệ thống chỉ tập trung đúng vào quy định hỗ trợ sinh viên thay vì truy xuất nhầm vào quy chế dành cho giảng viên hay học phí liên kết quốc tế, giúp agent không bị lẫn lộn (hallucinate).

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

**Những phân tích (insights) hay nhất nhóm sẽ trình bày:**
> - **RAG không thần thánh:** Score Cosine cao chưa chắc đã là đoạn chứa đáp án đúng (có khi chỉ là trùng lặp từ khóa chủ đề, đặc biệt khi dùng MockEmbedder).
> - **Tầm quan trọng của Chunking:** Với văn bản pháp quy, việc cắt đứt một câu "Nếu... thì..." sẽ dẫn đến thảm họa LLM trả lời sai hoàn toàn. HeadingChunker là chân ái của pháp lý.
> - **Sức mạnh của Metadata:** Metadata filter giúp thu hẹp không gian tìm kiếm, tăng độ chính xác lên gấp nhiều lần so với chỉ dùng Vector Search thuần.

**Bài học rút ra khi so sánh trong nhóm:**
> Cùng một tài liệu, cùng 5 query, nhưng chiến lược FixedSize cho kết quả tệ nhất vì nó vô tình cắt ngang câu và bảng biểu. Trong khi đó, việc đầu tư viết một HeadingChunker phức tạp lại cho kết quả Retrieval điểm 10 vì nó giữ nguyên vẹn cấu trúc logic Điều/Mục của văn bản. Ngoài ra, Mock Embedding không thực sự hiểu ngữ nghĩa, chỉ mang tính chất test code.

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**
> Nhóm sẽ thực hiện thêm bước *Data Cleaning* mạnh tay hơn: thay thế các bảng biểu phức tạp trong PDF thành dạng text tuần tự hoặc Markdown Table chuẩn để mô hình dễ đọc. Ngoài ra, nhóm sẽ nâng cấp từ Mock Embedder lên Local Embedder (Sentence Transformers) thực thụ để cải thiện khả năng nắm bắt ngữ nghĩa tiếng Việt.

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Lựa chọn tài liệu (Document Set Quality) | 10 / 10 |
| Thiết kế chiến lược (Strategy Design) | 15 / 15 |
| Chất lượng truy xuất (Retrieval Quality) | 10 / 10 |
| Thuyết trình (Demo) | 5 / 5 |
| **Tổng phần nhóm** | **40 / 40** |
