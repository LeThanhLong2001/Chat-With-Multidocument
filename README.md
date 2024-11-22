# Chat-With-Multidocument
Ứng dụng chatbot cho phép người dùng hỏi đáp với dữ liệu của họ 
## Description
Dự án sử dụng framework LlamaIndex để xây dựng RAG pipeline, LlamaParse API để trích xuất văn bản từ bảng biểu, hình ảnh,... trong file data.
LLM được sử dụng là llama-3.1-70b-versatile được đưa vào ứng dụng thông qua API của Groq để tận dụng tốc độ phản hồi của LLM.
Mô hình Embedding all-MiniLM-L6-v2 từ HuggingFace được sử dụng để embedding dữ liệu. Cuối cùng là streamlit để xây dựng giao diện ứng dụng.
## Installation
### 1. Cài đặt các thư viện, framework cần thiết trong file requirements.txt
### 2. Đăng ký API key
- Để chạy được dự án người dùng cần đăng ký api key cho Groq, LlamaParse ở các trang https://console.groq.com/keys và https://docs.cloud.llamaindex.ai/llamaparse/getting_started/web_ui.
- Tạo 1 file .env để chứa thông tin api key.
### 3. Chạy ứng dụng
- Sau khi đã cài đặt các yêu cầu ở mục 1, người dùng có thể chạy lệnh streamlit run app.py trong Terminal để khởi động ứng dụng.
- Người dùng có thể chat ngay mà không cần kéo thả tài liệu vào ứng dụng. Ứng dụng sẽ trả lời dựa trên dữ liệu đã được đào tạo.
- Người dùng có thể kéo thả vào ứng dụng 1 hoặc nhiều file và ứng dụng chỉ hỗ trợ 3 định dạng .doc, .pdf, .pptx.
- Sau khi ứng dụng hiện thông báo 'Đã xử lý xong tài liệu!' người dùng có thể bắt đầu hỏi đáp dựa trên tài liệu hoặc hỏi không liên quan đến tài liệu.
- Ứng dụng sẽ trả lời cụ thể là câu trả lời được dựa trên tài liệu của người dùng hay dựa trên dữ liệu đã được đào tạo.
- Để ứng dụng có thể trả lời tốt, người dùng nên đọc qua hoặc hiểu về tài liệu, đặt câu hỏi sát với tài liệu nhất có thể. Nếu đặt câu hỏi quá chung chung, ứng dụng sẽ tự trả lời trên dữ liệu đã đào tạo.
- Ứng dụng chưa có tính năng sau khi tải lên tài liệu và tương tác thì người dùng có thể tải lên tiếp tài liệu. Nếu muốn người dùng có thể F5 lại trang và tải lên lại.
### 4. Demo:
- Link demo cho ứng dụng: https://drive.google.com/file/d/1ezuK6CO95rcMrqiSVApRs4zjWNtyNFQS/view?usp=sharing

