AI-Knowledge-Inbox

OVERVIEW:

This project is a minimal AI knowledge Inbox

The goal of the assignment was to evaluvate approach to:
-Backend and frontend integratiom
-Async workflows
-AI Integration(Rag)
-overall system design

within almost 10 hours of work, I implemented small web application that allows:
-ingesting text notes or urls
-Asking question over the ingested content
-Retrieving answers using semantic search over the stored data

Features:

Ingestion: 

-Add plain text notes
-Add URLs
-Automatic input normalisation and validation
-SQLite based persistence

Semantic Search + RAG:

-Text is chunked to fixed sized fragments
-Embedding generated using local sentence transformer model(all-MiniLM-L6-v2)
-query embeddings are matched against the stored chunks using cosine similarity
-Top matching chunks returned as context for answering

Techstack:

BACKEND:
-FastAPI(python)
-SQLite
-sentence-transformers(all-MiniLM-L6-v2)
-request+BeautifulSoup for url ingestion

FRONTEND:
-React(Vite)
-inliine styling


Step 1: Clone the repository

```bash
git clone <your-github-repo-url>
cd AI-knowledge-inbox


Step 2: Backend setup (FastAPI)

I used a Python virtual environment to keep backend dependencies isolated.

cd backend
python -m venv venv


Activate the virtual environment:
Windows:
venv\Scripts\activate

macOS / Linux:
source venv/bin/activate

Install backend dependancies
pip install -r requirements.txt

start the backend server
uvicorn main:app --reload


Step 3: Frontend setup(React)
In separate terminal start a fronted
cd frontend/ai-knowledge-ui
npm install
npm run dev




