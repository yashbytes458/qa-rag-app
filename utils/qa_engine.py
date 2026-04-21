--- FILE: /qa_rag_app/utils/qa_engine.py ---
"""
QA engine module for generating answers using retrieved context.
Implements the retrieval-augmented generation workflow.
"""


def generate_answer(question, context_chunks, client):
    """
    Generate an answer to a question using provided context chunks.
    Strictly enforces answering only from provided context.
    
    Args:
        question (str): The user's question
        context_chunks (list[str]): Retrieved context chunks from the document
        client (OpenAI): OpenAI client instance
    
    Returns:
        str: Generated answer from the model
        
    Raises:
        ValueError: If API call fails
    """
    
    # Join chunks with clear separator for context
    joined_context = "\n\n---\n\n".join(context_chunks)
    
    # Define strict system prompt that enforces grounding in context
    system_prompt = (
        "You are a strict question-answering assistant. "
        "Answer ONLY using information from the provided context. "
        "If the answer is not present in the context, respond exactly with: "
        "'Answer not found in the provided context.' "
        "Do not guess, infer, or add any information beyond what is stated."
    )
    
    # Format user message with context and question
    user_message = f"Context:\n{joined_context}\n\nQuestion: {question}"
    
    try:
        # Call OpenAI API with strict parameters
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0,  # Deterministic responses
            max_tokens=500
        )
        
        # Extract and return the answer
        answer = response.choices[0].message.content.strip()
        return answer
    
    except Exception as e:
        raise ValueError(f"Failed to generate answer: {str(e)}")
--- END FILE ---