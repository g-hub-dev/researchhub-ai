from fastapi import APIRouter
import requests
import xml.etree.ElementTree as ET
saved_papers = []

router = APIRouter()

@router.get("/papers/search")
def search_papers(query: str):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=20"
    
    response = requests.get(url)
    root = ET.fromstring(response.content)

    ns = {"atom": "http://www.w3.org/2005/Atom"}

    papers = []

    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text
        summary = entry.find("atom:summary", ns).text

        authors = []
        for author in entry.findall("atom:author", ns):
            name = author.find("atom:name", ns).text
            authors.append(name)

        link = entry.find("atom:id", ns).text

        papers.append({
            "title": title.strip(),
            "authors": authors,
            "abstract": summary.strip(),
            "link": link
        })

    return {"papers": papers}
from pydantic import BaseModel
from utils.groq_client import client

class SummaryRequest(BaseModel):
    abstract: str

@router.post("/papers/summarize")
def summarize_paper(request: SummaryRequest):
    prompt = f"""
    Explain the following research paper abstract in simple terms:

    {request.abstract}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instan",
        messages=[{"role": "user", "content": prompt}]
    )

    summary = response.choices[0].message.content

    return {"summary": summary}
from pydantic import BaseModel

class Paper(BaseModel):
    title: str
    link: str
    summary: str

@router.post("/papers/save")
def save_paper(paper: Paper):
    saved_papers.append(paper.dict())
    return {"message": "Paper saved successfully"}
@router.get("/papers/saved")
def get_saved_papers():
    return {"saved_papers": saved_papers}