import os
from ingest import build_knowledge_base
from src.chunking import SentenceChunker, RecursiveChunker
from src.agent import KnowledgeBaseAgent
from src.embeddings import _mock_embed, LocalEmbedder, OpenAIEmbedder
from dotenv import load_dotenv

load_dotenv(override=False)

# Cấu hình embedder
provider = os.getenv("EMBEDDING_PROVIDER", "mock").strip().lower()
if provider == "local":
    embedder = LocalEmbedder(model_name=os.getenv("LOCAL_EMBEDDING_MODEL", "all-MiniLM-L6-v2"))
elif provider == "openai":
    embedder = OpenAIEmbedder()
else:
    embedder = _mock_embed

def demo_llm(prompt: str) -> str:
    preview = prompt[:150].replace("\n", " ")
    return f"[DEMO LLM] Generated answer from prompt: {preview}..."

# 1. Chọn chunker của riêng bạn (Anh/chị đang chọn SentenceChunker)
# chunker = RecursiveChunker(chunk_size=400)
chunker = SentenceChunker(max_sentences_per_chunk=3)

print(f"=== Đang nạp dữ liệu bằng chiến lược: {chunker.__class__.__name__} ===")

# 2. Nạp cả thư mục corpus (Chỉ nạp 1 lần duy nhất để tối ưu)
data_dir = "data/k3_hust"
store = build_knowledge_base(data_dir, embedding_fn=embedder, chunker=chunker)
print(f"Đã nạp tổng cộng {store.get_collection_size()} chunks vào hệ thống.\n")

agent = KnowledgeBaseAgent(store=store, llm_fn=demo_llm)

# 3. Chạy 5 query đã chốt (Câu 5 có sử dụng bộ lọc audience=student)
queries = [
    ("Sinh viên nộp học phí muộn so với quy định sẽ bị xử lý như thế nào?", None),
    ("Điểm trung bình tích lũy (CPA) tối thiểu để sinh viên không bị cảnh báo học tập là bao nhiêu?", None),
    ("Sinh viên K70 cần đạt chuẩn đầu ra ngoại ngữ tương đương IELTS bao nhiêu để đủ điều kiện xét tốt nghiệp?", None),
    ("Điều kiện tối thiểu về điểm học tập và rèn luyện để đạt học bổng Khuyến khích học tập loại Khá là gì?", None),
    ("Sinh viên khuyết tật có được miễn giảm học phí không?", {"audience": "student"})
]

for i, (q, filter_dict) in enumerate(queries, 1):
    print(f"{'='*60}\nCÂU HỎI {i}: {q}")
    if filter_dict:
        print(f"(Có dùng bộ lọc Metadata: {filter_dict})")
        results = store.search_with_filter(q, top_k=3, metadata_filter=filter_dict)
    else:
        results = store.search(q, top_k=3)
        
    print("--- TOP 3 CHUNKS TRUY XUẤT ĐƯỢC ---")
    for idx, r in enumerate(results, 1):
        doc_id = r.get("metadata", {}).get("doc_id", "unknown")
        print(f"  [{idx}] score={r.get('score', 0):.3f} | doc_id={doc_id}")
        print(f"      Preview: {r['content'][:120].replace(chr(10), ' ')}...")
        
    print("\n--- CÂU TRẢ LỜI CỦA AGENT ---")
    print(agent.answer(q, top_k=3, metadata_filter=filter_dict))
    print("\n")
