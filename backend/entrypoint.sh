#!/bin/sh

set -e

echo "Iniciando RAG"

echo "Esperando a Ollama..."

until curl -s http://ollama:11434/api/tags > /dev/null
do
    sleep 2
done

echo "Ollama disponible."


MODELS=$(curl -s http://ollama:11434/api/tags)

if ! echo "$MODELS" | grep -q "$LLM_MODEL"; then

    echo "Descargando modelo $LLM_MODEL..."

    curl http://ollama:11434/api/pull \
        -d "{\"name\":\"$LLM_MODEL\"}"

else

    echo "Modelo $LLM_MODEL encontrado."

fi

MODELS=$(curl -s http://ollama:11434/api/tags)

if ! echo "$MODELS" | grep -q "$EMBEDDING_MODEL"; then

    echo "Descargando modelo $EMBEDDING_MODEL..."

    curl http://ollama:11434/api/pull \
        -d "{\"name\":\"$EMBEDDING_MODEL\"}"

else

    echo "Modelo $EMBEDDING_MODEL encontrado."

fi

if [ ! -f "$CHROMA_PATH/chroma.sqlite3" ]; then

    echo "No existe índice Chroma."

    echo "Indexando documentos..."

    python src/index.py

else

    echo "Índice Chroma encontrado."

fi

echo "Iniciando FastAPI..."

exec uvicorn src.app:app \
    --host ${HOST:-0.0.0.0} \
    --port ${PORT:-8000}