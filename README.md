# 🔬 ResearchHub AI

An AI-powered research assistant that helps users **discover, understand, and organize research papers efficiently**.

Built as a full-stack application integrating search, AI, and document analysis.

---

## 🚀 Features

### 🔍 Research Paper Search
- Search papers using arXiv API
- View paper details including title, authors, and abstract
- Direct link to read the full paper on arXiv

### 🧠 AI-Powered Summarization
- Generate concise summaries of research papers
- Helps quickly understand complex abstracts

### ⭐ Save Papers (Personal Library)
- Save important papers for later reference
- View saved papers in a dedicated section
- Designed for future database integration

### 💬 AI Research Assistant
- Ask questions related to research topics
- Get intelligent responses powered by LLM

### 📄 PDF Upload & Question Answering
- Upload research papers (PDF)
- Ask specific questions about the document
- Extract insights without reading the full paper

### 🎯 Smooth User Flow
- Search → Analyze → Save → Revisit
- Designed to mimic real-world research workflow

---

## 🧠 Tech Stack

### Backend
- FastAPI
- Python

### Frontend
- Streamlit

### AI / APIs
- Groq API (LLM for chat, summarization, QA)
- arXiv API (research paper search)

### Libraries
- PyPDF2 (PDF text extraction)
- Requests (API calls)
- Python-dotenv (environment variables)

---

## 💡 Problem Statement

Understanding research papers is time-consuming and complex.  
This project simplifies the process by combining:

- Paper discovery  
- AI summarization  
- Interactive Q&A  
- Personal research tracking  

---

## ⚙️ How to Run

### 1️⃣ Clone the Repository

git clone https://github.com/g-hub-dev/researchhub-ai.git
cd researchhub-ai

---

### 2️⃣ Setup Backend

cd bk
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn streamlit requests python-dotenv python-multipart groq PyPDF2

Run backend:
python -m uvicorn main:app --reload

---

### 3️⃣ Run Frontend

Make sure you are in the folder where `app.py` exists:
streamlit run app.py

---

## 📌 Current Limitations

- Saved papers are not stored permanently (no database yet)
- No user login system
- UI can be improved further

---

## 🔮 Future Improvements

- Database (MongoDB / PostgreSQL)
- Recommendation system
- Authentication
- Advanced dashboard

---

## 🎥 Demo

(Add your demo video link here)

---

## 👩‍💻 Author

Srividya G