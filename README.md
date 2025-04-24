# ChatBot- Hướng dẫn cài đặt và chạy bài test AI
Ứng dụng chatbot sử dụng mô hình Gemini miễn phí từ Google, có thể:
- Trò chuyện bằng tiếng Việt
- Tóm tắt nội dung bài báo
- Trả lời về sự kiện mới nhất
- Hỏi đáp theo tài liệu PDF
---
## ⚙️ Các bước cài đặt và chạy
### 1. Tải và giải nén thư mục
- Tải project dưới dạng file `.zip`
- Giải nén ra một thư mục (ví dụ: `Chat Bot LLM`)
- Mở PowerShell hoặc CMD, dùng lệnh sau để **truy cập vào thư mục**:
- đảm bảo đã tải 3.10 python version
```powershell
cd "Đường_dẫn_đến_thư_mục\Chat Bot LLM"
### 2. Tạo mô trường ảo
    py -3.10 -m venv env310 (env310 là tên môi trường)
### 3. Kích hoạt môi trường
    .\env310\Scripts\Activate
### 4. cài đặt các thư viện cần thiết
	pip install -r requirements.txt
### 5. sau khi cài xong chạy app
    python app.py
    hiện ra địa chỉ tương tự http://127.0.0.1:xxxx/
    nhấn ctrl + click để truy cập 
thực hiện kiểm tra