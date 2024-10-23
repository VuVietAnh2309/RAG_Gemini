# VA-VSS: Hệ thống hỏi đáp Y tế VSS

## Giới thiệu

**VA-VSS** (Virtual Assistant VSS) là trợ lý ảo thông minh được thiết kế để hỗ trợ người dùng một cách toàn diện trong các hoạt động chăm sóc khách hàng. Với khả năng tương tác, hướng dẫn, và thu thập phản hồi từ người dùng, VA-VSS giúp nâng cao trải nghiệm khách hàng, đồng thời được tích hợp sâu vào hệ thống chăm sóc khách hàng của **Vietsens**. Chatbot này không chỉ giúp giải đáp thắc mắc mà còn đóng vai trò là cầu nối giúp khách hàng sử dụng các sản phẩm và dịch vụ một cách hiệu quả hơn.

## Mô hình sử dụng

Phiên bản mới của **VA-VSS** được nâng cấp để kết hợp giữa công nghệ **RAG** (Retrieval-Augmented Generation) và **Gemini**, thay vì chỉ sử dụng các mô hình ngôn ngữ lớn (LLMs) như trước đây. Sự kết hợp này mang lại khả năng tìm kiếm và truy vấn dữ liệu hiệu quả, đồng thời sinh câu trả lời chính xác hơn bằng cách kết hợp kiến thức truy xuất từ cơ sở dữ liệu với mô hình ngôn ngữ.

- **RAG (Retrieval-Augmented Generation)**: Tìm kiếm các câu trả lời từ cơ sở dữ liệu lớn và kết hợp với mô hình sinh để tạo phản hồi tự nhiên và chính xác.
- **Gemini**: Là một mô hình nhỏ, tinh gọn nhưng hiệu quả, giúp giảm tải tính toán và tối ưu hóa hiệu năng, đặc biệt khi triển khai trên CPU.

## Hiệu suất

Việc sử dụng kết hợp RAG và Gemini cho phép **VA-VSS** không chỉ hoạt động mạnh mẽ trên GPU mà còn chạy mượt mà trên **CPU**, mang đến tính linh hoạt cao trong quá trình triển khai. Mô hình có thể cung cấp phản hồi nhanh chóng ngay cả khi không sử dụng các tài nguyên phần cứng đắt đỏ như GPU.

Điều này đặc biệt hữu ích khi triển khai mô hình trong các môi trường có hạn chế về tài nguyên, đồng thời vẫn đảm bảo hiệu suất cao trong việc xử lý và phản hồi các câu hỏi từ người dùng.

## Nền tảng và tài nguyên triển khai mô hình

Với việc chuyển đổi sang sử dụng **RAG** và **Gemini**, **VA-VSS** hiện có thể được triển khai hoàn toàn trên **CPU**, giúp giảm bớt sự phụ thuộc vào các tài nguyên phần cứng cao cấp như GPU, đồng thời vẫn đảm bảo khả năng phản hồi nhanh chóng và chính xác.

Việc triển khai trên **Google Colab** và **Kaggle** vẫn là lựa chọn phổ biến, nhưng nhờ khả năng hoạt động tốt trên CPU, mô hình giờ đây có thể được sử dụng linh hoạt trên các môi trường tính toán khác mà không cần GPU. Điều này giúp giảm chi phí và mở rộng khả năng triển khai trong các hệ thống thực tế có giới hạn tài nguyên.

Ngoài ra, nền tảng **FAISS** được tích hợp để quản lý cơ sở dữ liệu tìm kiếm hiệu quả, giúp **VA-VSS** có thể truy vấn và tìm kiếm câu trả lời từ nguồn dữ liệu lớn trong thời gian ngắn. Kết hợp với khả năng sinh văn bản tự nhiên của Gemini, hệ thống mang đến trải nghiệm tương tác tốt hơn cho người dùng.

## Hướng dẫn sử dụng

1. **Chạy mô hình trên CPU**: Mô hình có thể được triển khai và chạy mượt mà trên CPU mà không cần cấu hình phức tạp. Điều này mang đến tính linh hoạt cho những ai không có sẵn GPU nhưng vẫn muốn triển khai hệ thống AI chất lượng cao.
2. **Tích hợp RAG**: VA-VSS giờ đây không chỉ dựa vào mô hình sinh văn bản mà còn có khả năng truy xuất dữ liệu từ cơ sở tri thức có sẵn, đảm bảo rằng các câu trả lời luôn chính xác và dựa trên các thông tin mới nhất từ hệ thống dữ liệu của **Vietsens**.

### Kết luận

Phiên bản mới của **VA-VSS** tận dụng sức mạnh của **RAG** và **Gemini**, giúp tối ưu hiệu suất, giảm chi phí triển khai, và mang lại khả năng hoạt động trên các hệ thống tính toán với tài nguyên hạn chế như CPU. Đây là một bước tiến lớn trong việc nâng cao trải nghiệm khách hàng và tối ưu hóa quy trình hỗ trợ tại **Vietsens**.

---

## Cách chạy project

### Bước 1: Clone repository

```bash
# Lệnh clone mã nguồn từ github.
!git clone https://github.com/VuVietAnh2309/RAG_Gemini.git
```


### Bước 2: Di chuyển vào thư mục dự án
``` bash
%cd /content/RAG_Gemini
```

### Bước 3: Cài đặt file môi trường nếu cần thiết
``` bash
# Tạo file .env với nội dung env_content
with open('.env', 'w') as f:
    f.write(env_content)

# Kiểm tra nội dung file đã tạo
!cat .env
```

### Bước 4: Cài đặt các gói phụ thuộc
``` bash
!pip install -r requirments.txt
```

### Bước 5: Chạy file lưu faiss and qa data
``` bash
!python faiss_index.py
```

### Bước 6: Chạy ứng dụng
``` bash
!python app.py
```