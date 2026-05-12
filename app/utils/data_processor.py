def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)

    return chunks



import re

def get_relevent_chunk(query: str, chunks: list, top_n: int = 2):
    query_words = set(re.findall(r'\w+', query.lower()))

    # counting how many query words appear each chunk
    scored_chunks = []
    for chunk in chunks:
        chunk_words = set(re.findall(r'\w+', chunk.lower()))
        score = len(query_words.intersection(chunk_words))
        scored_chunks.append((score, chunk))

    # sorting by score (highest first) and return top_n
    scored_chunks.sort(key = lambda x: x[0], reverse = True)
    return [c[1] for c in scored_chunks[:top_n] if c[0] > 0]




# Quick logic testing

# if __name__ == "__main__":
#     sample_text = "Data Engineering is the practice of designing and building systems for collecting, storing, and analyzing data at scale. It is a broad field with applications in nearly every industry."
#     test_chunks = chunk_text(sample_text, chunk_size=50, overlap=10)
#     for i, c in enumerate(test_chunks):
#         print(f"Chunks {i}: {c}")
