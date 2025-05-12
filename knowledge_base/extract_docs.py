import os
import re
from langchain_community.document_loaders import TextLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, "texts")

# Функция очистки текста
def clean_text(text: str) -> str:
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 30]
    return '\n'.join(lines)

documents = []

for filename in os.listdir(DATA_DIR):
    file_path = os.path.join(DATA_DIR, filename)

    if filename.endswith(".txt"):
        loader = TextLoader(file_path, encoding='utf-8')
    elif filename.endswith(".docx"):
        loader = Docx2txtLoader(file_path)
    else:
        continue  # пропускаем другие форматы

    docs = loader.load()

    # Очистка каждого документа
    for doc in docs:
        doc.metadata["source"] = filename
        doc.page_content = clean_text(doc.page_content)

    documents.extend(docs)

print(f"Загружено документов: {len(documents)}")

# Разбивка на чанки
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", ".", "!", "?", " "]
)
chunks = text_splitter.split_documents(documents)

print(f"Чанков после деления: {len(chunks)}")

# Векторизация и сохранение в Chroma
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vectorstore = Chroma.from_documents(documents=chunks, embedding=embedding, persist_directory="./vectorstore")

print("Векторная база знаний сохранена в knowledge_base/vectorstore")