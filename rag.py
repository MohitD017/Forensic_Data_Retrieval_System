import tkinter as tk
from tkinter import scrolledtext
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
import fitz  # PyMuPDF for handling PDF
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain_ollama import OllamaLLM
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document  
import os

# --- Custom PDF Loader ---
def load_pdf(file_path):
    doc = fitz.open(file_path)
    text = "".join(page.get_text() for page in doc)
    return Document(page_content=text, metadata={'source': os.path.basename(file_path)})

# --- Custom Document Loader ---
def load_documents(file_path):
    file_extension = os.path.splitext(file_path)[-1].lower()
    if file_extension == '.txt':
        loader = TextLoader(file_path)
        documents = loader.load()
    elif file_extension == '.pdf':
        documents = [load_pdf(file_path)]
    else:
        raise ValueError("Unsupported file type. Only .txt and .pdf are supported.")
    return documents

# --- Load Documents and Prepare RAG ---
file_path = "E:\\UBalt_Assignment\\CYFI-600_renamed\\new.pdf"  
documents = load_documents(file_path)

# Ensure 'source' is in metadata
for doc in documents:
    doc.metadata['source'] = os.path.basename(file_path)

# Split Text into Chunks with Metadata
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

for i, doc in enumerate(texts):
    doc.metadata['source'] = os.path.basename(file_path)

# Embed Text using Ollama
embedding = OllamaEmbeddings(model="phi")
text_content = [doc.page_content for doc in texts]

# Store Embeddings in FAISS
vectorstore = FAISS.from_texts(text_content, embedding)

# Create a Strict Conversational Retrieval Chain
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=OllamaLLM(model="phi"),
    retriever=retriever,
    memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer"),
    chain_type="stuff",
    return_source_documents=True,
    return_generated_question=True
)

# --- Tkinter GUI ---
def send_question():
    query = question_entry.get()
    if query.lower() == "exit":
        root.destroy()
        return

    chat_history_text.config(state=tk.NORMAL)
    chat_history_text.insert(tk.END, f"\n🟢 **Your Question:** {query}\n", "question")  
    chat_history_text.config(state=tk.DISABLED)
    question_entry.delete(0, tk.END)

    def process_question():
        try:
            result = qa_chain.invoke({"question": query})
            response = result['answer']
            source_docs = result['source_documents']

            if not source_docs:
                response = "I'm sorry, but I couldn't find any relevant information in the provided document."

            chat_history_text.config(state=tk.NORMAL)
            chat_history_text.insert(tk.END, f"\n🔵 **RAG's Answer:** {response}\n", "answer")  

            if source_docs:
                chat_history_text.insert(tk.END, "\n📂 **Relevant Source(s):**\n", "source")
                for doc in source_docs:
                    source_filename = os.path.basename(doc.metadata['source'])  
                    chat_history_text.insert(tk.END, f"📄 {source_filename}\n", "source")  

            chat_history_text.config(state=tk.DISABLED)
            chat_history_text.see(tk.END)

        except Exception as e:
            chat_history_text.config(state=tk.NORMAL)
            chat_history_text.insert(tk.END, f"\n❌ **Error:** {e}\n", "error")
            chat_history_text.config(state=tk.DISABLED)
            chat_history_text.see(tk.END)

    root.after(100, process_question)

# --- Tkinter UI Setup ---
root = tk.Tk()
root.title("Strict RAG Chat")

chat_history_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 11))
chat_history_text.pack(fill=tk.BOTH, expand=True)

# Add Welcome Message
chat_history_text.config(state=tk.NORMAL)
chat_history_text.insert(tk.END, "🤖 **Welcome!** How can I assist you today?\n", "welcome")
chat_history_text.config(state=tk.DISABLED)

question_label = tk.Label(root, text="Enter your question:")
question_label.pack()

question_entry = tk.Entry(root)
question_entry.pack(fill=tk.X)

send_button = tk.Button(root, text="Send", command=send_question)
send_button.pack()

# --- Apply Text Formatting ---
chat_history_text.tag_config("welcome", foreground="green", font=("Arial", 12, "bold"))
chat_history_text.tag_config("question", foreground="blue", font=("Arial", 12, "bold"))
chat_history_text.tag_config("answer", foreground="dark red", font=("Arial", 12, "bold"))
chat_history_text.tag_config("source", foreground="purple", font=("Arial", 10, "italic"))
chat_history_text.tag_config("error", foreground="red", font=("Arial", 10, "bold"))

root.mainloop()
