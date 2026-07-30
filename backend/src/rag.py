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

        Responde únicamente utilizando la información presente en el CONTEXTO y el HISTORIAL.

        Reglas:

        - No inventes información.
        - Si la respuesta no aparece en el contexto, indícalo claramente.
        - Si la pregunta depende de mensajes anteriores, utiliza el historial para interpretarla.

        Formato de salida:

        - Responde SIEMPRE en Markdown válido.
        - Nunca utilices HTML.
        - Cada título debe estar separado por una línea en blanco.
        - Cada párrafo debe estar separado por una línea en blanco.
        - Antes de cualquier lista debe existir una línea en blanco.
        - Después de cualquier lista debe existir una línea en blanco.
        - Los comandos deben ir dentro de bloques de código Markdown.

        Ejemplo del formato esperado:

        ## Acceso a la base de datos

        Para acceder sigue estos pasos.

        1. Configurar SSH

        2. Autenticarse

        3. Conectarse a la base de datos

        ### Configuración SSH

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
