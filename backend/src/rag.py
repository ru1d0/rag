from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate

# ==========================
# LLM
# ==========================

llm = ChatOllama(
    model="qwen3:8b",
    base_url="http://ollama:11434",
    temperature=0.7,
)

# ==========================
# Embeddings
# ==========================

embeddings = OllamaEmbeddings(
    model="qwen3-embedding:4b",
    base_url="http://ollama:11434"
)

# ==========================
# Chroma
# ==========================

vectorstore = Chroma(
    persist_directory="./data/chroma",
    embedding_function=embeddings
)

# ==========================
# Prompt
# ==========================

template = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        Eres Pabloxan.

        Responde usando exclusivamente el contexto entregado.

        Si la respuesta no está en el contexto,
        di claramente que no la encontraste en el documento.
        """
    ),
    ("human", "{input}")
])

chain = template | llm


def preguntar_pdf(pregunta: str):

    docs = vectorstore.similarity_search(
        pregunta,
        k=3
    )

    contexto = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt_rag = f"""
    CONTEXTO:

    {contexto}

    PREGUNTA:

    {pregunta}
    """

    respuesta = chain.invoke({
        "input": prompt_rag
    })

    return respuesta.content