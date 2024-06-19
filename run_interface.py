import ollama
import chromadb
import os
import gradio as gr
import css

# Set the embedding model and persist directory
embedding_model = 'nomic-embed-text'
model = "llama3"
persist_directory = './VectorStore'

# Ensure the persist directory exists
if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)

# Initialize the ChromaDB client
client = chromadb.PersistentClient(path=persist_directory)
collection = client.get_collection("document_collection")

# Function to query and retrieve from the vector store
def query_vector_store(prompt, n_results=2):
    response = ollama.embeddings(model=embedding_model, prompt=prompt)
    query_embedding = response["embedding"]
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
    sources = [metadata['source'] for metadata in results['metadatas'][0]] if results['metadatas'] else ["No result found."]
    return sources

# Function to generate a response
def generate_response(prompt):
    response = ollama.generate(model=model, prompt=prompt)
    return response['response']

# Set LLM temperature
def set_temperature(new_temperature):
    global llm
    llm = lambda prompt: ollama.generate(model=model, prompt=prompt)['response']

# Template for the prompt
template = """Use the following pieces of context to answer the question. 
If pieces of context do not contain the answer use your internal knowledge.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use three sentences maximum for the answer. Keep the answer as concise as possible. 
Always say "thanks for asking!" at the end of the answer. 
{context}
Question: {question}
Answer:"""

# Function to get the answer
def get_answer(question, temperature):
    set_temperature(temperature)  # Adjust the model's temperature
    retrieved_sources = query_vector_store(question, n_results=2)
    context = ", ".join(retrieved_sources)
    combined_prompt = template.format(context=context, question=question)
    response = generate_response(combined_prompt)
    return response

# Gradio interface function
def get_answer_with_temp(question, temperature):
    return get_answer(question, temperature)

# Set up Gradio interface
frontend = gr.Interface(
    fn=get_answer_with_temp,
    inputs=[
        gr.Textbox(lines=2, placeholder="Type your question here", label="Question"),
        gr.Slider(minimum=0, maximum=10, step=1, label="Creativity Level (Temperature)")
    ],
    outputs=gr.Textbox(label="Answer", lines=5, placeholder="Due to CPU inference, please allow time to process"),
    title="Locally Hosted LLM ChatBot",
    theme="Monochrome",
    description="Enter a question to get an answer. Adjust the model's temperature to control randomness.",
    css=css.custom_css 
)

# Launch Gradio interface
frontend.launch(
    inbrowser=True,
    share=True,
    auth=("username", "password"),
    auth_message="Please enter the Username and Password provided to you.",
    favicon_path="./images/favicon.jpg"
)
