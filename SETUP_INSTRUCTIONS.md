═══════════════════════════════════════════════════════════════════════════════
SETUP INSTRUCTIONS - QA RAG APPLICATION
═══════════════════════════════════════════════════════════════════════════════

OVERVIEW:
This is a complete, production-ready Question Answering system using Retrieval-
Augmented Generation (RAG) with Flask backend, FAISS vector search, and OpenAI API.

═══════════════════════════════════════════════════════════════════════════════
STEP 1: PREREQUISITES
═══════════════════════════════════════════════════════════════════════════════

✓ Python 3.10 or higher installed
✓ pip package manager available
✓ OpenAI API key (from https://platform.openai.com/api-keys)

═══════════════════════════════════════════════════════════════════════════════
STEP 2: CLONE/SETUP PROJECT
═══════════════════════════════════════════════════════════════════════════════

1. Navigate to project directory:
   cd c:\Users\INDIA\Desktop\qa_rag_app-1

2. Verify project structure:
   qa_rag_app/
   ├── app.py
   ├── requirements.txt
   ├── .env.example
   ├── .env (create this next)
   ├── templates/
   │   └── index.html
   ├── static/
   │   └── style.css
   └── utils/
       ├── __init__.py
       ├── document_loader.py
       ├── chunker.py
       ├── embeddings.py
       └── qa_engine.py

═══════════════════════════════════════════════════════════════════════════════
STEP 3: CONFIGURE ENVIRONMENT
═══════════════════════════════════════════════════════════════════════════════

1. Create .env file from template:
   On Windows:
   copy .env.example .env
   
   On macOS/Linux:
   cp .env.example .env

2. Edit .env file and add your OpenAI API key:
   OPENAI_API_KEY=sk-proj-YOUR-ACTUAL-KEY-HERE

   ⚠️ IMPORTANT: Keep .env secure - never commit to version control!
   The .gitignore should already exclude it.

═══════════════════════════════════════════════════════════════════════════════
STEP 4: INSTALL DEPENDENCIES
═══════════════════════════════════════════════════════════════════════════════

Run this command to install all required packages:

pip install -r requirements.txt

This will install:
- Flask 3.0.3         (Web framework)
- OpenAI 1.30.1       (API client - NEW format)
- FAISS CPU 1.8.0     (Vector search)
- NumPy 1.26.4        (Numerical computing)
- PyMuPDF 1.24.5      (PDF extraction)
- python-dotenv 1.0.1 (Environment variables)

═══════════════════════════════════════════════════════════════════════════════
STEP 5: RUN THE APPLICATION
═══════════════════════════════════════════════════════════════════════════════

Start the Flask development server:

python app.py

Expected output:
  * Running on http://0.0.0.0:5000
  * Debug mode: off
  * Click http://127.0.0.1:5000 to open in browser

The application is now running and accessible at:
http://localhost:5000

═══════════════════════════════════════════════════════════════════════════════
STEP 6: USE THE APPLICATION
═══════════════════════════════════════════════════════════════════════════════

OPTION A: Upload Text
1. Copy and paste document text into the textarea
2. Click "Upload & Process Document"
3. Wait for success message showing chunk count
4. Type a question in the QA section
5. Click "Get Answer" to receive AI-generated response

OPTION B: Upload File
1. Click "Choose File" to select a PDF or TXT file
2. Click "Upload & Process Document"
3. Wait for success message showing chunk count
4. Type a question in the QA section
5. Click "Get Answer" to receive AI-generated response

═══════════════════════════════════════════════════════════════════════════════
STEP 7: API ENDPOINTS
═══════════════════════════════════════════════════════════════════════════════

GET /
  Returns: HTML homepage

POST /upload
  Request:
    - File upload (multipart): file field with PDF or TXT
    - Text input (JSON): { "text": "document content" }
  
  Response (success):
    { "status": "ready", "chunk_count": 42 }
  
  Response (error):
    { "error": "Error message" }

POST /ask
  Request:
    { "question": "What is the main topic?" }
  
  Response (success):
    { "answer": "The main topic is..." }
  
  Response (error):
    { "error": "Error message" }

═══════════════════════════════════════════════════════════════════════════════
STEP 8: ARCHITECTURE OVERVIEW
═══════════════════════════════════════════════════════════════════════════════

RAG WORKFLOW:

1. Document Upload
   └─> load_document() → Extract text from PDF/TXT or use raw text

2. Text Processing
   └─> chunk_text() → Split into 500-char overlapping chunks

3. Embedding Creation
   └─> create_embeddings() → Call OpenAI API to get vector embeddings
       └─> store_in_faiss() → Create searchable FAISS index

4. Question Answering
   └─> retrieve_relevant_chunks() → Find most relevant chunks via vector search
   └─> generate_answer() → Call GPT-4o-mini with context to generate answer

STORAGE: All data stored in Flask app memory (session-based) - no database needed.

═══════════════════════════════════════════════════════════════════════════════
STEP 9: TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════════

Issue: "OPENAI_API_KEY environment variable is not set"
Fix:
  1. Verify .env file exists in project root
  2. Check .env contains: OPENAI_API_KEY=sk-proj-...
  3. Restart Flask server after creating/editing .env

Issue: "Unsupported file type" error
Fix:
  Only PDF and TXT files are supported. Ensure file extension is correct.

Issue: "No document loaded. Please upload a document first."
Fix:
  Upload a document before asking questions.

Issue: API rate limits
Fix:
  OpenAI has rate limits. Wait a moment before retrying.
  Consider upgrading your OpenAI plan for higher limits.

Issue: "Answer not found in the provided context"
Fix:
  The document doesn't contain information about your question.
  Ask questions about content actually present in the document.

═══════════════════════════════════════════════════════════════════════════════
STEP 10: PRODUCTION DEPLOYMENT
═══════════════════════════════════════════════════════════════════════════════

For production deployment:

1. Use production WSGI server:
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app

2. Use reverse proxy (Nginx/Apache)

3. Enable HTTPS/SSL

4. Store environment variables securely (not in .env file)

5. Use cloud-based vector store instead of in-memory FAISS for persistence

6. Monitor API usage and costs

═══════════════════════════════════════════════════════════════════════════════
TECHNICAL SPECIFICATIONS
═══════════════════════════════════════════════════════════════════════════════

Document Processing:
  - Max chunk size: 500 characters
  - Chunk overlap: 50 characters (for context continuity)
  - Min chunk length: 30 characters (to filter noise)

Embeddings:
  - Model: text-embedding-3-small (OpenAI)
  - Vector dimension: 1536
  - Distance metric: L2 (Euclidean)

Question Answering:
  - Model: gpt-4o-mini (OpenAI)
  - Temperature: 0 (deterministic responses)
  - Max tokens: 500
  - Top-k chunks: 4 (most relevant)

Server:
  - Framework: Flask 3.0.3
  - Host: 0.0.0.0 (all interfaces)
  - Port: 5000
  - Debug: False (production mode)

═══════════════════════════════════════════════════════════════════════════════
