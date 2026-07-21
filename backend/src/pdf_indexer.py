from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

embeddings = OllamaEmbeddings(
    model="qwen3-embedding:4b",
    base_url="http://ollama:11434"
)

def indexar_pdf(pdf: Path):

    loader = PyPDFLoader(str(pdf))
    documentos = loader.load()

    for doc in documentos:
        doc.metadata["source"] = pdf.name
    
    chunks = splitter.split_documents(documentos)

    vectorstore = Chroma(
        persist_directory="/storage/chroma",
        embedding_function=embeddings
    )

    vectorstore.add_documents(chunks)

    print(f"Indexado completado para {pdf.name}. Total de chunks generados: {len(chunks)}")