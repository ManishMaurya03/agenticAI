import time
from reranker import CrossEncoderReranker
from context_compressor import compress_context
from langchain_openai import ChatOpenAI

reranker = CrossEncoderReranker()
rewriter_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def rewrite_query(user_query: str) -> str:
    prompt = f"""
Rewrite the following question into an enterprise policy search query.

Question: {user_query}

Return only the rewritten query.
"""
    return rewriter_llm.invoke(prompt).content.strip()


def build_context(retriever, query):
    start = time.time()

    rewritten_query = rewrite_query(query)
    print("Rewritten Query:", rewritten_query)

    # 1️⃣ Retrieve for recall
    docs = retriever.invoke(rewritten_query)
    print(f"Retrieved {len(docs)} candidate chunks")

    # 2️⃣ Rerank for precision
    reranked_docs = reranker.rerank(rewritten_query, docs, top_k=3)

    print("=== Reranked Chunks ===")
    for d in reranked_docs:
        print(d.page_content[:200])

    # 3️⃣ Context Compression (NEW)
    compressed_chunks = compress_context(query, reranked_docs)

    print("=== Compressed Context ===")
    for c in compressed_chunks:
        print(c)

    final_context = "\n\n".join(compressed_chunks)

    retrieval_time = time.time() - start
    return final_context, retrieval_time