import chromadb
from chromadb.utils import embedding_functions
from config import CHROMA_COLLECTION, CHROMA_PATH, EMBEDDING_MODEL, N_RESULTS

_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)
_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _client.get_or_create_collection(
    name = CHROMA_COLLECTION,
    embedding_function=_ef,
    metadata={"hnsw:space": "cosine"}
)

def embed(chunks):
    _collection.add(
        documents = [i["text"] for i in chunks],
        metadatas=[{"source": i["source"]} for i in chunks],
        ids = [i["id"] for i in chunks]
    )

def retrieve(query, n_results=N_RESULTS):
    
    if _collection.count() == 0:
        return []

    results = _collection.query(
        query_texts = [query],
        n_results = n_results,
        include = ["documents", "metadatas", "distances"]
    )

    results_list = []

    for i in range(len(results["ids"][0])):
        temp = {}
        temp["text"] = results["documents"][0][i]
        temp["source"] = results["metadatas"][0][i]["source"]
        temp["distance"] = results["distances"][0][i]
        results_list.append(temp)

    return results_list

def get_collection():
    return _collection



# testing
# queries = [
#     "What concern about threats to American democracy did Lincoln express in the Lyceum Address?",
#     "How did Lincoln describe slavery in both the Cooper Union Address and the Second Inaugural Address?", 
#     "How did Lincoln's view of preserving the Union change between the First Inaugural Address and the Second Inaugural Address?"
# ]

# for query in queries:
#     print(f"Query: {query}")
#     results = retrieve(query)
#     for r in results:
#         print(f"  [{r['distance']:.3f}] ({r['source']}) {r['text'][:100]}")
#     print("---")