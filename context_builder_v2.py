import time
from typing import List, Tuple

from langchain_openai import ChatOpenAI
from langchain_core.documents import Document

from reranker import CrossEncoderReranker
from context_compressor import compress_context


# =====================================================
# Models
# =====================================================

# Cheap + deterministic LLM for query rewrite
QUERY_REWRITER_LLM = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# Cross-encoder reranker (local model)
reranker = CrossEncoderReranker()


# =====================================================
# Query Rewrite
# =====================================================
def rewrite_query(user_query: str) -> str:
    """
    Rewrite user question into enterprise-policy-friendly search query.
    IMPORTANT:
    - Use policy-style vocabulary.
    """
    prompt = f"""
Rewrite the following question into a precise enterprise policy search query.

Rules:
- Use terms commonly found in policy documents.
- Keep it short and specific.

Question:
{user_query}

Return ONLY the rewritten query.
"""
    return QUERY_REWRITER_LLM.invoke(prompt).content.strip()


# =====================================================
# Context Builder
# =====================================================
def build_contexts(
    retriever,
    user_query: str,
    rerank_top_k: int = 3
) -> Tuple[str, str, float]:
    """
    Builds both RAW and COMPRESSED context for the given query.

    Returns:
        raw_context (str)
        compressed_context (str)
        retrieval_latency_sec (float)
    """

    start_time = time.time()

    # -------------------------------------------------
    # 1. Query Rewrite
    # -------------------------------------------------
    rewritten_query = rewrite_query(user_query)
    print("\n🔁 Rewritten Query:")
    print(rewritten_query)

    # -------------------------------------------------
    # 2. High-recall Retrieval
    # -------------------------------------------------
    candidate_docs: List[Document] = retriever.invoke(rewritten_query)
    print(f"\n📥 Retrieved {len(candidate_docs)} candidate chunks")

    # Debug: inspect candidates
    for i, d in enumerate(candidate_docs):
        print(f"\n--- Candidate {i+1} ---")
        print(d.page_content[:300])

    # -------------------------------------------------
    # 3. Cross-Encoder Reranking
    # -------------------------------------------------
    reranked_docs: List[Document] = reranker.rerank(
        rewritten_query,
        candidate_docs,
        top_k=rerank_top_k
    )

    print("\n🎯 Top Reranked Chunks:")
    for i, d in enumerate(reranked_docs):
        print(f"\n--- Reranked {i+1} ---")
        print(d.page_content)

    # -------------------------------------------------
    # 4. RAW Context (no compression)
    # -------------------------------------------------
    raw_context = "\n\n".join([d.page_content for d in reranked_docs])

    # -------------------------------------------------
    # 5. Context Compression (loss-aware)
    # -------------------------------------------------
    compressed_chunks = compress_context(
        query=user_query,
        docs=reranked_docs,
        max_words=120
    )

    print("\n🗜️ Compressed Context:")
    for c in compressed_chunks:
        print(c)

    compressed_context = "\n\n".join(compressed_chunks)

    retrieval_latency = round(time.time() - start_time, 2)

    return raw_context, compressed_context, retrieval_latency