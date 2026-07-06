from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma



carpeta_pdfs = Path("/data/pdfs")

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

all_chunks = []

for pdf in carpeta_pdfs.glob("*.pdf"):
    print(f"Procesando {pdf.name}...")
    loader = PyPDFLoader(str(pdf))
    documentos = loader.load()
    
    for doc in documentos:
        doc.metadata["source"] = pdf.name
    
    chunks = splitter.split_documents(documentos)
    all_chunks.extend(chunks)
print(f"Total de chunks generados: {len(all_chunks)}")

embeddings = OllamaEmbeddings(
    model="qwen3-embedding:4b",
    base_url="http://ollama:11434"
)

vectorstore = Chroma.from_documents(
    documents=all_chunks,
    embedding=embeddings,
    persist_directory="./data/chroma"
)

print("Indexado completado.")