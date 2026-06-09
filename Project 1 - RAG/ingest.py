import os
from config import DOCS_PATH


def load_documents():
    documents = []
    for filename in sorted(os.listdir(DOCS_PATH)):
        if filename.endswith(".txt"):
            filepath = os.path.join(DOCS_PATH, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            speech_name = filename.replace(".txt", "").replace("_", " ").title()
            documents.append({
                "speech": speech_name,
                "filename": filename,
                "text": text,
            })
    return documents

# asfd
def chunk_document(text, source):
    chunk_size = 100
    overlap = 0
    min_length = 50

    chunks = []
    prefix = source.lower().replace(" ", "_")
    counter = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if len(chunk) >= min_length:
            chunk_id = f"{prefix}_{counter}"
            chunks.append({
                "id": chunk_id,
                "text": chunk,
                "source": source,
            })
            counter += 1

        start += chunk_size - overlap

    return chunks

