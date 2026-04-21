# QA RAG Application - Complete Documentation

A production-ready **Question Answering System** using **Retrieval-Augmented Generation (RAG)** architecture with OpenAI API, FAISS vector search, and Flask backend.

## 📋 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file
copy .env.example .env

# 3. Add your OpenAI API key to .env
# Edit .env and add: OPENAI_API_KEY=sk-proj-your-key-here

# 4. Run the application
python app.py

# 5. Open browser to http://localhost:5000
```

## 📁 Project Structure

```
qa_rag_app/
├── app.py                      # Flask application & API routes
├── requirements.txt            # Python dependencies (pinned versions)
├── .env.example               # Environment variables template
├── .env                       # Your local API key (git-ignored)
├── SETUP_INSTRUCTIONS.md      # Detailed setup guide
├── EXAMPLE_TEST.md            # Test scenarios & validation
├── README.md                  # This file
├── templates/
│   └── index.html             # Single-page frontend (HTML + JS)
├── static/
│   └── style.css              # Professional styling
└── utils/
    ├── __init__.py            # Package initialization
    ├── document_loader.py     # PDF/TXT extraction
    ├── chunker.py             # Text segmentation
    ├── embeddings.py          # OpenAI embeddings + FAISS
    └── qa_engine.py           # Answer generation with GPT-4o-mini
```

## 🚀 Features

- **PDF & TXT Upload** - Extract text from files or paste raw text
- **Intelligent Chunking** - 500-char overlapping chunks for context preservation
- **Vector Search** - FAISS-based semantic search (no external DB)
- **OpenAI Integration** - Uses GPT-4o-mini for accurate answers
- **Context-Grounded** - Strict system prompt ensures answers use document context only
- **Professional UI** - Responsive, gradient-themed interface with spinners
- **Full Error Handling** - JSON error responses with clear messages
- **Session-Based Storage** - In-memory FAISS index (no database needed)

## 🔧 Technology Stack

| Component | Package | Version |
|-----------|---------|---------|
| Framework | Flask | 3.0.3 |
| LLM API | OpenAI | 1.30.1 |
| Vector DB | FAISS (CPU) | 1.8.0 |
| Math | NumPy | 1.26.4 |
| PDF Parser | PyMuPDF | 1.24.5 |
| Config | python-dotenv | 1.0.1 |

## 📡 API Endpoints

### GET `/`
Returns the main HTML interface.

### POST `/upload`
Upload a document for processing.

**Request (Text):**
```json
{
  "text": "Your document content here..."
}
```

**Request (File):** Multipart form with `file` field (PDF or TXT)

**Response:**
```json
{
  "status": "ready",
  "chunk_count": 12
}
```

### POST `/ask`
Ask a question about the uploaded document.

**Request:**
```json
{
  "question": "What is the main topic?"
}
```

**Response:**
```json
{
  "answer": "The main topic is... [based on document]"
}
```

## 🎯 How It Works

### RAG Pipeline

1. **Document Upload** → `load_document()` extracts text
2. **Text Chunking** → `chunk_text()` creates 500-char overlapping segments
3. **Embedding** → `create_embeddings()` converts text to vectors via OpenAI
4. **Index Storage** → `store_in_faiss()` creates searchable index
5. **Question Processing** → `retrieve_relevant_chunks()` finds top-4 similar chunks
6. **Answer Generation** → `generate_answer()` uses GPT-4o-mini with context

### Key Design Decisions

- **Temperature = 0** - Deterministic, consistent responses
- **Top-K = 4** - Balances context window with relevance
- **Chunk Overlap = 50** - Preserves context at chunk boundaries
- **Min Chunk = 30 chars** - Filters noise and incomplete segments
- **System Prompt** - Enforces strict context-grounded answering

## 🔐 Environment Setup

Create `.env` file:
```
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

**Security Notes:**
- Never commit `.env` to version control
- `.env` is in `.gitignore` by default
- Use secure environment variable management in production

## 🧪 Testing

See [EXAMPLE_TEST.md](./EXAMPLE_TEST.md) for:
- Sample test document
- 5+ test scenarios with expected answers
- Error handling test cases
- Performance metrics
- API curl examples

