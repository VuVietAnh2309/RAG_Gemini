import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer

# Load dữ liệu QA và FAISS index
with open('qa_data.json', 'r', encoding='utf-8') as f:
    qa_data = json.load(f)
    questions = qa_data['questions']
    answers = qa_data['answers']
    contexts = qa_data['contexts']

# Load FAISS index và mô hình
index = faiss.read_index('faiss_index.index')
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2', device='cpu')

# Hàm tìm kiếm các câu hỏi và câu trả lời liên quan trong FAISS
def search_documents(query, k=5):
    query_embedding = model.encode([query], batch_size=8)
    distances, indices = index.search(query_embedding, k)
    
    results = []
    for idx in indices[0]:
        results.append({
            'question': questions[idx],
            'answer': answers[idx],
            'context': contexts[idx]
        })
    
    return results

# Gọi API Google Gemini
import requests

def call_gemini_api(question, api_key):
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": question}]}]
    }

    response = requests.post(api_url, json=payload, headers=headers)
    
    if response.status_code == 200:
        try:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        except KeyError:
            return "Không tìm thấy câu trả lời hợp lệ."
    else:
        return f"Lỗi {response.status_code}: {response.text}"

# Tích hợp tìm kiếm và sinh câu trả lời với Gemini API
def generate_response_with_rag(query, api_key):
    query_embedding = model.encode(query)
    distances, indices = index.search(np.array([query_embedding]), k=3)

    relevant_questions = [questions[idx] for idx in indices[0]]
    relevant_answers = [answers[idx] for idx in indices[0]]
    relevant_contexts = [contexts[idx] for idx in indices[0]]

    combined_context = "\n\n".join(
        [f"Câu hỏi: {q}\nCâu trả lời: {a}\nNgữ cảnh: {c}" for q, a, c in zip(relevant_questions, relevant_answers, relevant_contexts)]
    )

    combined_question = f"Với thông tin sau đây:\n{combined_context}\nhãy trả lời câu hỏi: {query}"
    return call_gemini_api(combined_question, api_key)
