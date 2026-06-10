from retriever import retrieve
from generator import generate_response

def ask(question):
    chunks = retrieve(question)
    
    # DEBUG
    print(f"Query: {question}")
    for c in chunks:
        print(f"  distance: {c['distance']:.3f} | source: {c['source']} | text: {c['text'][:100]}")
    
    answer = generate_response(question, chunks)
    sources = list(set([c["source"] for c in chunks if c["distance"] < 0.7]))
    
    return {
        "answer": answer,
        "sources": sources
    }