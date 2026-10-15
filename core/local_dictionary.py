import csv
import os

class LocalDictionary:
    """加载ECDICT开源全量英汉词典，76万词条，包含音标、词性、考试标签、完整释义"""
    
    def __init__(self):
        self.dict = {}
        self._load_ecdict()
    
    def _load_ecdict(self):
        csv_path = os.path.join(os.path.dirname(__file__), "ecdict.csv")
        if not os.path.exists(csv_path):
            self._load_fallback()
            return
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader, None)
                # ECDICT列顺序: word, phonetic, definition, translation, pos, collins, oxford, tag, bnc, frq, exchange
                for row in reader:
                    if len(row) >= 8:
                        word = row[0].strip().lower()
                        phonetic = row[1].strip()  # 音标
                        definition = row[2].strip()  # 英文释义
                        translation = row[3].strip().replace('\\n', '\n')  # 中文释义，转义换行
                        tag = row[7].strip()  # 考试标签：zk(考研)/cet4/cet6/ielts等
                        if word:
                            self.dict[word] = {
                                "phonetic": phonetic,
                                "definition": definition,
                                "translation": translation,
                                "tag": tag
                            }
            print(f"ECDICT词典加载完成，共 {len(self.dict)} 词条")
        except Exception as e:
            print(f"ECDICT加载失败，使用内置词典: {e}")
            self._load_fallback()
    
    def _load_fallback(self):
        self.dict = {
            "it": {"phonetic": "/ɪt/", "definition": "pron. it", "translation": "pron. 它", "tag": "cet4"},
            "scroll": {"phonetic": "/skroʊl/", "definition": "v. scroll", "translation": "v. 滚动；n. 卷轴", "tag": ""},
        }
    
    def lookup(self, word):
        """查询单词，返回完整信息字典，找不到返回None"""
        word = word.lower().strip()
        return self.dict.get(word, None)
