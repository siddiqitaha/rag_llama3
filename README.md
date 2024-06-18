### README.md

# Local LLM ChatBot with Embeddings and Retrieval

This project uses a local LLM with Ollama for embeddings and ChromaDB for document retrieval. It features a Gradio interface for users to ask questions and adjust response creativity. Documents are pulled from URLs, embedded, stored in ChromaDB, and retrieved to provide concise, sourced answers.

<div style="display: flex; justify-content: center; text-align: center;">
  <div style="margin-right: 30px;">
    <p>**Vector Store Creation**</p>
    <img src="https://github.com/siddiqitaha/rag_llama3/assets/92089684/950bc8ea-5051-4222-9b42-07cb11bfba83" alt="Vector Store Creation" width="400"/>
  </div>
  <div style="margin-left: 30px;">
    <p>**Gradio Interface**</p>
    <img src="https://github.com/siddiqitaha/rag_llama3/assets/92089684/ecac0f7a-3407-4dd5-a9a8-3e1e39c1c28f" alt="Gradio Interface" width="400"/>
  </div>
</div>

## Features

- **Local Embedding Generation**: Uses Ollama's `nomic-embed-text` model.
- **ChromaDB Integration**: Efficiently stores and retrieves document embeddings.
- **Customizable LLM Responses**: Adjust the LLM's temperature for varied responses.
- **Gradio Web Interface**: Easy-to-use interface for user interaction.

### Prerequisites
Before running the software to collect more data for the Vector Database, ensure you have Python installed along with the necessary dependencies:
- Python 3.8 or newer
- Install [Ollama](https://ollama.com/download)
- Install Git
- Install CUDA (GPU only)

## Setup Instructions

1. **Install Ollama (Linux):**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

2. **Clone the Repository:**
   ```bash
   git clone https://github.com/siddiqitaha/rag_llama3.git
   cd rag_llama3
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Vector Store Creation Script**
   ```bash
   python create_vector_store.py
   ```

5. **Start the Gradio Interface**
   ```bash
   python run_interface.py
   ```

## Usage

- Open the Gradio interface in your browser.
- Type your question in the input box.
- Adjust the temperature slider to control response creativity.
- View the generated answer, including references to the sources.

## Acknowledgements

- [Ollama](https://www.ollama.com) for the embedding and LLM models.
- [ChromaDB](https://www.chromadb.com) for the vector store solution.
- [Gradio](https://www.gradio.app) for the user-friendly web interface.