**Quick Test:**
1. Upload the sample Renaissance document
2. Ask: "What did Johannes Gutenberg invent?"
3. Expect accurate answer with date and impact

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────┐
│          User Interface (HTML/JS)           │
│     index.html + style.css (Responsive)     │
└────────────┬────────────────────────────────┘
             │
        ┌────┴─────┐
        │ Flask App │ (app.py)
        └────┬──────┘
             │
      ┌──────┴──────┐
      │ /upload │ /ask
      │  routes     │
      └──┬──────────┘
         │
    ┌────┴────────────────────┐
    │  Utility Modules         │
    ├─────────────────────────┤
    │ document_loader.py      │ PDF/TXT extraction
    │ chunker.py              │ Text segmentation
    │ embeddings.py           │ OpenAI + FAISS
    │ qa_engine.py            │ GPT-4o-mini
    └────┬────────────────────┘
         │
    ┌────┴────────────────────┐
    │  External APIs          │
    ├─────────────────────────┤
    │ OpenAI Embeddings API   │
    │ OpenAI Chat API (GPT)   │
    └────┬────────────────────┘
         │
    ┌────┴────────────────────┐
    │  In-Memory Storage      │
    ├─────────────────────────┤
    │ FAISS Index             │
    │ Chunk List              │
    └────────────────────────┘
```

## ⚙️ Configuration

**Chunking Parameters** (in `chunker.py`):
- `chunk_size`: 500 characters
- `overlap`: 50 characters
- `min_length`: 30 characters

**Embedding Model** (in `embeddings.py`):
- Model: `text-embedding-3-small`
- Dimension: 1536
- Distance: L2 (Euclidean)

**Generation Model** (in `qa_engine.py`):
- Model: `gpt-4o-mini`
- Temperature: 0
- Max tokens: 500
- Top-K chunks: 4

## 🚨 Error Handling

All routes return JSON with descriptive error messages:

```json
{
  "error": "No document loaded. Please upload a document first."
}
```

| Error | Status | Cause |
|-------|--------|-------|
| No file/text provided | 400 | Empty upload |
| Unsupported file type | 400 | Non-PDF/TXT file |
| Chunk generation failed | 400 | Document too short |
| No document loaded | 400 | Ask without upload |
| Empty question | 400 | Question field missing |
| API error | 500 | OpenAI API failure |

## 🎨 Frontend Features

- **Clean Gradient Design** - Modern, professional appearance
- **Responsive Layout** - Optimized for desktop and mobile
- **Real-time Feedback** - Status messages and loading spinners
- **Error Display** - Clear, user-friendly error messages
- **Smooth Transitions** - Subtle animations for better UX
- **Accessibility** - Semantic HTML, keyboard support

## 📈 Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Document upload | < 1s | Local processing |
| Embedding creation | 1-2s | OpenAI API call |
| Vector search | < 100ms | Local FAISS |
| Answer generation | 2-5s | OpenAI API call |
| **Total Q&A latency** | **3-6s** | Dependent on API |

## 🔄 Production Deployment

For production use:

1. **Use WSGI Server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Add Reverse Proxy** (Nginx/Apache)

3. **Enable HTTPS/SSL** (Let's Encrypt)

4. **Secure Environment Variables** (avoid .env files)

5. **Use Cloud Vector Store** (for persistence beyond session)

6. **Monitor API Usage** (OpenAI billing)

## 📝 File Descriptions

| File | Purpose | Key Functions |
|------|---------|---|
| `app.py` | Flask application | `@app.route("/upload")`, `@app.route("/ask")` |
| `document_loader.py` | Extract document text | `load_document()` |
| `chunker.py` | Split text into chunks | `chunk_text()` |
| `embeddings.py` | Vector operations | `create_embeddings()`, `store_in_faiss()`, `retrieve_relevant_chunks()` |
| `qa_engine.py` | Answer generation | `generate_answer()` |
| `index.html` | Web interface | Upload UI + Question form |
| `style.css` | Styling | Responsive design + animations |

## 🤝 Contributing

This is a complete, production-ready system. All features are fully implemented.

## 📄 License

Production-ready template for RAG applications.

## 🆘 Support

For issues:
1. Check [SETUP_INSTRUCTIONS.md](./SETUP_INSTRUCTIONS.md) - Troubleshooting section
2. Verify `.env` file with correct OpenAI API key
3. Ensure all dependencies installed: `pip install -r requirements.txt`
4. Check OpenAI API status and quota

---

**Version:** 1.0.0  
**Last Updated:** 2026-04-21  
**Status:** Production-Ready ✓
