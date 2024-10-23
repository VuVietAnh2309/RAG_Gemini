import os
import json
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

# Đường dẫn đến folder chứa các file QA
folder_path = '/content/RAG_Gemini/Data'

# Load mô hình Sentence Transformer cho tiếng Việt (phobert)
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2', device='cpu')

# Danh sách các câu hỏi, câu trả lời và ngữ cảnh
questions = []
answers = []
contexts = []

# Đọc từng file trong folder và trích xuất câu hỏi, câu trả lời và ngữ cảnh
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
            qa_data = json.load(f)
            for item in qa_data:
                questions.append(item['question'])
                answers.append(item['answer'])
                contexts.append(item['context'])  # Lấy 'context' từ file JSON

# Mã hóa các context
context_embeddings = model.encode(contexts)

# Mã hóa các câu hỏi
question_embeddings = model.encode(questions)

# Kết hợp embeddings của context và câu hỏi
combined_embeddings = []
for question_emb, context_emb in zip(question_embeddings, context_embeddings):
    combined_embedding = (question_emb + context_emb) / 2  # Trung bình 2 embeddings
    combined_embeddings.append(combined_embedding)

combined_embeddings = np.array(combined_embeddings)  # Chuyển về dạng numpy array

# Tạo FAISS index
dimension = combined_embeddings.shape[1]  # Kích thước embeddings
index = faiss.IndexFlatL2(dimension)  # Sử dụng L2 distance
index.add(combined_embeddings)  # Thêm embeddings kết hợp vào FAISS index

# Lưu FAISS index
faiss.write_index(index, 'faiss_index.index')

# Lưu câu hỏi và câu trả lời
with open('qa_data.json', 'w', encoding='utf-8') as f:
    json.dump({'questions': questions, 'answers': answers, 'contexts': contexts}, f, ensure_ascii=False, indent=4)
