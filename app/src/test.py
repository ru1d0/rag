from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

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

        Responde usando el contexto entregado.

        Si la respuesta no está en el contexto,
        di claramente que no la encontraste en el documento.
        """
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

chain = template | llm


def limpiar_texto(texto):
    return texto.encode("utf-8", errors="ignore").decode("utf-8")


def ejecutar_chatbot():

    print("¡Hola! Soy Pabloxan. ¿En qué puedo ayudarte?")

    chat_history = []

    while True:

        user_input = input("Tú: ")

        if user_input.lower() in ["salir", "exit"]:
            print("¡Hasta luego!")
            break

        user_input = limpiar_texto(user_input)

        # ==========================
        # Recuperar contexto
        # ==========================

        docs = vectorstore.similarity_search(
            user_input,
            k=3
        )

        contexto = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        prompt_rag = f"""
        CONTEXTO:

        {contexto}

        PREGUNTA:

        {user_input}
        """

        # ==========================
        # Consultar LLM
        # ==========================

        response = chain.invoke({
            "input": prompt_rag,
            "chat_history": chat_history
        })

        respuesta = limpiar_texto(response.content)

        chat_history.append(
            HumanMessage(content=user_input)
        )

        chat_history.append(
            AIMessage(content=respuesta)
        )

        print(f"\nPabloxan: {respuesta}\n")


if __name__ == "__main__":
    ejecutar_chatbot()