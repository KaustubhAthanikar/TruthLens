def create_chunks(text,chunk_size=8):

    sentences = text.split(".")

    chunks=[]


    for i in range(0,len(sentences),chunk_size):
        chunk = ".".join(
            sentences[i:i+chunk_size]
        )
        if chunk.strip():
            chunks.append(
                chunk.strip()
            )


    return chunks