from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.rag import preguntar_pdf
from fastapi.responses import StreamingResponse
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Hello, World!"}

@app.post("/chat")
def chat(request: ChatRequest):
    def generar():
        respuesta = preguntar_pdf(
            request.message
        )

        for palabra in respuesta.split():
            yield palabra + " "
            time.sleep(0.05)  

    return StreamingResponse(generar(), media_type="text/plain")