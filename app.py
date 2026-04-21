--- FILE: /qa_rag_app/app.py ---
"""
Flask application for QA RAG system.
Provides API endpoints for document upload and question answering.
"""

from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

from utils.document_loader import load_document
from utils.chunker import chunk_text
from utils.embeddings import create_embeddings, store_in_faiss, retrieve_relevant_chunks
from utils.qa_engine import generate_answer

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please create a .env file with your API key.")

client = OpenAI(api_key=api_key)

# Configuration for storing document state in memory (per session)
app.config["FAISS_INDEX"] = None
app.config["DOCUMENT_CHUNKS"] = None


@app.route("/", methods=["GET"])
def home():
    """Serve the main HTML page."""
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    """
    Upload and process a document (PDF, TXT, or raw text).
    
    Expects either:
    - File upload: multipart/form-data with 'file' field
    - Raw text: JSON with 'text' field
    
    Returns:
        JSON: { "status": "ready", "chunk_count": <int> }
        or
        JSON: { "error": "<message>" } with 400/500 status
    """
    try:
        document_text = None
        
        # Check if file was uploaded
        if "file" in request.files:
            file = request.files["file"]
            if file.filename == "":
                return jsonify({"error": "No file selected"}), 400
            
            document_text = load_document(file)
        
        # Check if raw text was provided
        elif "text" in request.json:
            document_text = request.json.get("text", "").strip()
            if not document_text:
                return jsonify({"error": "Empty text provided"}), 400
        
        else:
            return jsonify({"error": "No file or text provided"}), 400
        
        # Process document: chunk and embed
        chunks = chunk_text(document_text)
        if not chunks:
            return jsonify({"error": "Document too short or no valid chunks produced"}), 400
        
        embeddings = create_embeddings(chunks, client)
        faiss_index = store_in_faiss(embeddings)
        
        # Store in app context for later use
        app.config["FAISS_INDEX"] = faiss_index
        app.config["DOCUMENT_CHUNKS"] = chunks
        
        return jsonify({
            "status": "ready",
            "chunk_count": len(chunks)
        }), 200
    
    except ValueError as e:
        # Document loading or processing error
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        # Unexpected error
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route("/ask", methods=["POST"])
def ask():
    """
    Answer a question based on the uploaded document.
    
    Expects JSON: { "question": "<string>" }
    
    Returns:
        JSON: { "answer": "<string>" }
        or
        JSON: { "error": "<message>" } with appropriate status code
    """
    try:
        # Check if a document has been loaded
        if app.config["FAISS_INDEX"] is None or app.config["DOCUMENT_CHUNKS"] is None:
            return jsonify({
                "error": "No document loaded. Please upload a document first."
            }), 400
        
        # Get question from request
        data = request.json
        question = data.get("question", "").strip()
        
        if not question:
            return jsonify({"error": "Question cannot be empty"}), 400
        
        # Retrieve relevant chunks and generate answer
        relevant_chunks = retrieve_relevant_chunks(
            question,
            app.config["FAISS_INDEX"],
            app.config["DOCUMENT_CHUNKS"],
            client,
            top_k=4
        )
        
        answer = generate_answer(question, relevant_chunks, client)
        
        return jsonify({"answer": answer}), 200
    
    except ValueError as e:
        # API or processing error
        return jsonify({"error": str(e)}), 500
    
    except Exception as e:
        # Unexpected error
        return jsonify({"error": f"Server error: {str(e)}"}), 500


if __name__ == "__main__":
    # Run Flask app in production mode
    app.run(host="0.0.0.0", port=5000, debug=False)
--- END FILE ---