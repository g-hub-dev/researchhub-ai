from fastapi import UploadFile, File, Form
import PyPDF2
from fastapi import APIRouter
from utils.groq_client import client, MODEL_CONFIG

router = APIRouter()

@router.post("/chat")
async def chat(message: str):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful research assistant."},
            {"role": "user", "content": message}
        ],
        **MODEL_CONFIG
    )

    return {
        "response": response.choices[0].message.content
    }
@router.post("/pdf-qa")
async def pdf_qa(file: UploadFile = File(...), question: str = ""):
    try:
        contents = await file.read()

        with open("temp.pdf", "wb") as f:
            f.write(contents)

        reader = PyPDF2.PdfReader("temp.pdf")

        text = ""
        for page in reader.pages:
            text += page.extract_text()

        # Limit text size (important for token limits)
        text = text[:5000]

        prompt = f"""
        Answer the question based ONLY on the document below.

        Document:
        {text}

        Question:
        {question}
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response.choices[0].message.content

        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}
@router.post("/ai/pdf-analyze")
async def analyze_pdf(file: UploadFile = File(...)):
    try:
        # ---- READ PDF ----
        pdf_reader = PyPDF2.PdfReader(file.file)
        text = ""

        for page in pdf_reader.pages:
            text += page.extract_text()

        # ---- LIMIT TEXT (important for model) ----
        text = text[:4000]

        # ---- SEND TO GROQ ----
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # use working model
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Analyze this research paper and give:
                    1. Title
                    2. Summary
                    3. 5 Key Points
                    4. Domain (AI/ML/NLP/etc)

                    Paper:
                    {text}
                    """
                }
            ]
        )

        return {
            "analysis": response.choices[0].message.content
        }

    except Exception as e:
        return {"error": str(e)}