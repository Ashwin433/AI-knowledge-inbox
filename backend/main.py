from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from db import save_item,get_items,get_chunks
from search import find_similar
from rag import answer

import requests
from bs4 import BeautifulSoup
from embed import make_embeddings
from db import save_chunk
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class noteInput(BaseModel):
    text: str
    source: str

def split_text(text, max_length=500):
    chunks = []
    for i in range(0, len(text), max_length):
        chunks.append(text[i:i+max_length])
    return chunks

@app.post("/ingest")
def save_note(data: noteInput):

    source = data.source.strip().lower()

    if source not in ["url","note"]:
        raise HTTPException(status_code=400,detail="Invalid source type")

    if source == "url":

        if not data.text.startswith("http://") and not data.text.startswith("https://"):
            data.text = "https://" + data.text
        try:
            response = requests.get(data.text,timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            raise HTTPException(status_code=400,detail=f"Failed to fetch URL: {e}")
        
        soup = BeautifulSoup(response.text,"html.parser")

        for tag in soup(["script","style"]):
            tag.decompose()

        final_text = ' '.join(soup.get_text().split())

    else:
        final_text = data.text

    
    item_id = save_item(final_text,source)
    chunks = split_text(final_text)
    embeddings=make_embeddings(chunks)

    for chunk ,embedding in zip(chunks,embeddings):
        save_chunk(item_id,chunk,embedding)
    return {"status":"success"}

@app.get("/items")
def items():
    return get_items()


class questionInput(BaseModel):
    question: str

@app.post("/query")
def query(data: questionInput):
    chunks = get_chunks()
    query_embedding = make_embeddings([data.question])[0]

    top_chunks = find_similar(query_embedding,chunks,top_k=5)
    final_answer = answer(data.question,top_chunks)

    return {"answer": final_answer,"sources": top_chunks}
