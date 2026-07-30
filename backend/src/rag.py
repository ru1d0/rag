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
    persist_directory="/storage/chroma",
    embedding_function=embeddings
)

# Prompt

template = ChatPromptTemplate.from_messages([
    (
    "system",
            """
    Eres Pabloxan.

    Responde únicamente utilizando la información del CONTEXTO y del HISTORIAL.

    Reglas:

    - No inventes información.
    - Si la respuesta no está en el contexto, dilo claramente.
    - Si la pregunta depende del historial, úsalo para responder.

    Formato:

    - Responde SIEMPRE en Markdown.
    - Nunca escribas HTML.
    - Deja una línea en blanco entre párrafos.
    - Usa títulos con ## y ### cuando corresponda.
    - Usa listas con '-' o numeradas cuando sea apropiado.
    - Antes de cada lista, escribe un salto de línea.
    - Los comandos deben ir dentro de bloques de código.

    Ejemplo:

    ## Configuración SSH

    Ejecuta:

    ```bash
    ssh usuario@servidor -p 4490
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
