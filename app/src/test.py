from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

llm = ChatOllama(
    model="qwen3:8b",
    base_url="http://ollama:11434",
    temperature=0.7,
    streaming=True,
)

template = ChatPromptTemplate.from_messages([
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

        # Limpiar entrada
        user_input = limpiar_texto(user_input)

        response = chain.invoke({
            "input": user_input,
            "chat_history": chat_history
        })

        # Limpiar salida
        respuesta = limpiar_texto(response.content)

        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=respuesta))

        print(f"Pabloxan: {respuesta}")


if __name__ == "__main__":
    ejecutar_chatbot()