import math


def similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)


def find_similar(query_embedding, chunks, top_k=5):
    scores = []
    for text,embeddings in chunks:
        scores=similarity(query_embedding,embeddings)
        scores.append((scores,text))

    scores.sort(reverse=True)
    return [text for _, text in scores[:top_k]]  
