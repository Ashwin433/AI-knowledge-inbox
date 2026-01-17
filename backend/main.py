from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from db import save_item,get_items

import requests
from bs4 import BeautifulSoup

app = FastAPI()

class noteInput(BaseModel):
    text: str
    source: str

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


    save_item(data.text, data.source)
    return {"status": "saved"}

@app.get("/items")
def items():
    return get_items()


def split_text(text, max_length=500):
    chunks = []
    for i in range(0, len(text), max_length):
        chunks.append(text[i:i+max_length])
    return chunks