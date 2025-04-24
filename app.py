from openai import OpenAI
import gradio as gr
import os
from dotenv import load_dotenv
from newspaper import Article
import requests
from bs4 import BeautifulSoup
import fitz  # xử lý PDF

# Lưu nội dung PDF
pdf_context = {"content": ""}

# Tải PDF
def upload_pdf(file):
    text = ""
    try:
        doc = fitz.open(file.name)
        for page in doc:
            text += page.get_text()
        pdf_context["content"] = text
        return "✅ Đã tải và đọc nội dung PDF thành công!"
    except Exception as e:
        return f"❌ Lỗi đọc PDF: {e}"

# Tìm kiếm tin tức
def is_news_query(text):
    keywords = ["sự kiện", "tin tức", "thời sự", "mới nhất", "tin nóng"]
    return any(kw in text.lower() for kw in keywords)

def get_latest_news():
    try:
        url = "https://vnexpress.net/rss/tin-moi-nhat.rss"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, features="xml")
        items = soup.findAll("item")[:3]
        news = "\n\n".join(f"{i+1}. {item.title.text}" for i, item in enumerate(items))
        return news
    except Exception as e:
        return f"Không lấy được tin tức mới: {e}"

# Trích xuất bài báo
def is_url(text):
    return text.startswith("http://") or text.startswith("https://")

def summarize_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except:
        return "Không thể trích xuất nội dung từ đường link này."

# Load KEY
load_dotenv()
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Hàm chính
def chat_with_gemini(message, history):
    # 1. Hỏi sự kiện
    if is_news_query(message):
        raw_news = get_latest_news()
        prompt = f"Hãy tóm tắt và phân tích các sự kiện sau bằng tiếng Việt:\n\n{raw_news}"
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    # 2. Link bài báo
    if is_url(message):
        article_text = summarize_article(message)
        if article_text.startswith("❌"):
            return article_text
        prompt = f"Tóm tắt bài báo sau bằng tiếng Việt ngắn gọn:\n\n{article_text}"
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    # 3. Nếu có PDF thì kết hợp vào prompt
    prompt = ""
    if pdf_context["content"]:
        prompt = f"Dựa vào tài liệu sau, trả lời câu hỏi:\n\n{pdf_context['content']}\n\nCâu hỏi: {message}"
    else:
        prompt = message

    messages = [{"role": "system", "content": "Bạn là trợ lý AI thân thiện."}]
    for user, bot in history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": bot})
    messages.append({"role": "user", "content": prompt})

    stream = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=messages,
        stream=True
    )

    full_reply = ""
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
            full_reply += chunk.choices[0].delta.content
    return full_reply

# Giao diện chatbot
with gr.Blocks() as app:
    gr.Markdown("ChatBot")
    pdf_upload = gr.File(label="📄 Tải lên file PDF", file_types=[".pdf"])
    upload_status = gr.Textbox(label="Trạng thái đọc file", interactive=False)
    chatbot = gr.ChatInterface(fn=chat_with_gemini)
    pdf_upload.change(fn=upload_pdf, inputs=pdf_upload, outputs=upload_status)

app.launch()
