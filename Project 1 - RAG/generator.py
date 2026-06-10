from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)

def generate_response(query, retrieved_chunks):
    if not retrieved_chunks:
        return "I don't have enough information on that."

    knowledge = ""
    sources = []
    for i in retrieved_chunks:
        if i["distance"] < 0.7:
            knowledge += f"From {i['source']}: {i['text']}\n\n"
            if i["source"] not in sources:
                sources.append(i["source"])

    if not knowledge:
        return "I don't have enough information on that."

    prompt = f"""You are a helpful assistant that answers questions about Abraham Lincoln's speeches.
Use ONLY the following excerpts to answer the question. If the answer is not in the excerpts, say "I don't have enough information on that."

{knowledge}

Question: {query}

Answer:"""

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Answer using ONLY the provided context. If the context doesn't contain the answer, say 'I don't have enough information on that.'"},
            {"role": "user", "content": prompt}
        ]
    )

    
    return response.choices[0].message.content