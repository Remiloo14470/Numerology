from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
db = Chroma(persist_directory="./vectorstore", embedding_function=embedding)

# Пример запроса — ты можешь заменить на любой другой
query = "Что такое Матрица Судьбы?"

results = db.similarity_search(query, k=3)

for i, doc in enumerate(results):
    print(f"\n--- Результат {i + 1} ---")
    print(doc.page_content)
    print(f"--- Результат {i+1} (файл: {doc.metadata['source']}) ---")
    print(doc.page_content)