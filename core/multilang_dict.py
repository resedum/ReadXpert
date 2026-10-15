import csv
import os

class MultiLangDict:
    """多语言核心互译词典，自动加载core目录下所有en-xx.csv文件"""
    
    def __init__(self):
        self.dict = {}
        self._load_all_csv()
        self._build_reverse_index()
    
    def _load_all_csv(self):
        """加载所有多语言CSV词典，格式: word,target_word"""
        core_dir = os.path.dirname(__file__)
        for fname in os.listdir(core_dir):
            if fname.startswith("en-") and fname.endswith(".csv"):
                lang = fname.replace("en-", "").replace(".csv", "")
                try:
                    with open(os.path.join(core_dir, fname), 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        next(reader, None)
                        count = 0
                        for row in reader:
                            if len(row) >= 2:
                                en_word = row[0].strip().lower()
                                trans_word = row[1].strip()
                                if en_word:
                                    if en_word not in self.dict:
                                        self.dict[en_word] = {"en": en_word}
                                    self.dict[en_word][lang] = trans_word
                                    count += 1
                    print(f"加载{lang}词典完成: {count}词条")
                except Exception as e:
                    print(f"加载{lang}词典失败: {e}")
    
    def _build_reverse_index(self):
        """构建反向索引，支持任意语言互译"""
        self.reverse_index = {}
        for lang in ["zh", "en", "ja", "ko", "fr", "de", "ru", "es"]:
            self.reverse_index[lang] = {}
            for entry in self.dict.values():
                word = entry.get(lang, "")
                if word:
                    self.reverse_index[lang][word.lower()] = entry
    
    def lookup(self, word, target_lang="zh", source_lang="en"):
        """查询单词在目标语言下的释义，支持任意语言互译"""
        word = word.lower().strip()
        entry = None
        
        if source_lang in self.reverse_index:
            entry = self.reverse_index[source_lang].get(word)
        
        if not entry:
            for lang, index in self.reverse_index.items():
                for w, e in index.items():
                    if word == w:
                        entry = e
                        break
                if entry:
                    break
        
        if entry:
            return entry.get(target_lang, None)
        return None
