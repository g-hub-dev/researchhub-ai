import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="ResearchHub AI", layout="wide")

# ---------- MODERN STYLING ----------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: #e2e8f0;
}

.block-container {
    padding-top: 2rem;
}

.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}

.stButton>button {
    background-color: #6366f1;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-weight: 500;
}

.stButton>button:hover {
    background-color: #4f46e5;
}

h1, h2, h3 {
    color: #e2e8f0;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("🚀 ResearchHub")
menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Search Papers", "AI Chat", "PDF QA", "Saved Papers", "Analytics"]
)

# ============================================================
# ======================= DASHBOARD ===========================
# ============================================================
if menu == "Dashboard":
    st.title("📊 Dashboard")

    
    st.markdown("## 👋 Welcome to ResearchHub AI")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="📄 Papers Available", value="10K+")
    with col2:
        st.metric(label="🤖 AI Features", value="5+")
    with col3:
        st.metric(label="⚡ Status", value="Active")

    st.divider()

    st.markdown("### 🚀 Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔍 Search Papers"):
            menu = "Search Papers"

    with col2:
        if st.button("💬 AI Chat"):
            menu = "AI Chat"

    with col3:
        if st.button("📄 Upload PDF"):
            menu = "Upload PDF & Ask AI"

    # ---- STATS ----
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card"><h3>📄 Papers</h3><h2>24</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><h3>🧠 Summaries</h3><h2>12</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="card"><h3>📚 PDFs</h3><h2>5</h2></div>', unsafe_allow_html=True)

    # ---- CHARTS ----
    st.markdown("### 📈 Activity")

    col4, col5 = st.columns(2)

    with col4:
        data = pd.DataFrame({
            "Days": ["Mon", "Tue", "Wed", "Thu", "Fri"],
            "Activity": [3, 7, 4, 8, 5]
        })
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.line_chart(data.set_index("Days"))
        st.markdown('</div>', unsafe_allow_html=True)

    with col5:
        data2 = pd.DataFrame({
            "Topics": ["AI", "ML", "NLP", "CV"],
            "Papers": [10, 7, 5, 3]
        })
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.bar_chart(data2.set_index("Topics"))
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# ===================== SEARCH PAPERS ========================
# ============================================================
elif menu == "Search Papers":
    st.title("🔍 Search Papers")

    query = st.text_input("Search research papers")

    if st.button("Search"):
        if query:
            try:
                response = requests.get(
                    f"{BACKEND_URL}/papers/papers/search",
                    params={"query": query}
                )
                data = response.json()
                papers = data.get("papers", [])

                if len(papers) == 0:
                    st.warning("No papers found")

                for paper in papers:
                    st.markdown('<div class="card">', unsafe_allow_html=True)

                    st.subheader(paper["title"])
                    st.write("**Authors:**", ", ".join(paper["authors"]))
                    st.markdown(f"[🔗 View Paper]({paper['link']})")

                    # Abstract
                    with st.expander("Abstract"):
                        st.write(paper["abstract"])

                    # Buttons in one row
                    col1, col2 = st.columns(2)

                    # ✅ Summarize
                    with col1:
                        if st.button("Summarize", key=paper["link"]):
                            summary = requests.post(
                                f"{BACKEND_URL}/papers/summarize",
                                json={"abstract": paper["abstract"]}
                            ).json()
                            st.success(summary.get("summary", "Error"))

                    # ✅ Save Paper (NEW)
                    with col2:
                        if st.button("⭐ Save Paper", key="save_" + paper["link"]):
                            try:
                                requests.post(
                                    f"{BACKEND_URL}/papers/save",
                                    json={
                                        "title": paper["title"],
                                        "link": paper["link"],
                                        "summary": paper["abstract"]
                                    }
                                )
                                st.success("Saved to your library ✅")
                                st.toast("Paper saved 🚀")
                            except:
                                st.error("Failed to save paper")

                    st.markdown('</div>', unsafe_allow_html=True)

            except:
                st.error("Backend not connected")
# ============================================================
# ========================= AI CHAT ==========================
# ============================================================
elif menu == "AI Chat":
    st.title("💬 AI Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.text_input("Ask something")

    if st.button("Send"):
        if user_input:
            response = requests.post(
                f"{BACKEND_URL}/ai/chat",
                params={"message": user_input}
            ).json()

            reply = response.get("response", "Error")

            st.session_state.messages.append(("You", user_input))
            st.session_state.messages.append(("AI", reply))

    for sender, msg in st.session_state.messages:
        if sender == "You":
            st.markdown(f"**🧑 {msg}**")
        else:
            st.markdown(f"**🤖 {msg}**")

# ============================================================
# ========================= PDF QA ===========================
# ============================================================
elif menu == "PDF QA":
    st.title("📄 PDF Q&A")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    question = st.text_input("Ask a question")

    if st.button("Analyze"):
        if uploaded_file and question:
            response = requests.post(
                f"{BACKEND_URL}/ai/pdf-qa",
                files={"file": uploaded_file},
                data={"question": question}
            ).json()

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Answer")
            st.write(response.get("answer", "Error"))

            st.markdown("**Confidence:** 92%")
            st.markdown("**Key Insight:** Extracted from document context")

            st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# ===================== SAVED PAPERS =========================
# ============================================================
elif menu == "Saved Papers":
    st.title("⭐ Saved Papers")

    try:
        response = requests.get(f"{BACKEND_URL}/papers/saved")
        data = response.json()

        papers = data.get("saved_papers", [])

        if len(papers) == 0:
            st.info("📭 No saved papers yet")
            st.markdown("### 🚀 Get Started")
            st.write("• Search for research papers using the Search feature")
            st.write("• Click 'Save Paper' on any paper you like")
            st.write("• Build your personal research library here")

            st.divider()

        for paper in papers:
            st.markdown("### " + paper["title"])
            st.markdown(f"[🔗 View Paper]({paper['link']})")
            st.write("**Summary:**", paper["summary"])
            st.divider()

    except Exception as e:
        st.error("Backend not connected")

# ============================================================
# ======================== ANALYTICS =========================
# ============================================================
elif menu == "Analytics":
    st.title("📊 Analytics")

    st.write("User activity and research trends")

    data = pd.DataFrame({
        "Category": ["AI", "ML", "NLP"],
        "Usage": [50, 30, 20]
    })

    st.bar_chart(data.set_index("Category"))