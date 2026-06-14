import gradio as gr
from query import ask
from ingest import load_documents, chunk_document
from retriever import embed, get_collection

def run_ingestion():
    collection = get_collection()

    if collection.count() > 0:
        return
    
    documents = load_documents()
    all_chunks = []

    for i in documents:
        chunks = chunk_document(i["text"], i["speech"])
        all_chunks.extend(chunks)

    if all_chunks:
        embed(all_chunks)
    else:
        print("no chunks")

def handle_query(question):
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

with gr.Blocks(title="LincolnBot") as demo:
    gr.HTML("""
        <div style="text-align:center; padding:1.25rem 0 0.5rem;">
            <h1 style="font-size:2rem; font-weight:700; color:#312e81; margin:0;">
                LincolnBot
            </h1>
            <p style="color:#6b7280; font-size:1rem; margin:0.4rem 0 0;">
                Ask anything about his speeches.
            </p>
        </div>
    """)

    inp = gr.Textbox(label="Your question", placeholder="When was the Gettysburg Address spoken?")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    run_ingestion()
    demo.launch()