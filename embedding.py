import chromadb
from chromabd.utils import embedding_functions
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