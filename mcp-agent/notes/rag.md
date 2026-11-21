# RAG notes
- RAG = retrieve relevant text first, then give it to the LLM along with the question.
- Chunk size: 300-500 tokens is a common starting point.
- Smaller chunks are more precise; larger chunks keep more context.
- Chunk overlap of about 10-15% stops sentences from being cut in half.
- Retrieval usually uses embeddings and a vector database.