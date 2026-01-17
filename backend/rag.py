def answer(question,context_chunks):
    if not context_chunks:
        return "I don't have enough information to answer that question."
    return  context_chunks[0]  # Placeholder implementation