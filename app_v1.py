import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from context_builder_v2 import build_contexts
from metrics import (
    MetricSnapshot,
    count_tokens,
    calculate_cost
)

# --------------------------------------------------
# Environment
# --------------------------------------------------
load_dotenv()

MODEL_NAME = "gpt-4o-mini"

# --------------------------------------------------
# LLM (final answer generation)
# --------------------------------------------------
llm = ChatOpenAI(
    model=MODEL_NAME,
    temperature=0
)

# --------------------------------------------------
# Vector DB + Retriever
# --------------------------------------------------
embeddings = OpenAIEmbeddings()

vector_db = Chroma(
    persist_directory="db",
    embedding_function=embeddings
)

# IMPORTANT: high k for recall (semantic chunking + rerank)
retriever = vector_db.as_retriever(
    search_kwargs={"k": 15}
)

# --------------------------------------------------
# Main execution with metrics
# --------------------------------------------------
def run_query_with_metrics(user_query: str):
    print("\n==============================")
    print("User Question:", user_query)
    print("==============================")

    # Build both contexts
    raw_context, compressed_context, retrieval_latency = build_contexts(
        retriever=retriever,
        user_query=user_query,
        rerank_top_k=3
    )

    results = {}

    for label, context in {
        "WITHOUT_CONTEXT_COMPRESSION": raw_context,
        "WITH_CONTEXT_COMPRESSION": compressed_context
    }.items():

        print(f"\n🚀 Running: {label}")

        metrics = MetricSnapshot()

        prompt = f"""
You are an enterprise policy assistant.

Answer the question using ONLY the context below.
If multiple policies or SLA types exist, choose the one that best answers the question.
Do not guess or mix policies.

Context:
{context}

Question:
{user_query}

Answer:
"""

        # Token counting (prompt)
        prompt_tokens = count_tokens(prompt, MODEL_NAME)

        # LLM call
        response = llm.invoke(prompt)

        # Token counting (completion)
        completion_tokens = count_tokens(response.content, MODEL_NAME)

        # Metrics
        metrics.prompt_tokens = prompt_tokens
        metrics.completion_tokens = completion_tokens
        metrics.cost = calculate_cost(
            prompt_tokens,
            completion_tokens,
            MODEL_NAME
        )
        metrics.stop()

        results[label] = {
            "answer": response.content,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "cost_usd": metrics.cost,
            "cost_usd_display": f"${float(metrics.cost):.6f}",
            "latency_sec": metrics.latency,
        }

    # --------------------------------------------------
    # Print comparison
    # --------------------------------------------------
    print("\n📊 METRICS COMPARISON")
    print("Retrieval + Rerank Latency:", retrieval_latency, "sec")

    for label, data in results.items():
        print("\n------------------------------")
        print(label)
        print("------------------------------")
        print("Answer:", data["answer"])
        print("Prompt tokens:", data["prompt_tokens"])
        print("Completion tokens:", data["completion_tokens"])
        print("Total tokens:", data["total_tokens"])
        print("Cost (USD):", data["cost_usd"])
        print("LLM Latency (sec):", data["latency_sec"])

    print("\n==============================\n")

    no_comp = results["WITHOUT_CONTEXT_COMPRESSION"]
    comp = results["WITH_CONTEXT_COMPRESSION"]

    print("\n📊 FINAL METRICS – CONTEXT COMPRESSION IMPACT")
    print("============================================")

    print(f"Prompt Tokens        : {no_comp['prompt_tokens']} → {comp['prompt_tokens']} "
          f"({improvement(no_comp['prompt_tokens'], comp['prompt_tokens'])} reduction)")

    print(f"Total Tokens         : {no_comp['total_tokens']} → {comp['total_tokens']} "
          f"({improvement(no_comp['total_tokens'], comp['total_tokens'])} reduction)")

    print(f"Cost (USD)           : ${no_comp['cost_usd']:.6f} → ${comp['cost_usd']:.6f} "
          f"({improvement(no_comp['cost_usd'], comp['cost_usd'])} reduction)")

    print(f"Latency (sec)        : {no_comp['latency_sec']} → {comp['latency_sec']} "
          f"({improvement(no_comp['latency_sec'], comp['latency_sec'])} improvement)")


def improvement(old, new):
    if old == 0:
        return "N/A"
    return f"{((old - new) / old) * 100:.2f}%"

\
    
# --------------------------------------------------
# CLI Loop
# --------------------------------------------------
if __name__ == "__main__":
    while True:
        user_input = input("\nAsk a question (or type 'exit'): ")
        if user_input.lower() == "exit":
            break

        run_query_with_metrics(user_input)
        