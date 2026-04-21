--- FILE: /qa_rag_app/utils/document_loader.py ---
"""
Document loader module for extracting text from PDF and TXT files.
Handles both file uploads and raw text input.
"""

import fitz


def load_document(file_storage_or_text):
    """
    Load and extract text from a file or return raw text string.
    
    Args:
        file_storage_or_text: Either a Flask FileStorage object or a string
    
    Returns:
        str: Extracted text from the document
        
    Raises:
        ValueError: If file type is not supported or extraction fails
    """
    
    # If input is a string, return it directly (raw text input)
    if isinstance(file_storage_or_text, str):
        return file_storage_or_text
    
    # Otherwise, it's a Flask FileStorage object
    filename = file_storage_or_text.filename.lower()
    
    try:
        if filename.endswith('.pdf'):
            # Extract text from PDF using PyMuPDF
            pdf_bytes = file_storage_or_text.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = ""
            for page_num in range(len(doc)):
                page = doc[page_num]
                text += page.get_text()
            doc.close()
            return text
        
        elif filename.endswith('.txt'):
            # Extract text from plain text file
            text_bytes = file_storage_or_text.read()
            return text_bytes.decode('utf-8')
        
        else:
            raise ValueError(f"Unsupported file type: {filename}. Only .pdf and .txt files are supported.")
    
    except UnicodeDecodeError:
        raise ValueError("Failed to decode text file. Please ensure it is valid UTF-8 encoded text.")
    except Exception as e:
        raise ValueError(f"Error processing document: {str(e)}")
--- END FILE ---