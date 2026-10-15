import requests
import json

class AIEngine:
    def __init__(self, config):
        self.config = config
        self.api_key = config["ai"]["api_key"]
        self.base_url = config["ai"]["base_url"]
        self.model = config["ai"]["model"]

    def is_available(self):
        return bool(self.api_key)

    def _call_chat(self, prompt, system_prompt="你是一个专业的语言教育助手。"):
        if not self.is_available():
            raise Exception("请先在设置中配置API Key")
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            raise Exception(f"AI调用失败: {str(e)}")

    def generate_article(self, exam_type, theme, word_count, target_words=None):
        system_prompt = "你是专业的考试命题专家，擅长生成各类语言考试阅读文章。"
        
        prompt = f"""请生成一篇符合{exam_type}考试难度的阅读文章，主题是{theme}，字数大约{word_count}词。
要求：
1. 严格匹配{exam_type}的词汇难度、句子复杂度和文体风格
2. 文章结构清晰，符合真题阅读的行文逻辑
3. 不要附带题目，只输出文章正文
"""
        
        if target_words and len(target_words) > 0:
            prompt += f"\n4. 文章中必须自然包含以下所有词汇：{', '.join(target_words)}"
        
        return self._call_chat(prompt, system_prompt)

    def translate_text(self, text, target_lang="zh-CN", context=""):
        system_prompt = "你是专业的翻译，翻译要准确自然，符合目标语言表达习惯。"
        
        prompt = f"""请将以下文本翻译成{target_lang}。
如果有上下文，请结合上下文给出最准确的语境释义。

上下文：{context if context else "无"}

待翻译文本：
{text}

只输出翻译结果，不要解释。"""
        
        return self._call_chat(prompt, system_prompt)

    def get_word_detail(self, word, context=""):
        system_prompt = "你是专业的词典专家。"
        
        prompt = f"""请给出单词「{word}」的详细信息，格式如下：
1. 核心释义
2. 词性
3. 常见变形（单复数、时态、比较级等）
4. 常见搭配
5. 例句

如果有上下文「{context}」，优先给出该语境下的释义。"""
        
        return self._call_chat(prompt, system_prompt)

    def get_base_form(self, word):
        prompt = f"""请返回单词「{word}」的原形/词根形式。
只输出单词原形，不要任何解释。"""
        try:
            return self._call_chat(prompt).strip().lower()
        except:
            return word.lower()
