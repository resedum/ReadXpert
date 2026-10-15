import os
import json
from datetime import datetime

class ArticleManager:
    def __init__(self, data_dir="data/articles"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.progress_file = os.path.join(data_dir, "read_progress.json")
        self.progress = self._load_progress()

    def _load_progress(self):
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_progress(self, article_id, scroll_pos, font_size):
        self.progress[article_id] = {
            "scroll_pos": scroll_pos,
            "font_size": font_size,
            "last_read": datetime.now().isoformat()
        }
        self._save_progress_file()

    def _save_progress_file(self):
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, ensure_ascii=False, indent=2)

    def _read_docx(self, file_path):
        from docx import Document
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)

    def _read_pdf(self, file_path):
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        full_text = []
        for page in reader.pages:
            full_text.append(page.extract_text())
        return '\n'.join(full_text)

    def import_article(self, file_path):
        file_name = os.path.basename(file_path)
        article_id = os.path.splitext(file_name)[0]
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.docx':
            content = self._read_docx(file_path)
        elif ext == '.pdf':
            content = self._read_pdf(file_path)
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        
        save_path = os.path.join(self.data_dir, f"{article_id}.txt")
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return article_id, content

    def get_article_content(self, article_id):
        for file in os.listdir(self.data_dir):
            if os.path.splitext(file)[0] == article_id:
                with open(os.path.join(self.data_dir, file), 'r', encoding='utf-8') as f:
                    return f.read()
        return ""

    def save_generated_article(self, title, content):
        file_name = f"{title}.txt"
        save_path = os.path.join(self.data_dir, file_name)
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return title, content

    def get_article_list(self):
        articles = []
        for file in os.listdir(self.data_dir):
            if file.endswith(('.txt', '.md')):
                articles.append(os.path.splitext(file)[0])
        return articles
