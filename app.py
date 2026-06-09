import gradio
from ingest import load_documents, chunk_document
from retriever import embed, retrieve, get_collection
from generator import generate_responses

def run_ingestion():
    collection = get_collection()

    if collection.count() > 0:
        return
    
    documents = load_documents()
    all_chunks = []

    for i in documents:
        chunks = chunk_document(doc["text"], doc["source"])
        all_chunks.extend(chunks)

    if all_chunks:
        embed(all_chunks)
    else:
        print("no chunks")


def chat(message, history):
    if not message.strip():
        return ""
    
    return generate_responses(message, retrieve(message))

with gradio.Blocks(
    theme = gradio.themes.Soft(primary_hue="black"),
    title = "LincolnBot"
) as demo:
    gradio.HTML("""
        <div style="text-align:center; padding:1.25rem 0 0.5rem;">
            <h1 style="font-size:2rem; font-weight:700; color:#312e81; margin:0;">
                LincolnBot
            </h1>
            <p style="color:#6b7280; font-size:1rem; margin:0.4rem 0 0;">
                Ask anything about his speeches.
            </p>
        </div>
    """)

    with gradio.Row():
        with gradio.Column(scale = 3):
            gradio.ChatInterface(
                fn = chat,
                type = "messages",
                chatbot = gradio.Chatbot(
                    height = 440,
                    type = "messages",
                    placeholder=(
                        "<div style='text-align:center; color:#9ca3af; margin-top:3rem;'>"
                        "Ask anything"
                        "</div>"
                    ),
                ),
                textbox = gradio.Textbox(
                    placeholder="When was the Gettsbrug Address spoken?",
                    container = False,
                    scale = 7
                ),
                examples = [
                    "How did Lincoln's view of preserving the Union change between the First Inaugural Address and the Second Inaugural Address?",
                    "Which speech contains the phrase 'government of the people, by the people, for the people,' and what was the occasion?",
                    "What concern about threats to American democracy did Lincoln express in the Lyceum Address?",
                    "How did Lincoln describe slavery in both the Cooper Union Address and the Second Inaugural Address?",
                    "hat was Lincoln's message in his Farewell Address to Springfield, and how does it compare with the tone of his Last Public Address?"
                ],
                cache_examples = False
            )

            with gradio.Column(scale=1, min_width=180):
                gradio.HTML("""
                <div style="background:#f5f3ff; border:1px solid #ddd6fe;
                            border-radius:10px; padding:1rem; margin-top:0.5rem;">
                    <ul style="font-size:0.85rem; color:#5b21b6; list-style:none;
                                padding:0; margin:0; line-height:1.8;">
                        <li>Cooper Union Address</li>
                        <li>Eulogy on Henry Clay</li>
                        <li>Farewell Address</li>
                        <li>First Inagural Address</li>
                        <li>Gettysburg Address</li>
                        <li>House Divided</li>
                        <li>Last Public Address</li>
                        <li>Lyceum Address</li>
                        <li>Second Inagural Address</li>
                        <li>Temperance Address</li>
                    </ul>
                    <hr style="border:none; border-top:1px solid #ddd6fe; margin:0.75rem 0;">
                    <p style="font-size:0.75rem; color:#7c3aed; margin:0; line-height:1.5;">
                        Answers are grounded in the loaded speeches only.
                    </p>
                </div>
            """)
                
if __name__ == "__main__":
    run_ingestion()
    demo.launch()
