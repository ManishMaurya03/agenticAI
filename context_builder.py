import time
from reranker import CrossEncoderReranker

reranker = CrossEncoderReranker()

def build_context(retriever, query):
    start = time.time()

    # Step 1: retrieve more candidates from vector DB
    docs = retriever.invoke(query)   # k = 10

    retrieval_time = time.time() - start
    print(f"Retrieved {len(docs)} chunks")

    # Step 2: rerank using cross-encoder
    reranked_docs = reranker.rerank(query, docs, top_k=3)

    print("Top reranked chunks:")
    for i, d in enumerate(reranked_docs):
        print(f"\n--- Chunk {i+1} ---")
        print(d.page_content[:500])

    context = "\n\n".join([doc.page_content for doc in reranked_docs])

    return context, retrieval_time