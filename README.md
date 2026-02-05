 # Retrieval-Augmented Generation (RAG) 

RAG system that answers enterprise policy questions accurately, while optimizing cost and latency, 
and measuring the impact of each optimization.

# High-Level Architecture

User Query
   ↓
Query Rewriter (LLM)
   ↓
Vector Retrieval (High Recall)
   ↓
Cross-Encoder Reranker (Precision)
   ↓
Context Builder
   ├── Raw Context
   └── Compressed Context
   ↓
LLM Answer Generation
   ↓
Metrics Engine (Tokens, Cost, Latency)
   ↓
Final Answer + Improvement Report


