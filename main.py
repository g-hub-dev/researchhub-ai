from fastapi import FastAPI
from routers import auth, papers, chat

app = FastAPI(title="ResearchHub AI")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(papers.router, prefix="/papers", tags=["Papers"])
app.include_router(chat.router, prefix="/ai", tags=["AI Chat"])

@app.get("/")
def home():
    return {"message": "ResearchHub AI backend running"}