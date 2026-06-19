from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model="qwen3-embedding:4b",
    base_url="http://ollama:11434"
)

vector = embeddings.embed_query(
    "Hola mundo"
)

print(f"Dimensión: {len(vector)}")
print(vector[:10])