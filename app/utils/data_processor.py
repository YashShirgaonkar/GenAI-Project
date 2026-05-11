def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)

    return chunks

# Quick logic testing

# if __name__ == "__main__":
#     sample_text = "Data Engineering is the practice of designing and building systems for collecting, storing, and analyzing data at scale. It is a broad field with applications in nearly every industry."
#     test_chunks = chunk_text(sample_text, chunk_size=50, overlap=10)
#     for i, c in enumerate(test_chunks):
#         print(f"Chunks {i}: {c}")
