--- FILE: /qa_rag_app/utils/chunker.py ---
"""
Text chunking module for splitting documents into overlapping chunks.
Uses character-based sliding window approach for RAG processing.
"""


def chunk_text(text, chunk_size=500, overlap=50):
    """
    Split text into overlapping chunks using a sliding window.
    
    Args:
        text (str): The text to chunk
        chunk_size (int): Target size of each chunk in characters (default: 500)
        overlap (int): Number of overlapping characters between chunks (default: 50)
    
    Returns:
        list[str]: List of text chunks with whitespace stripped
    """
    
    chunks = []
    step_size = chunk_size - overlap  # Distance to move the window forward
    
    # Use sliding window to create overlapping chunks
    for i in range(0, len(text), step_size):
        chunk = text[i : i + chunk_size]
        
        # Strip whitespace from chunk
        chunk = chunk.strip()
        
        # Only include chunks that meet minimum length threshold
        if len(chunk) >= 30:
            chunks.append(chunk)
    
    return chunks
--- END FILE ---