# 🎬 AskTube AI

**AskTube AI** is a Streamlit-powered web app that lets you ask questions about any YouTube video and get instant, AI-generated answers based on the video’s transcript. Just paste a YouTube link, and start chatting with your video!

---

## 🚀 Features

- **YouTube Video Q&A:** Paste a YouTube link, and ask anything about the video.
- **Automatic Transcript Extraction:** Fetches and processes the video transcript for you.
- **AI-Powered Answers:** Uses advanced language models to answer your questions contextually.
- **Instant Video Preview:** Watch the video alongside your Q&A session.
- **Modern, User-Friendly UI:** Built with Streamlit for a seamless experience.

---

## 🛠️ Tech Stack

- **Frontend & UI:** [Streamlit](https://streamlit.io/)
- **AI & Chains:** [LangChain](https://python.langchain.com/)
- **Transcripts:** [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)
- **Vector Store:** [ChromaDB](https://www.trychroma.com/)
- **Translation:** [googletrans](https://py-googletrans.readthedocs.io/en/latest/)

---

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Set up environment variables:**
   - If you use API keys or environment variables, create a `.env` file in the root directory.

---

## 🏃‍♂️ Usage

1. **Start the app:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser:**  
   Go to [http://localhost:8501](http://localhost:8501)

3. **Paste a YouTube video URL** in the sidebar, submit, and start asking questions!

---

## 📁 Project Structure

```
.
├── app.py                  # Main Streamlit app
├── chains/
│   └── query_chain.py      # AI chain logic
├── services/
│   ├── transcript_service.py   # Transcript extraction
│   └── vector_store_service.py # Vector store setup
├── utils/
│   └── prompt_templates.py     # Prompt templates for AI
├── requirements.txt
└── README.md
```

---


