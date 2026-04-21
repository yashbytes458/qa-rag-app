--- FILE: /qa_rag_app/utils/embeddings.py ---
"""
Embeddings module for creating vector embeddings and FAISS index operations.
Handles OpenAI embedding API calls and vector similarity search.
"""

import numpy as np
import faiss


def create_embeddings(chunks, client):
    """
    Create embeddings for text chunks using OpenAI API.
    
    Args:
        chunks (list[str]): List of text chunks to embed
        client (OpenAI): OpenAI client instance
    
    Returns:
        list[list[float]]: List of embedding vectors
        
    Raises:
        ValueError: If embedding API call fails
    """
    
    try:
        # Call OpenAI embeddings API with all chunks at once
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunks
        )
        
        # Extract embeddings from response (maintain order)
        embeddings = [item.embedding for item in response.data]
        return embeddings
    
    except Exception as e:
        raise ValueError(f"Failed to create embeddings: {str(e)}")


def store_in_faiss(embeddings):
    """
    Create and populate a FAISS index with embedding vectors.
    
    Args:
        embeddings (list[list[float]]): List of embedding vectors
    
    Returns:
        faiss.IndexFlatL2: FAISS index containing all vectors
    """
    
    # Convert embeddings to numpy float32 array (required by FAISS)
    embeddings_array = np.array(embeddings, dtype=np.float32)
    
    # Get the dimension of embeddings (1536 for text-embedding-3-small)
    dimension = embeddings_array.shape[1]
    
    # Create FAISS index with L2 distance metric
    index = faiss.IndexFlatL2(dimension)
    
    # Add all vectors to the index
    index.add(embeddings_array)
    
    return index


def retrieve_relevant_chunks(question, index, chunks, client, top_k=4):
    """
    Retrieve the most relevant chunks for a given question using vector similarity.
    
    Args:
        question (str): The user's question
        index (faiss.IndexFlatL2): FAISS index with embedded chunks
        chunks (list[str]): Original chunk strings (parallel to index)
        client (OpenAI): OpenAI client instance
        top_k (int): Number of most similar chunks to return (default: 4)
    
    Returns:
        list[str]: Top-k most relevant chunk strings
    """
    
    # Embed the question using the same model
    question_embedding = create_embeddings([question], client)
    question_vector = np.array(question_embedding, dtype=np.float32)
    
    # Search FAISS index for nearest neighbors
    distances, indices = index.search(question_vector, top_k)
    
    # Return the relevant chunks in order by similarity
    relevant_chunks = [chunks[i] for i in indices[0]]
    
    return relevant_chunks
--- END FILE ---