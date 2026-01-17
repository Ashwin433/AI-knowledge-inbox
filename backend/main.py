from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from db import save_item,get_items

import requests
from bs4 import BeautifulSoup
from embed import make_embeddings
from db import save_chunk

app = FastAPI()

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

    if data.source == "url":
        response = requests.get(data.text,timeout=10)
        soup = BeautifulSoup(response.content,"html.parser")

        for tag in soup(["script","style"]):
            tag.decompose()

        final_text = ' '.join(soup.get_text().split())

    else:
        final_text = data.text

    
    item_id = save_item(final_text, data.source)
    chunks = split_text(final_text)
    embeddings=make_embeddings(chunks)

    for chunk ,embedding in zip(chunks,embeddings):
        save_chunk(item_id,chunk,embedding)
    return {"status":"success"}

@app.get("/items")
def items():
    return get_items()



