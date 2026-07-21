from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.rag import preguntar_pdf
from fastapi.responses import StreamingResponse
import time
from pathlib import Path
from fastapi.responses import FileResponse
import shutil
from pdf_indexer import indexar_pdf

app = FastAPI()
PDF_PATH = Path("/data/pdfs")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
                   "http://localhost:5173",
                   "http://127.0.0.1:5173",
                   "http://192.168.40.7:5173"
                ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: list = []

@app.get("/")
def home():
    return {"message": "Hello, World!"}

@app.post("/chat")
async def chat(request: ChatRequest):
    def generar():
        respuesta = preguntar_pdf(
            request.message,
            request.history or []
        )

        for palabra in respuesta.split():
            yield palabra + " "
            time.sleep(0.05)  

    return StreamingResponse(generar(), media_type="text/plain")

@app.get("/pdfs")
def listar_pdfs():

    carpeta = Path("/data/pdfs")

    return [
        archivo.name 
        for archivo in carpeta.glob("*.pdf")
    ]

@app.get("/pdfs/{filename:path}")
def obtener_pdf(filename: str):
    return FileResponse(
        f"/data/pdfs/{filename}",
        media_type="application/pdf",
    )

@app.post("/upload")
async def upload_pdf(pdf: UploadFile = File(...)):
    
    if not pdf.filename.endswith(".pdf"):
        return {"error": "El archivo debe ser un PDF."}
    
    destino = PDF_PATH / pdf.filename
    with destino.open("wb") as buffer:
        shutil.copyfileobj(pdf.file, buffer)
    try:
        indexar_pdf(destino)
    except Exception as e:
        destino.unlink(missing_ok=True)  
        return {"error": f"Error al indexar el PDF: {str(e)}"}
    return {"message": f"Archivo {pdf.filename} subido correctamente.",
            "filename": pdf.filename
            }