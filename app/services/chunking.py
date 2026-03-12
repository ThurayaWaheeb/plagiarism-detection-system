def chunk_text_with_overlap(text, chunk_size=20, overlap=5):
    words = text.split()
    chunks = []
    step = chunk_size - overlap

    for i in range(0, len(words), step):
        chunk_words = words[i : i + chunk_size]
        chunk = " ".join(chunk_words)

        if len(chunk_words) >= 5:
            chunks.append(chunk)

    return chunks