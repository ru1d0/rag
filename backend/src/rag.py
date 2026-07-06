from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate


# LLM

llm = ChatOllama(
    model="qwen3:8b",
    base_url="http://ollama:11434",
    temperature=0.7,
)

# Embeddings

embeddings = OllamaEmbeddings(
    model="qwen3-embedding:4b",
    base_url="http://ollama:11434"
)

# Chroma

vectorstore = Chroma(
    persist_directory="./data/chroma",
    embedding_function=embeddings
)

# Prompt

template = ChatPromptTemplate.from_messages([
    (
        "system",
        """
       Eres Pabloxan.

        Puedes utilizar:

        1. El historial de conversación.
        2. El contexto recuperado desde los documentos.

        Si la pregunta depende de mensajes anteriores,
        usa el historial para interpretarla.

        Si la información no aparece ni en el historial ni en el contexto,
        indica claramente que no fue encontrada.
        """
    ),
    ("human", "{input}")
])

chain = template | llm


def preguntar_pdf(pregunta: str, history: list = []):

    docs = vectorstore.similarity_search(
        pregunta,
        k=3
    )

    historial = "\n\n".join(
        [
            f"{msg['role']}: {msg['content']}" for msg in history[-10:]
        ]
    )

    contexto = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt_rag = f"""
    HISTORIAL:

    {historial}

    CONTEXTO:

    {contexto}

    PREGUNTA:

    {pregunta}
    """

    respuesta = chain.invoke({
        "input": prompt_rag
    })

    return respuesta.content