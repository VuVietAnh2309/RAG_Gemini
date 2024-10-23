import gradio as gr
from search import generate_response_with_rag
import time
import re

# Hàm xử lý câu hỏi đầu vào và sinh phản hồi từ hệ thống
def generate_response_stream(user_input, chat_history):
    api_key = 'AIzaSyD3Hu747dbztC-jogggDfZudh_zYg40PJg'  # Thay bằng API key của bạn
    try:
        response = generate_response_with_rag(user_input, api_key)

        # Thêm phản hồi ban đầu vào lịch sử chat
        chat_history.append((user_input, ""))

        # Thay thế ký tự xuống dòng bằng <br> để bảo toàn dấu xuống dòng
        formatted_text = response.replace('\n', '<br>')

        # Chia phản hồi thành từng từ
        words = formatted_text.split()

        # Cập nhật dần dần từng từ với hiệu ứng thời gian
        for i, word in enumerate(words):
            chat_history[-1] = (user_input, " ".join(words[:i + 1]))
            time.sleep(0.05)  # Điều chỉnh thời gian chờ giữa các từ
            yield gr.update(value=chat_history)
        
    except Exception as e:
        chat_history.append(("Error", f"Error: {str(e)}"))
        yield gr.update(value=chat_history)

# CSS cho giao diện
custom_css = """
#title {
    font-size: 3em;
    text-align: center;
    font-weight: bold;
    margin-bottom: 20px;
    margin-top: 20px;
    color: #333;
}

#interface {
    background-color: #f5f5f5;
    padding: 30px;
    border-radius: 5px;
    width: 80%;
    max-width: 1200px;
    margin: auto;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

#chatbot {
    width: 90%; /* Đảm bảo khung chatbot chiếm 90% chiều rộng của vùng chứa */
    height: 700px; /* Tăng chiều cao của chatbot */
    overflow-y: auto; /* Cho phép cuộn theo chiều dọc nếu nội dung dài */
    word-wrap: break-word; /* Xuống dòng khi văn bản quá dài */
    padding: 15px; /* Đảm bảo không gian nội dung thoáng */
    background-color: #ffffff;
    border-radius: 10px;
    font-size: 2.0em;
    line-height: 1.5;
    white-space: normal; /* Đảm bảo văn bản xuống dòng tự nhiên */
}

#chatbot p {
    margin: 0;
}
"""

# Giao diện Gradio
with gr.Blocks() as iface:
    with gr.Column():  # Sắp xếp các thành phần theo chiều dọc
        gr.Markdown("<h1 id='title'>Hệ Thống Hỏi Đáp Y Tế VSS AI</h1>")
        gr.Markdown("Nhập câu hỏi của bạn vào ô bên dưới và nhận phản hồi lại từ hệ thống của chúng tôi.")
        chatbot = gr.Chatbot(elem_id="chatbot", label="Trò chuyện")
        user_input = gr.Textbox(label="Nhập câu hỏi của bạn tại đây", placeholder="Ví dụ: Các vấn đề bạn cần hỗ trợ là gì?")
        submit_button = gr.Button("Gửi câu hỏi")

    # Định nghĩa hành vi khi gửi câu hỏi
    user_input.submit(generate_response_stream, inputs=[user_input, gr.State([])], outputs=[chatbot])
    submit_button.click(generate_response_stream, inputs=[user_input, gr.State([])], outputs=[chatbot])

    submit_button.click(lambda x: gr.update(value=""), None, [user_input], queue=False)

# Tăng concurrency và threads để tối ưu hiệu năng
iface.queue(default_concurrency_limit=5)
iface.launch(max_threads=50, share=True)
