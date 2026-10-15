import re

class TextProcessor:
    @staticmethod
    def simple_base_form(word):
        word = word.lower().strip()
        if len(word) <= 3:
            return word
            
        if word.endswith('ies') and len(word) > 4:
            return word[:-3] + 'y'
        if word.endswith('es'):
            return word[:-2]
        if word.endswith('s') and not word.endswith('ss'):
            return word[:-1]
            
        if word.endswith('ied') and len(word) > 4:
            return word[:-3] + 'y'
        if word.endswith('ed'):
            return word[:-2]
        if word.endswith('ing') and len(word) > 5:
            return word[:-3]
            
        return word

    @staticmethod
    def highlight_words(text, words_list, color="#fff3cd"):
        for word in words_list:
            pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
            text = pattern.sub(f'<span style="background-color:{color};">\\g<0></span>', text)
        return text

    @staticmethod
    def add_inline_comment(text, word, comment):
        pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
        return pattern.sub(f'\\g<0>（{comment}）', text)

    @staticmethod
    def markdown_to_html(md_text):
        try:
            import markdown
            return markdown.markdown(md_text)
        except:
            return md_text.replace('\n', '<br>')
