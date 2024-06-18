from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
import ollama
import chromadb
import os
import uuid

# Pull the embedding model
os.system("ollama pull nomic-embed-text")
persist_directory = './VectorStore'

# Ensure the persist directory exists
if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)

def loader():
    urls = [
        "https://en.wikipedia.org/wiki/University_of_Aberdeen",
        "https://www.topuniversities.com/universities/university-aberdeen",
        "https://www.scotland.org/study/scottish-universities/university-of-aberdeen",
        # "https://www.shiksha.com/studyabroad/uk/universities/university-of-aberdeen",
    ]
    loader = WebBaseLoader(urls)
    documents = loader.load()
    return documents

documents = loader()

text_splitter = CharacterTextSplitter(
    chunk_size=3400,
    chunk_overlap=300,
    is_separator_regex=False,
)

# Initialize the ChromaDB client with explicit settings
client = chromadb.PersistentClient(path=persist_directory)

# Create a collection in the client
collection = client.create_collection("document_collection")

for doc in documents:
    content = doc.page_content
    texts = text_splitter.create_documents([content])

    # Adding source metadata to each chunk with unique IDs
    for i, text in enumerate(texts):
        text.metadata["source"] = doc.metadata.get('source', 'default_source')
        doc_id = str(uuid.uuid4())

        # Generate embedding using Ollama directly
        response = ollama.embeddings(
            model='nomic-embed-text',
            prompt=text.page_content
        )
        embedding = response["embedding"]

        collection.add(
            documents=[text.page_content],
            metadatas=[{"source": text.metadata["source"], "chunk_id": i}],
            ids=[doc_id],
            embeddings=[embedding]
        )

# Function to query and view the contents of the vector store
def view_vector_store():
    # Use a dummy text query to retrieve all documents
    dummy_query = "dummy query to retrieve all documents"
    response = ollama.embeddings(
        model='nomic-embed-text',
        prompt=dummy_query
    )
    dummy_embedding = response["embedding"]
    
    # Perform a query with a dummy embedding to retrieve all documents
    try:
        all_docs = collection.query(query_embeddings=[dummy_embedding], n_results=100)
    except Exception as e:
        print(f"Error during query: {e}")
        return
    
    # Check if the collection retrieval was successful
    if all_docs is None or not all_docs.get("ids"):
        print("No documents retrieved from the collection.")
        return

    for doc_id, doc_content, metadata, embedding in zip(all_docs["ids"][0], all_docs["documents"][0], all_docs["metadatas"][0], all_docs["embeddings"][0]):
        print(f"ID: {doc_id}")
        print(f"Content: {doc_content[:100]}...")  # Print the first 100 characters of the content for brevity
        print(f"Metadata: {metadata}")
        print(f"Embedding: {embedding[:10]}...")  # Print the first 10 values of the embedding for brevity
        print()

# View the contents of the vector store
# view_vector_store()
