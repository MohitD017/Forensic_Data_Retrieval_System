# RAG for Cyber Forensics

This project demonstrates a simple Retrieval-Augmented Generation (RAG) system for cyber forensics using Ollama and LangChain. It allows you to ask questions about a document related to cyber forensics, and the system will provide answers based on the information in the document.

## What is RAG?

Retrieval-Augmented Generation (RAG) is a technique that combines information retrieval with text generation to provide more accurate and contextually relevant responses. It works by:

1.  **Retrieving** relevant information from a knowledge base (e.g., documents, databases) based on a user's query.
2.  **Generating** a response using the retrieved information and a language model.

This approach allows language models to access and process external knowledge, making them more useful for tasks that require specific information or domain expertise.

## How this project works

This project uses the following components:

* **Ollama:** An open-source large language model (LLM) that can be run locally.
* **LangChain:** A framework for developing applications powered by language models.
* **FAISS:** A library for efficient similarity search and clustering of vectors.
* **Tkinter:** A standard Python GUI library used to create the user interface.

The system works as follows:

1.  **Load and split:** The cyber forensics document is loaded and split into smaller chunks.
2.  **Embed:** Each chunk is embedded into a vector representation using Ollama's embedding model.
3.  **Store:** The embeddings are stored in a FAISS index for efficient similarity search.
4.  **Query:** When a user asks a question, the question is embedded and used to search the FAISS index for relevant chunks.
5.  **Answer:** The relevant chunks are passed to Ollama, which generates an answer based on the retrieved information.

## Code Overview

The code is structured as follows:

* **Document loading and processing:** The cyber forensics document is loaded using `TextLoader`, split into chunks using `CharacterTextSplitter`, and embedded using `OllamaEmbeddings`.
* **Vectorstore creation:** A FAISS vectorstore is created using the embeddings.
* **Conversational Chain:** A `ConversationalRetrievalChain` is set up to handle multi-turn conversations and maintain context.
* **Tkinter GUI:** A GUI is created using Tkinter, with a text area to display the conversation, an entry field for user input, and a button to send questions.
* **Error handling:** A `try-except` block handles potential errors, such as questions outside the knowledge base.

## Why this approach is better

This RAG-based approach offers several advantages over traditional methods:

* **Contextualized responses:** The system provides answers grounded in the provided cyber forensics document, ensuring relevance and accuracy.
* **Interactive interface:** The Tkinter GUI allows for a user-friendly chat-like interaction.
* **Transparency:** The source documents used to generate the answers are displayed, providing traceability and allowing for verification.
* **Efficiency:** FAISS enables fast similarity search for retrieving relevant information.
* **Local execution:** Ollama allows for local execution of the language model, enhancing privacy and reducing reliance on external APIs.
* **Document format support:** Currently, the LLM supports `.txt` as well as `.pdf` files as knowledge base.

## Setup and Usage

1.  **Install dependencies:**

    ```bash
    pip install langchain langchain_community langchain_ollama ollama faiss-cpu tkinter
    ```

2.  **Download an Ollama model:**

    I've used the `phi` model in this code as it is an efficient model, but you can use any model of your choice. Refer to the official Ollama website (https://ollama.com/search) to find available models.

    To download a model, use the following command:

    ```bash
    ollama pull <model_name>
    ```

    (Replace `<model_name>` with the name of the model you want to use.)

3.  **Replace `"D:\\RAG\\sample.txt"` with the path to your cyber forensics document.**

4.  **Update the code to use the chosen model:**

    * In the `OllamaEmbeddings` instantiation: `embedding = OllamaEmbeddings(model="<model_name>")`
    * In the `OllamaLLM` instantiation: `llm=OllamaLLM(model="<model_name>")`

5.  **Run the code:**

    ```bash
    python rag.py
    ```

6.  **Type your questions in the GUI window.**

## Features

* **GUI:** A simple Tkinter-based GUI for interacting with the system.
* **Progress bar:** Shows the progress while the question is being processed.
* **Response time:** Displays the time taken to generate the answer.
* **Source documents:** Shows the source document(s) from which the answer was extracted.
* **Error handling:** Provides informative messages for questions outside the knowledge base.

## Contributing

Contributions are welcome! Feel free to open issues or pull requests for bug fixes, improvements, or new features.

## License

This project is licensed under the MIT License.
