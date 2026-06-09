from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq (api_key=GROQ_API_KEY)

def generate_response(query, retrieved_chunks):
    if not in retrieved_chunks:
        return "cannot find anything"
    
    knolwedge = ""
    for i in retrieved_chunks:
        if i["distance"] < 0.5:
            knowledge += f"From {i['source']}: {i['text']}\n\n\n\n"

            prompt = f"""
            You are a helpful assistant. Use ONLY the following knowledge to answer the question. If you don't know the answer, say you don't know.
            You are a speaker on Abraham Lincoln's speeches and you show what he said.
            Use the knowledge provided
            {knowledge}

            Question: {query}

            Answer:

            """
            response = _client.chat.completions.create(
                model = LLM_MODEL,
                messages = [{"role": "system", "content": "You are a helpful assistant. Use ONLY the following knowledge to answer the question. If you don't know the answer, say you don't know."},
                            {"role": "user", "content": prompt}

                ]
            )

            return response.choices[0].message.content