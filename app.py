import gradio as gr
from search import generate_response_with_rag

# Hàm xử lý câu hỏi đầu vào và sinh phản hồi từ hệ thống
def generate_response_stream(user_input, chat_history):
    api_key = 'AIzaSyD3Hu747dbztC-jogggDfZudh_zYg40PJg'  # Thay bằng API key của bạn
    try:
        response = generate_response_with_rag(user_input, api_key)
        chat_history.append((user_input, response))
        yield gr.update(value=chat_history)
    except Exception as e:
        chat_history.append(("Error", f"Error: {str(e)}"))
        yield gr.update(value=chat_history)

# CSS cho giao diện
custom_css = """
#title { font-size: 3em; text-align: center; font-weight: bold; color: #333; }
#interface { background-color: #f5f5f5; padding: 30px; border-radius: 5px; }
#chatbot { width: 90%; height: 700px; padding: 15px; background-color: #fff; border-radius: 10px; font-size: 2.0em; }
"""

# Giao diện Gradio
with gr.Blocks() as iface:
    with gr.Column():
        gr.Markdown("<h1 id='title'>Hệ Thống Hỏi Đáp Y Tế VSS AI</h1>")
        chatbot = gr.Chatbot(elem_id="chatbot", label="Trò chuyện")
        user_input = gr.Textbox(label="Nhập câu hỏi của bạn", placeholder="Nhập câu hỏi tại đây")
        submit_button = gr.Button("Gửi câu hỏi")
    
    user_input.submit(generate_response_stream, inputs=[user_input, gr.State([])], outputs=[chatbot])
    submit_button.click(generate_response_stream, inputs=[user_input, gr.State([])], outputs=[chatbot])
    submit_button.click(lambda x: gr.update(value=""), None, [user_input], queue=False)

iface.queue(default_concurrency_limit=5)
iface.launch(max_threads=50, share=True)
